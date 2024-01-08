""" Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at https://developer.cisco.com/docs/licenses.
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import os
from dotenv import load_dotenv
import requests
import json
import pandas as pd

load_dotenv()

class ThousandEyes:

    def __init__(self):
        self.token = os.getenv("TOKEN")
        self.agent = os.getenv("AGENT")
        self.underlay_csv_file = os.getenv("UNDERLAY_CSV_FILE")
        self.overlay_csv_file = os.getenv("OVERLAY_CSV_FILE")
        self.base_url = "https://api.thousandeyes.com/v6"
        self.header = {
            "Authorization": f"Bearer {self.token}", 
            "Content-Type": "application/json", 
            "Accept": "application/json"
        }
        self.df_test_existing_csv = None
        self.df_test_existing_api = None
    
    def csv_to_dataframe(self, csv_file, test_type):
        dataframe = pd.read_csv(csv_file, dtype={'siteId': str, 'port': str, 'testName': 'str'})
        new_column = []
        for index, row in dataframe.iterrows():
            new_column.append(f"{row['customerName']}_{row['siteId']}_{test_type}")
        dataframe['testName'] = new_column
        dataframe.sort_values(by=['testName'], inplace=True)
        return dataframe

    def get_tests(self):
        tests = requests.get(url=self.base_url+"/tests", headers=self.header).json()['test']
        return tests
    
    def get_agent_to_server_tests(self):
        agent_to_server_tests = requests.get(url=self.base_url+"/tests/agent-to-server", headers=self.header).json()['test']
        return agent_to_server_tests
    
    def get_test_id(self, test_name):
        tests = self.get_tests()
        for test in tests:
            if test['testName'] == test_name:
                test_id = test['testId']
        return test_id
    
    def create_dictionary_test_id(self, tests):
        test_dictionary = {}
        for test in tests:
            test_dictionary[test['testName']] = test['testId']
        return test_dictionary
    
    def api_to_dataframe(self, tests):
        dic_list = []
        for test in tests:
            if 'testName' in test:
                row_data = {
                        'siteId': test['testName'].split("_")[1],
                        'customerName': test['testName'].split("_")[0],
                        'server': test['server'].split(":")[0],
                        'protocol': test['protocol'],
                        'port': test['server'].split(":")[1],
                        'testName': test['testName']
                    }
                dic_list.append(row_data)

        dataframe = pd.DataFrame(dic_list)
        dataframe.sort_values(by=['testName'], inplace=True)
        return dataframe
    
    def check_for_new_tests(self, df_csv, df_api):
        df_test_existing_csv = pd.DataFrame(columns = ['siteId', 'customerName', 'server', 'protocol', 'port', 'testName'])
        df_test_new = pd.DataFrame(columns = ['siteId', 'customerName', 'server', 'protocol', 'port', 'testName'])
        for index, row in df_csv.iterrows():
            if row['testName'] in df_api.values:
                df_test_existing_csv = pd.concat([df_test_existing_csv, pd.DataFrame([row])], ignore_index=True)
            else:
                print("New test to be created with the name: ", row['testName'])
                df_test_new = pd.concat([df_test_new, pd.DataFrame([row])], ignore_index=True)
        return df_test_new, df_test_existing_csv
    
    def check_for_deleted_tests(self, df_csv, df_api):
        df_test_delete = pd.DataFrame(columns = ['siteId', 'customerName', 'server', 'protocol', 'port', 'testName'])
        df_test_existing_api = pd.DataFrame(columns = ['siteId', 'customerName', 'server', 'protocol', 'port', 'testName'])
        list_tests_delete = []
        for index, row in df_api.iterrows():
            if row['testName'] not in df_csv['testName'].values:
                print("Test to be deleted with the name: ", row['testName'])
                df_test_delete = pd.concat([df_test_delete, pd.DataFrame([row])], ignore_index=True)
                testId = self.get_test_id(row['testName'])
                list_tests_delete.append(testId)
            else:
                df_test_existing_api = pd.concat([df_test_existing_api, pd.DataFrame([row])], ignore_index=True)
        return list_tests_delete, df_test_existing_api
    
    def check_for_changed_tests(self, df_test_existing_csv, df_test_existing_api):
        dic_test_existing_csv = df_test_existing_csv.to_dict('records')
        dic_test_existing_api = df_test_existing_api.to_dict('records')
        list_tests_changed = []
        list_payloads = []
        for elem in dic_test_existing_csv:
            if elem in dic_test_existing_api:
                pass
            else:
                print("Test changed with the name: ", elem['testName'])
                payload = {
                    "agents": [
                        {"agentId": self.agent}
                    ],
                    "testName": elem['testName'],
                    "server": elem['server'],
                    "port": elem['port'],
                }
                list_payloads.append(payload)
                testId = self.get_test_id(elem['testName'])
                list_tests_changed.append(testId)
        return list_payloads, list_tests_changed

    def create_tests(self, dataframe):
        for index, row in dataframe.iterrows():
            payload = {
                "interval": 300,
                "agents": [
                    {"agentId": self.agent}
                ],
                "testName": row['testName'],
                "server": row['server'],
                "port": row['port'],
            }
            response = requests.post(url=self.base_url+"/tests/agent-to-server/new.json", headers=self.header, data=json.dumps(payload))
    
    def update_tests(self, testIds, payloads):
        for (testId, payload) in zip(testIds, payloads):
            response = requests.post(url=self.base_url+f"/tests/agent-to-server/{testId}/update.json", headers=self.header, data=json.dumps(payload))
    
    def delete_tests(self, testIds):
        for testId in testIds:
            response = requests.post(url=self.base_url+f"/tests/agent-to-server/{testId}/delete.json", headers=self.header)
    
    def get_labels(self):
        labels = requests.get(url=self.base_url+"/groups.json", headers=self.header).json()['groups']
        return labels
    
    def get_groupId(self, label_name): 
        labels = self.get_labels()
        for label in labels:
            if label['name'] == label_name:
                groupId = label['groupId']
        return groupId
    
    def get_label_details(self, groupId):
        label_details = requests.get(url=self.base_url+f"/groups/{groupId}.json", headers=self.header).json()['groups']
        return label_details
    
    def create_custom_labels_dictionary(self):
        labels = self.get_labels()
        custom_labels_dictionary = {}
        for label in labels:
            if label['builtin'] == 0 and label['type'] == 'tests':
                custom_labels_dictionary[label['name']] = label['groupId']
        return custom_labels_dictionary
    
    def create_labels(self, custom_labels_dictionary):
        tests = self.get_agent_to_server_tests()
        new_labels_dictionary = {}
        existing_labels_dictionary = {}
        for test in tests:
            test_id = test['testId']
            label_names = test['testName'].split("_")
            if 'groups' in test.keys():
                for label in test['groups']:
                    for name in label_names:
                        if name in label.values() and name not in existing_labels_dictionary and name in custom_labels_dictionary:
                            existing_labels_dictionary[label['name']] = [test_id]
                        elif name in label.values() and name in existing_labels_dictionary and name in custom_labels_dictionary and test_id not in existing_labels_dictionary[label['name']]:
                            existing_labels_dictionary[label['name']].append(test_id)
                        elif name not in label.values() and name not in new_labels_dictionary and name not in custom_labels_dictionary:
                            new_labels_dictionary[name] = [test_id]
                        elif name not in label.values() and name in new_labels_dictionary and name not in custom_labels_dictionary and test_id not in new_labels_dictionary[name]:
                            new_labels_dictionary[name].append(test_id)
                        elif name not in label.values() and name in existing_labels_dictionary and name in custom_labels_dictionary and test_id not in existing_labels_dictionary[name]:
                            existing_labels_dictionary[name].append(test_id)
            else:
                for name in label_names:
                    if name not in existing_labels_dictionary and name in custom_labels_dictionary:
                        existing_labels_dictionary[name] = [test_id]
                    elif name in existing_labels_dictionary and name in custom_labels_dictionary:
                        existing_labels_dictionary[name].append(test_id)
                    elif name not in new_labels_dictionary and name not in custom_labels_dictionary:
                        new_labels_dictionary[name] = [test_id]
                    elif name in new_labels_dictionary and name not in custom_labels_dictionary:
                        new_labels_dictionary[name].append(test_id)

        for label, test_ids in new_labels_dictionary.items():
            print("Creating new label for: ", label)
            payload = {
                "name": label,
                "tests": [{"testId": item} for item in test_ids]
            }
            new_siteId_label = requests.post(url=self.base_url+"/groups/tests/new", headers=self.header, data=json.dumps(payload))

        for label, test_ids in existing_labels_dictionary.items():
            print("Updating existing label for: ", label)
            groupId = custom_labels_dictionary[label]
            payload = {
                "name": label,
                "tests": [{"testId": item} for item in test_ids]
            }
            existing_siteId_label = requests.post(url=self.base_url+f"/groups/{groupId}/update", headers=self.header, data=json.dumps(payload))

    def delete_labels(self, custom_labels_dictionary):
        for group in custom_labels_dictionary:
            groupId = custom_labels_dictionary[group]
            details = self.get_label_details(groupId)
            if 'tests' not in details[0].keys():
                print("Deleting label: ", details[0]['name'])
                delete_label = requests.post(url=self.base_url+f"/groups/{groupId}/delete", headers=self.header)