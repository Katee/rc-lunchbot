# -*- coding: utf-8 -*-

from bot import Lunchbot
from defaults import defaults


def handler(event, context):
    lunchbot = Lunchbot(
        defaults["zulip_username"],
        defaults["zulip_api_key"],
        defaults["zulip_site"],
        defaults["zulip_stream"],
        date_overrides=defaults["date_overrides"],
        test_mode=(not defaults["production"])
    )

    lunchbot.handle_command(event["command"])
