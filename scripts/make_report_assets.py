"""Render a dependency-free SVG metric chart from results/metrics.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
metrics = json.loads((ROOT / "results/metrics.json").read_text(encoding="utf-8"))
models = metrics["models"]
colors = {"mean": "#ff8f8f", "knn": "#8c78ff", "ridge": "#42d8c8"}
bars = []
for i, name in enumerate(["mean", "knn", "ridge"]):
    value = models[name]["mae"]
    width = min(620, value * 45)
    y = 145 + i * 75
    bars.append(
        f'<text x="70" y="{y+23}" fill="#e8f4fa" font-size="18">{name.upper()}</text>'
        f'<rect x="210" y="{y}" width="620" height="32" rx="8" fill="#19344a"/>'
        f'<rect x="210" y="{y}" width="{width:.1f}" height="32" rx="8" fill="{colors[name]}"/>'
        f'<text x="850" y="{y+23}" fill="{colors[name]}" font-size="18">MAE {value:.2f}</text>'
    )
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="420">
<rect width="1000" height="420" rx="22" fill="#091827"/>
<g font-family="Segoe UI,Arial">
<text x="70" y="58" fill="white" font-size="28" font-weight="700">Leave-one-study-out benchmark</text>
<text x="70" y="90" fill="#93afbf" font-size="15">{metrics['n_formulations']} demo formulations · {metrics['n_studies']} held-out studies · lower is better</text>
{''.join(bars)}
</g></svg>"""
(ROOT / "assets/benchmark.svg").write_text(svg, encoding="utf-8")
print(ROOT / "assets/benchmark.svg")
