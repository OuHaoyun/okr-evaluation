import os
import pandas as pd


from constants import data_folder_path, salesperson_info_excel_path
from utils import read_roadshow_files, okr_calculation_pipeline, write_dfs_to_excel





def main(data_folder):
    """
    Traverse the given data folder and process each OKR Excel file.
    
    Args:
    - data_folder (str): Path to the data folder containing OKR Excel files.
    
    """



    for file_name in os.listdir(data_folder):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(data_folder, file_name)
            print(file_path)

            # Read the OKR Excel file
            df_okr, df_salespeople_info = read_roadshow_files(file_path, salesperson_info_excel_path)

            # calculate the OKR
            df_roadshow, df_researcher, df_team, df_org, df_special = okr_calculation_pipeline(df_okr, df_salespeople_info)

            dfs_dict = {
                        'roadshow': df_roadshow,
                        'special': df_special,
                        'researcher': df_researcher,
                        'team': df_team,
                        'organization': df_org
                        }
    
            # Write the DataFrames to Excel
            write_dfs_to_excel(dfs_dict, file_path)
            
    

if __name__ == '__main__':
    main(data_folder_path)
