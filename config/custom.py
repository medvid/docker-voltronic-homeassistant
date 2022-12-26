#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime
import json
import requests

poller_json = json.load(sys.stdin)
Inverter_mode = int(poller_json["Inverter_mode"])
AC_grid_voltage = float(poller_json["AC_grid_voltage"])
Battery_voltage = float(poller_json["Battery_voltage"])
Battery_capacity = float(poller_json["Battery_capacity"])
Load_watt= float(poller_json["Load_watt"])

POWER = 0 if Inverter_mode == 4 else 1

GROUP = 3
NOW = datetime.now()
HOUR = NOW.hour
WEEKDAY= NOW.isoweekday()
K = 108
if HOUR == 0:
  WEEKDAY = WEEKDAY - 1
PLAN = ((int((K - HOUR)/4) - WEEKDAY - GROUP) % 3) / 2

headers = {'api-key': '[IOTPLOTTER_API_KEY]'}
payload = {}
payload["data"] = {}
payload["data"]["POWER"] = []
payload["data"]["POWER"].append({"value":POWER})
payload["data"]["PLAN"] = []
payload["data"]["PLAN"].append({"value":PLAN})
payload["data"]["AC_V"] = []
payload["data"]["AC_V"].append({"value":AC_grid_voltage})
payload["data"]["BAT_V"] = []
payload["data"]["BAT_V"].append({"value":Battery_voltage})
payload["data"]["BAT_C"] = []
payload["data"]["BAT_C"].append({"value":Battery_capacity})
payload["data"]["LOAD_W"] = []
payload["data"]["LOAD_W"].append({"value":Load_watt})

requests.post("https://iotplotter.com/api/v2/feed/[IOTPLOTTER_FEED]", headers=headers, data=json.dumps(payload))

API_KEY="[THINGSPEAK_API_KEY]"
requests.post(f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={POWER}&field2={PLAN}&field3={AC_grid_voltage}&field4={Battery_voltage}&field5={Battery_capacity}&field6={Load_watt}")
