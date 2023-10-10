import os
import datetime
now = datetime.datetime.now()

data_folder_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/2023Q1&Q2研究院工作量统计/'
output_folder_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/exp-data/'
okr_excel_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/2023Q1&Q2研究院工作量统计/2023.5.1-5.31研究院工作量统计0607.xlsx'
# /Users/haoyunou/Desktop/ms-security/研究院绩效考核/2023Q1&Q2研究院工作量统计/2023.4.1-4.30研究院工作量统计0509-团队补充0608.xlsx
# /Users/haoyunou/Desktop/ms-security/研究院绩效考核/2023Q1&Q2研究院工作量统计/2023.5.1-5.31研究院工作量统计0607.xlsx
# /Users/haoyunou/Desktop/ms-security/研究院绩效考核/2023Q1&Q2研究院工作量统计/2023.6.1-6.30研究院工作量统计0705-团队补充0706.xlsx

txt_folder = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/exp-data/roadshow_txts/'


txt_folder_path = txt_folder + now.strftime("%Y-%m-%d_%H-%M-%S") + '/'

# Create the path if it doesn't exist
if not os.path.exists(txt_folder_path):
    os.makedirs(txt_folder_path)

researcher_info_excel_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/分析师列表（修正版）.xlsx'
salesperson_info_excel_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/销售列表.xlsx'

exp_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/exp-data/data-exp1.xlsx'

output_excel_path = '/Users/haoyunou/Desktop/ms-security/研究院绩效考核/exp-data/okr_roadshow_202305.xlsx'

