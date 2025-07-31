import glob
import os
from urllib.parse import quote_plus

import requests
import json
import re

import pandas as pd

from sqlalchemy import create_engine, delete

import mysql.connector

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

cnx = create_engine('mysql+mysqlconnector://root:%s@localhost/tnbc' % quote_plus("thaarun@2005"),echo=False)

conn=mysql.connector.connect(user='root',password='thaarun@2005', host='localhost', database='tnbc')
cursor=conn.cursor()


# reads clinical patient data from a CSV file, filters the data based on TNBC status, and returns the TNBC patient list.
def get_patients():
    # load the data from the file
    data = pd.read_csv('/Users/thaarun/Documents/nationwidechildrens.org_clinical_patient_brca.txt', sep='\t')
    # print(data.head(10))

    v_index=data[data['bcr_patient_uuid'] == 'bcr_patient_uuid'].index
    data.drop(v_index, inplace = True)

    v_index = data[data['bcr_patient_uuid'] == 'CDE_ID:'].index
    data.drop(v_index, inplace=True)

    # print(data.head(10))
    # # Note: use 'append' or 'replace' depending on the desired action
    data.to_sql(con=cnx, name='clinical_patient_brca', if_exists='replace', index=False)

    # filter the data for patients with TNBC
    # TNBC = (data['er_status_by_ihc'] == 'Negative') & (data['pr_status_by_ihc'] == 'Negative') & (data['her2_status_by_ihc'] == 'Negative') & (data['ajcc_metastasis_pathologic_pm'] == 'M1')
    TNBC_patients = data['bcr_patient_uuid'].tolist()

    # display the filtered data in a datatable
    # print(TNBC_patients)
    return(TNBC_patients)

# takes the TNBC patient list and retrieves the file UUID list
# from the GDC API by sending a GET request with appropriate filters.
# populates case_file_id table with the response values
def populate_file_uuid_patient(patient_id):
    print(patient_id)
    files_endpt = "https://api.gdc.cancer.gov/files"
    # patient_id_chunks = [patient_id[x:x + 100] for x in range(0, len(patient_id), 100)]
    file_uuid_list = []

    # dele = tnbc.case_file_id.delete()
    # cnx.execute(case_file_id.delete())
    cursor.execute("DROP TABLE IF EXISTS tnbc.case_file_id")
    print ("Deleted table tnbc.case_file_id")

    for x in range(0, len(patient_id)):


        filters = {
            "op": "and",
            "content": [
                {
                    "op": "in",
                    "content": {
                        "field": "cases.case_id",
                        "value": patient_id[x]
                    }
                },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "cases.project.primary_site",
                #         "value": [
                #             "breast"
                #         ]
                #     }
                # },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "cases.project.project_id",
                #         "value": [
                #             "TCGA-BRCA"
                #         ]
                #     }
                # },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "files.data_category",
                #         "value": [
                #             "dna methylation"
                #         ]
                #     }
                # },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "files.file_name",
                #         "value": [
                #             "e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt"
                #         ]
                #     }
                # },
                {
                    "op": "in",
                    "content": {
                        "field": "files.data_format",
                        "value": [
                            "TXT"
                        ]
                    }
                },
                {
                    "op": "in",
                    "content": {
                        "field": "files.platform",
                        "value": [
                            "Illumina Human Methylation 450"
                        ]
                    }
                }
            ]
        }

        # Here a GET is used, so the filter parameters should be passed as a JSON string.

        params = {
            "filters": json.dumps(filters),
            "fields": "file_id,file_name",
            "format": "JSON",
            "size": "3000"
        }

        response = requests.get(files_endpt, params=params)
        print(response.content.decode("utf-8"))
        print(json.loads(response.content.decode("utf-8"))["data"])
        print(json.loads(response.content.decode("utf-8"))["data"]["hits"])

        response_values=json.loads(response.content.decode("utf-8"))["data"]["hits"]
        df_case_file_id = pd.DataFrame(response_values)
        df_case_file_id["bcr_patient_uuid"] = patient_id[x]
        print(df_case_file_id)

        df_case_file_id.to_sql(con=cnx, name='case_file_id', if_exists='append', index=False)



        # This step populates the download list with the file_ids from the previous query
        for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
            file_uuid_list.append(file_entry["file_id"])


    return(file_uuid_list)

# retrieves the file UUID list and returns it.
def retrieve_file_uuid_patient(patient_id):
    print(patient_id)
    files_endpt = "https://api.gdc.cancer.gov/files"
    patient_id_chunks = [patient_id[x:x + 100] for x in range(0, len(patient_id), 100)]
    file_uuid_list = []

    # # dele = tnbc.case_file_id.delete()
    # # cnx.execute(case_file_id.delete())
    # cursor.execute("DROP TABLE IF EXISTS tnbc.case_file_id")
    # print ("Deleted table tnbc.case_file_id")

    for x in range(0, len(patient_id_chunks)):


        filters = {
            "op": "and",
            "content": [
                {
                    "op": "in",
                    "content": {
                        "field": "cases.case_id",
                        "value": patient_id_chunks[x]
                    }
                },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "cases.project.primary_site",
                #         "value": [
                #             "breast"
                #         ]
                #     }
                # },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "cases.project.project_id",
                #         "value": [
                #             "TCGA-BRCA"
                #         ]
                #     }
                # },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "files.data_category",
                #         "value": [
                #             "dna methylation"
                #         ]
                #     }
                # },
                # {
                #     "op": "in",
                #     "content": {
                #         "field": "files.file_name",
                #         "value": [
                #             "e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt"
                #         ]
                #     }
                # },
                {
                    "op": "in",
                    "content": {
                        "field": "files.data_format",
                        "value": [
                            "TXT"
                        ]
                    }
                },
                {
                    "op": "in",
                    "content": {
                        "field": "files.platform",
                        "value": [
                            "Illumina Human Methylation 450"
                        ]
                    }
                }
            ]
        }

        # Here a GET is used, so the filter parameters should be passed as a JSON string.

        params = {
            "filters": json.dumps(filters),
            "fields": "file_id",
            "format": "JSON",
            "size": "3000"
        }

        response = requests.get(files_endpt, params=params)
        # print(response.content.decode("utf-8"))
        # print(json.loads(response.content.decode("utf-8"))["data"])
        # print(json.loads(response.content.decode("utf-8"))["data"]["hits"])

        response_values=json.loads(response.content.decode("utf-8"))["data"]["hits"]
        df_case_file_id = pd.DataFrame(response_values)
        print(df_case_file_id)

        # df_case_file_id.to_sql(con=cnx, name='case_file_id', if_exists='append', index=False)



        # This step populates the download list with the file_ids from the previous query
        for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
            file_uuid_list.append(file_entry["file_id"])


    return(file_uuid_list)


# downloads methylation files by opening a file with the file_name variable as the path,
# and then writing the content of the response to this file. methylation files are retrieved
# using POST request to data_endpt URL using the list of file UUIDs
def download_file_uuid(file_uuid_list):
    # print(file_uuid_list)
    # file_uuid_list = ['601dbd4c-76d6-4bc0-8e25-3141c4152a3d','cd2ceade-bbef-46fa-bca0-f4c847f4a037']
    # file_uuid_list = ['62916b2f-4487-4446-8ad8-e49a522094ea', '88df0116-ab6e-4fec-b69b-40ef65763b1b']

    # file_uuid_list_chunks = [file_uuid_list[x:x + 100] for x in range(0, len(file_uuid_list), 100)]
    # print(file_uuid_list_chunks)

    file_uuid_list_chunks= file_uuid_list

    # print(file_uuid_list)

    for x in range(0, len(file_uuid_list_chunks)):
        print(f"\n Processing {x} file")

        print(file_uuid_list_chunks[x])
        data_endpt = "https://api.gdc.cancer.gov/data"

        params = {"ids": file_uuid_list_chunks[x]}

        response = requests.post(data_endpt, data=json.dumps(params), headers={"Content-Type": "application/json"})
        print(response.headers)
        response_head_cd = response.headers["Content-Disposition"]
        print(response_head_cd)
        file_name = re.findall("filename=(.+)", response_head_cd)[0]
        file_name = '/Users/thaarun/PythonProjects/TCGAProject/output/allfiles/' + file_name
        print(file_name)

        with open(file_name,"wb") as output_file:
            output_file.write(response.content)

if __name__=="__main__":
    # List of patient IDs
    patient_ids = get_patients()
    # patient_ids = json.dumps(patient_id) #' '.join([str(elem) for elem in patient_id])
    print(patient_ids)

    # patient_ids=['6E7D5EC6-A469-467C-B748-237353C23416', '55262FCB-1B01-4480-B322-36570430C917']
    # patient_ids = ['6E7D5EC6-A469-467C-B748-237353C23416']

    # file_uuid_list=populate_file_uuid_patient(patient_ids)
    # print(file_uuid_list)

    file_uuid_list=retrieve_file_uuid_patient(patient_ids)
    print(file_uuid_list)

    # file_uuid_list = ['62916b2f-4487-4446-8ad8-e49a522094ea']
    # file_uuid_list = ['62916b2f-4487-4446-8ad8-e49a522094ea', '88df0116-ab6e-4fec-b69b-40ef65763b1b']

    if len(file_uuid_list) >0:
        download_file_uuid(file_uuid_list)

