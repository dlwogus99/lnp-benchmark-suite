from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lnpbench.sources import SOURCES  # noqa: E402

for key, source in SOURCES.items():
    print(f"[{key}] {source['title']}")
    print(f"  {source['url']}")
    print(f"  scope: {source['data_scope']}")
    print(f"  terms: {source['license_note']}")
