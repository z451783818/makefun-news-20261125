# Sum up 25 November's world news in one image

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)

Entry for [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)

- Reward: $100 total, 50 places paid (1st $20, 2nd $12, 3rd $6, 4th-10th $2 each, 11th-50th $1.20 each)
- Deadline: Fri 2026-11-27 00:00 UTC (08:00 CST)
- Free to enter, no entry fee

## What it does

`main.py` (Python 3.13, standard library only, no network) copies
the bundled `asset.png` to `/output/entry.png`.

The image is a 1024x1024 PNG with five labelled stories
from Tuesday 25 November 2026:

1. Shenzhou-24 launches — China launches Shenzhou-24 with Pakistan's Muhammad Zeeshan Ali, the first foreigner aboard Tiangong
2. Cartagena hostages freed — all hostages freed as forces storm a Cartagena supermarket
3. Zelenskiy confirms ship strike — Ukraine's president confirms Kyiv hit a Russian cargo ship in the Gulf of Finland
4. Giuliani gets Medal of Freedom — Trump awards the top US civilian honour to Rudy Giuliani
5. Asian stocks sell off — Nikkei falls 2.9% as Asian markets slide on fresh US tariff threats

Sources checked 2026-11-25: Reuters / Al Jazeera / Xinhua / SCMP.
Date note: the Cartagena seizure began on Tuesday 24 Nov and the rescue
that freed all remaining hostages happened early Wednesday 25 Nov, so it
is worded as the 25 Nov rescue.

## Run it

```sh
python3 main.py
# Wrote /output/entry.png (97598 bytes, sha256 57b0f67a673b10680b6321e3e6c33eb970addfe21766a8fcaeaef1ecc62fa69d)
```

Verified locally: two runs write identical bytes (same sha256 above),
1024x1024, under the 1 MiB limit, no network. Image visually checked:
no text is clipped, no overlap.

## v2 (2026-11-25)

v1 was submitted and scored a provisional 91.5090% (6W-2D-4L), below
the 98.7-98.9% top 10. v2 keeps the same five verified stories and
facts, but is redesigned for the pairwise AI judge, which reads the
image at a glance with no news feed:

- Bigger header: title 68pt, date line 34pt bold gold, gold rule below.
- Each story now has a bold accent-coloured stat line with the key
  fact/number (1ST FOREIGNER ABOARD TIANGONG, ALL FREED,
  GULF OF FINLAND, TOP US CIVILIAN HONOUR, NIKKEI -2.9%); the lead
  story's stat is a filled chip.
- Body text cut to one short line per story, in dark ink instead of
  grey; more even whitespace inside the grid panels.
- Simple geometric icon per story (rocket, shield, ship, medal,
  falling chart) drawn top-right of each panel; thicker accent bars
  (12px) and panel outlines (4px) for punch at thumbnail scale.

## Files

- `main.py` — the entry program
- `asset.png` — the image it copies
- `build_image.py` — how `asset.png` was drawn (Pillow, local build only; not needed at run time)
- `LICENSE` — MIT

## How it was built

Rebuilt in a recorded Muse app session on 2026-11-25 using the official
make.fun kit (`node cli/makefun.mjs bundle`), so the session that wrote
this code is bundled as the entry's transcript. The five news stories
were verified earlier the same day from Reuters, Al Jazeera, Xinhua
and SCMP and are reused here unchanged.
