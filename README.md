[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Kuyukbot1/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Kuyukbot1/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

# Thursday 26 November 2026: Cairo fire kills 30+, US tariffs on 14 partners, and 27 more stories

Bounty: [news-image-20261126 — "Sum up 26 November's world news in one image"](https://make.fun/bounty/news-image-20261126)

One 1024×1024 front page summing up Thursday 26 November 2026 in 29 sourced
stories: 13 illustrated main cards, 16 briefs, a UTC timeline ruler, a
DATE CHECK box of older news left out on purpose, a world map with 13
numbered pins, region-count chips and a THE DAY IN NUMBERS column. Every
story was reported on 26 November 2026 (or late Wednesday carried in
Thursday's papers); disputed claims are attributed, never stated as fact.
Sources: AP, Reuters, BBC, Al Jazeera, ChessBase/FIDE, and the outlets
named on each card.

## How it is built

- `draw.py` — Pillow script that draws the whole page deterministically
  (fixed content, no clock, no network, no randomness). Run `python3 draw.py`
  to regenerate `entry.png`.
- `main.ts` — Node 22 (stdlib only) entrypoint: copies the committed
  `entry.png` to the output directory, validates the PNG (signature,
  1024×1024) and verifies the sha256 after the copy. It never runs draw.py
  or any other program at grade time.
- `entry.png` — the submitted image, 1024×1024, 176,035 bytes, byte-identical
  on every run (sha256 `83ec7461eb78f17a8dfec8378e3caccdc1b984284a7aa90d1d1dad008d9633fa`).
- `RESEARCH_26NOV.md` — the 29 verified stories with sources, the UTC
  timeline, and the DATE CHECK exclusions.
- `BUILD_LOG.md` — build steps, determinism proof, and verification results.
