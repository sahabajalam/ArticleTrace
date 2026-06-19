"""ColPali indexer — PDF page → image embeddings → Neo4j `:Page` nodes.

SCAFFOLDING ONLY. The class compiles and the interface is fixed; the model
load + inference path is gated behind a runtime import so the rest of the
service can keep running without `colpali-engine` installed.

To enable:
  pip install colpali-engine pdf2image pillow
  # plus poppler on PATH (Windows: download from Conda or pre-built binaries)

Reference: https://arxiv.org/abs/2407.01449 (ColPali, July 2024)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PageEmbedding:
    """A single page's multi-vector embedding plus provenance.

    `vectors` is shape (num_tokens, dim) — typically (1024, 128) for ColPali.
    Stored on a :Page node alongside vector property for MaxSim scoring.
    """
    doc_id: str          # e.g. "AIACT_PDF_OFFICIAL"
    page_number: int     # 1-indexed
    vectors: list[list[float]]   # multi-vector ColPali representation
    image_hash: str      # SHA-1 of the rendered image — for change detection


class ColPaliIndexer:
    """PDF → page-image embeddings via ColPali.

    Usage (when fully enabled):
        idx = ColPaliIndexer()
        idx.index_pdf(Path("data/multimodal_pdfs/EU_AI_ACT_OFFICIAL.pdf"),
                      doc_id="AIACT_PDF_OFFICIAL",
                      neo4j_writer=lambda pe: ...)  # caller persists
    """

    def __init__(
        self,
        model_name: str = "vidore/colpali-v1.3",
        device: str = "cpu",  # "cuda" if available; CPU is slow but works
    ):
        self.model_name = model_name
        self.device = device
        self._model = None
        self._processor = None

    def _load_model(self) -> None:
        """Lazy-load to keep import-time cheap."""
        if self._model is not None:
            return
        try:
            from colpali_engine.models import ColPali, ColPaliProcessor  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "colpali-engine not installed. Install with: pip install colpali-engine"
            ) from exc
        logger.info("Loading ColPali model %s on %s ...", self.model_name, self.device)
        self._model = ColPali.from_pretrained(self.model_name).to(self.device).eval()
        self._processor = ColPaliProcessor.from_pretrained(self.model_name)

    def pdf_to_images(self, pdf_path: Path) -> list[Any]:
        """Render PDF pages to PIL images via pdf2image (needs poppler)."""
        try:
            from pdf2image import convert_from_path  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "pdf2image not installed. Install with: pip install pdf2image"
            ) from exc
        return convert_from_path(str(pdf_path), dpi=150)

    def index_pdf(
        self,
        pdf_path: Path,
        doc_id: str,
        neo4j_writer=None,
    ) -> list[PageEmbedding]:
        """Embed every page in the PDF.

        If `neo4j_writer` is provided, calls it once per page so the caller
        can stream-persist without holding all embeddings in memory.
        """
        self._load_model()
        import hashlib

        images = self.pdf_to_images(pdf_path)
        logger.info("Indexing %d pages from %s (doc_id=%s)", len(images), pdf_path.name, doc_id)

        out: list[PageEmbedding] = []
        for page_num, image in enumerate(images, start=1):
            # Run ColPali forward pass — produces multi-vector embedding
            batch = self._processor.process_images([image]).to(self.device)
            with self._no_grad():
                emb = self._model(**batch)  # shape (1, n_tokens, dim)
            vectors = emb.squeeze(0).cpu().tolist()

            img_bytes = image.tobytes()
            image_hash = hashlib.sha1(img_bytes).hexdigest()  # noqa: S324  # not for security
            pe = PageEmbedding(
                doc_id=doc_id,
                page_number=page_num,
                vectors=vectors,
                image_hash=image_hash,
            )
            out.append(pe)
            if neo4j_writer is not None:
                neo4j_writer(pe)
        return out

    @staticmethod
    def _no_grad():
        """Lazy import of torch.no_grad to keep import-time cheap."""
        import torch  # type: ignore
        return torch.no_grad()
