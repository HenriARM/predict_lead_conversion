
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

import pandas as pd

# filepath = "./chunk_100.csv"
filepath = "ds_task_ jeff.csv"

data = pd.read_csv(filepath, low_memory=False)

lead_utm_cols = ['lead_utm_source', 'lead_utm_medium', 'lead_utm_campaign']
redirect_utm_cols = ['redirect_utm_source', 'redirect_utm_medium', 'redirect_utm_campaign']

# for lead_col, redirect_col in zip(lead_utm_cols, redirect_utm_cols):
#     num_different_rows = (data[lead_col] != data[redirect_col]).sum()
#     print(f"Number of rows where {lead_col} and {redirect_col} are different: {num_different_rows}")

# TODO: apply to _utm_campaign dimensionality reduction
lead_utm_cols = ['lead_utm_source', 'lead_utm_medium']
redirect_utm_cols = ['redirect_utm_source', 'redirect_utm_medium']

# TODO: check different_redirect_partners,different_redirect_sources,different_ips,different_uas
# TODO: calc correlation of numerical columns and drop what's not needed
# TODO: "lead_ip_city" has 577 unique columns, try frequency encoding, target encoding, binary encoding or dim reduction
# TODO: how I will know which method is the best one
# TODO: SimpleImputer


X = pd.get_dummies(data[lead_utm_cols + redirect_utm_cols])
# drop null values
X = X.dropna()


lead_ip_cols = ['lead_ip_country_code', 'lead_ip_region_name', 'lead_ip_city', 'lead_ip_isp', 'lead_ip_as_name', 'lead_ip_is_hosting', 'lead_ip_is_mobile', 'lead_ip_is_proxy']
redirect_ip_cols = ['redirect_ip_country_code', 'lredirect_ip_region_name', 'redirect_ip_city', 'redirect_ip_isp', 'redirect_ip_as_name', 'redirect_ip_is_hosting', 'redirect_ip_is_mobile', 'redirect_ip_is_proxy']

# for lead_col, redirect_col in zip(lead_utm_cols, redirect_utm_cols):
#     num_different_rows = (data[lead_col] != data[redirect_col]).sum()
#     print(f"Number of rows where {lead_col} and {redirect_col} are different: {num_different_rows}")


lead_time_cols = ['lead_hour_of_registration', 'lead_weekday_of_registration', 'lead_month_day_of_registration', 'lead_referrer']
redirect_time_cols = ['redirect_timestamp', 'redirect_hour', 'redirect_weekday', 'redirect_month_day', 'redirect_referrer']

lead_ua_cols = ['lead_ua_device_class', 'lead_ua_device_name', 'lead_ua_device_brand', 'lead_ua_os_class', 'lead_ua_os_name', 'lead_ua_os_version', 'lead_ua_os_version_name', 'lead_ua_layout_engine_class', 'lead_ua_layout_engine_version', 'lead_ua_agent_class', 'lead_ua_agent_name', 'lead_ua_agent_version']
redirect_ua_cols = ['redirect_ua_device_class', 'redirect_ua_device_name', 'redirect_ua_device_brand', 'redirect_ua_os_class', 'redirect_ua_os_name', 'redirect_ua_os_version', 'redirect_ua_os_version_name', 'redirect_ua_layout_engine_class', 'redirect_ua_layout_engine_version', 'redirect_ua_agent_class', 'redirect_ua_agent_name', 'redirect_ua_agent_version']


le = LabelEncoder()
data['redirect_partner_class'] = le.fit_transform(data['redirect_partner'])
mapping = dict(zip(le.classes_, range(len(le.classes_))))
print(mapping)


import numpy as np
from scipy.stats import chi2_contingency

def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

# Calculate Cramér's V for each pair of columns
for lead_col, redirect_col in zip(lead_ip_cols, redirect_ip_cols):
    v = cramers_v(data[lead_col], data[redirect_col])
    print(f"Cramér's V for {lead_col} and {redirect_col}: {v}")


"""
# Identify categorical and numerical columns
categorical_cols = data.select_dtypes(include=["object", "bool"]).columns.to_list()
numerical_cols = data.select_dtypes(include=["int64", "float64"]).columns.to_list()

# We'll remove identifiers and timestamp columns as they are not useful for prediction
categorical_cols_to_use = [
    col
    for col in categorical_cols
    if col not in ["redirect_id", "lead_id", "redirect_timestamp"]
]
numerical_cols_to_use = [col for col in numerical_cols if col not in ["redirect_id"]]

# Define preprocessing for numerical and categorical data
numerical_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_cols_to_use),
        ("cat", categorical_transformer, categorical_cols_to_use),
    ]
)

# Define the model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42)),
    ]
)

# Split data into features and target
y = data[
    "converted_to_a"
]  # Assuming 'converted_to_a' as the target for demonstration, adjust as needed
X = data.drop(
    [
        "converted_to_a",
        "converted_to_b",
        "conversion_revenue",
        "expected_b_revenue",
        "expected_a_revenue",
    ],
    axis=1,
)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model training
model.fit(X_train, y_train)

# Score the model on the test set
score = model.score(X_test, y_test)

print(score)
"""