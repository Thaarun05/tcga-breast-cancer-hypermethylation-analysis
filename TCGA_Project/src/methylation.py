import csv
import glob
import os
import pandas as pd
import numpy as np
from matplotlib import ticker
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import mysql.connector
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functools import reduce

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# creating connection to sql localhost code.
cnx = create_engine('mysql+mysqlconnector://root:%s@localhost/tnbc' % quote_plus("thaarun@2005"), echo=False)

conn = mysql.connector.connect(user='root', password='thaarun@2005', host='localhost', database='tnbc')
cursor = conn.cursor()


def get_methylated_sites_transposed():
    df_list = []

    cursor.execute("DROP TABLE IF EXISTS tnbc.sites_beta_value_trans")
    print("Deleted table tnbc.sites_beta_value_trans")

    os.remove("/Users/thaarun/PythonProjects/TCGAProject/output/result/result.txt")

    file_path = '/Users/thaarun/PythonProjects/TCGAProject/output/allfiles/'
    file_list = glob.glob(os.path.join(file_path, "*.txt"))
    # print(file_list)
    if len(file_list) > 0:
        for file_item in file_list:
            print(f'Processing file  {file_item}')
            df_temp = pd.read_csv(file_item, sep='\t', header=None)
            df_temp.rename(columns={df_temp.columns[0]: "sites"}, inplace=True)
            df_temp.rename(columns={df_temp.columns[1]: "beta_value"}, inplace=True)
            print(f'Transposing DF ....  {file_item}')
            df_temp = df_temp.set_index('sites').T
            file_name = os.path.basename(file_item)
            df_temp['FileName'] = file_name
            # print(df_temp.head())
            # print(df_temp.shape[0])
            df_list.append(df_temp)
            print(f'Writing to table ....  {file_item}')
            # df_temp.to_sql(con=cnx, name='sites_beta_value_trans', if_exists='append', index=False)

            # df_temp.to_csv('/Users/thaarun/PythonProjects/TCGAProject/output/result/result.txt', header=None, index=False, sep='\t', mode='a')

        df_methylated_sites = pd.concat(df_list, axis=0, ignore_index=True)
        # df_methylated_sites.to_sql(con=cnx, name='sites_beta_value_trans', if_exists='replace', index=False)
        # print(df_methylated_sites.shape[0])
        df_methylated_sites.to_csv('/Users/thaarun/PythonProjects/TCGAProject/output/result/result.txt', index=False,
                                   sep='\t', mode='a')

    return None


def get_methylated_sites():
    df_list = []

    # cursor.execute("DROP TABLE IF EXISTS tnbc.sites_beta_value")
    # print("Deleted table tnbc.sites_beta_value")

    cursor.execute("truncate table tnbc.sites_beta_value")
    print("truncated table tnbc.sites_beta_value")

    file_path = '/Users/thaarun/PythonProjects/TCGAProject/output/allfiles/'
    file_list = glob.glob(os.path.join(file_path, "*.txt"))
    print(file_list)
    if len(file_list) > 0:
        for file_item in file_list:
            print(f'Processing file  {file_item}')
            df_temp = pd.read_csv(file_item, sep='\t', header=None)
            df_temp.rename(columns={df_temp.columns[0]: "sites"}, inplace=True)
            df_temp.rename(columns={df_temp.columns[1]: "beta_value"}, inplace=True)
            file_name = os.path.basename(file_item)
            df_temp['FileName'] = file_name
            # print(df_temp.head())
            # print(df_temp.shape[0])
            # df_list.append(df_temp)
            print(f'Writing to table ....  {file_item}')
            df_temp.to_sql(con=cnx, name='sites_beta_value', if_exists='append', index=False)
        # df_methylated_sites = pd.concat(df_list, axis=0, ignore_index=True)

        # print(df_methylated_sites.shape[0])
    return None  # df_methylated_sites


def get_methylated_sites_nonull():
    # Retrieving sites with NULL values as well so all sites can be joined.

    df_list = []

    cursor.execute("truncate table tnbc.sites_beta_values")
    print("truncated table tnbc.sites_beta_values")

    file_path = '/Users/thaarun/PythonProjects/TCGAProject/output/allfiles/'
    file_list = glob.glob(os.path.join(file_path, "*.txt"))
    print(file_list)
    if len(file_list) > 0:
        for file_item in file_list:
            print(f'Processing file  {file_item}')
            df_temp = pd.read_csv(file_item, sep='\t', header=None)
            df_temp.rename(columns={df_temp.columns[0]: "sites"}, inplace=True)
            df_temp.rename(columns={df_temp.columns[1]: "beta_value"}, inplace=True)
            file_name = os.path.basename(file_item)
            df_temp['FileName'] = file_name
            # print(df_temp.head())
            # print(df_temp.shape[0])
            # df_list.append(df_temp)
            df_temp.dropna(inplace=True)
            print(f'Writing to table ....  {file_item}')
            df_temp.to_sql(con=cnx, name='sites_beta_values', if_exists='append', index=False)
        # df_methylated_sites = pd.concat(df_list, axis=0, ignore_index=True)

        # print(df_methylated_sites.shape[0])
    return None  # df_methylated_sites


def plotsample():
    # File content
    # "Sites", "M1P1", "M1P2", "M0P3", "M0P4"
    # "cg07549526", "0.953379", "0.983379", "0.011577", "0.041831"
    # "cg16670573", "0.983097", "0.953097", "0.031092", "0.011577"
    # "cg09969830", "0.989223", "0.969223", "0.014294", "0.030159"
    # "cg00179196", "0.965455", "0.985455", "0.108456", "0.041831"
    # "cg03948744", "0.899163", "0.839163", "0.108456", "0.06697"
    df_temp = pd.read_csv('/Users/thaarun/PythonProjects/TCGAProject/output/plot/sample.csv', quoting=csv.QUOTE_ALL)
    print(df_temp)

    df_temp.set_index('Sites', inplace=True)

    print(df_temp)

    # create figure and axis
    fig, ax = plt.subplots()

    # setting the axis' labels
    ax.set_ylabel('Beta Value', fontsize=12)
    ax.set_xlabel('Sites', fontsize=12)

    # transposing (switchung rows and columns) of DataFrame df and
    # plot a line for each column on the axis ax, which was created previously
    df_temp.plot(ax=ax, linestyle='--', marker='o')
    plt.show()

    return None


def plot():
    v_sql = f"SELECT distinct FileName  FROM plot_scenario_1 where FileName in ('e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt','c9a71a6a-451c-43d6-a183-bf42adb6ba44.methylation_array.sesame.level3betas.txt')"
    v_sql = f"SELECT distinct FileName  FROM plot_scenario_1"
    df_FileName = pd.read_sql(v_sql, con=conn)
    l_FileName = df_FileName['FileName'].tolist()
    print(l_FileName)

    df_list = []

    if len(l_FileName) > 0:
        for file_item in l_FileName:
            v_sql = f"select sites, beta_value, metastasis from tnbc.plot_scenario_1 where FileName ='{file_item}'"
            df_FileData = pd.read_sql(v_sql, con=conn)
            # print(df_FileData)
            new_column_name = df_FileData.metastasis.unique()[0]
            df_FileData.rename(columns={'beta_value': new_column_name}, inplace=True)
            df_FileData.drop('metastasis', axis=1, inplace=True)
            # print(df_FileData)
            df_list.append(df_FileData)

        df_methylated_sites = reduce(lambda df1, df2: pd.merge(df1, df2, on='sites', how='outer'), df_list)
        # print(df_methylated_sites)

        df_methylated_sites.set_index('sites', inplace=True)

        print(df_methylated_sites)

        # create figure and axis
        fig, ax = plt.subplots()

        # setting the axis' labels
        ax.set_ylabel('Beta Value', fontsize=12)
        ax.set_xlabel('Sites', fontsize=12)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        # transposing (switching rows and columns) of DataFrame df and
        # plot a line for each column on the axis ax, which was created previously
        df_methylated_sites.plot(ax=ax, linestyle='--', marker='o')

        ax.legend(bbox_to_anchor=(1.1, 2.05))

        # df1 = pd.DataFrame({'Sites', })
        # df2.plot.line(ax=ax, x='Sites', y=["Beta Value"])

        plt.show()

    return None


def plot_full():
    # v_sql = f"SELECT distinct FileName  FROM plot_scenario_1_full where FileName in ('e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt','c9a71a6a-451c-43d6-a183-bf42adb6ba44.methylation_array.sesame.level3betas.txt')"
    v_sql = f"SELECT distinct FileName  FROM plot_scenario_1_full where sites in ('cg00820405','cg06282596','cg06721601','cg12245706','cg14196395','cg17291767','cg18766900','cg20253855','cg21113446','cg22300566')"
    # v_sql = f"SELECT distinct FileName  FROM plot_scenario_1_full"
    df_FileName = pd.read_sql(v_sql, con=conn)
    l_FileName = df_FileName['FileName'].tolist()
    print(l_FileName)

    df_list_M1 = []
    df_list_M0 = []

    if len(l_FileName) > 0:
        for file_item in l_FileName:
            v_sql = f"select sites, beta_value, metastasis from tnbc.plot_scenario_1_full where FileName ='{file_item}' and sites in ('cg21526205','cg06761719','cg12210255','cg12231969')"
            # v_sql = f"select sites, beta_value, metastasis from tnbc.plot_scenario_1_full where FileName ='{file_item}'"
            df_FileData = pd.read_sql(v_sql, con=conn)
            # print(df_FileData)
            if df_FileData.empty:
                continue
            else:
                new_column_name = df_FileData.metastasis.unique()[0]
                df_FileData.rename(columns={'beta_value': new_column_name}, inplace=True)
                df_FileData.drop('metastasis', axis=1, inplace=True)
                # print(df_FileData)
                if (new_column_name.startswith('M1')):
                    df_list_M1.append(df_FileData)
                else:
                    df_list_M0.append(df_FileData)

        # print(df_methylated_sites)

        # create figure and axis
        fig, ax = plt.subplots()

        # setting the axis' labels
        ax.set_ylabel('Beta Value', fontsize=12)
        ax.set_xlabel('Sites', fontsize=12)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.legend(loc="upper right")

        # plot M1

        df_methylated_sites_M1 = reduce(lambda df1, df2: pd.merge(df1, df2, on='sites', how='outer'), df_list_M1)
        # df_methylated_sites_M1 = df_methylated_sites_M1.iloc[:10]
        print(df_methylated_sites_M1)

        df_methylated_sites_M1.set_index('sites', inplace=True)
        # transposing (switching rows and columns) of DataFrame df and
        # plot a line for each column on the axis ax, which was created previously
        df_methylated_sites_M1.plot(ax=ax, linestyle='-', marker='o')

        # plot M0
        df_methylated_sites_M0 = reduce(lambda df1, df2: pd.merge(df1, df2, on='sites', how='outer'), df_list_M0)
        # df_methylated_sites_M0 = df_methylated_sites_M0.iloc[:10]
        # ,how='outer'
        # print(df_methylated_sites)

        df_methylated_sites_M0.set_index('sites', inplace=True)
        # transposing (switching rows and columns) of DataFrame df and
        # plot a line for each column on the axis ax, which was created previously
        df_methylated_sites_M0.plot(ax=ax, linestyle='--', marker='o')

        plt.show()

    return None


def identify_top_sites():
    # v_sql = f"SELECT distinct FileName  FROM plot_scenario_1_full where FileName in ('4549c3d2-cc38-4fea-9091-36125a418a0c.methylation_array.sesame.level3betas.txt')"
    # ('e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt','c9a71a6a-451c-43d6-a183-bf42adb6ba44.methylation_array.sesame.level3betas.txt','c8e84511-71ce-4938-a374-99980bf6d7ba.methylation_array.sesame.level3betas.txt')"
    v_sql = f"SELECT distinct FileName  FROM plot_scenario_1_full"
    df_FileName = pd.read_sql(v_sql, con=conn)
    l_FileName = df_FileName['FileName'].tolist()
    print(l_FileName)

    df_list_M1 = []
    df_list_M0 = []

    if len(l_FileName) > 0:
        for file_item in l_FileName:
            # v_sql = f"select sites, beta_value, metastasis from tnbc.plot_scenario_1_full where FileName ='4549c3d2-cc38-4fea-9091-36125a418a0c.methylation_array.sesame.level3betas.txt'
            # and sites in ('cg21526205','cg06761719','cg12210255','cg12231969')"
            v_sql = f"select sites, beta_value, metastasis from tnbc.plot_scenario_1_full where FileName ='{file_item}'"
            print(v_sql)
            df_FileData = pd.read_sql(v_sql, con=conn)
            # print(df_FileData)
            new_column_name = df_FileData.metastasis.unique()[0]
            df_FileData.rename(columns={'beta_value': new_column_name}, inplace=True)
            df_FileData.drop('metastasis', axis=1, inplace=True)
            # print(df_FileData)
            if (new_column_name.startswith('M1')):
                df_list_M1.append(df_FileData)
            else:
                df_list_M0.append(df_FileData)

        # print(df_list_M1)
        df_methylated_sites_M1 = reduce(lambda df1, df2: pd.merge(df1, df2, on='sites', how='outer'), df_list_M1)
        # df_methylated_sites_M1 = df_methylated_sites_M1.iloc[:10]
        # df_methylated_sites_M1.set_index('sites', inplace=True)
        # df_methylated_sites_M1['array_']
        # print(df_methylated_sites_M1)
        # for index, row in df_methylated_sites_M1.iterrows():
        #     print (type(row ))

        df_methylated_sites_M1.to_excel('/Users/thaarun/PythonProjects/TCGAProject/output/top_sites/top_sites_m1.xlsx')

        # print(df_list_M0)
        df_methylated_sites_M0 = reduce(lambda df1, df2: pd.merge(df1, df2, on='sites', how='outer'), df_list_M0)
        # df_methylated_sites_M0 = df_methylated_sites_M0.iloc[:10]
        # df_methylated_sites_M0.set_index('sites', inplace=True)
        # print(df_methylated_sites_M0)

        df_methylated_sites_M0.to_excel('/Users/thaarun/PythonProjects/TCGAProject/output/top_sites/top_sites_m0.xlsx')

        df_methylated_sites_M1_M0 = pd.merge(df_methylated_sites_M1, df_methylated_sites_M0, on='sites', how='outer')
        print(df_methylated_sites_M1_M0.shape)
        # print(df_methylated_sites_M1_M0)
        df_methylated_sites_M1_M0.to_excel('/Users/thaarun/PythonProjects/TCGAProject/output/top_sites/top_sites.xlsx')

    return None

def plot_heatmap():
    df_heatmap=pd.read_excel('/Users/thaarun/PythonProjects/TCGAProject/output/top_sites/top_sites.xlsx')
    # print (df_heatmap.head(2))
    df_heatmap=df_heatmap.round(2)
    df_heatmap.fillna('Null', inplace=True)
    # print(df_heatmap.head(2))
    # df_heatmap.set_index('sites', inplace=True)
    # df_heatmap.drop('sites', axis=1, inplace=True)
    df_heatmap.to_excel('/Users/thaarun/PythonProjects/TCGAProject/output/top_sites/top_sites_heatmap.xlsx')
    # sns.color_palette("husl", 8)
    # sns.heatmap(df_heatmap,vmin=-0, vmax=1, yticklabels=True, xticklabels=False)
    # plt.show()
    return None

def identify_MX():
    v_sql = f"SELECT distinct FileName  FROM all_MX_top50_Sites"
    df_FileName = pd.read_sql(v_sql, con=conn)
    l_FileName = df_FileName['FileName'].tolist()
    print(l_FileName)

    df_list = []

    if len(l_FileName) > 0:
        for file_item in l_FileName:
            v_sql = f"select sites, beta_value, metastasis from tnbc.all_MX_top50_Sites where FileName ='{file_item}'"
            df_FileData = pd.read_sql(v_sql, con=conn)
            # print(df_FileData)
            new_column_name = df_FileData.metastasis.unique()[0]
            df_FileData.rename(columns={'beta_value': new_column_name}, inplace=True)
            df_FileData.drop('metastasis', axis=1, inplace=True)
            # print(df_FileData)
            df_list.append(df_FileData)
        # print(df_list)
        df_methylated_sites = reduce(lambda df1, df2: pd.merge(df1, df2, on='sites', how='outer'), df_list)
        df_methylated_sites.to_excel('/Users/thaarun/PythonProjects/TCGAProject/output/top_sites/top_sites_mx.xlsx')

    return None


if __name__ == "__main__":
    # #Write all 894 files into a single result.txt file with sites as columns(457K columns)
    # get_methylated_sites_transposed()

    # reading the 6GB result.txt file is taking long
    # df_data = pd.read_csv('/Users/thaarun/PythonProjects/TCGAProject/output/result/result.txt', sep='\t')
    # print(df_data.head(2))

    # get_methylated_sites()

    # worked - start
    # #Able to successfully write all sites that had non null value into table sites_beta_values
    # get_methylated_sites_nonull()

    # plotsample()

    # plot()

    # plot_full()

    # identify_top_sites()

    plot_heatmap()

    # identify_MX()

    # worked - end

    # methylated_sites_data = get_methylated_sites()
    # print(methylated_sites_data.shape[0])

    # methylated_sites_data = methylated_sites_data.dropna()
    #
    # vectorized_methylated_sites = np.vectorize(methylated_sites)
    # methylated_sites_data['Sites_Methylated'] = vectorized_methylated_sites(methylated_sites_data['beta_value'])
    # print(methylated_sites_data.head())
    # print(methylated_sites_data.shape[0])
