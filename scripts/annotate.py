"""Two-pass annotation runner.

NOTE: The annotation phase for this experiment is complete and the corpus is frozen.
corpus/annotations-a.json and corpus/annotations-b.json are sealed artifacts written
before any classifier prompt was composed. They must not be modified.

This script is preserved as documentation of the annotation procedure. Running it
against the frozen corpus would violate the sealed-annotation constraint in PROTOCOL.md.
To understand the annotation methodology, read PROTOCOL.md Section 2 and METHODOLOGY.md
Section 1.

Reads:  corpus/scenarios.json
Writes: corpus/annotations-{pass}.json  (FROZEN -- do not overwrite)
Config: params.json (provider, model, temperature)
"""

import sys


def main() -> None:
    print(
        "Annotation phase is complete. corpus/annotations-a.json and "
        "corpus/annotations-b.json are sealed artifacts. "
        "Running this script would overwrite frozen data. Exiting.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
