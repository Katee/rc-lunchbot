#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lunchbot import Lunchbot, defaults, parse_date_overrides


def handler(event, context):
    lunchbot = Lunchbot(
        defaults["zulip_username"],
        defaults["zulip_api_key"],
        defaults["zulip_site"],
        defaults["zulip_stream"],
        date_overrides=parse_date_overrides(defaults["date_overrides"].split(',')),
        test_mode=(not defaults["production"])
    )

    lunchbot.handle_command(event["command"])
