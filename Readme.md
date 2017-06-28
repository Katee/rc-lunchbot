# RC Lunchbot

New at RC and want to meet new people? Lunchbot is a simple opt-in Zulip bot that assigns randomized lunch groups.

## How it works

Join the 'lunchbot' stream to opt-in.
On days when RC is open Lunchbot will privately message you after 11am to verify you want to be part of a lunch group.
Around noon Lunchbot posts the lunch groups for that day in the 'lunchbot' stream.

### Date overrides

Sometimes lunchbot needs to run on non standard dates. To handle this you can set `ENV['ZULIP_LUNCHBOT_DATE_OVERRIDES']` to a comma separated list of dates prefixed by "+" or "-" in the format "2017-07-03". See `.env.sample` for examples.

## Local setup

Add the expected variables to ENV. An easy way to do this is to `cp .env.sample .env` and edit `.env` to have the correct values. Then you can `source .env` before running `python bot.py`.

## Deployment on Lambda

This project runs on AWS Lambda. It uses Cloudwatch cron events to trigger the function `lambda_handler` in `bot.py`. The secrets are stored in Lambda environment variables. Look at `.env.sample` to see the variables that are required. Note: `zulip-beta` requires something to be set for `ENV["HOME"]` and by default a Lambda does not have `ENV["HOME"]`. Setting `HOME` to an empty string will allow it to run.

### Lambda package creation

The project is uploaded to Lambda as a zip, `bin/package_lambda.sh` is included to make creating `package.zip` easy. It expects `virtualenv` to be available on your system.

## Nice to haves

* Have Lunchbot make restaurant recommendations from a curated list compiled by RCers (it would be extra nice to take into account dietary restrictions)
* Have options for lunch groups (example: some people want to be in a small group others want to be in a large group)
* Find out which days RC is open (maybe based on the calendar?)
