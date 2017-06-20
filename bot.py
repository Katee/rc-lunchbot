#! /usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import random
import time
import datetime
import math
import re

import zulip

from utils import ordinal


class Lunchbot():
    """
    On Zulip create a bot under "settings" and use the username and API key to initialize this bot.
    Stream is the stream the bot should be active on.
    """
    def __init__(self, zulip_username, zulip_api_key, zulip_site, stream, test_mode=True):
        self.test_mode = test_mode
        self.client = zulip.Client(zulip_username, zulip_api_key, site=zulip_site)
        self.stream = stream

        # Subscribe to our stream
        self.client.add_subscriptions([{'name': self.stream}])

    def clean_message_content(self, message):
        p = re.compile('([^\w]*)')
        content = message['content'].lower()
        return p.sub('', content)

    def message_sentiment(self, message):
        """Using a simple hardcoded list figure out the meaning of a message"""
        content = self.clean_message_content(message)

        skip_responses = [
            'ski', 'skip',
            'pass',
            'rsvp no',
        ]

        yes_responses = [
            'y', 'ye', 'yes', 'yea', 'yeah',
            'rsvp yes',
        ]

        is_skip_response = content in skip_responses
        is_yes_response = content in yes_responses

        if is_yes_response and not is_skip_response:
            return 1
        elif is_skip_response:
            return -1
        else:
            print(" !!! Unknown message sentiment")
            self.print_message(message)
            return 0

    def is_bot_email(self, email):
        return email.endswith('@recurse.zulipchat.com')

    def subscriber_emails(self):
        """Return all emails for non bot subscribers"""
        subscriber_emails = self.client.get_subscribers(stream=self.stream)['subscribers']
        return [email for email in subscriber_emails if not self.is_bot_email(email)]

    def members_from_emails(self, emails):
        """Return a list of member for each passed in email"""
        all_members = self.client.get_members()['members']
        return [member for member in all_members if member['email'] in emails]

    def recent_messages(self):
        request = {
            'num_before': 100,
            'num_after': 0,
            'anchor': 1000000000,
            'apply_markdown': False
        }

        return self.client.call_endpoint(
            url='messages',
            method='GET',
            request=request,
        )

    def relevant_messages(self):
        messages = self.recent_messages()

        if 'messages' in messages:
            return [message for message in messages['messages'] if self.is_message_relevant(message)]

        return []

    def is_message_relevant(self, message):
        """Test if a message is to Lunchbot and has been sent recently in the last four hours"""
        epoch_time = int(time.time())

        return (message['subject'] == self.rollcall_subject() or message['type'] == "private") \
            and message['sender_full_name'] != "Lunchbot" \
            and abs(message['timestamp'] - epoch_time) < (60 * 60 * 4)

    def rollcall_subject(self):
        d = datetime.datetime.today()
        return "Lunchbot %s%s" % (d.strftime("%A %B %-d"), ordinal(d.day))

    def message_subject(self, group_index):
        d = datetime.datetime.today()
        return "Lunchbot %s%s: Group %s" % (d.strftime("%A %B %-d"), ordinal(d.day), group_index)

    def create_lunch_groups(self, subscribers):
        """Assign groups of approximately 5 people"""
        num_groups = int(math.ceil(len(subscribers) / 5.0))
        groups = [[] for i in range(num_groups)]

        for i in range(len(subscribers)):
            groups[i % num_groups].append(subscribers[i])

        return groups

    def handle_message(self, message):
        message_sentiment = self.message_sentiment(message)

        if message_sentiment == 1:
            self.opted_in_emails.add(message['sender_email'])
        elif message_sentiment == -1:
            try:
                self.opted_in_emails.remove(message['sender_email'])
            except KeyError:
                pass  # don't care

    def do_lunch(self):
        self.opted_in_emails = set()
        relevant_messages = self.relevant_messages()

        for message in relevant_messages:
            self.handle_message(message)

        subscribers = self.members_from_emails(self.opted_in_emails)
        random.shuffle(subscribers)
        groups = self.create_lunch_groups(subscribers)

        for group_index, group in enumerate(groups):
            groups_msg = {
                'to': self.stream,
                'subject': self.message_subject(group_index),
                'content': "Meet up with your group at 12:30 by the door (or figure out a different time) and get lunch together. " + ', '.join([self.mention_member(user) for user in groups[group_index]])
            }
            self.send_message('stream', groups_msg)

    def is_asf_day(self):
        return datetime.datetime.today().weekday() == 3

    def do_pre_lunch(self):
        """PM members of the stream to see if they want to do lunch today"""
        subscriber_emails = self.subscriber_emails()

        for subscriber_email in subscriber_emails:
            print("Sending PM to %s" % subscriber_email)
            msg_content = "Would you like to be assigned a group of RCers to have lunch with today? I understand responses like 'yes' or 'skip'. If you want to skip you can also just not respond."

            # Mention Abstract Salad Factory when relevant
            if self.is_asf_day():
                msg_content += " Alternatively today is Abstract Salad Factory, grab an ingredient and head to Hopper at 1pm to make a salad."

            self.send_message('private', {
                'to': subscriber_email,
                'subject': self.rollcall_subject(),
                'content': msg_content
            })

    def do_asf(self):
        """Send a reminder for Abstract Salad Factory"""
        food_msg = {
            'to': 'food',
            'subject': 'Abstract Salad Factory',
            'content': "Abstract Salad Factory is happening tomorrow from 1-2pm. Bring an ingredient (or a few!) to Hopper and make some salad happen."
        }
        self.send_message('stream', food_msg)

    def mention_member(self, member):
        if self.test_mode:
            return "@**test-%s**" % member['full_name']
        else:
            return "@**%s**" % member['full_name']

    def send_message(self, msg_type, msg):
        """Sends a message to Zulip stream or user."""
        if self.test_mode:
            self.print_message(msg)
        else:
            self.client.send_message({
                "type": msg_type,
                "to": msg['to'],
                "subject": msg['subject'],
                "content": msg['content']
            })

    def print_message(self, message):
        print(json.dumps(message, indent=4))


if __name__ == "__main__":
    ZULIP_USERNAME = os.environ['ZULIP_LUNCHBOT_EMAIL']
    ZULIP_API_KEY = os.environ['ZULIP_LUNCHBOT_KEY']
    ZULIP_SITE = os.getenv('ZULIP_LUNCHBOT_SITE', 'https://recurse.zulipchat.com')
    ZULIP_STREAM = os.getenv('ZULIP_LUNCHBOT_STREAM', 'lunchbot-staging')
    IN_PRODUCTION = os.getenv('ZULIP_LUNCHBOT_IN_PRODUCTION', False) in [True, 'True', 'true']

    bot = Lunchbot(
        ZULIP_USERNAME,
        ZULIP_API_KEY,
        ZULIP_SITE,
        ZULIP_STREAM,
        test_mode=(not IN_PRODUCTION)
    )

    first_argument = sys.argv[1]

    if first_argument == 'pre_lunch':
        bot.do_pre_lunch()
    elif first_argument == 'lunch':
        bot.do_lunch()
    elif first_argument == 'asf':
        bot.do_asf()
    else:
        print("Nothing to do with those arguments.")
