def get_df_unique(df_roadshow):
    unique_teams_per_roadshow = df_roadshow.groupby('序号')['所属团队'].nunique().reset_index(name='unique_teams_count')
    merged_df = df_roadshow.merge(unique_teams_per_roadshow, on='序号', how='left')
    multi_team_rows = merged_df[merged_df['unique_teams_count'] > 1].drop_duplicates(subset=['序号', '所属团队'])
    single_team_rows = merged_df[merged_df['unique_teams_count'] == 1].drop_duplicates(subset=['序号'])
    filtered_df = pd.concat([multi_team_rows, single_team_rows])
    return filtered_df

def get_unique_teams_per_roadshow(df):
    """
    Get the number of unique teams per roadshow
    """
    unique_teams_per_roadshow = df.groupby('序号')['所属团队'].nunique().reset_index(name='unique_teams_count')
    return unique_teams_per_roadshow




    total_roadshows_per_team = filtered_df.groupby('所属团队')['序号'].count().reset_index(name='总路演次数')
    service_counts_per_team = filtered_df.groupby(['所属团队', '服务事项']).size().reset_index(name='count')
    pivot_service_counts = service_counts_per_team.pivot(index='所属团队', columns='服务事项', values='count').fillna(0).astype(int).reset_index()
    result_df = total_roadshows_per_team.merge(pivot_service_counts, on='所属团队', how='left')

    return result_df