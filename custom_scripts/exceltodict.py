import pandas as pd
import random
import numpy as np
import re
import exceltodict as excel_to_dict
from reformat_excel import get_dataframe_with_reformatted_names

# Read the data from the excel file and convert to dictionary format
def read_excel(file_path,  no_of_cols = [0,1,2]):
    # data = pd.read_excel(file_path, usecols=[0,1,2])
    try:
        dataFrame = get_dataframe_with_reformatted_names(file_path, no_of_cols)
        #random sample of 5 rows from the dataframe
        # dataFrame = dataFrame.sample(n=5, random_state=1)
        return dataFrame
    except Exception as e:
        print('Error in read_excel: ', e)


def return_matching_names(personName, names):
    indexes = []
    personName = personName.upper()
    exact_match_index = np.where(names == personName)[0]
    if len(exact_match_index) > 0:
        indexes = exact_match_index
        return [indexes, names[indexes]]

    for pos, name in enumerate(names):
        start = 0
        while True:
            index = np.char.find(name, personName, start)
            if index == -1:
                break
            else:
                indexes.append(pos)
            start = index + 1
    # filtered neams from the list of indexes and convert to list from numpy array so that it can be passed
    # to serialize in slotset function later.
    filtered_names = names[indexes].tolist()
    return [indexes, filtered_names]


def return_matching_names_from_dept(deptName, dept_names):
    indexes = []

    exact_match_index = np.where(dept_names == deptName)[0]
    if len(exact_match_index) > 0:
        indexes = exact_match_index
        return [indexes, dept_names[indexes]]

    for pos, name in enumerate(dept_names):
        start = 0
        while True:
            index = np.char.find(name, deptName, start)
            if index == -1:
                break
            else:
                indexes.append(pos)
            start = index + 1
    # filtered neams from the list of indexes and convert to list from numpy array so that it can be passed
    # to serialize in slotset function later.
    filtered_names = dept_names[indexes].tolist()
    return [indexes, filtered_names]

# if __name__ == '__main__':  
#     try:
#         df = excel_to_dict.read_excel('../data/listado.xlsx')
#         # print(df.head())
#         personName = 'JORGE LOBO'
#         names = df[df.columns[0]].values.astype(str)
#         return_matched_names = return_matching_names(personName, names)
#         print(return_matched_names)

#         if bool(len(return_matched_names) > 0): #check if the person name is present in the excel sheet on first column
#             print('Person Name is present in the excel sheet')
#             # row = df.loc[df[df.columns[0]] == personName]
#             # department = row.iloc[0,1]
#             # office_num = row.iloc[0,2]
#             #print('Department: ', department)
#         else:
#             print('Person Name is not present in the excel sheet')
            
#     except Exception as e:
#         print(e)



# df = read_excel(file_path = file_path)
                # df_dict = df.to_dict()
                # print(df_dict.keys())
                # #get first ten key value pairs
                # print(dict(list(df_dict.items())[0:10]))

                # # print(personName in df[df.columns[0]].values  == True)

                # if(personName in df[df.columns[0]].values == True): #check if the person name is present in the excel sheet on first column
                #     row = df.loc[df[df.columns[0]] == personName]
                #     department = row.iloc[0,1]
                #     office_num = row.iloc[0,2]