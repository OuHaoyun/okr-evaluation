import os
import pandas as pd
from constants import output_folder_path, txt_folder_path

# ------------------------------------------- #
# Step 1: Clean datasets and EDA              #
# ------------------------------------------- #

def read_roadshow_files(okr_excel_path, salesperson_info_excel_path):
    df_okr = pd.read_excel(okr_excel_path, sheet_name='路演', engine='openpyxl')
    df_salespeople_info = pd.read_excel(salesperson_info_excel_path)

    return df_okr, df_salespeople_info


def print_na_rate(df: pd.DataFrame) -> None:
    """
    Print the na rate of a DataFrame
    :param df: the DataFrame
    :return: None
    """
    print('The na rate of the DataFrame is:')
    print(df.isna().sum() / len(df))


def get_researcher_columns(df: pd.DataFrame) -> list:
    """
    Get the columns contains '研究员'
    :param df: the DataFrame
    :return: the columns contains '研究员'
    """
    researcher_columns = []
    for col in df.columns:
        if '研究员' in col:
            researcher_columns.append(col)
    return researcher_columns


def get_sales_name_list(df: pd.DataFrame) -> list:
    """
    Get the sales name list
    :param df: the DataFrame of the salesperson sheet
    :return: the sales name list
    """
    sales_name_list = df['员工姓名'].tolist()
    return sales_name_list


def treat_empty_xuhao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Treat the empty values in '序号'
    :param df: the DataFrame
    :return: the DataFrame with no empty values in '序号'
    """
    special_list = []
    df_special = pd.DataFrame()

    # Check if there are NaN values in '序号'
    if df['序号'].isna().sum() > 0:
        for i in range(1, len(df)):  # Start from the second row
            if pd.isna(df.loc[i, '序号']):
                # Append the current row and the preceding row to the special_list
                special_list.extend([i-1, i])

        # Remove duplicates from the special_list
        special_list = list(set(special_list))
        special_list.sort()

        # Forward fill the '序号' column
        df.loc[:, '序号'] = df['序号'].fillna(method='ffill')

    # Create a DataFrame with the special cases
    if len(special_list) > 0:
        df_special = df.iloc[special_list, :].copy()
        df_special.reset_index(drop=True, inplace=True)

    return df, df_special


def treat_special_researcher(df: pd.DataFrame, sales_name_list) -> pd.DataFrame:
    """
    Treat the special values in '研究员'
    :param df: the DataFrame
    :return: the DataFrame with no special values in '研究员'
    """
    # special case 1
    df_temp = df[df['研究员'].str.contains('无研究员') == False].copy()
    # # special case 2
    # df_temp.loc[df_temp['研究员'].str.contains('胡又文'), '研究员'] = '所长'
    # # write ‘所长’ in the column of '所属团队'
    df_temp.loc[df_temp['研究员'] == '胡又文', '所属团队'] = '所长'
    
    # special case 3
    df_temp = df_temp[df_temp['研究员'].isin(sales_name_list) == False].copy()
    return df_temp

# ------------------------------------------- #
# Step 2: Transform the unstructure Excel manuscript to a structured dataframe
# Save the special cases into additional dataframe for future validation            #
# ------------------------------------------- #

def get_df_roadshow(df: pd.DataFrame, sales_name_list = None) -> pd.DataFrame:
    """
    Get the roadshow DataFrame
    :param df: the DataFrame of the roadshow sheet
    :return: the roadshow DataFrame
    """
    # Define roadshow columns
    service_columns = ['序号', '服务事项', '客户机构', '客户分级', '客户区域', '所属团队']
    researcher_columns = get_researcher_columns(df)
    roadshow_columns = service_columns + researcher_columns

    # Read relavant columns and fillna
    df_temp = df[roadshow_columns].copy()
    df_temp, df_special = treat_empty_xuhao(df_temp)
    df_temp.loc[:, '序号'] = df_temp['序号'].astype(int)
    df_temp.loc[:, '客户区域'] = df_temp['客户区域'].fillna(df_temp['客户机构'])
    df_temp.loc[:, '客户分级'] = df_temp['客户分级'].fillna(df_temp['客户机构'])

    # Melt the df based on researcher columns
    df_temp_melted = pd.melt(df_temp, id_vars=service_columns, value_vars=researcher_columns, value_name='研究员姓名')
    df_temp_melted.drop('variable', axis=1, inplace=True) 
    df_temp_melted.dropna(subset=['研究员姓名'], inplace=True)
    df_temp_melted.rename(columns={'研究员姓名': '研究员'}, inplace=True)

    # Treat special values in '研究员'
    df_temp_melted = treat_special_researcher(df_temp_melted, sales_name_list)

    # Sort the DataFrame based on '序号'
    df_temp_sorted = df_temp_melted.sort_values(by='序号')
    df_temp_sorted.reset_index(drop=True, inplace=True)

    # Make a copy of the temp df as the roadshow df
    df_roadshow = df_temp_sorted.copy()

    return df_roadshow, df_special

# ------------------------------------------- #
# Step 3: Calculate the okr for researchers, teams, and the orgnization            #
# ------------------------------------------- #

def get_df_researcher(df_roadshow):
    # 1. Modify the df_researcher DataFrame structure
    df_researcher = df_roadshow.drop_duplicates(subset='研究员')[['研究员', '所属团队']].reset_index(drop=True)

    # 2. Calculate the total number of roadshows for each researcher
    total_roadshows = df_roadshow.groupby('研究员').size().reset_index(name='总路演次数')
    df_researcher = df_researcher.merge(total_roadshows, on='研究员', how='left')

    # 3. Calculate the number of each type of researcher's roadshow
    roadshow_counts = df_roadshow.groupby(['研究员', '服务事项']).size().reset_index(name='count')
    pivot_roadshow = roadshow_counts.pivot(index='研究员', columns='服务事项', values='count').fillna(0).reset_index()
    df_researcher = df_researcher.merge(pivot_roadshow, on='研究员', how='left').fillna(0)

    # 4. Calculate the number of times each researcher served 5A or 4A customers
    filtered_customers = df_roadshow[df_roadshow['客户分级'].isin(['5A', '4A'])]
    customer_counts = filtered_customers.groupby('研究员').size().reset_index(name='54A路演次数')
    df_researcher = df_researcher.merge(customer_counts, on='研究员', how='left').fillna(0)
    df_researcher['54A路演次数'] = df_researcher['54A路演次数'].astype(int)

    # 5. Calculate the number of times each researcher served customers in each region
    regions_counts = df_roadshow[df_roadshow['客户区域'].isin(['北京', '上海', '广深'])]  # Filter for specified regions
    regions_counts = regions_counts.groupby(['研究员', '客户区域']).size().reset_index(name='count')
    pivot_regions = regions_counts.pivot(index='研究员', columns='客户区域', values='count').fillna(0).reset_index()
    df_researcher = df_researcher.merge(pivot_regions, on='研究员', how='left').fillna(0)

    # sort df_researcher by industry
    df_researcher.sort_values(by='所属团队', inplace=True)

    return df_researcher


def get_df_team(df_roadshow):
    # drop duplicates for df_roadshow based on '序号'
    df_unique = df_roadshow.drop_duplicates(subset=['序号'], keep='first')

    # Calculate the number of times each team served customers
    total_roadshows_per_team = df_unique.groupby('所属团队')['序号'].count().reset_index(name='总路演次数')
    service_counts_per_team = df_unique.groupby(['所属团队', '服务事项']).size().reset_index(name='count')
    pivot_service_counts = service_counts_per_team.pivot(index='所属团队', columns='服务事项', values='count').fillna(0).astype(int).reset_index()
    df_team = total_roadshows_per_team.merge(pivot_service_counts, on='所属团队', how='left')

    # Calculate the number of times each team served 5A or 4A customers
    filtered_customers = df_unique[df_unique['客户分级'].isin(['5A', '4A'])]
    customer_counts = filtered_customers.groupby('所属团队').size().reset_index(name='54A路演次数')
    df_team = df_team.merge(customer_counts, on='所属团队', how='left').fillna(0)
    df_team['54A路演次数'] = df_team['54A路演次数'].astype(int)

    # Calculate the number of times each researcher served customers in each region
    regions_counts = df_unique[df_unique['客户区域'].isin(['北京', '上海', '广深'])] 
    regions_counts = regions_counts.groupby(['所属团队', '客户区域']).size().reset_index(name='count')
    pivot_regions = regions_counts.pivot(index='所属团队', columns='客户区域', values='count').fillna(0).reset_index()
    df_team = df_team.merge(pivot_regions, on='所属团队', how='left').fillna(0)

    return df_team


def get_df_org(df_researcher):
    df_org = pd.DataFrame()

    # Get the numeric columns by excluding the first two columns
    numeric_columns = df_researcher.columns[2:]

    # Iterate through the numeric columns of df_researcher
    for column in numeric_columns:
        # Sum the column
        column_sum = df_researcher[column].sum()
        # Create a new row with the column name and sum, and append it to df_org
        new_row = pd.DataFrame({'Attribute': [column + '（总计）'], 'Sum': [column_sum]})
        df_org = pd.concat([df_org, new_row], ignore_index=True)

    # Rename the columns of df_org
    df_org = df_org.rename(columns={'Attribute': '路演指标', 'Sum': '合计值'})

    return df_org


def okr_calculation_pipeline(df_okr, df_salespeople_info):
    sales_name_list = get_sales_name_list(df_salespeople_info)
    df_roadshow, df_special = get_df_roadshow(df_okr, sales_name_list)
    df_researcher = get_df_researcher(df_roadshow)
    df_team = get_df_team(df_roadshow)
    df_org = get_df_org(df_researcher)

    return df_roadshow, df_researcher, df_team, df_org, df_special



# ------------------------------------------- #
# Step 4 (Optional): Save cleansed okr data to Excel     #
# ------------------------------------------- #

def compose_output_file_name(okr_excel_path, output_folder_path):
    """
    Compose the output file name based on the OKR Excel file name.
    # retrieve the year and month from the okr_excel_path
    # compose the output file name

    :param okr_excel_path: the path of the OKR Excel file
    :return: the output file name
    """
    # Get the file name from the OKR Excel file path
    okr_excel_file_name = okr_excel_path.split('/')[-1]
    # Get the year and month from the file name
    year = okr_excel_file_name.split('.')[0]
    month = okr_excel_file_name.split('.')[1]
    # Compose the output file name
    output_file_name = f'okr_roadshow_{year}{month}.xlsx'
    # Compose the output file path
    output_file_path = output_folder_path + output_file_name
    return output_file_path


def write_dfs_to_excel(dfs_dict, okr_excel_path , engine='openpyxl'):
    """
    Write DataFrames to Excel
    :param dfs_dict: the dictionary of DataFrames
    :param output_path: the output path
    :param engine: the engine to write Excel
    :return: None
    """

    output_path = compose_output_file_name(okr_excel_path, output_folder_path)

    # dfs_dict = {name[3:]: globals()[name] for name in SHEET_NAMES if name in globals()}

    if not dfs_dict:
        raise ValueError("No DataFrames provided to write to Excel.")
    
    with pd.ExcelWriter(output_path, engine=engine) as writer:
        for sheet_name, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


# ------------------------------------------- #
# Step 6: Write okrs into separated txt files  #
# ------------------------------------------- #

def get_df_dict(df: pd.DataFrame, id_vars: list, var_name: str, value_name: str, split_var: str) -> dict:
    """
    Melt a DataFrame and return a dictionary of DataFrames, with each DataFrame corresponding to a unique value of the
    variable that was melted.

    Args:
        df: The DataFrame to melt.
        id_vars: The columns to keep as is.
        var_name: The name of the variable that will be melted.
        value_name: The name of the value that will be melted. 

    Returns:
        A dictionary of DataFrames, with each DataFrame corresponding to a unique value of the variable that was melted.
    """
    df_melt = df.melt(id_vars=id_vars, var_name=var_name, value_name=value_name)
    df_melt[value_name] = df_melt[value_name].astype(int)
    df_dict = {i: df_melt[df_melt[split_var] == i] for i in df_melt[split_var].unique()}
    return df_dict


def get_period_from_excel_name(excel_path: str) -> str:
    """
    Extracts the year and month from the filename of an excel file and returns the result as a string
    in the "某年某月" format
    """
    # Extract the year and month from the excel name
    excel_filename = excel_path.split('/')[-1]
    year, month = map(int, excel_filename.split('.')[:2])
    
    # Format the year and month as a string in the "某年某月" format
    year_month_str = f"{year}年{month}月"

    return year_month_str

def clean_file_name(name: str) -> str:
    """Clean up a file name by replacing problematic characters.
    
    Args:
        name: The file name to clean up.
    
    Returns:
        The cleaned file name.
    """
    return name.replace('/', '-').replace(' ', '_').replace('(', '').replace(')', '')


def write_dict_to_txts(data_dict, performance_type, folder_path, date):
    for key, value in data_dict.items():
        cleaned_key = clean_file_name(key)
        file_name = f'{performance_type}_{cleaned_key}_{date}.txt'
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write the file name (without the .txt extension) as the first line of the text file
            file.write(file_name.replace('.txt', '') + '\n')
            file.write(value.to_string(index=False))


def write_df_to_txt(df, performance_type, folder_path, date):
    file_name = f'{performance_type}_{date}.txt'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        # Write the file name (without the .txt extension) as the first line of the text file
        file.write(file_name.replace('.txt', '') + '\n')
        file.write(df.to_string(index=False))


def prepare_txt_pipeline(df_researcher, df_team, df_org, okr_excel_path):
    df_researcher_dict = get_df_dict(df_researcher, ['研究员', '所属团队'], '路演指标', '路演次数' , '研究员')
    df_team_dict = get_df_dict(df_team, ['所属团队'], '路演指标', '路演次数', '所属团队')

    date = get_period_from_excel_name(okr_excel_path)
    print(date)
    # Write txts for df_researcher_dict
    write_dict_to_txts(df_researcher_dict, '研究员绩效', txt_folder_path, date)

    # Write txts for df_team_dict
    write_dict_to_txts(df_team_dict, '团队绩效', txt_folder_path, date)

    # Write txt for df_org
    write_df_to_txt(df_org, '研究院绩效', txt_folder_path, date)

    return


