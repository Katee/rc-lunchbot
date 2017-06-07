# RC Lunchbot

New at RC and want to meet new people? Lunchbot is a simple opt-in Zulip bot that assigns randomized lunch groups.

## How it works

Join the 'lunchbot' stream to opt-in.
On days when RC is open Lunchbot will privately message you after 11am to verify you want to be part of a lunch group.
Around noon Lunchbot posts the lunch groups for that day in the 'lunchbot' stream.

## Setup

Add the expected variables to ENV. An easy way to do this is to `cp .env.sample .env` and edit `.env` to have the correct values. Then you can `source .env` before running `python bot.py`.

## Nice to Haves

* Have Lunchbot make restaurant recommendations from a curated list compiled by RCers (it would be extra nice to take into account dietary restrictions)
* Have options for lunch groups (example: some people want to be in a small group others want to be in a large group)
* Find out which days RC is open (maybe based on the calendar?)
