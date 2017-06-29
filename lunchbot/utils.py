# -*- coding: utf-8 -*-
import datetime


def ordinal(n):
    if 10 <= n % 100 < 20:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, "th")


def parse_date_overrides(date_overrides):
    parsed_date_overrides = {}

    for date_override_string in date_overrides:
        if len(date_override_string) == 0:
            continue

        if date_override_string[0] == "+":
            override = True
        elif date_override_string[0] == "-":
            override = False
        else:
            raise Exception("Missing '+' or '-' prefix for date override '%s'" % date_override_string)

        date = datetime.datetime.strptime(date_override_string[1:], '%Y-%m-%d')
        parsed_date_overrides[date] = override

    return parsed_date_overrides
