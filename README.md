# Sum up 25 November's world news in one image

Entry for https://make.fun/bounty/news-image-20261125

- Reward: $100 total, 50 places paid (1st $20, 2nd $12, 3rd $6, 4th-10th $2 each, 11th-50th $1.20 each)
- Deadline: Fri 2026-11-27 00:00 UTC (08:00 CST)
- Free to enter, no entry fee

## What it does

`main.py` (Python 3.13, standard library only, no network) copies
the bundled `asset.png` to `/output/entry.png`.

The image is a 1024x1024 PNG, 86,853 bytes, with five labelled stories
from Tuesday 25 November 2026:

1. Shenzhou-24 launches — China launches Shenzhou-24 with Pakistan's Muhammad Zeeshan Ali, the first foreigner aboard Tiangong
2. Cartagena hostages freed — all hostages rescued as forces storm a Cartagena supermarket; about 30 were seized on Tuesday
3. Zelenskiy confirms ship strike — Ukraine's president confirms Kyiv hit a Russian cargo ship in the Gulf of Finland
4. Giuliani gets Medal of Freedom — Trump awards the top US civilian honour to Rudy Giuliani
5. Asian stocks sell off — Nikkei falls 2.9% as Asian markets slide on fresh US tariff threats

Sources checked 2026-11-25: Reuters (world news summary, markets, Shenzhou coverage via Qatar Tribune / WireMinute), Al Jazeera and Xinhua (Cartagena rescue), SCMP (Giuliani). Date note: the Cartagena seizure began on Tuesday 24 Nov and the rescue that freed all remaining hostages happened early Wednesday 25 Nov, so it is worded as the 25 Nov rescue; the Chen Jining graft-probe announcement was 24 Nov, so it was not used.

## Run it

```sh
python3 main.py
# Wrote /output/entry.png (86853 bytes, sha256 3b31a75a56d8c0b910e75df10bd81e574c2342fbcb927ac5d5f61416dc524a8a)
```

Verified locally: two runs write identical bytes (same sha256 above),
1024x1024, under the 1 MiB limit, no network. Image visually checked:
no text is clipped.

## Files

- `main.py` — the entry program
- `asset.png` — the image it copies
- `build_image.py` — how `asset.png` was drawn (Pillow, local build only; not needed at run time)
- `LICENSE` — MIT

## Notes / risks

- This entry was built in a Muse chat session, not in a recorded
  coding-agent session with provider token usage. make.fun may treat
  a handed-over session as ineligible for a paid place; check the
  bounty requirements before submitting.
- Whether China-based users are restricted was not confirmed on
  public make.fun pages.
- Nothing here has been submitted or claimed. Submission and claiming
  need the owner's GitHub account and Solana wallet.
