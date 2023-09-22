import os
import pandas as pd
from constants import SHEET_NAMES


from constants import data_folder_path, researcher_info_excel_path, salesperson_info_excel_path, output_excel_path
from utils import okr_roadshow_data_pipeline, write_dfs_to_excel


from constants import SHEET_NAMES




def main(data_folder):
    """
    Traverse the given data folder and process each OKR Excel file.
    
    Args:
    - data_folder (str): Path to the data folder containing OKR Excel files.
    """
    for file_name in os.listdir(data_folder):
        # print(file_name)
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(data_folder, file_name)
            okr_roadshow_data_pipeline(file_path, researcher_info_excel_path, salesperson_info_excel_path, output_excel_path)
            ### todo:
            ### to be modified: the output paths should also be changed
            ### how about move the writing part to main.py?
            # Write data to output Excel
            dfs_dict = {name[3:]: globals()[name] for name in SHEET_NAMES if name in globals()}
            write_dfs_to_excel(output_excel_path, dfs_dict)

    

if __name__ == '__main__':
    main(data_folder_path)
