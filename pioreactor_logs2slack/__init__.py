# -*- coding: utf-8 -*-
import json
import logging
import click
from requests import post
from pioreactor.background_jobs.base import BackgroundJob
from pioreactor.config import config
from pioreactor.whoami import get_unit_name, get_latest_experiment_name


class Logs2Slack(BackgroundJob):
    job_name="logs2slack"

    def __init__(self, unit, experiment):
        super(Logs2Slack, self).__init__(
            unit=unit, experiment=experiment
        )
        self.slack_webhook_url = config.get("logs2slack", "slack_webhook_url")
        if not self.slack_webhook_url:
            self.logger.error("[logs2slack] slack_webhook_url is not defined in your config.ini.")
            raise ValueError("[logs2slack] slack_webhook_url is not defined in your config.ini.")

        self.log_level = config.get("logs2slack", "log_level", fallback="INFO")
        self.start_passive_listeners()

    def publish_to_slack(self, msg):
        payload = json.loads(msg.payload)

        # check to see if we should allow the logs based on the level.
        if getattr(logging, self.log_level) > getattr(logging, payload['level']):
            return
        elif payload['task'] == self.job_name:
            # avoid an infinite loop, https://github.com/Pioreactor/pioreactor-logs2slack/issues/2
            return

        slack_msg = f"[{payload['level']}] [{self.unit}] [{payload['task']}] {payload['message']}"
        encoded_json = json.dumps({"text": slack_msg}).encode("utf-8")

        r = post(
            self.slack_webhook_url, data=encoded_json,
            headers={'Content-Type': 'application/json'}
        )

        r.raise_for_status()

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
