#!/usr/bin/env python3
#
# sms2po is a simple Python HTTP server listening on port 8088 to act as a custom SMSC provider
# in QNAP Notification Center. It will pull the the message text from SMS notifications and send
# via Pushover instead.
#
# Environment variables in compose.yaml:
#   PUSHOVER_TOKEN : required
#    PUSHOVER_USER : required
#   PUSHOVER_TITLE : optional, default "QNAP NAS"
#   PUSHOVER_SOUND : optional, default "none" (silent) - https://pushover.net/api#sounds
#    PUSHOVER_PRIO : optional, default "0" (normal) - https://pushover.net/api#priority
#
# You must add a CUSTOM SMS service provider in Notification Center
#
# + Add SMSC Service
# Select "custom" as the "SMS service provider"
# "Alias" can be whatever you like
# For "URL template text" specify:
#   http://<host>:8088?phone=@@PhoneNumber@@&text=@@Text@@
# "SMS server login name" and "SMS server login password" can be left blank
#
# <host>:8088 is where this container is running - perhaps on the QNAP itself in Container Station
#
# The recipient phone number you configure in Notifcation Center can be anything - it is ignored when using Pushover
#

import os
import logging
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

def pushover(poToken, poUser, poTitle, poSound, poPrio, message):
  params={
    "token": poToken,
    "user": poUser,
    "title": poTitle,
    "sound": poSound,
    "priority": poPrio,
    "message": message
  }
  r = requests.post("https://api.pushover.net/1/messages.json", params).json()
  if r['status'] != 1:
    logging.info("Pushover API error: %s" % r['errors'])
  return r['status']

class MyHandler(BaseHTTPRequestHandler):
  def log_message(self, fmt, *args):
    logging.info("{0} {1}".format(self.address_string(), fmt % args))
  def do_GET(self):
    params = parse_qs(urlparse(self.path).query)
    message = params['text'][0]
    if pushover(PUSHOVER_TOKEN, PUSHOVER_USER, PUSHOVER_TITLE, PUSHOVER_SOUND, PUSHOVER_PRIO, message) == 1:
      self.send_response(200) # Pushover msg sent - return "success" to QNAP Notification Center
    else:
      self.send_response(500) # Return "failure" to QNAP NC (for requeue presumably...)
    self.end_headers()

logging.basicConfig(format="%(asctime)s | %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TITLE = os.getenv("PUSHOVER_TITLE", "QNAP NAS")
PUSHOVER_SOUND = os.getenv("PUSHOVER_SOUND", "none")
PUSHOVER_PRIO = os.getenv("PUSHOVER_PRIO", "0")

if PUSHOVER_TOKEN is None or PUSHOVER_USER is None:
  logging.info("PUSHOVER_TOKEN and PUSHOVER_USER variables are required - aborting")
  quit()

logging.info(f"PUSHOVER_TOKEN = {PUSHOVER_TOKEN}")
logging.info(f"PUSHOVER_USER  = {PUSHOVER_USER}")
logging.info(f"PUSHOVER_TITLE = {PUSHOVER_TITLE}")
logging.info(f"PUSHOVER_SOUND = {PUSHOVER_SOUND}")
logging.info(f"PUSHOVER_PRIO  = {PUSHOVER_PRIO}")

httpd = HTTPServer(("", 8088), MyHandler)
logging.info("Listening on port 8080")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
logging.info("Exiting")
