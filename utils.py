import numpy as np
import pandas as pd

n = 50000
n_columns = 10
random_na = 100
n_other_columns = 500


def generate_test_df():
    """Generate data source df"""
    numerical_columns_value = np.random.random([n, n_columns])
    numerical_columns_value[
        np.random.randint(0, n, random_na), np.random.randint(0, n_columns, random_na)
    ] = np.nan
    other_columns_value = np.random.random([n, n_other_columns])

    # categorical_columns_options = [np.random.randint(1,6, np.random.randint(3,5,1)) for i in range(n_columns)]
    categorical_columns_value = np.array(
        [
            np.random.choice(np.arange(1, np.random.randint(3, 5, 1)), n)
            for i in range(n_columns)
        ]
    ).T
    numerical_columns_name = [f"numerical_{str(i)}" for i in range(n_columns)]
    categorical_columns_name = [f"categorical_{str(i)}" for i in range(n_columns)]
    other_columns_name = [f"other_{str(i)}" for i in range(n_other_columns)]
    date_column = pd.date_range("2010-01-01", periods=n, freq="d").strftime("%Y-%m-%d")

    df = pd.DataFrame(
        np.concatenate(
            [numerical_columns_value, categorical_columns_value, other_columns_value],
            axis=1,
        ),
        columns=numerical_columns_name + categorical_columns_name + other_columns_name,
    )
    df["date"] = date_column
    df = df.astype({name: "int" for name in categorical_columns_name}).astype(
        {name: "str" for name in categorical_columns_name}
    )
    return df
