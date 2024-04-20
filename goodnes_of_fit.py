from scipy.stats import chisquare
import pandas as pd

def test_uniformity(df, column):
    # Calculate the observed frequencies of each category
    observed_frequencies = df[column].value_counts()
    
    # Calculate the expected frequencies assuming a uniform distribution
    n_categories = len(observed_frequencies)
    expected_frequency = len(df) / n_categories
    
    # Perform the Chi-square test for goodness of fit
    chi2_stat, p_value = chisquare(observed_frequencies, f_exp=[expected_frequency]*n_categories)
    
    # Determine whether the distribution is close to uniform based on the p-value
    if p_value < 0.05:  # Significance level of 0.05
        print("The distribution of categories in '{}' is not close to uniform.".format(column))
    else:
        print("The distribution of categories in '{}' is close to uniform.".format(column))

# Sample usage:
# df = pd.DataFrame({'category': ['A', 'B', 'C', 'A', 'B', 'A', 'C', 'C']})
# test_uniformity(df, 'category')
