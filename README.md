[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) [![rank](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) [![reward](https://make.fun/badge/news-image-20261125/z451783818/makefun-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World Today — 25 November 2026 (v6)

A one-image front page summing up 25 November 2026's world news.

- Bounty: [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)
- Leaderboard: [news-image-20261125 leaderboard](https://make.fun/bounty/news-image-20261125/leaderboard)

## What it is

`main.py` (Python standard library only, no network) copies `asset.png`
into `/output/entry.png`. `asset.png` is a 1024x1024 front page drawn by
`build_image.py` with Pillow: masthead "THE WORLD TODAY", gold date line
"WEDNESDAY 25 NOVEMBER 2026", a KPI bar (36 stories, 9 regions, 25+
sources, 100% dated), three hero cards with drawn scenes, a UTC timeline
of the day, a "By the numbers" data bar, and 33 sourced one-line briefs
— 36 stories in total, each labelled with its source.

## Stories (all verified against 25 Nov 2026 reporting)

Heroes: Shenzhou-24 launches with Pakistan's Muhammad Zeeshan Ali, the
first foreigner aboard Tiangong; all remaining hostages freed in a dawn
raid on a Cartagena supermarket; the US proposes tariffs on 14 economies
(Vietnam 35%, China 20%).

New in v6: Cairo fuel-tanker fire kills 31; a flooded illegal gold mine
in West Java leaves 9 dead and 17 trapped; Ramaphosa wins the Phala
Phala court fight; a 10% duty is proposed on Embraer aircraft; Russian
ballistic missiles hit Kyiv; an Islamic State attack kills two Syrian
security men in Hasaka.

Also covered: Zelenskiy confirms the strike on a Russian cargo ship;
Giuliani receives the Medal of Freedom; Nikkei -2.9%; Houthi strike on a
Saudi refinery; Huawei guilty verdict; Chen Jining graft probe;
Bangladesh wage hike; North Korea expels the Swiss envoy; UK sabotage
warning; Gulf plane crash; Canary Islands migrant record; Puigdemont
returns; WHO pulls its Ebola team out of a Congo hospital;
Australia–Solomon Islands security pact (A$740M); 15-year-old
Sooryavanshi smashes 204 off 53 balls; Kospi -6.2%; UK energy price cap
+26% to £2,166 a year; CIA open-source system hacked; Australia
apologises to LGBTQ veterans; Saudi-led coalition strikes Hodeidah port;
Ukraine sinks the Russian corvette Merkury off Libya; leaked data puts
Russian war dead at 490,000 confirmed (720,000 with missing); Abu Dhabi
talks stall; Nvidia gives back 6%; Taiex -4.8% (down 1,927 points);
Russia hits Ukraine's power grid with 112 drones overnight; Anthropic
slips below its IPO price.

Sources include Reuters, Al Jazeera, AP, CNN, Yonhap, CNA, Xinhua, Gulf
News, Focus Taiwan, Investopedia and IOL.

## Build

```sh
python3 build_image.py   # writes asset.png (1024x1024, deterministic)
python3 main.py          # writes /output/entry.png
```

## Licence

MIT — see LICENSE.
