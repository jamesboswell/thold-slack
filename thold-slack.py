#!/usr/bin/python
# - Copyright 2015 - Jim Boswell

import sys
import email
from email import parser, FeedParser
from email.Iterators import typed_subpart_iterator
import urllib2,json
# read in piped input from sendmail
# /etc/aliases
# thold-slack: | /etc/smrsh/thold-slack.py
data = sys.stdin.readlines()

def get_charset(message, default="ascii"):
    """Get the message charset"""

    if message.get_content_charset():
        return message.get_content_charset()

    if message.get_charset():
        return message.get_charset()

    return default

def get_body(message):
    """Get the body of the email message"""

    if message.is_multipart():
        #get the plain text version only
        text_parts = [part
                      for part in typed_subpart_iterator(message,
                                                         'text',
                                                         'plain')]
        body = []
        for part in text_parts:
            charset = get_charset(part, get_charset(message))
            body.append(unicode(part.get_payload(decode=True),
                                charset,
                                "replace"))

        return u"\n".join(body).strip()

    else: # if it is not multipart, the payload will be a string
          # representing the message body
        body = unicode(message.get_payload(decode=True),
                       get_charset(message),
                       "replace")
        return body.strip()

# create email parser
feed = email.parser.FeedParser()

# read in our stdin into FeedParser feed
for line in data:
    feed.feed(line)

# call feed close to create mail object
mail = feed.close()


message = get_body(mail)
# print message

# determine Slack attachment color
# allows for nice color coding of msgs
if mail['subject'].startswith('ALERT'):
    color = 'danger'
elif mail['subject'].startswith('WARNING'):
    color = 'warning'
else:
 color = '#439FE0' # a nice blue



# Slack Webhook URL (https://inetworks.slack.com/services/new/incoming-webhook)
# ex:  
url = 'webhook URL goes here'
channel = '#alerts'


# build payload (https://api.slack.com/docs/attachments)
payload = {
    'channel': channel,
    'username': 'Cacti THOLD',
    'icon_emoji': ':cactus:',
    'attachments': [
        {
            "fallback": mail['subject'],
            "pretext": "",
            "title": mail['subject'],
            "title_link": "***REMOVED***cacti/plugins/thold/thold_graph.php?sort_column=lastread&sort_direction=DESC",
            "text": message,
            "color": color
        }
    ]
}


req = urllib2.Request(url)
req.add_header('Content-Type','application/json')

# JSONify our POST data
postdata = json.dumps(payload)

# POST data to Slack API
try:
    urllib2.urlopen(req,postdata)
except HTTPError as e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
    print e.read()
except URLError as e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
else:
    print "POST to Slack.com successful"
    # everything is fine