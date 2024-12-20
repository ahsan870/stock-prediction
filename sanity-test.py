import os

import requests

hosts = ["httpbin.org", "portswigger.net"]  # Add your 18 hosts here
#hosts = ["http://httpbin.org", "host2", "host3"]  # Add your 18 hosts here
ports = [80, 443]  # Add the 3 ports
apps = ["get", "hello"]  # Add the 20 applications
#apps = ["app1", "app2", "app3", ... ]  # Add the 20 applications

failures = []
success = []

for host in hosts:
    for port in ports:
        for app in apps:
            url = f"http://{host}:{port}/{app}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    success.append(url)
                else:
                    failures.append(url)
            except requests.exceptions.RequestException as e:
                failures.append(url)

# Generate a simple report
print("Validation Summary")
print(f"Total Successful: {len(success)}")
print(f"Total Failed: {len(failures)}")
print("\nFailed URLs:")
for url in failures:
    print(url)

#Optionally, save the results to a file
with open("validation_report.txt", "w") as report:
    report.write(f"Total Successful: {len(success)}\n")
    report.write(f"Total Failed: {len(failures)}\n")
    report.write("\nFailed URLs:\n")
    for url in failures:
        report.write(f"{url}\n")

# Ensure directory is writable and save the report
# report_file_path = "validation_report.txt"
#
#
# try:
#     with open(report_file_path, "w") as report:
#         report.write(f"Total Successful: {len(success)}\n")
#         report.write(f"Total Failed: {len(failures)}\n")
#         report.write("\nFailed URLs:\n")
#         for url in failures:
#             report.write(f"{url}\n")
#     print(f"\nReport successfully saved to {os.path.abspath(report_file_path)}")
# except IOError as e:
#     print(f"Error saving report: {e}")
