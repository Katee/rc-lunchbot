# -*- coding: utf-8 -*-

import os

defaults = {
    'zulip_username': os.getenv('ZULIP_LUNCHBOT_EMAIL', None),
    'zulip_api_key': os.getenv('ZULIP_LUNCHBOT_KEY', None),
    'zulip_site': os.getenv('ZULIP_LUNCHBOT_SITE', 'https://recurse.zulipchat.com'),
    'zulip_stream': os.getenv('ZULIP_LUNCHBOT_STREAM', 'lunchbot-staging'),
    'date_overrides': os.getenv('ZULIP_LUNCHBOT_DATE_OVERRIDES', ''),
    'production': False,
}
