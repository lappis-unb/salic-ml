import scipy.stats as stats
import numpy as np

def is_outlier(x, mean, standard_deviation, c=1.5):
    return x > (mean + c * standard_deviation)


def maximum_expected_value(mean, standard_deviation, c=1.5):
    return mean + c * standard_deviation


def outlier_probability(mean, standard_deviation, c=1.5):
    probability = stats.norm(mean, standard_deviation).cdf(
        mean + c * standard_deviation)
    return probability

def outlier_scale(x, mean, standard_deviation, c=1.5):
    if (is_outlier(x, mean, standard_deviation)):
        start_probality = outlier_probability(mean, standard_deviation,c)
        current_probability = stats.norm(mean, standard_deviation).cdf(x)
        probability = (current_probability - start_probality)/(1 - start_probality)
    else:
        probability = -1

    return probability