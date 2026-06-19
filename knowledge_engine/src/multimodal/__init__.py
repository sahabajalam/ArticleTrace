"""Multimodal retrieval — ColPali-style page-image embeddings for regulatory PDFs.

Status: scaffolding only. The integration is designed but not deployed; running
end-to-end requires (a) `colpali-engine` installed, (b) `poppler` available on
PATH for PDF → image conversion, (c) ~5 GB of model weights cached, and
(d) the EU AI Act + GDPR official PDFs in `data/multimodal_pdfs/`. None of
these are bundled in repo.

See `devlog/design-evolution/v05-multimodal-colpali.md` for the design
record and acceptance criteria.

Read order for code reviewers:
  1. colpali_indexer.py     — PDF → page images → ColPali embeddings → Neo4j nodes
  2. multimodal_retrieval.py — Query → ColPali query embedding → MaxSim scoring
                               → integration into RRF as a third retrieval arm
"""
