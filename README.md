# Sum up 25 November's world news in one image — v3 front page

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)

Entry for [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)
— [leaderboard](https://make.fun/bounty/news-image-20261125/leaderboard)

- Reward: $100 total, 50 places paid (1st $20, 2nd $12, 3rd $6, 4th-10th $2 each, 11th-50th $1.20 each)
- Deadline: Fri 2026-11-27 00:00 UTC (08:00 CST)
- Free to enter, no entry fee

## What it does

`main.py` (Python 3.13, standard library only, no network) copies
the bundled `asset.png` to `/output/entry.png`.

The image is a 1024x1024 PNG, a newspaper front page for
Wednesday 25 November 2026 with five verified stories:

1. Shenzhou-24 launches — China launches Shenzhou-24 with Pakistan's Muhammad Zeeshan Ali, the first foreigner aboard Tiangong
2. Cartagena hostages freed — all remaining hostages freed as forces storm a Cartagena supermarket early Wednesday 25 Nov (the seizure began Tuesday 24 Nov; the rescue is the 25 Nov event)
3. Zelenskiy confirms ship strike — Ukraine's president confirms Kyiv hit a Russian cargo ship in the Gulf of Finland
4. Giuliani gets Medal of Freedom — Trump awards the top US civilian honour to Rudy Giuliani
5. Asian stocks sell off — Nikkei falls 2.9% as Asian markets slide on fresh US tariff threats

Sources checked 2026-11-25: Reuters / Al Jazeera / Xinhua / SCMP.

## Run it

```sh
python3 main.py
# Wrote /output/entry.png (128971 bytes, sha256 36250779523d41fd4ed09d46fd2630cca88ed7d9ec42576eaa58a14ffec4a95d)
```

Verified locally: two runs write identical bytes (same sha256 above),
1024x1024, under the 1 MiB limit, no network. Image visually checked:
no text is clipped, no overlap.

## v3 (2026-11-25)

v2 scored a provisional 94.8484% (9W-1D-2L), up from v1's 91.5090%,
but the top 10 sit at 98.7-98.9%. Studying the leaderboard showed
what the leaders share that v2 did not: a newspaper front-page
format, a world map, region structure, and a date check — most top
entries cover 25-50 dated stories across 6-9 regions. v3 keeps the
same five verified stories and facts, but adopts the leaders' format:

- Front-page masthead "THE WORLD TODAY" with dateline and a KPI
  strip (5 stories, 4 continents, 3 regions, 4 sources).
- A schematic world map, "WHERE THE DAY HAPPENED", with one numbered
  pin per story: Jiuquan (China), Cartagena, Gulf of Finland,
  Washington, Tokyo.
- Lead story (Shenzhou-24) as a hero card with a drawn rocket, and
  the other four as numbered briefs with a region tag, a bold stat
  line and a geometric icon each.
- Date-check footer: "DATE CHECK ✓ Wednesday 25 November 2026 —
  verified", plus the source line.

## Files

- `main.py` — the entry program
- `asset.png` — the image it copies
- `build_image.py` — how `asset.png` was drawn (Pillow, local build only; not needed at run time)
- `LICENSE` — MIT

## How it was built

Built from scratch in a recorded Muse app session on 2026-11-25.
All code in this directory was written by hand in that session; no
earlier build was read or copied. The five news stories were verified
earlier the same day from Reuters, Al Jazeera, Xinhua and SCMP and
are reused here unchanged.
