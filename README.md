[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) [![rank](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) [![reward](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# THE WORLD TODAY — 25 November 2026 in one image

A front-page newspaper summing up Wednesday 25 November 2026 in a single
1024×1024 image: **50 verified stories, 12 regions, 30+ sources, 100% dated**.

- 3 hero stories: Shenzhou-24 launches, Cartagena hostages freed, US tariffs
  hit 14 economies.
- 47 briefs, each with a per-story source/credibility tag.
- 15 hand-drawn geometric scenes, a clean world map with 8 pins, a UTC
  timeline (04:00 Shenzhou → 23:57 Steelers cut) and a BY THE NUMBERS data
  bar (KOSPI -6.2% · TAIEX -4.8% · NIKKEI -2.9% · UK CAP GBP 2,166 ·
  31 killed in Cairo · PCE 3.8%).

## How it works

`main.py` (Python 3.13, standard library + Pillow) draws the page with no
network access and writes `asset.png` (and `output/entry.png`). The render is
fully deterministic — two runs produce byte-identical PNGs.

```sh
python3 main.py
```

## Story list (all verified against 25 November 2026 reporting)

Heroes: Shenzhou-24 launches (Qatar Tribune) · Cartagena hostages freed
(Al Jazeera) · US tariffs hit 14 economies (Reuters).

Briefs: Kyiv hits Russian cargo ship · Giuliani gets Medal of Freedom ·
Nikkei -2.9% · Cairo tanker fire: 31 dead · Java gold mine flood: 9 dead ·
Ramaphosa wins court case · Embraer faces 10% tariff · Kyiv hit by ballistic
missiles · IS attack kills 2 in Hasaka · Houthi strike on Saudi refinery ·
Huawei guilty in US trial · Chen Jining graft probe · Bangladesh wage +36% ·
N. Korea expels Swiss envoy · UK warns of Russian sabotage · Gulf plane crash:
6 dead · Canary Islands migrant record · Puigdemont to return Dec 12 ·
WHO pulls Ebola team · Australia–Solomons pact A$740M · Sooryavanshi 204 off
53 balls · Kospi -6.2% · UK energy cap +26% to £2,166 · CIA system hacked ·
Australia apologises to LGBTQ veterans · Coalition strikes Hodeidah · Ukraine
sinks Russian corvette · Russian war dead leak: 490k · Abu Dhabi talks stall ·
Nvidia -6% · Taiex -4.8% · Russia hits Ukraine grid · Anthropic below IPO
price · Netanyahu judges urge drop case · Iowa blasts 5 tons of explosives ·
Saudi kidnapped in Niger · India bars 'Cockroach' leader passport · Bulgaria
stops migrant boat · China presses Dutch on Nexperia · Abrego Garcia leaves
for Spain · US confidence near 2-year high · US inflation 3.8% in October ·
Houthi drone hits Riyadh tower · Trump spares turkeys · Melania reunites
children · Steelers cut Aaron Rodgers · NBA unveils $11B arena plan.

## Links

- Bounty: https://make.fun/bounty/news-image-20261125
- Leaderboard: https://make.fun/bounty/news-image-20261125/leaderboard

## License

MIT — see [LICENSE](LICENSE).
