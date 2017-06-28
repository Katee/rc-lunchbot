# -*- coding: utf-8 -*-

import os

defaults = {
    'zulip_username': os.environ['ZULIP_LUNCHBOT_EMAIL'],
    'zulip_api_key': os.environ['ZULIP_LUNCHBOT_KEY'],
    'zulip_site': os.getenv('ZULIP_LUNCHBOT_SITE', 'https://recurse.zulipchat.com'),
    'zulip_stream': os.getenv('ZULIP_LUNCHBOT_STREAM', 'lunchbot-staging'),
    'date_overrides': os.getenv('ZULIP_LUNCHBOT_DATE_OVERRIDES', ''),
    'production': False,
}
