import os
import pandas as pd
from constants import SHEET_NAMES


from constants import data_folder_path, researcher_info_excel_path, salesperson_info_excel_path, output_excel_path
from utils import read_roadshow_files, okr_calculation_pipeline, write_dfs_to_excel


from constants import SHEET_NAMES




def main(data_folder):
    """
    Traverse the given data folder and process each OKR Excel file.
    
    Args:
    - data_folder (str): Path to the data folder containing OKR Excel files.
    """
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(data_folder, file_name)

            # Read the OKR Excel file
            df_okr, df_salespeople_info = read_roadshow_files(file_path, researcher_info_excel_path, salesperson_info_excel_path)

            # calculate the OKR
            df_roadshow, df_researcher, df_special = okr_calculation_pipeline(df_okr, df_salespeople_info)

            # Write the DataFrames to Excel
            dfs_dict = {name[3:]: globals()[name] for name in SHEET_NAMES if name in globals()}
            write_dfs_to_excel(dfs_dict, file_path)
            
    

if __name__ == '__main__':
    main(data_folder_path)
