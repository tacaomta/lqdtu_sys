def remove_duplicates(df):

    # remove duplicate DOI

    if "DOI" in df.columns:

        df = df.drop_duplicates(
            subset=["DOI"],
            keep="first"
        )

    return df
