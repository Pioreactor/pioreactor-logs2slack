# -*- coding: utf-8 -*-
import json
import logging
import click
from requests import post
from pioreactor.background_jobs.base import BackgroundJob
from pioreactor.config import config
from pioreactor.whoami import get_unit_name, get_latest_experiment_name


class Logs2Slack(BackgroundJob):

    def __init__(self, unit, experiment):
        super(Logs2Slack, self).__init__(
            unit=unit, experiment=experiment, job_name="logs2slack"
        )
        self.slack_webhook_url = config.get("logs2slack", "slack_webhook_url")
        self.log_level = config.get("logs2slack", "log_level", fallback="INFO")

        if not self.slack_webhook_url:
            raise ValueError("[logs2slack] slack_webhook_url is not defined in your config.ini.")

        self.start_passive_listeners()

    def publish_to_slack(self, msg):
        payload = json.loads(msg.payload)

        # check to see if we should allow the logs based on the level.
        if getattr(logging, self.log_level) > getattr(logging, payload['level']):
            return

        slack_msg = f"[{payload['level']}] [{payload['task']}] {payload['message']}"
        encoded_json = json.dumps({"text": slack_msg}).encode("utf-8")

        post(
            self.slack_webhook_url, data=encoded_json,
            headers={'Content-Type': 'application/json'}
        )

    def start_passive_listeners(self):
        self.subscribe_and_callback(self.publish_to_slack, f"pioreactor/{self.unit}/+/logs/+")


@click.command(name="logs2slack")
def click_logs2slack():
    """
    turn on logging to Slack
    """

    lg = Logs2Slack(
        unit=get_unit_name(), experiment=get_latest_experiment_name()
    )
    lg.block_until_disconnected()
