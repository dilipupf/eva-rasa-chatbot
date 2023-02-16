import pandas as pd
import re


def get_dataframe_with_reformatted_names(file_path, no_of_cols):
    try:

        #read in the excel file from data folder
        df = pd.read_excel(file_path, usecols= no_of_cols)

        #include the first column from the excel file
        df_names = df[df.columns[0]]

        # conver the names column from last name, first name to first name last name format using the regular expression
        # if isinstance(x, str) is a check to make sure that the value is a string
        df_names = df_names.apply(lambda x: re.sub(r'([^,]+),\s*(.+)', r'\2 \1', x) if isinstance(x, str) else x)


        # Convert the DataFrame to a list and return only values and remove empty spaces in the end of the string
        df_names = df_names.values.tolist()


        # df_names = [ (x.strip()) for x in df_names if isinstance(x, str) else x ] # remove empty spaces in the end of the string

        # remove empty spaces in the end of the string and exclude non-string values like NaN
        df_names = ([(x.strip() if isinstance(x, str) else x ) for x in df_names]) 

        # remove empty spaces in dataframe column names
        df.rename(columns=lambda x: (x.strip() if isinstance(x, str) else x), inplace=True)

        # add the reformatted names column to the dataframe
        df[df.columns[0]] = df_names
        
        # drop rows with empty values
        df.dropna(inplace=True)


    except Exception as e:
        print('Error in get_dataframe_with_reformatted_names: ', e)

    #print(df_names[:5])
    # print first 5 rows of the list
    #print('reformatted dataframe', df[:5])


    return df

# if __name__ == '__main__':
#     try:
#         df = get_dataframe_with_reformatted_names('../data/listado.xlsx', [0,1,2])
#         print(df)
#     except Exception as e:
#         print(e)

        


