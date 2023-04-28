import pandas as pd
import numpy as np


def main():
    filenames = ["pre_PANAS.xlsx", "post_PANAS.xlsx"]
    positive_affect_indices = [1, 3, 5, 9, 10, 12, 14, 16, 17, 19]
    negative_affect_indices = [2, 4, 6, 7, 8, 11, 13, 15, 18, 20]

    cols_to_save = {}

    for filename in filenames:
        prefix = filename.split("_")[0]

        df = pd.read_excel(filename)

        num_cols = df.shape[0]
        pos_PANAS_col_name = f"{prefix}_positive_PANAS"
        neg_PANAS_col_name = f"{prefix}_negative_PANAS"

        cols_to_save[pos_PANAS_col_name] = []
        cols_to_save[neg_PANAS_col_name] = []

        df[pos_PANAS_col_name] = [np.nan] * num_cols
        df[neg_PANAS_col_name] = [np.nan] * num_cols

        for row_tuple in df.iterrows():
            row_index, row = row_tuple
            row = list(row)[1:21]

            pos_panas_score = 0
            neg_panas_score = 0

            for i, emotion_val in enumerate(row):
                if i in positive_affect_indices:
                    pos_panas_score += emotion_val
                elif i in negative_affect_indices:
                    neg_panas_score += emotion_val

            df.loc[row_index, neg_PANAS_col_name] = neg_panas_score
            df.loc[row_index, pos_PANAS_col_name] = pos_panas_score

        cols_to_save[pos_PANAS_col_name].append(df.loc[:, pos_PANAS_col_name])
        cols_to_save[neg_PANAS_col_name].append(df.loc[:, neg_PANAS_col_name])

    df = df.drop(columns=["name", neg_PANAS_col_name, pos_PANAS_col_name])

    for col_name, col_values in cols_to_save.items():
        df[col_name] = col_values[0]

    df.to_csv("phission_PANAS_results.xlsx", index=False)


if __name__ == "__main__":
    main()
