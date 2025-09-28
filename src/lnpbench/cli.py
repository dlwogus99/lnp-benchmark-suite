import argparse
import json

from .benchmark import load_rows, run_benchmark, write_results


def main() -> None:
    parser = argparse.ArgumentParser(description="LNP study-aware benchmark")
    parser.add_argument("--input", default="data/demo/lnp_formulations.csv")
    parser.add_argument("--output", default="results")
    parser.add_argument("--knn-k", type=int, default=3)
    parser.add_argument("--ridge-alpha", type=float, default=1.0)
    args = parser.parse_args()
    summary, predictions = run_benchmark(load_rows(args.input), args.knn_k, args.ridge_alpha)
    write_results(args.output, summary, predictions)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
