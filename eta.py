import pandas as pd

pd.set_option("future.no_silent_downcasting", True)
# # Options to display all rows and columns
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)

filepath = "./ds_task_jeff.csv"


def process_chunk(df: pd.DataFrame, headers=None):
    # if headers is not None:
    #     df.columns = headers
    # else:
    #     headers = df.columns.tolist()

    # # set index
    # if df[idx_column].nunique() == len(df):
    #     df.set_index(idx_column, inplace=True)

    # # TODO: tmp
    # columns_to_drop = [
    #     "Cits",
    #     "Vai slimnīcā Jūs piedzīvojāt kādu/-us ar pacienta drošību saistītu/-us atgadījumu/-us:",
    #     "Cits ar zālēm saistīts atgadījums",
    # ]
    # for column in columns_to_drop:
    #     if column in df.columns:
    #         df.drop(column, axis=1, inplace=True)

    # # drop row if at least one NaN
    # df.dropna(axis=0, how="any", inplace=True)

    # question_columns = df.drop(
    #     [year_column, other_reason_column], axis=1
    # ).columns.tolist()

    # # make sure there is no other values than "Yes" or "No"
    # for column in question_columns:
    #     assert set(df[column].unique()).issubset({"Jā", "Nē", "Y", 1, 9999})

    # # convert column values Yes No to 1 0
    # df[question_columns] = df[question_columns].replace(
    #     {"Jā": 1, "Nē": 0, "Y": 1, 9999: 0}
    # )

    # # print full raw as a dict
    # # print(json.dumps(df.iloc[3].to_dict(), indent=4, ensure_ascii=False))
    return df

def main():

    # total rows: 314151
    # df = pd.read_csv(filepath)
    # print(len(df))

    first_row = 0
    chunksize = 10000
    total = 1 * chunksize + first_row

    # count rows

    for skip in range(first_row, total, chunksize):
        df = pd.read_csv(filepath, skiprows=skip, nrows=chunksize)
        continue

        numerical_descriptive_stats = df.describe()
        # TODO: swap and save as a file
        # print(numerical_descriptive_stats)
        missing_values = df.isnull().mean() * 100
        # print(missing_values[missing_values != 0])
        conversion_correlations = df[
            [
                "converted_to_a",
                "converted_to_b",
                "conversion_revenue",
                "expected_b_revenue",
                "expected_a_revenue",
            ]
        ].corr()

        data = df

        # descriptive statistics (analyze basic statistics of numerical and categorical features to understand the distribution of key variables,
        # identify outliers, and detect any immediate data quality issues.)

        # Categorical variables of interest
        categorical_vars = [
            "lead_utm_source",
            "lead_utm_medium",
            "lead_utm_campaign",
            "redirect_partner",
        ]

        # Distribution of Categorical Variables
        categorical_distributions = {
            var: data[var].value_counts(normalize=True).head(10)
            for var in categorical_vars
        }

        # Conversion Rates by Categorical Variables
        # For simplicity, we'll consider a lead as converted if either converted_to_a or converted_to_b is 1
        data["converted"] = data[["converted_to_a", "converted_to_b"]].max(axis=1)
        conversion_rates_by_category = {
            var: data.groupby(var)["converted"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            for var in categorical_vars
        }

        print(categorical_distributions)
        print(conversion_rates_by_category)

        # print(df)
        # print statistics
        # print(df.describe())
        # print(df.dtypes)
        # print all columns and types and one example of data from it
        # print(df.iloc[80])
        # cols = []
        # for i in range(1, 19):
        #     if i == 9:
        #         continue
        #         # cols.append(f"has_postback_from_{i}")
        #     else:
        #         cols.append(f"has_postback_from_{i}")
        # print(df[cols])

        # TODO make sure redirect is unique
        # print(df["redirect_id"].nunique())

        # TODO correlation of categorical variables

        
if __name__ == "__main__":
    main()


"""
redirect_id,
lead_id,


TODO: make them integer why they are float numbers :D ?
redirect_timestamp,
redirect_hour,redirect_weekday,redirect_month_day,

TODO: how here lead is different from redirect
TODO: clusterize
lead_utm_source,lead_utm_medium,lead_utm_campaign,
redirect_utm_source,redirect_utm_medium,redirect_utm_campaign,

TODO: make new column time difference between lead registration and redirect
lead_hour_of_registration,lead_weekday_of_registration,lead_month_day_of_registration,
TODO: is it same as hours_since_registration


TODO dont understand those columns????
lead_referrer, redirect_referrer
lead_brand, redirect_brand

IP
lead_ip_country_code,lead_ip_region_name,lead_ip_city,lead_ip_isp,lead_ip_as_name,
lead_ip_is_hosting,lead_ip_i s_mobile,lead_ip_is_proxy,

redirect_ip_country_code,lredirect_ip_region_name,redirect_ip_city,redirect_ip_isp,redirect_ip_as_name,
redirect_ip_is_hosting,redirect_ip_is_mobile,redirect_ip_is_proxy,

ip_matches_lead
--------------------------------

TODO: could be correlation between columns - arbitrary data
UA
lead_ua_device_class,lead_ua_device_name,lead_ua_device_brand,
lead_ua_os_class,lead_ua_os_name,lead_ua_os_version,lead_ua_os_version_name,lead_ua_layout_engine_class,
lead_ua_layout_engine_version,lead_ua_agent_class,lead_ua_agent_name,lead_ua_agent_version,

redirect_ua_device_class,redirect_ua_device_name,redirect_ua_device_brand,
redirect_ua_os_class,redirect_ua_os_name,redirect_ua_os_version,redirect_ua_os_version_name,redirect_ua_layout_engine_class,
redirect_ua_layout_engine_version,redirect_ua_agent_class,redirect_ua_agent_name,redirect_ua_agent_version,

ua_matches_lead
--------------------------------

TODO: same values? 
previous_redirect_count,has_previous_redirect


TODO: why source is different from partner
different_redirect_partners
different_redirect_sources

TODO: ????
different_ips,
different_uas,

TODO: sources 11, partners 14, why her is 18 (take bigger dataset)
redirects_to_1,redirects_to_2,redirects_to_3,redirects_to_4,redirects_to_5,redirects_to_6,
redirects_to_7,redirects_to_8,redirects_to_atm_9,redirects_to_10,redirects_to_11,redirects_to_12,
redirects_to_13,redirects_to_14,redirects_to_15,redirects_to_16,redirects_to_on_17,redirects_to_18,

has_redirect_to_same_partner,
previous_postback_count,
different_postback_partners,
hours_since_last_revenue,

Postback
TODO: test A + B is total postback? 
has_postback_from_1,has_postback_from_2,has_postback_from_3,has_postback_from_4,
has_postback_from_5,has_postback_from_6,has_postback_from_7,has_postback_from_8,
has_postback_from_atm_9,has_postback_from_10,has_postback_from_11,has_postback_from_12,
has_postback_from_13,has_postback_from_14,has_postback_from_15,has_postback_from_16
,has_postback_from_17,has_postback_from_18,

has_a_postback_from_1,has_a_postback_from_2,has_a_postback_from_3,has_a_postback_from_4,
has_a_postback_from_5,has_a_postback_from_6,has_a_postback_from_7,has_a_postback_from_8,
has_a_postback_from_9,has_a_postback_from_10,has_a_postback_from_11,has_a_postback_from_12,
has_a_postback_from_13,has_a_postback_from_14,has_a_postback_from_15,has_a_postback_from_16,has_a_postback_from_17,has_a_postback_from_18,

has_b_postback_from_1,has_b_postback_from_2,has_b_postback_from_3,has_b_postback_from_4,
has_b_postback_from_5,has_b_postback_from_6,has_b_postback_from_7,has_b_postback_from_8,
has_b_postback_from_9,has_b_postback_from_10,has_b_postback_from_11,has_b_postback_from_12,
has_b_postback_from_13,has_b_postback_from_14,has_b_postback_from_15,has_b_postback_from_16,
has_b_postback_from_17,has_b_postback_from_18,

revenue_from_1,revenue_from_2,revenue_from_3,revenue_from_4,revenue_from_5,revenue_from_6,
revenue_from_7,revenue_from_8,revenue_from_9,revenue_from_10,revenue_from_11,revenue_from_12,
revenue_from_13,revenue_from_14,revenue_from_15,revenue_from_16,revenue_from_17,revenue_from_18,

revenue_count_from_1,revenue_count_from_2,revenue_count_from_3,revenue_count_from_4,
revenue_count_from_5,revenue_count_from_6,revenue_count_from_7,revenue_count_from_8,
revenue_count_from_9,revenue_count_from_10,revenue_count_from_11,revenue_count_from_12,
revenue_count_from_13,revenue_count_from_14,revenue_count_from_15,revenue_count_from_16,
revenue_count_from_17,revenue_count_from_18,

time_since_revenue_from_1,time_since_revenue_from_2,time_since_revenue_from_3,time_since_revenue_from_4,
time_since_revenue_from_5,time_since_revenue_from_6,time_since_revenue_from_7,time_since_revenue_from_8,
time_since_revenue_from_9,time_since_revenue_from_10,time_since_revenue_from_11,time_since_revenue_from_12,
time_since_revenue_from_13,time_since_revenue_from_14,time_since_revenue_from_15,time_since_revenue_from_16,
time_since_revenue_from_17,time_since_revenue_from_18,

TODO: 1,2,3,... what is it?
b_count,a_count,

TODO: ?
b_in_1d,b_in_7d,b_in_30d,a_in_1d,a_in_7d,a_in_30d,

b_cr_to_different_partner,a_cr_to_different_partner,
non_converted_to_partner,
redirect_partner,

# booleans, 0 or 1
converted_to_b,converted_to_a,

# integer value, e.x. {0, 10, 20, 30, ..., 90}
conversion_revenue,


expected_b_revenue,expected_a_revenue

"""

# TODO how to check if a column is categorical
