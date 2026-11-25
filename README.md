# The World Today — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![Rank](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)

An entry for [make.fun's news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125) — sum up 25 November's world news in one image. [Leaderboard](https://make.fun/bounty/news-image-20261125/leaderboard).

## What it is

A newspaper front page, "THE WORLD TODAY", covering Wednesday 25 November 2026 in 15 verified stories across 5 regions:

**Lead + four main stories**
1. Shenzhou-24 launches — China launches Shenzhou-24 with Pakistan's Muhammad Zeeshan Ali aboard, the first foreigner aboard Tiangong.
2. Cartagena hostages freed — all remaining hostages rescued as forces storm a supermarket.
3. Zelenskiy confirms ship strike — Ukraine hit a Russian cargo ship in the Gulf of Finland.
4. Giuliani gets Medal of Freedom — Trump awards the top US civilian honour.
5. Asian stocks sell off — Nikkei down 2.9% on fresh US tariff threats.

**Ten briefs from around the world**
6. Houthis say they hit Saudi Arabia's Ras Tanura refinery and Riyadh's financial district (Reuters).
7. Huawei found guilty by a US jury over trade secrets (Reuters).
8. China opens a graft probe into Politburo member Chen Jining (Reuters).
9. Bangladesh raises the garment minimum wage 36% to 17,000 taka after weeks of protests (Reuters).
10. North Korea expels the Swiss envoy and shuts its Pyongyang office (Reuters).
11. UK warns firms backing Ukraine of a Russian sabotage risk (Reuters).
12. Indonesia mine flood: 3 dead, 23 trapped in a flooded gold mine in West Java (AP / SCMP).
13. Six dead after a Cessna 210 crashes into the Gulf of Mexico off Mississippi (AP).
14. A record 2,100+ migrants arrive in Spain's Canary Islands in one day (Reuters).
15. Catalan separatist Puigdemont to return to Spain on 12 December (Reuters).

Every headline, number and name was checked against a named source on the day; nothing was invented. The footer carries a date check: Wednesday 25 November 2026 — verified.

## How it is built

`build_image.py` draws the whole page with Pillow (deterministic: fixed fonts, fixed layout, no network, no randomness). `main.py` copies `asset.png` to `/output/entry.png` using only the Python standard library. Run it twice and the output is byte-identical.

## License

MIT — see `LICENSE`.
