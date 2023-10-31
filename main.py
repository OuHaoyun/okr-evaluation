import os
from typing import Dict
import pandas as pd
from constants import DATA_FOLDER_PATH, SALESPERSON_INFO_EXCEL_PATH
from utils import read_roadshow_files, okr_calculation_pipeline, write_dfs_to_excel, prepare_txt_pipeline


def main(data_folder: str) -> None:
    """
    Main function to process OKR Excel files in the specified data folder.
    
    For each Excel file in the data folder:
    - Reads the OKR data and salesperson information.
    - Calculates the OKR.
    - Writes the results to Excel.
    - Writes the OKRs to separate txt files.
    
    Args:
        data_folder (str): Path to the folder containing the OKR Excel files.
    
    Returns:
        None
    """
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(data_folder, file_name)
            print(f"Processing file: {file_path}")

            # Read the OKR Excel file
            df_okr, df_salespeople_info = read_roadshow_files(file_path, SALESPERSON_INFO_EXCEL_PATH)

            # Calculate the OKR
            df_roadshow, df_researcher, df_team, df_org, df_special = okr_calculation_pipeline(df_okr, df_salespeople_info)

            dfs_dict: Dict[str, pd.DataFrame] = {
                        'roadshow': df_roadshow,
                        'special': df_special,
                        'researcher': df_researcher,
                        'team': df_team,
                        'organization': df_org
                        }
    
            # Write the DataFrames to Excel
            write_dfs_to_excel(dfs_dict, file_path)

            # Write okrs in separate txt files
            prepare_txt_pipeline(df_researcher, df_team, df_org, file_path)
            

if __name__ == '__main__':
    main(DATA_FOLDER_PATH)
