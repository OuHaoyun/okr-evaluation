import pandas as pd

def get_df_roadshow(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the roadshow DataFrame
    :param df: the DataFrame of the roadshow sheet
    :return: the roadshow DataFrame
    """
    # Define roadshow columns
    researcher_columns = ['研究员', '研究员.1', '研究员.2', '研究员.3', '研究员.4', '研究员.5', '研究员.6']
    service_columns = ['序号','所属团队', '服务事项', '客户机构', '客户分级', '客户区域']
    roadshow_columns = service_columns + researcher_columns

    # Read relavant columns and fillna
    df_temp = df[roadshow_columns].copy()
    df_temp.loc[:, '序号'] = df_temp['序号'].fillna(method='ffill')
    df_temp.loc[:, '序号'] = df_temp['序号'].astype(int)

    # Melt the df based on researcher columns
    df_temp_melted = pd.melt(df_temp, id_vars=service_columns, value_vars=researcher_columns, value_name='研究员姓名')
    df_temp_melted.drop('variable', axis=1, inplace=True) 
    df_temp_melted.dropna(subset=['研究员姓名'], inplace=True)
    df_temp_melted.rename(columns={'研究员姓名': '研究员'}, inplace=True)
    df_temp_melted.loc[:, '所属团队'] = df_temp_melted['所属团队'].fillna(method='ffill')

    # Sort the DataFrame based on '序号'
    df_temp_sorted = df_temp_melted.sort_values(by='序号')
    df_temp_sorted.reset_index(drop=True, inplace=True)

    # Make a copy of the temp df as the roadshow df
    df_roadshow = df_temp_sorted.copy()

    return df_roadshow