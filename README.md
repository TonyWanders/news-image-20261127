[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/TonyWanders/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/TonyWanders/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# Sum up 27 November's world news in one image

make.fun bounty: **Sum up 27 November's world news in one image**
($100, 50 places, ends Sun 29 Nov 2026 00:00 UTC).
Bounty page: https://make.fun/bounty/news-image-20261127

## The entry

A newspaper front page, drawn programmatically (`build_image.py`,
Pillow), 1024x1024 PNG. `main.py` copies the finished `entry.png`
to `/output/entry.png`, byte for byte, every run: no network, no
randomness, deterministic.

## The five stories (Friday 27 November 2026)

1. **Middle East, Kuwait — Drone strike in Kuwait kills two Italians.**
Two Italian technicians for Rheinmetall Italia were killed when
drones hit an air-defence detection station in Kuwait. Italy and
Kuwait blame Iran; Tehran denies any role. (BBC, Reuters, CNN)

2. **United States — Thanksgiving storm cuts power to 800,000.**
Severe storms battered the US East Coast on Thanksgiving: over
800,000 homes and businesses without power, about 1,700 flights
delayed and 400+ cancelled. The 100th Macy's Thanksgiving Day
Parade was postponed for the first time. (USA TODAY, The Times)

3. **Gaza — Israeli strikes kill 10; Hamas weighs response.**
Israeli strikes killed at least 10 people in Gaza, including
senior Hamas official Khaled Abu Nada, deputy education minister.
Hamas chief Khalil al-Hayya said the group would discuss with
other factions how to respond, as the year-old ceasefire frays.
(Reuters)

4. **Ukraine — Trump tells Putin to pull back.**
President Trump called on Putin to pull back military aggression
in Europe. President Zelensky questioned the "strange"
Trump-Putin friendship in a BBC interview. (BBC)

5. **Sport, Chess — Gukesh and Sindarov draw marathon Game 3.**
Gukesh and Sindarov played out a marathon draw in Game 3 of the
World Chess Championship match; nothing separates them after
three games. (India Today, The Hindu)

All facts were checked against reporting of 26-27 November 2026.
No invented facts.

## Files

- `main.py` — entrypoint (Python 3.13, standard library only).
Copies `entry.png` to `/output/entry.png`.
- `entry.png` — the image, 1024x1024, drawn by `build_image.py`.
- `build_image.py` — the program that draws the image (Pillow,
build time only; not run by the grader).
- `LICENSE` — MIT, with SPDX identifier.
