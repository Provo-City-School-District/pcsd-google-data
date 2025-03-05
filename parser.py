import json
import xlsxwriter

with open("all_devices.json") as f:
    out = xlsxwriter.Workbook("out.xlsx")
    sh = out.add_worksheet()
    row_idx = 1

    sh.write(0, 0, "Serial")
    sh.write(0, 1, "Report Time")
    sh.write(0, 2, "Free RAM (bytes)")
    sh.write(0, 3, "Total RAM (bytes)")

    file_content = f.read()
    data = json.loads(file_content)
    for device in data:
        sn = device["serialNumber"]
        ram_total = device["systemRamTotal"]
        # skip 0 
        if not "systemRamFreeReports" in device:
            continue


        for report in device["systemRamFreeReports"]:
            report_time = report["reportTime"]
            free_info = report["systemRamFreeInfo"][0]

            sh.write(row_idx, 0, sn) # sn, report_time, free_info, ram_total)
            sh.write(row_idx, 1, report_time)
            sh.write(row_idx, 2, free_info)
            sh.write(row_idx, 3, ram_total)
            row_idx += 1
        #for storage 

    out.close()