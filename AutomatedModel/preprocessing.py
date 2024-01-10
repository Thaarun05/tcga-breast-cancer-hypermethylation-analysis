"""
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_resampled, y_resampled = smote.fit_resample(df_x_train, df_y_train)
"""
import os
from urllib.parse import quote_plus

import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

conn = mysql.connector.connect(user='root', password='thaarun@2005', host='localhost', database='tnbc')
cursor = conn.cursor()


# collect raw data 86 patients (14 M1 & 72 M0)
# conn = mysql.connector.connect(user='root', password='thaarun@2005', host='localhost', database='tnbc')
# cursor = conn.cursor()

def get_additional_features():
    v_sql = "SELECT CONCAT(cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid) as patient_name, " \
            "cfi.file_name, cpb.ajcc_metastasis_pathologic_pm, cpb.ajcc_pathologic_tumor_stage, " \
            "cpb.anatomic_neoplasm_subdivision, cpb.metastasis_site, COUNT(DISTINCT CONCAT(" \
            "cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid)) as distinct_count FROM tnbc.case_file_id " \
            "cfi INNER JOIN tnbc.clinical_patient_brca cpb ON cfi.bcr_patient_uuid = cpb.bcr_patient_uuid WHERE " \
            "cpb.ajcc_metastasis_pathologic_pm IN ('M0', 'M1', 'MX') AND cpb.ajcc_metastasis_pathologic_pm != '[Not " \
            "Available]' AND cpb.ajcc_pathologic_tumor_stage != '[Not Available]' AND " \
            "cpb.anatomic_neoplasm_subdivision != '[Not Available]' AND cpb.metastasis_site != '[Not Available]' " \
            "GROUP BY cpb.ajcc_metastasis_pathologic_pm,cfi.bcr_patient_uuid,cfi.file_name," \
            "cpb.ajcc_pathologic_tumor_stage,cpb.anatomic_neoplasm_subdivision,cpb.metastasis_site; "
    df_additional_features = pd.read_sql(v_sql, con=conn)
    # df_additional_features.to_csv('/Users/thaarun/PythonProjects/AIResearch/output/dataset_features_non_null.txt')
    # print(df_additional_features)

    return df_additional_features


def get_uuid_metastasis(filename):
    v_sql = f"SELECT concat(p.ajcc_metastasis_pathologic_pm ,'_', p.bcr_patient_uuid ) FROM tnbc.case_file_id f inner " \
            f"join tnbc.clinical_patient_brca p on f.bcr_patient_uuid = p.bcr_patient_uuid where f.file_" \
            f"name = '{filename}' "
    cursor.execute(v_sql)
    uuid_metastasis = cursor.fetchone()
    # print(uuid_metastasis)
    return uuid_metastasis


# ML dataset
def create_dataset():
    df_list = []

    df_features = get_additional_features()
    # print(df_features)
    patient_filename = list(df_features['file_name'])

    # print(patient_filename)
    # print (df_features)

    # for item in patient_filename:
    #     # filename = df_features[df_features['file_name'] == item]['patient_name'].iloc[0]
    #     filename = df_features[df_features['file_name'] == item]
    #     print('-----------------------')
    #     print(filename)
    #     print(type(filename))
    #     print('-----------------------')
    #     filename = df_features[df_features['file_name'] == item]['patient_name']
    #     print(filename)
    #     print(type(filename))
    #     print('-----------------------')
    #     filename = df_features[df_features['file_name'] == item]['patient_name'].iloc[0]
    #     print(filename)
    #     print(type(filename))
    #     break

    for item in patient_filename:
        # print(item)
        meth_datafile = '/Users/thaarun/PythonProjects/TCGAProject/output/allfiles/' + item
        # print(meth_datafile)
        df_temp = pd.read_csv(meth_datafile, sep='\t', header=None)
        # print(df_temp.head())

        df_temp.rename(columns={df_temp.columns[0]: "sites"}, inplace=True)
        df_temp.rename(columns={df_temp.columns[1]: "beta_value"}, inplace=True)
        # print(df_temp.head())
        df_temp = df_temp.set_index('sites')
        # print(df_temp.head())
        df_temp = df_temp.T
        # print(df_temp.head())
        df_temp['patient_name'] = df_features[df_features['file_name'] == item]['patient_name'].iloc[0]
        df_list.append(df_temp)
        # print(df_list)

    df_dataset = pd.concat(df_list, axis=0, ignore_index=True)
    first_column = df_dataset.pop('patient_name')

    # insert column using insert(position,column_name,first_column) function
    df_dataset.insert(0, 'patient_name', first_column)
    df_dataset.insert(0, 'patient_file_name', df_features['file_name'])
    df_dataset.insert(2, 'tumor_stage', df_features['ajcc_pathologic_tumor_stage'])
    df_dataset.insert(3, 'metastatic_status', df_features['ajcc_metastasis_pathologic_pm'])
    df_dataset.insert(4, 'anatomic_neoplasm_subdivision', df_features['anatomic_neoplasm_subdivision'])
    df_dataset.insert(5, 'metastasis_site', df_features['metastasis_site'])
    df_dataset = df_dataset.dropna(how="all", axis=1)

    # print(df_dataset.head())

    # df_dataset.to_csv('/Users/thaarun/PythonProjects/AIResearch/output/results/MLDatasetFeatures.txt', index=False,
    # sep='\t', mode='a')

    df_dataset.to_csv('/Users/thaarun/PythonProjects/AIResearch/output/results/MLDatasetFeatures.csv', index=False,
                      sep='\t', mode='a')


# preprocessing for null values


# use SMOTE to synthesize more M1 patients


if __name__ == "__main__":
    # get_methylated_sites_transposed()
    # get_additional_features()
    # get_uuid_metastasis('63b72249-ec2d-42c6-9f70-19318e48488c.methylation_array.sesame.level3betas.txt')
    create_dataset()
