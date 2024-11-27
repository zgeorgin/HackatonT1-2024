
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

def dubl(df,ser):
    list = []
    if ser not in df.columns:
        raise ValueError(f"Столбец '{ser}' не найден в DataFrame.")
    dupl = df[df.duplicated(subset=[ser],keep=False)]
    dupl1 = dupl['client_id'].unique()
    for i in dupl1:
        list.append(dupl.loc[dupl.client_id == i].to_dict())
    return list