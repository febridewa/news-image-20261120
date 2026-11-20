# The World in One Day — Friday 20 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261120-blue)](https://make.fun/bounty/news-image-20261120)

One image summing up the world news of **Friday 20 November 2026** — a
morning-edition front page with 50 stories, all of which happened or were
first reported on that day.

## The image

`entry.png` (1024×1024, 593 KB) is a newspaper front page:

- **Headline:** Friday 20 November 2026, with the day's three biggest stories
  in the subhead — Cyclone Akvan's landfall in Odisha, Trump putting the Iran
  decision off to 2027, and Asia's markets sliding.
- **12 picture stories** with original art drawn in code: Akvan, the Iran
  call, the AI selloff, the first photos of the damaged PIF Tower in Riyadh,
  Voyager 1 crossing one light-day, Hayabusa2 dropping its asteroid landing,
  COP31's final day, South Korea's top court clearing ex-PM Han, Fiji's
  drought disaster, the Crimean Bridge attack, the US–Venezuela thaw, and
  Justice Varma.
- **38 more stories** in the "Also on Friday 20 November" list, plus a
  dotted world map with numbered pins.
- **DATE CHECK box:** every story was checked against the day it broke.
  Stories that broke on Thursday 19 November — the ICJ's genocide ruling on
  Myanmar, the Trump–Xi–Putin summit in Shenzhen, the Houthi strike on
  Riyadh's PIF Tower, GTA VI's launch, Anthropic's Nasdaq debut, Denmark's
  Greenland deal — are left out (the Riyadh item is Friday's follow-up: the
  first photos of the damage).

## How it was built

`draw.py` draws the whole page with Python + PIL (DejaVu fonts): layout,
flat illustrations, the dotted world map and every line of text. `main.py`
(Python 3.13, standard library only) copies `entry.png` to `/output/entry.png`.

    python3 draw.py        # re-render entry.png
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

## Sources

Reuters, AP, AFP, BBC, The Hindu, NDTV, NASA, IMD. Stories as reported by
01:00 UTC, 20 November 2026.

Referral: `6etrfz79`
