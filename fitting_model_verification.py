import preparation

from scipy.stats import weibull_min, lognorm, gamma, expon
import numpy as np

data_df = preparation.prepare_main_data(data_name="data")

data_df.dropna(inplace=True)

data = data_df["speed"]


# Define a function to safely compute log-likelihoods
def safe_log_likelihood(data, distribution, params):
    """
    Safely calculate the log-likelihood for a given distribution and parameters.
    Handles small probabilities to avoid log(0) errors.
    """
    try:
        # Compute PDF values
        pdf_values = np.clip(distribution.pdf(data, *params), a_min=1e-10, a_max=None)
        # Compute log-likelihood
        return np.sum(np.log(pdf_values))
    except Exception as e:
        print(f"Error calculating log-likelihood for {distribution.name}: {e}")
        return -np.inf


# Fit different distributions and compute AIC
aic_values = {}

# Weibull distribution
try:
    weibull_params = weibull_min.fit(data)  # Constrain loc to 0 if necessary
    weibull_ll = safe_log_likelihood(data, weibull_min, weibull_params)
    aic_values["Weibull"] = 2 * len(weibull_params) - 2 * weibull_ll
except Exception as e:
    print(f"Error fitting Weibull: {e}")

# Log-Normal distribution
try:
    lognorm_params = lognorm.fit(data)
    lognorm_ll = safe_log_likelihood(data, lognorm, lognorm_params)
    aic_values["Log-Normal"] = 2 * len(lognorm_params) - 2 * lognorm_ll
except Exception as e:
    print(f"Error fitting Log-Normal: {e}")

# Gamma distribution
try:
    gamma_params = gamma.fit(data)
    gamma_ll = safe_log_likelihood(data, gamma, gamma_params)
    aic_values["Gamma"] = 2 * len(gamma_params) - 2 * gamma_ll
except Exception as e:
    print(f"Error fitting Gamma: {e}")

# Exponential distribution
try:
    expon_params = expon.fit(data)
    expon_ll = safe_log_likelihood(data, expon, expon_params)
    aic_values["Exponential"] = 2 * len(expon_params) - 2 * expon_ll
except Exception as e:
    print(f"Error fitting Exponential: {e}")

# Output AIC values
for dist, aic in aic_values.items():
    print(f"AIC for {dist}: {aic}")

# Identify the best-fitting model
if aic_values:
    best_fit = min(aic_values, key=aic_values.get)
    print(f"The best-fitting model is: {best_fit}")
