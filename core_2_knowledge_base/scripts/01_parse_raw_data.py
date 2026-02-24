"""Phase 1: Parse all raw text files into structured JSON.

Reads from Data/ (88 files), outputs to parsed_data/ (validated JSON).

Exit criteria:
- 99 GDPR articles, 113 AI Act articles
- 173 GDPR recitals, 180 AI Act recitals
- 13 annexes, 20 cases, 21 guidelines, 15 enforcement actions
- All JSON validates against Pydantic schema
- No data loss: full_text character counts ≥ 95% of raw text
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.parsers.article_parser import ArticleParser
from src.parsers.recital_parser import RecitalParser
from src.parsers.annex_parser import AnnexParser
from src.parsers.case_law_parser import CaseLawParser
from src.parsers.guideline_parser import GuidelineParser
from src.parsers.enforcement_parser import EnforcementParser

# ── Configuration ──────────────────────────────────────────────────────────

RAW_DATA_DIR = PROJECT_ROOT.parent / "Data"
PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"


def write_json(data: list | dict, output_path: Path) -> None:
    """Write data to JSON file with consistent formatting."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    print(f"  Wrote {output_path.name}: ", end="")
    if isinstance(data, list):
        print(f"{len(data)} entries")
    else:
        print(f"{len(data.get('articles', data.get('items', [])))} entries")


# ── Parse functions ────────────────────────────────────────────────────────

def parse_articles() -> tuple[int, int]:
    """Parse GDPR and AI Act articles. Returns (gdpr_count, ai_act_count)."""
    parser = ArticleParser()

    # GDPR
    print("\n[1/8] Parsing GDPR articles...")
    gdpr_chapters, gdpr_articles = parser.parse_all(
        RAW_DATA_DIR / "gdpr_chapters", "GDPR"
    )
    write_json(gdpr_chapters, PARSED_DATA_DIR / "legal" / "gdpr_chapters.json")
    write_json(gdpr_articles, PARSED_DATA_DIR / "legal" / "gdpr_articles.json")

    # AI Act
    print("\n[2/8] Parsing EU AI Act articles...")
    ai_chapters, ai_articles = parser.parse_all(
        RAW_DATA_DIR / "ai_act_chapters", "EU_AI_ACT"
    )
    write_json(ai_chapters, PARSED_DATA_DIR / "legal" / "ai_act_chapters.json")
    write_json(ai_articles, PARSED_DATA_DIR / "legal" / "eu_ai_act_articles.json")

    return len(gdpr_articles), len(ai_articles)


def parse_recitals() -> tuple[int, int]:
    """Parse GDPR and AI Act recitals. Returns (gdpr_count, ai_act_count)."""
    parser = RecitalParser()

    print("\n[3/8] Parsing GDPR recitals...")
    gdpr_recitals = parser.parse_file(
        RAW_DATA_DIR / "gdpr_recitals" / "gdpr_recitals.txt", "GDPR"
    )
    write_json(gdpr_recitals, PARSED_DATA_DIR / "legal" / "gdpr_recitals.json")

    print("\n[4/8] Parsing EU AI Act recitals...")
    ai_recitals = parser.parse_file(
        RAW_DATA_DIR / "ai_act_recitals" / "euai_recitals.txt", "EU_AI_ACT"
    )
    write_json(ai_recitals, PARSED_DATA_DIR / "legal" / "ai_act_recitals.json")

    return len(gdpr_recitals), len(ai_recitals)


def parse_annexes() -> int:
    """Parse AI Act annexes. Returns count."""
    parser = AnnexParser()

    print("\n[5/8] Parsing EU AI Act annexes...")
    annexes = parser.parse_file(RAW_DATA_DIR / "ai_act_annexes" / "ai_act_annexes.txt")
    write_json(annexes, PARSED_DATA_DIR / "legal" / "ai_act_annexes.json")

    return len(annexes)


def parse_case_law() -> int:
    """Parse CJEU case law. Returns count."""
    parser = CaseLawParser()

    print("\n[6/8] Parsing CJEU case law...")
    cases = parser.parse_directory(RAW_DATA_DIR / "cjeu_case_law")
    write_json(cases, PARSED_DATA_DIR / "interpretive" / "case_law.json")

    return len(cases)


def parse_guidelines() -> int:
    """Parse EDPB guidelines. Returns count."""
    parser = GuidelineParser()

    print("\n[7/8] Parsing EDPB guidelines...")
    guidelines = parser.parse_directory(RAW_DATA_DIR / "edpb_guidelines")
    write_json(guidelines, PARSED_DATA_DIR / "interpretive" / "edpb_guidelines.json")

    return len(guidelines)


def parse_enforcement() -> int:
    """Parse enforcement actions. Returns count."""
    parser = EnforcementParser()

    print("\n[8/8] Parsing enforcement actions...")
    actions = parser.parse_directory(RAW_DATA_DIR / "enforcement_actions")
    write_json(actions, PARSED_DATA_DIR / "interpretive" / "enforcement_actions.json")

    return len(actions)


# ── Validation ─────────────────────────────────────────────────────────────

def validate_counts(counts: dict[str, tuple[int, int]]) -> bool:
    """Validate parsed entity counts against expected values."""
    expected = {
        "GDPR Articles": (99, 99),
        "AI Act Articles": (113, 113),
        "GDPR Recitals": (173, 173),
        "AI Act Recitals": (180, 180),
        "AI Act Annexes": (13, 13),
        "CJEU Cases": (20, 20),
        "EDPB Guidelines": (21, 21),
        "Enforcement Actions": (15, 15),
    }

    print("\n" + "=" * 60)
    print("PHASE 1 VALIDATION REPORT")
    print("=" * 60)

    all_pass = True
    for name, (expected_min, expected_max) in expected.items():
        actual = counts.get(name, (0, 0))
        actual_count = actual if isinstance(actual, int) else actual[0]
        status = "PASS" if expected_min <= actual_count <= expected_max else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {name:25s}: {actual_count:4d} (expected {expected_min}) [{status}]")

    print("=" * 60)
    if all_pass:
        print("ALL COUNTS PASS — Phase 1 exit gate satisfied.")
    else:
        print("SOME COUNTS FAILED — investigate before proceeding to Phase 2.")

    return all_pass


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    """Run the full Phase 1 parsing pipeline."""
    print("=" * 60)
    print("PHASE 1: Parse Raw Data -> Structured JSON")
    print(f"Source: {RAW_DATA_DIR}")
    print(f"Output: {PARSED_DATA_DIR}")
    print("=" * 60)

    # Verify source directory exists
    if not RAW_DATA_DIR.exists():
        print(f"ERROR: Raw data directory not found: {RAW_DATA_DIR}")
        sys.exit(1)

    # Parse all 8 categories
    gdpr_art_count, ai_art_count = parse_articles()
    gdpr_rec_count, ai_rec_count = parse_recitals()
    annex_count = parse_annexes()
    case_count = parse_case_law()
    guideline_count = parse_guidelines()
    enforcement_count = parse_enforcement()

    # Validate
    counts = {
        "GDPR Articles": gdpr_art_count,
        "AI Act Articles": ai_art_count,
        "GDPR Recitals": gdpr_rec_count,
        "AI Act Recitals": ai_rec_count,
        "AI Act Annexes": annex_count,
        "CJEU Cases": case_count,
        "EDPB Guidelines": guideline_count,
        "Enforcement Actions": enforcement_count,
    }

    passed = validate_counts(counts)

    total = sum(v if isinstance(v, int) else v[0] for v in counts.values())
    print(f"\nTotal entities parsed: {total}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
