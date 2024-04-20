"""
One-Hot Encoding:
    Suitable for nominal categorical variables with a small number of unique categories.
    Useful when categories are not ordinal and have no inherent order.
    Can lead to high-dimensional sparse datasets.

Label Encoding:
    Suitable for ordinal categorical variables with an inherent order.
    Converts categories into ordinal integers.
    May not be suitable for algorithms that assume numerical relationships between categories.

Target Encoding (Mean Encoding):
    Suitable for classification tasks.
    Replaces categories with the mean of the target variable for each category.
    Helps capture target-specific information within categorical variables.
    May lead to overfitting if not used carefully, especially with high cardinality variables.

Frequency Encoding:
    Suitable when the frequency of categories provides meaningful information.
    Replaces categories with their frequency in the dataset.
    Useful for high cardinality variables.

Binary Encoding:
    Suitable for high cardinality variables with a large number of unique categories.
    Reduces the dimensionality of the data by encoding each category into binary digits.
    Maintains interpretability and reduces the risk of overfitting compared to one-hot encoding.
"""

import pandas as pd
import category_encoders as ce
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


def target_encoding(df: pd.DataFrame, column: str, target: str) -> pd.DataFrame:
    target_encoding = df.groupby(column)[target].mean()
    df[column + "_encoded"] = df[column].map(target_encoding)
    return df


def frequency_encoding(df: pd.DataFrame, column: str) -> pd.DataFrame:
    frequency_encoding = df[column].value_counts(normalize=True)
    df[column + "_encoded"] = df[column].map(frequency_encoding)
    return df


def label_encoding(df: pd.DataFrame, column: str) -> pd.DataFrame:
    label_encoder = LabelEncoder()
    df[column + "_encoded"] = label_encoder.fit_transform(df[column])
    return df


def one_hot_encoding(df: pd.DataFrame, column: str) -> pd.DataFrame:
    one_hot_encoded = pd.get_dummies(df[column], prefix=column)
    df = pd.concat([df, one_hot_encoded], axis=1)
    return df


def binary_encoding(df: pd.DataFrame, column: str) -> pd.DataFrame:
    binary_encoder = ce.BinaryEncoder(cols=[column])
    df_binary = binary_encoder.fit_transform(df[column])
    return df_binary


# Sample usage:
# df = pd.DataFrame({"category": ["A", "B", "C", "A", "B"], "target": [1, 0, 1, 1, 0]})
# df_encoded = target_encoding(df, "category", "target")
# df_encoded = frequency_encoding(df, "category")
# df_encoded = label_encoding(df, "category")
# df_encoded = binary_encoding(df, "category")
# df_encoded = one_hot_encoding(df, "category")
# print(df_encoded)
