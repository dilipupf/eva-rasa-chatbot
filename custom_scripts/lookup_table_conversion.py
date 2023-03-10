#takes xlsx file listado.xlsx and converts to yml file with just the names column and stores in data folder as person_names.yml

import pandas as pd
import yaml
import os
import sys
import re

# Add the current directory to the path so that the script can find the data folder
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Path to the lookup table file
yml_filecreation_path = '../data/person_names.yml'
excel_file_path = '../data/listado.xlsx'
person_names = 'person_names' # name of the lookup table


print('running lookuptable conversion')


def lookup_table_conversion():

        df = pd.read_excel(excel_file_path)
        
        #include the first column from the excel file
        df = df[df.columns[0]]

        # convert the names column from last name, first name to first name last name format using the regular expression
        # if isinstance(x, str) is a check to make sure that the value is a string
        df = df.apply(lambda x: re.sub(r'([^,]+),\s*(.+)', r'\2 \1', x) if isinstance(x, str) else x)

        # Drop any rows that have a NaN value in the first column
        df = df.dropna()

        # Convert the DataFrame to a list and return only values and remove empty spaces in the end of the string
        data = df.values.tolist()
        data_list = [x.strip() for x in data] # remove empty spaces in the end of the string

        # print first 5 rows of the list
        # print(data_list[:5])


        #Write the YAML string to a file in the lookup_tables folder the way the rasa docs say to do it
        with open(yml_filecreation_path, 'w') as outfile:

                def write_to_yml_file(name):
                        outfile.write("\n      - " + name)

                outfile.write("\nversion: \"2.0\"\nnlu:\n  - lookup: "+person_names+"\n    examples: |")
                
                for full_name in data_list:
                        write_to_yml_file(full_name)
                        [write_to_yml_file(each_word_of_name) for each_word_of_name in full_name.split(' ')]
               

                print('finished lookuptable conversion')


if __name__ == '__main__':
        try:
                lookup_table_conversion()
        except Exception as e:
                print(e)