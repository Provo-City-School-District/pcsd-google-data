#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Zero-touch enrollment quickstart sample.

This script forms the quickstart introduction to the zero-touch enrollemnt
customer API. To learn more, visit https://developer.google.com/zero-touch
"""

import sys
import json
from apiclient import discovery
from dotenv import load_dotenv
from os import getenv
from google.oauth2 import service_account



def get_credential():
    SERVICE_ACCOUNT_KEY_FILE = 'service_account_key.json'
    SCOPES = getenv("SCOPE").split(",")

    credential = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_KEY_FILE,
        scopes=SCOPES,
        subject="googleapi@provo.edu"
    )

    if not credential:
        print('Unable to authenticate using service account key.')
        sys.exit()
    return credential


def get_service():
    creds = get_credential()
    return discovery.build('admin', 'directory_v1', credentials=creds)

def main():
    load_dotenv()
    service = get_service()
    next_page_token = None
    all_devices = []
    while True:
        response = service.chromeosdevices().list(customerId=getenv("CUSTOMER_ID"), 
            maxResults=300, 
            pageToken=next_page_token).execute()
        devices = response.get("chromeosdevices", [])
        print(f"fetched another {len(devices)} devices")
        all_devices.extend(devices)
        next_page_token = response.get("nextPageToken")
        if next_page_token == None:
            break

    print(len(all_devices))
    with open("all_devices.json", 'w') as f:
        json.dump(all_devices, f, indent=4)
    


if __name__ == '__main__':
  main()