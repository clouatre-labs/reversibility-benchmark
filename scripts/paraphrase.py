"""Paraphrase sub-experiment runner. Full implementation deferred to Step 8."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Paraphrase sub-experiment (stub)")
    parser.add_argument("--help-full", action="store_true")
    parser.parse_args()
    print("Paraphrase sub-experiment not yet implemented (Step 8).", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
