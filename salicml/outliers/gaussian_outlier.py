import scipy


def is_outlier(x, mean, standard_deviation, c=1.5):
    return x > (mean + c * standard_deviation)


def maximum_expected_value(mean, standard_deviation, c=1.5):
    return mean + c * standard_deviation


def outlier_probability(mean, standard_deviation, c=1.5):
    norm = scipy.stats.norm
    probability = norm(mean, standard_deviation).cdf(
        mean + c * standard_deviation)
    return probability
