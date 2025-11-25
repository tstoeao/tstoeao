#!/usr/bin/env python3
"""
Sync README.md from dois/doi-index.json

This first version is simple:
- Reads the local JSON file
- Writes a README.md with a table of DOIs and titles
- No network calls yet (no Zenodo API) – we can add that later.
"""

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOI_INDEX = ROOT / "dois" / "doi-index.json"
README = ROOT / "README.md"


def load_index():
    with DOI_INDEX.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("records", [])


def generate_readme(records):
    header = textwrap.dedent(
        """\
        # The Swygert Theory of Everything AO – DOI & GitHub Mirror

        This repository is the central index for John Swygert’s Swygert Theory of Everything AO universe:
        Zenodo DOIs, simulations, datasets, and GitHub code.

        All canonical works live on Zenodo (with DOIs minted by CERN/DataCite), and this repo
        mirrors them into a navigable GitHub structure for Castle, external AIs, and humans.

        ---

        ## DOI Index

        | DOI | Title | Category |
        | --- | ----- | -------- |
        """
    )

    rows = []
    for rec in records:
        doi = rec.get("doi", "").strip()
        title = rec.get("title", "").strip()
        category = rec.get("category", "").strip()
        if not doi:
            continue
        doi_code = f"`{doi}`"
        rows.append(f"| {doi_code} | {title} | {category} |")

    body = "\n".join(rows)

    footer = textwrap.dedent(
        """

        ---

        ## How to extend

        - Add new records to `dois/doi-index.json`.
        - Run this script locally to regenerate `README.md`.
        - Use this repo as the mirror/index for Castle and Secretary nodes.

        """
    )

    return header + body + footer


def main():
    records = load_index()
    readme_text = generate_readme(records)
    README.write_text(readme_text, encoding="utf-8")
    print(f"Wrote README with {len(records)} record(s).")


if __name__ == "__main__":
    main()
