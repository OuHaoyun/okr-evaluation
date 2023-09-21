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
    for i in range(len(df)):
        if pd.isna(df.loc[i, '序号']):
            special_list.append(i)
            df.loc[:, '序号'] = df['序号'].fillna(method='ffill')
    return df

def get_df_roadshow(df: pd.DataFrame) -> pd.DataFrame:
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
    df_temp.loc[:, '序号'] = df_temp['序号'].astype(int)
    if df_temp['序号'].isna().sum() > 0:
        df_temp = treat_empty_xuhao(df_temp)
    df_temp.loc[:, '客户区域'] = df_temp['客户区域'].fillna(df_temp['客户机构'])
    df_temp.loc[:, '客户分级'] = df_temp['客户分级'].fillna(df_temp['客户机构'])

    # Melt the df based on researcher columns
    df_temp_melted = pd.melt(df_temp, id_vars=service_columns, value_vars=researcher_columns, value_name='研究员姓名')
    df_temp_melted.drop('variable', axis=1, inplace=True) 
    df_temp_melted.dropna(subset=['研究员姓名'], inplace=True)
    df_temp_melted.rename(columns={'研究员姓名': '研究员'}, inplace=True)

    # Map team based on researcher name
    # todo

    # Sort the DataFrame based on '序号'
    df_temp_sorted = df_temp_melted.sort_values(by='序号')
    df_temp_sorted.reset_index(drop=True, inplace=True)

    # Make a copy of the temp df as the roadshow df
    df_roadshow = df_temp_sorted.copy()

    return df_roadshow


# print na rate of a df
def print_na_rate(df: pd.DataFrame) -> None:
    """
    Print the na rate of a DataFrame
    :param df: the DataFrame
    :return: None
    """
    print('The na rate of the DataFrame is:')
    print(df.isna().sum() / len(df))