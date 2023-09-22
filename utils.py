import pandas as pd

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

def treat_empty_xuhao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Treat the empty values in '序号'
    :param df: the DataFrame
    :return: the DataFrame with no empty values in '序号'
    """
    special_list = []
    df_special = pd.DataFrame()

    if df['序号'].isna().sum() > 0:
        for i in range(len(df)):
            if pd.isna(df.loc[i, '序号']):
                special_list.append(i)
                print('The empty value in "序号" is in row {}'.format(i))
                df.loc[:, '序号'] = df['序号'].fillna(method='ffill')
        print('The empty value in "序号" is treated.')

    if len(special_list) > 0:
        df_special = df.iloc[special_list, :].copy()
        df_special.reset_index(drop=True, inplace=True)

    return df, df_special

def get_sales_name_list(df: pd.DataFrame) -> list:
    """
    Get the sales name list
    :param df: the DataFrame of the salesperson sheet
    :return: the sales name list
    """
    sales_name_list = df['员工姓名'].tolist()
    return sales_name_list

def treat_special_researcher(df: pd.DataFrame, sales_name_list) -> pd.DataFrame:
    """
    Treat the special values in '研究员'
    :param df: the DataFrame
    :return: the DataFrame with no special values in '研究员'
    """
    # special case 1
    df_temp = df[df['研究员'].str.contains('无研究员') == False].copy()
    # special case 2
    df_temp.loc[df_temp['研究员'].str.contains('胡又文'), '研究员'] = '所长'
    # write ‘所长’ in the column of '所属团队'
    df_temp.loc[df_temp['研究员'] == '所长', '所属团队'] = '所长'
    
    # special case 3
    df_temp = df_temp[df_temp['研究员'].isin(sales_name_list) == False].copy()
    return df_temp


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


# print na rate of a df
def print_na_rate(df: pd.DataFrame) -> None:
    """
    Print the na rate of a DataFrame
    :param df: the DataFrame
    :return: None
    """
    print('The na rate of the DataFrame is:')
    print(df.isna().sum() / len(df))