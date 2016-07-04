## ABOUT

_thold-slack.py_  is a script to send Cacti THOLD alert messages to [Slack](https://slack.com)

## FEATURES
* Sends Cacti THOLD message to a Slack channel of your choice
* Allows hyperlink to URL of your choice (plugins/thold/thold_graph.php)
* Hyperlink to graph of threshold breached
* Optionally includes graph directly in Slack
* RED (Alert), YELLOW (Warning), BLUE (Restored) alerts

## INSTALLATION

This Python script is designed to ingest a Cacti THOLD email message as piped input from sendmail
and post the contents to a Slack channel as a rich format 'attachment' message as defined in the [Slack API](https://api.slack.com/docs/attachments)

*It is highly recommended to run this through sendmail restricted shell (smrsh)*

```shell
cd /tmp
git clone https://github.com/jamesboswell/thold-slack
cd thold-slack
# Edit thold-slack and set GLOBAL VARIABLES
cp thold-slack /etc/smrsh
chmod +x /etc/smrsh/thold-slack.py
```

Setup sendmail by doing the following, or manually editing /etc/aliases
You may, use any alias you choose,  example below uses 'thold-slack'

```shell
sudo echo "thold-slack: | /etc/smrsh/thold-slack.py" >> /etc/aliases
sudo newaliases
```

Optionally you can setup additional aliases that send THOLD messsages to different Slack channels by passing a channel name

For example to send to a #netadmin channel
```shell
sudo echo "thold-slack-netadmin: \"| /etc/smrsh/thold-slack.py netadmin\"" >> /etc/aliases
sudo newaliases
```

You will then need to setup your Cacti thresholds or threshold templates to send to the correct email alias as defined in previous steps.
