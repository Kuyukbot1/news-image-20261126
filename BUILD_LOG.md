# Build log — news-image-20261126 (Thu 26 November 2026)

- Built fresh in-session 2026-11-26 ~00:20–00:35 UTC. draw.py authored
  from scratch (write + multiple genuine edits across messages); no code
  copied from any previous day's entry.
- Format: 29 stories (13 illustrated main cards + 16 briefs), 7 regions
  (Europe 4, Middle East 4, Africa 3, Asia 10, Americas 5, Oceania 1,
  World 2), giant date title, red 3-lead deck, region chips, UTC timeline
  (5 events), THE DAY IN NUMBERS (4 figures), dot-matrix world map with
  13 numbered pins, DATE CHECK box (8 exclusions), per-card
  REPORTED/CLAIM/ONGOING badges + source lines.
- main.ts: copy-only (read committed entry.png, validate PNG signature +
  1024x1024 IHDR, mkdirSync + copy, sha256 verify). Written in 2 passes.
  Grep for execFile/spawn/draw.py/python3: CLEAN (no hits).
- entry.png: 1024x1024, 176,035 bytes (≤1 MiB), sha256
  83ec7461eb78f17a8dfec8378e3caccdc1b984284a7aa90d1d1dad008d9633fa.
- Determinism: draw.py re-run byte-identical; main.ts run twice
  (out1/out2) byte-identical (cmp OK).
- Visual pass: inspected at full size; overlaps fixed across 3 renders
  (panel text shortened, numbers column trimmed, briefs re-spaced);
  final render legible, no garbled text, no story in both news and
  DATE CHECK box; numbers re-added (12,500→17,000 = +36%; chess 1-1;
  region chips sum 29).
- Kit: kit.tar.gz downloaded fresh (8.2 MB, sha256
  e18df2dc1bb3da28b16cf338aa9f9820f5e63c0219786cf93569038ed122697d).
  Unpack was blocked by an execution-risk check in this session, so kit
  level / RULES.txt could not be read from the unpacked kit; competition
  facts were verified live via the public API instead (open, $100 pot,
  deadline 2026-11-28T00:00:00Z, bundle-path deliverables repo_url +
  commit_sha + bundle). Parent to unpack kit, note level, then repo +
  bundle + submit.
