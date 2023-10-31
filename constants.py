import os
import datetime

# Current timestamp for dynamic folder naming
now = datetime.datetime.now()

# Base paths for clarity and ease of modification
BASE_PATH = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/'
OUTPUT_BASE_PATH = os.path.join(BASE_PATH, 'exp-data')

# ----------------- # 
# Input Data Paths  #
# ----------------- #
DATA_FOLDER_PATH = os.path.join(BASE_PATH, '2023Q1&Q2研究院工作量统计/')
RESEARCHER_INFO_EXCEL_PATH = os.path.join(BASE_PATH, '分析师列表（修正版）.xlsx')
SALESPERSON_INFO_EXCEL_PATH = os.path.join(BASE_PATH, '销售列表.xlsx')

# ----------------- # 
# Output Data Path  #
# ----------------- #
OUTPUT_FOLDER_PATH = OUTPUT_BASE_PATH
TXT_FOLDER = os.path.join(OUTPUT_BASE_PATH, 'roadshow_txts')
TXT_FOLDER_PATH = os.path.join(TXT_FOLDER, now.strftime("%Y-%m-%d_%H-%M-%S"))

# Ensure the output path exists
if not os.path.exists(TXT_FOLDER_PATH):
    os.makedirs(TXT_FOLDER_PATH)

