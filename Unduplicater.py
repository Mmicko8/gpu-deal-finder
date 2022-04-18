import pandas as pd


def un_duplicate(df_new, old_deals_path):
    df_old = pd.read_csv(old_deals_path, sep='\t', index_col=0)

    # remove all rows from df_new that are present in df_old using left outer join
    df_new = pd.merge(df_new, df_old, indicator=True, how='outer')\
        .query('_merge=="left_only"')\
        .drop('_merge', axis=1)

    df_old = pd.concat([df_new, df_old], ignore_index=True, axis=0)
    df_old.to_csv(old_deals_path, sep='\t')

    return df_new
