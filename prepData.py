import pandas as pd
def fill_missing_values(df):
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(0, inplace=True)
        elif df[col].dtype == 'object':
            df[col].fillna('Не указано', inplace=True)
        elif df[col].dtype == 'datetime64[ns]':
            df[col].fillna('1901-01-01', inplace=True)
    return df

def prep(df):
    df = fill_missing_values(df)
    return df.to_dict()

def dubl(df,ser,matchCol):
    print(df)
    if ser not in df.columns:
        raise ValueError(f"Столбец '{ser}' не найден в DataFrame.")
    value_counts = df[ser].value_counts()
    nonunique_values = value_counts[value_counts > 1].index

    filtered_df = df[df[ser].isin(nonunique_values)]
    print(filtered_df)

    neededCol = filtered_df[['index', ser, matchCol]]
    print(neededCol)
    grouped =  neededCol.groupby(ser)
    dfs_list = grouped.agg({matchCol: lambda x: x, 'index': tuple})
    
    print(dfs_list)
    return dfs_list, value_counts[value_counts == 1].index
