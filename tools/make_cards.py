#!/usr/bin/env python3
"""Render the featured-project cards for the profile README.

Each project ships a light and a dark variant, selected with <picture> in the
README so the cards follow the visitor's GitHub theme.

Regenerate with:
    python3 tools/make_cards.py
"""

from __future__ import annotations

import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MONO = "Fira Code, DejaVu Sans Mono, SFMono-Regular, Menlo, monospace"

THEMES = {
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "index": "#8c959f",
        "path": "#8c959f",
        "name": {"argent": "#1f2328", "noxtrace": "#0969da"},
        "role": "#57606a",
        "body": "#57606a",
        "art": "#8c959f",
        "art_dim": "#afb8c1",
        "accent": {"argent": "#57606a", "noxtrace": "#0969da"},
        "tip": "#8c959f",
        "shadow": "#1f2328",
        "shadow_opacity": "0.10",
    },
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "index": "#6e7681",
        "path": "#6e7681",
        "name": {"argent": "#e6edf3", "noxtrace": "#79b8ff"},
        "role": "#8b949e",
        "body": "#8b949e",
        "art": "#6e7681",
        "art_dim": "#484f58",
        "accent": {"argent": "#c9d1d9", "noxtrace": "#58a6ff"},
        "tip": "#6e7681",
        "shadow": "#000000",
        "shadow_opacity": "0.55",
    },
}

PROJECTS = [
    {
        "key": "argent",
        "index": "01",
        "name": "ARGENT",
        "path": "raxwqx/argent",
        "role": "SYMBOLIC EXECUTION ENGINE",
        "description": "Forks at data-dependent branches, prunes infeasible paths with z3, "
                       "and replays every reported input concretely.",
        "tags": ["Python", "z3", "SMT", "32-bit ISA"],
        "art": "hexdump",
    },
    {
        "key": "noxtrace",
        "index": "02",
        "name": "NOXTRACE",
        "path": "raxwqx/NOXTRACE",
        "role": "MULTI-ENGINE SECURITY WORKSTATION",
        "description": "Network reconnaissance, web inspection, source analysis and digital "
                       "investigation in one workflow.",
        "tags": ["Python", "Go", "Rust", "C"],
        "art": "radar",
    },
]

HEX = [
    "4d 5a 90 00 03 00 00 00",
    "04 00 00 00 ff ff 00 00",
    "b8 00 00 00 00 00 00 00",
    "40 00 00 00 00 00 00 00",
]


def hexdump(t: dict) -> str:
    rows = [
        f'<text x="860" y="{118 + i * 30}" font-family="{MONO}" font-size="14" '
        f'letter-spacing="1" fill="{t["art"] if i else t["art_dim"]}">{line}</text>'
        for i, line in enumerate(HEX)
    ]
    rows.append(
        f'<rect x="882" y="105" width="19" height="17" rx="3" fill="{t["art"]}" '
        f'fill-opacity="0.08" stroke="{t["art"]}" stroke-opacity="0.45"/>'
    )
    return "\n            ".join(rows)


def radar(accent: str) -> str:
    cx, cy = 1036, 158
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" '
        f'stroke-opacity="{o}" stroke-width="1"/>'
        for r, o in ((30, 0.35), (58, 0.28), (86, 0.18))
    )
    sweep = (
        f'<path d="M{cx} {cy} L{cx + 86} {cy - 50}" stroke="{accent}" '
        f'stroke-opacity="0.55" stroke-width="1"/>'
        f'<path d="M{cx} {cy} A86 86 0 0 0 {cx + 74} {cy + 44} Z" fill="{accent}" '
        f'fill-opacity="0.06"/>'
    )
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="2.2" fill="{accent}" fill-opacity="{o}"/>'
        for x, y, o in (
            (cx + 32, cy - 26, 0.9),
            (cx - 44, cy + 12, 0.7),
            (cx + 10, cy + 54, 0.5),
        )
    )
    return rings + sweep + dots


def card(p: dict, t: dict) -> str:
    accent = t["accent"][p["key"]]
    art = hexdump(t) if p["art"] == "hexdump" else radar(accent)
    lines = textwrap.wrap(p["description"], width=62)
    desc = "\n            ".join(
        f'<text x="52" y="{236 + i * 26}" font-family="{MONO}" font-size="20" '
        f'fill="{t["body"]}">{line}</text>'
        for i, line in enumerate(lines)
    )
    tags = "    ".join(
        f'<tspan fill="{accent}">&#183;</tspan>  {tag}' for tag in p["tags"]
    )

    return textwrap.dedent(
        f'''\
        <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="344"
             viewBox="0 0 1200 344" role="img"
             aria-label="{p['name']} — {p['role'].title()}">
          <defs>
            <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stop-color="{accent}" stop-opacity="0.75"/>
              <stop offset="0.45" stop-color="{accent}" stop-opacity="0.18"/>
              <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
            </linearGradient>
            <clipPath id="frame">
              <rect width="1200" height="320" rx="16"/>
            </clipPath>
            <filter id="soft" x="-5%" y="-20%" width="110%" height="145%">
              <feGaussianBlur stdDeviation="9"/>
            </filter>
          </defs>

          <g transform="translate(0 8)">
          <rect y="14" width="1200" height="320" rx="16" fill="{t['shadow']}"
                opacity="{t['shadow_opacity']}" filter="url(#soft)"/>
          <rect width="1200" height="320" rx="16" fill="{t['bg']}"/>
          <g clip-path="url(#frame)">
            <rect y="318" width="1200" height="2" fill="url(#rule)"/>
            <rect x="52" y="122" width="3" height="68" fill="{accent}" opacity="0.55"/>
          </g>
          <rect x="0.5" y="0.5" width="1199" height="319" rx="16" fill="none"
                stroke="{t['border']}"/>

          <text x="52" y="58" font-family="{MONO}" font-size="13" letter-spacing="4"
                fill="{t['index']}">{p['index']}</text>
          <text x="1148" y="58" text-anchor="end" font-family="{MONO}" font-size="12"
                letter-spacing="2" fill="{t['path']}">{p['path']}</text>

          <text x="80" y="162" font-family="{MONO}" font-size="62" font-weight="700"
                letter-spacing="7" fill="{t['name'][p['key']]}">{p['name']}</text>
          <text x="82" y="194" font-family="{MONO}" font-size="12" letter-spacing="4.5"
                fill="{t['role']}">{p['role']}</text>

          {desc}
          <text x="52" y="298" font-family="{MONO}" font-size="15" letter-spacing="1"
                fill="{t['body']}">{tags}</text>

          <text x="1148" y="298" text-anchor="end" font-family="{MONO}" font-size="11"
                letter-spacing="2.5" fill="{t['tip']}">OPEN REPOSITORY &#8599;</text>

          <g opacity="0.9">
            {art}
          </g>
          </g>
        </svg>
        '''
    )


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for project in PROJECTS:
        for theme_name, theme in THEMES.items():
            target = ASSETS / f"{project['key']}-card-{theme_name}.svg"
            target.write_text(card(project, theme), encoding="utf-8")
            print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
