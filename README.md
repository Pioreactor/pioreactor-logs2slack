### Pioreactor Logs2Slack

This is a Pioreactor plugin to post a bioreactor's logs to a Slack room.

### Installation

This is a two part installation.

#### 1. Setting up your Slack workspace

1. You probably want a dedicated channel for incoming logs, as it can get chatty. So go ahead
and create a dedicated channel in your Slack workspace. I've called mine `experiment_logs`.

2. In [Your Apps](https://api.slack.com/apps/), click "Create New App" -> From "Scratch". Give it a name (something descriptive, like `Pioreactor Logs2Slack`), and select the workspace.

3. On the next page, select "Incoming Webhooks", and turn "Activate" to `On`

4. Click "Add new webhook to workspace"

5. In the next section, select the channel you made in step 1. Click "Allow".

6. On the next page, under "Webhook URL", is your new webhook URL, something like `https://hooks.slack.com/services/ABC.../124...`. **Important**: this is private, don't share it with untrusted people, don't commit it into Github, etc.


#### 2. Installing this plugin

1. In your Pioreactor interface, click on "Plugins". Find `pioreactor-logs2slack`, and click "Install" beside it. This will install the plugin for each Pioreactor in your cluster.

2. After installing (should take less than a minute), click on "Configuration". At the bottom of the page will be a section called `[logs2slack]`.

```
[logs2slack]
slack_webhook_url=
log_level=INFO
```

Add your webhook URL from step 6. here. Click "Save". You can also change the level of logs to report, see [Python logging levels](https://docs.python.org/3/library/logging.html#logging-levels).

3. In the "Pioreactors" page, you should see "Logs2Slack" as an activity now. You can start this activity like you would any other activity. Go ahead and start it.

4. In your dedicated Slack channel, you should start to see logs arrive!







