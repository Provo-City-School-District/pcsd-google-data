#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Zero-touch enrollment quickstart sample.

This script forms the quickstart introduction to the zero-touch enrollemnt
customer API. To learn more, visit https://developer.google.com/zero-touch
"""
import mysql.connector
import sys
import json
from datetime import datetime
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

def get_all_devices(service):
    next_page_token = None
    all_devices = []
    while True:
        response = service.chromeosdevices().list(customerId=getenv("CUSTOMER_ID"), 
            maxResults=300, 
            pageToken=next_page_token).execute()
        devices = response.get("chromeosdevices", [])
        print(f"fetched {len(devices)} devices (total={len(all_devices)})")
        all_devices.extend(devices)
        next_page_token = response.get("nextPageToken")
        if next_page_token == None:
            break

    return all_devices

def convert_google_timestamp(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")

def main():
    load_dotenv()

    # uncomment this to load newest data
    
    service = get_service()
    devices = get_all_devices(service)

    # write devices to file
    with open("all_devices.json", 'w') as f:
        json.dump(devices, f, indent=4)
    
    #insert data to vault DB
    vault_conn = mysql.connector.connect(
        host=getenv("VAULT_HOST_IP"),
        port=getenv("VAULT_HOST_PORT"),
        user=getenv("VAULT_USER"),
        password=getenv("VAULT_PASSWORD"),
        database=getenv("VAULT_DATABASE")
    )


    with open("all_devices.json") as f:
        device_data = json.loads(f.read())

    curs = vault_conn.cursor()

    for device in device_data:
        serial = device["serialNumber"]
        ram_total = device.get("systemRamTotal") if not None else 0
        os_version = device.get("osVersion") if not None else 0
        disk_space_usage = device.get("diskSpaceUsage")
        recent_users = device.get("recentUsers")
        status = device.get("status")
        ou_path = device.get("orgUnitPath")
        if recent_users is not None and len(recent_users) > 0:
            last_user = recent_users[0]
            last_user_email = last_user.get("email") if not None else ""
        else:
            last_user_email = ""

        if disk_space_usage is not None:
            storage_total = int(disk_space_usage["capacityBytes"])
            storage_free = storage_total - int(disk_space_usage["usedBytes"])
        else:
            storage_total = 0
            storage_free = 0

        last_check_in = convert_google_timestamp(device["lastSync"])

        query = """
            INSERT INTO google_admin_data 
                (serial, ram_total, os_version, storage_total, storage_free, last_check_in, last_user, ou_path, status)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                ram_total=%s, os_version=%s, storage_total=%s, 
                storage_free=%s, last_check_in=%s, last_user=%s,
                ou_path=%s, status=%s;
        """

        vals = (serial, ram_total, os_version, storage_total, storage_free, last_check_in, last_user_email, ou_path, status,
                ram_total, os_version, storage_total, storage_free, last_check_in, last_user_email, ou_path, status)
        #print(vals)
        res = curs.execute(query, vals)


    query = "INSERT INTO google_admin_ram_reports (serial, report_date, ram_free) VALUES "
    for device in device_data:
        serial = device["serialNumber"]
        ram_usage_reports = device.get("systemRamFreeReports")
        if ram_usage_reports is not None:
            for report in ram_usage_reports:
                report_date = convert_google_timestamp(report["reportTime"])
                ram_free = int(report["systemRamFreeInfo"][0])
                query += f"(\"{serial}\", \"{report_date}\", {ram_free}), "
    # remove trailing comma
    query = query[:-2]
    query += "ON DUPLICATE KEY UPDATE serial=serial, report_date=report_date, ram_free=ram_free;"

    print("inserting all ram reports")
    curs.execute(query)
    print("done")

    vault_conn.commit()
    
   # curs.execute("INSERT INTO google_admin_data assets")
   # myresult = curs.fetchall()


if __name__ == '__main__':
  main()
