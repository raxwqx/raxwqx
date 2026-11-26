#!/usr/bin/env python3
"""Render the two "selected work" cards used by the profile README.

Kept in the repository so the cards can be regenerated after edits:
    python3 tools/make_cards.py

Design notes: fixed 1200x300 frame, dark canvas, one accent per project,
monospace type, everything drawn with plain SVG (no external assets).
"""

from __future__ import annotations

import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "Fira Code, DejaVu Sans Mono, SFMono-Regular, Menlo, monospace"

PROJECTS = [
    {
        "slug": "argent-card",
        "index": "01",
        "name": "ARGENT",
        "path": "raxwqx/argent",
        "role": "SYMBOLIC EXECUTION ENGINE",
        "description": "Forks at data-dependent branches, prunes infeasible paths with z3, "
                       "and replays every reported input concretely.",
        "tags": ["Python", "z3", "SMT", "32-bit ISA"],
        "accent": "#c9d1d9",
        "accent_dim": "#6e7681",
        "name_fill": "url(#metal)",
        "art": "hexdump",
    },
    {
        "slug": "noxtrace-card",
        "index": "02",
        "name": "NOXTRACE",
        "path": "raxwqx/NOXTRACE",
        "role": "MULTI-ENGINE SECURITY WORKSTATION",
        "description": "Network reconnaissance, web inspection, source analysis and digital "
                       "investigation in one workflow.",
        "tags": ["Python", "Go", "Rust", "C"],
        "accent": "#58a6ff",
        "accent_dim": "#1f6feb",
        "name_fill": "url(#steel)",
        "art": "radar",
    },
]

HEX = [
    "4d 5a 90 00 03 00 00 00",
    "04 00 00 00 ff ff 00 00",
    "b8 00 00 00 00 00 00 00",
    "40 00 00 00 00 00 00 00",
]


def hexdump() -> str:
    rows = []
    for i, line in enumerate(HEX):
        y = 118 + i * 30
        rows.append(
            f'<text x="860" y="{y}" font-family="{MONO}" font-size="14" '
            f'letter-spacing="1" fill="{"#8b949e" if i else "#6e7681"}">{line}</text>'
        )
    # highlight one byte in the first row
    rows.append(
        '<rect x="882" y="105" width="19" height="17" rx="3" fill="#c9d1d9" fill-opacity="0.10" '
        'stroke="#8b949e" stroke-opacity="0.45"/>'
    )
    return "\n    ".join(rows)


def radar() -> str:
    cx, cy = 1036, 158
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#58a6ff" '
        f'stroke-opacity="{o}" stroke-width="1"/>'
        for r, o in ((30, 0.20), (58, 0.16), (86, 0.10))
    )
    sweep = (
        f'<path d="M{cx} {cy} L{cx + 86} {cy - 50}" stroke="#58a6ff" '
        f'stroke-opacity="0.55" stroke-width="1"/>'
        f'<path d="M{cx} {cy} A86 86 0 0 0 {cx + 74} {cy + 44} Z" fill="#58a6ff" fill-opacity="0.06"/>'
    )
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="2.2" fill="#58a6ff" fill-opacity="{o}"/>'
        for x, y, o in (
            (cx + 32, cy - 26, 0.9),
            (cx - 44, cy + 12, 0.7),
            (cx + 10, cy + 54, 0.5),
        )
    )
    return rings + sweep + dots


def card(p: dict) -> str:
    art = hexdump() if p["art"] == "hexdump" else radar()
    lines = textwrap.wrap(p["description"], width=62)
    desc = "".join(
        f'<text x="52" y="{236 + i * 26}" font-family="{MONO}" font-size="20" '
        f'fill="#8b949e">{line}</text>'
        for i, line in enumerate(lines)
    )
    tags = "    ".join(
        f'<tspan fill="{p["accent"]}">&#183;</tspan>  {t}' for t in p["tags"]
    )
    return textwrap.dedent(
        f'''\
        <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300"
             viewBox="0 0 1200 300" role="img"
             aria-label="{p['name']} — {p['role'].title()}">
          <defs>
            <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#f7f9fb"/>
              <stop offset="0.45" stop-color="#d3dae2"/>
              <stop offset="0.55" stop-color="#8b949e"/>
              <stop offset="0.68" stop-color="#c3ccd5"/>
              <stop offset="1" stop-color="#7d8792"/>
            </linearGradient>
            <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#cfe4ff"/>
              <stop offset="0.5" stop-color="#79b8ff"/>
              <stop offset="1" stop-color="#388bfd"/>
            </linearGradient>
            <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stop-color="{p['accent']}" stop-opacity="0.95"/>
              <stop offset="0.45" stop-color="{p['accent']}" stop-opacity="0.30"/>
              <stop offset="1" stop-color="{p['accent']}" stop-opacity="0"/>
            </linearGradient>
            <radialGradient id="glow" cx="0.82" cy="0.2" r="0.75">
              <stop offset="0" stop-color="{p['accent']}" stop-opacity="0.10"/>
              <stop offset="1" stop-color="{p['accent']}" stop-opacity="0"/>
            </radialGradient>
            <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
              <path d="M32 0H0V32" fill="none" stroke="#161b22" stroke-width="1"/>
            </pattern>
            <clipPath id="frame">
              <rect width="1200" height="300" rx="16"/>
            </clipPath>
          </defs>

          <rect width="1200" height="300" rx="16" fill="#0b0f14"/>
          <g clip-path="url(#frame)">
            <rect width="1200" height="300" fill="url(#grid)" opacity="0.7"/>
            <rect width="1200" height="300" fill="url(#glow)"/>
            <rect y="298" width="1200" height="2" fill="url(#rule)"/>
            <rect x="52" y="132" width="3" height="68" fill="{p['accent']}" opacity="0.55"/>
          </g>
          <rect x="0.5" y="0.5" width="1199" height="299" rx="16" fill="none"
                stroke="#21262d"/>

          <text x="52" y="62" font-family="{MONO}" font-size="13" letter-spacing="4"
                fill="{p['accent_dim']}">{p['index']}</text>
          <text x="1148" y="62" text-anchor="end" font-family="{MONO}" font-size="12"
                letter-spacing="2" fill="#6e7681">{p['path']}</text>

          <text x="80" y="170" font-family="{MONO}" font-size="62" font-weight="700"
                letter-spacing="7" fill="{p['name_fill']}">{p['name']}</text>
          <text x="82" y="202" font-family="{MONO}" font-size="12" letter-spacing="4.5"
                fill="#6e7681">{p['role']}</text>

          {desc}
          <text x="52" y="288" font-family="{MONO}" font-size="15" letter-spacing="1"
                fill="#6e7681">{tags}</text>

          <g opacity="0.9">
            {art}
          </g>
          <text x="1148" y="274" text-anchor="end" font-family="{MONO}" font-size="18"
                fill="{p['accent']}" fill-opacity="0.75">&#8599;</text>
        </svg>
        '''
    )


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for project in PROJECTS:
        target = ASSETS / f"{project['slug']}.svg"
        target.write_text(card(project), encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
