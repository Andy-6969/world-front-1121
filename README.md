# world-front-1121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Andy-6969/world-front-1121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Andy-6969/world-front-1121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Saturday 21 November 2026 on one page, made for the [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) bounty
"Sum up 21 November's world news in one image".

The lead is a map of the Gulf: Bahrain says an Iranian attack set an industrial site on fire, UKMTO
reports two tankers hit off Khasab, Iran's Guards say they downed US drones over Hormuz and Houthi
missiles aimed at Riyadh are shot down. Beside it: drones set the Russian cargo ship Sparta II ablaze
off Finland, and COP31 runs past its Friday deadline. Ten drawn stories follow (EU–Indonesia trade
pact, "El Chapo Isidro" arrested, killer-robot talks, BepiColombo at Mercury, two deep quakes, the
Bayelsa boat toll, the Hartha power-station fire, French cost-of-living marches, England 37–12 New
Zealand, BTS at MAMA), then 20 short items, a world map keyed to the story numbers and a date check
naming what was left out because it was first reported before Saturday.

## Build and run

- `src/front.html` is the page: HTML, CSS and inline SVG drawings written for it.
- `tools/build.py` fills in the coastlines from Natural Earth (public domain; set `NE_DIR` to a folder
  holding `ne_110m_land.geojson` and `ne_50m_admin_0_countries.geojson`, not committed) and writes
  `out/front.html`.
- `tools/render.ps1` screenshots it with headless Chrome at 2x and `tools/shrink.py` scales that to
  the 1024 x 1024 `entry.png`.
- `main.ts` (Node 22, standard library) checks `entry.png` and writes it to `/output/entry.png`:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Facts come from the outlets printed beside each story: Al Jazeera, Reuters, AP, AFP, BBC, USGS, ESA,
the European Commission, Euronews, NEMA, the Korea Times, the ICC and Finland's Border Guard, among
others. Times are UTC.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
