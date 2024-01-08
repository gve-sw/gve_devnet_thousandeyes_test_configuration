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

from thousand_eyes import ThousandEyes
import pandas as pd

te = ThousandEyes()

df_csv_tests_underlay = te.csv_to_dataframe(te.underlay_csv_file, 'underlay')

df_csv_tests_overlay = te.csv_to_dataframe(te.overlay_csv_file, 'overlay')

df_csv_tests = pd.concat([df_csv_tests_underlay, df_csv_tests_overlay]) 

df_api_tests = te.api_to_dataframe(te.get_tests())

df_test_new_underlay, df_test_existing_csv_underlay = te.check_for_new_tests(df_csv_tests_underlay, df_api_tests)

df_test_new_overlay, df_test_existing_csv_overlay = te.check_for_new_tests(df_csv_tests_overlay, df_api_tests)

df_test_existing_csv = pd.concat([df_test_existing_csv_underlay, df_test_existing_csv_overlay])

list_tests_delete, df_test_existing_api = te.check_for_deleted_tests(df_csv_tests, df_api_tests)

list_payloads, list_tests_changed = te.check_for_changed_tests(df_test_existing_csv, df_test_existing_api)


create_tests_underlay = te.create_tests(df_test_new_underlay)

create_tests_overlay = te.create_tests(df_test_new_overlay)

delete_test_underlay = te.delete_tests(list_tests_delete)

update_tests = te.update_tests(list_tests_changed, list_payloads)


custom_labels_dictionary = te.create_custom_labels_dictionary()

create_labels = te.create_labels(custom_labels_dictionary)

delete_labels = te.delete_labels(custom_labels_dictionary)