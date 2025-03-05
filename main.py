#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Zero-touch enrollment quickstart sample.

This script forms the quickstart introduction to the zero-touch enrollemnt
customer API. To learn more, visit https://developer.google.com/zero-touch
"""

import sys
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
    devices = service.chromeosdevices().list(customerId=getenv("CUSTOMER_ID")).execute()
    device_lst = devices.get("chromeosdevices", [])
    print(len(device_lst))
    


if __name__ == '__main__':
  main()