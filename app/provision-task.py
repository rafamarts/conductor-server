import os
import requests
import fmt
import sys
import json
import subprocess

wfjson = sys.argv[1]
print("Processing task file " + wfjson + "...")
subprocess.call("rm -f /tmp/error", shell=True)

with open(wfjson) as json_file:
    data = json.load(json_file)
    for d in data:
        name = d['name']
        print("Processing task " + name + "...")

        #verify if this task already exists
        r = requests.get('http://localhost:8080/api/metadata/taskdefs/' + name)
        if r.status_code == 200:
            update = os.environ["PROVISIONING_UPDATE_EXISTING_TASKS"]
            if update=="true":
                print('[INFO] Task already provisioned. Updating it with provisioning contents. name=' + name)
                contents = json.dumps(d)
                # print('Server task contents')
                # print(r.content)
                # print('Provisioning task contents')
                # print(contents)
                r = requests.put(url='http://localhost:8080/api/metadata/taskdefs', data=contents, headers={'Content-Type':'application/json'})
                if r.status_code == 200:
                    print('[INFO] Task updated successfully. name=' + name)

                else:
                    print('')
                    print('[ERROR] Error updating existing task. name=' + name + '; status=' + str(r.status_code) + '; body=' + r.content)
                    print('')
                    subprocess.call("touch /tmp/error", shell=True)
            else:
                print('[INFO] Task already provisioned. Skipping. name=' + name)

        elif r.status_code == 404:
            print('[INFO] Provisioning task. name=' + name)
            contents = "[" + json.dumps(d) + "]"
            print(contents)
            r = requests.post(url='http://localhost:8080/api/metadata/taskdefs', data=contents, headers={'Content-Type':'application/json'})
            if r.status_code == 200:
                print('[INFO] Task provisioned successfully. name=' + name)

            else:
                print('')
                print('[ERROR] Error provisioning task. name=' + name + '; status=' + str(r.status_code) + '; body=' + r.content)
                print('')
                subprocess.call("touch /tmp/error", shell=True)

        else:
            print('[ERROR] Error getting task. status=' + str(r.status_code) + '; name=' + name)
            subprocess.call("touch /tmp/error", shell=True)
