
import pandas as pd
import numpy as np


def matrix_to_df(matrix):
    columns, *rest = matrix
    d = {}
    values = np.array(rest)

    for i, column in enumerate(columns):
        d[column] = values[:,i]

    return pd.DataFrame(d)
