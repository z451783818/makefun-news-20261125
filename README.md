# Sum up 25 November's world news in one image

Entry for https://make.fun/bounty/news-image-20261125

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
# Wrote /output/entry.png (102565 bytes, sha256 379d48b9e2ab70d834e82e09c09e58658d70c5603ff2d7c03d900827b551e9b5)
```

Verified locally: two runs write identical bytes (same sha256 above),
1024x1024, under the 1 MiB limit, no network. Image visually checked:
no text is clipped.

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
