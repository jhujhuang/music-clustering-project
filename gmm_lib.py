import random
import numpy
import kmeans_lib

_CONVERGE_ORDER = 6

class GMM(object):

    def __init__(self, data, k, plusplus=False):
        self.num_samples = len(data)
        self.data = data
        self.k = k
        # Initialize centers with/without kmeans++ option
        self.mu = self._initialize_centers(plusplus)
        # Initialize covariance as identity matrices
        m = len(data[0])
        self.cov = numpy.identity(m) * k
        # Initialize pi as equally likely
        self.pi = numpy.ones(k) / k

    def find_clusters(self):
        old_log_ll = None
        log_ll = self._find_log_likelihood()
        # Run EM until convergence
        while not self._has_converged(log_ll, old_log_ll):
            # E Step
            resp = self._get_current_responsibilities()
            # M Step
            self._update_parameters(resp)

            old_log_ll = log_ll
            log_ll = self._find_log_likelihood()
        return []  # TODO

    def _initialize_centers(self, pp):
        if pp:
            return kmeans_lib.get_kmeans_plusplus(self.data, self.k)
        else:
            return random.sample(self.data, self.k)

    def _has_converged(self, log_ll, old_log_ll):
        if not old_log_ll:
            # Before first iteration
            return False
        increase = log_ll - old_log_ll
        if not self.first_check_increase:
            # First iteration
            self.first_check_increase = increase
        return increase < self.first_check_increase * 10 ** (-_CONVERGE_ORDER)

    def _find_log_likelihood(self):
        return sum(
            [numpy.log(sum(
                [self.pi[k] * pdf_multivariate_gauss(xx, self.mu[k], self.cov[k]) for k in range(0, self.k)]
            )) for xx in self.data]
        )

    def _get_current_responsibilities(self):
        resp = numpy.zeros(self.num_samples, self.k)
        for i in range(self.num_samples):
            for k in range(self.k):
                resp[i][k] = self.pi[k] * pdf_multivariate_gauss(self.data[i], self.mu[k], self.cov[k])
            resp[i] = resp[i] / sum(resp[i])  # Normalize
        return resp

    def _update_parameters(self, resp):
        big_n = [sum([resp[i][k] for i in range(self.num_samples)]) for k in range(self.k)]
        # Update mu
        for k in range(self.k):
            self.mu[k] = sum(
                [resp[i][k] * self.data[i] for i in range(self.num_samples)]
            ) / big_n[k]
        # Update cov
        for k in range(self.k):
            self.cov[k] = sum(
                [resp[i][k] * (self.data[i] - self.mu[k]).dot(numpy.transpose(self.data[i] - self.mu[k]))
                 for i in range(self.num_samples)]
            ) / big_n[k]
        # Update pi
        self.pi = big_n / self.num_samples


def pdf_multivariate_gauss(x, mu, cov):
    """ This helper method was edited from the example from
        https://www.reddit.com/r/Python/comments/236odt/is_there_really_no_good_library_for_a/

        Calculate the multivariate normal density (pdf)

        Keyword arguments:
            x = numpy array of a "d x 1" sample vector
            mu = numpy array of a "d x 1" mean vector
            cov = "numpy array of a d x d" covariance matrix
    """
    assert(mu.shape[0] > mu.shape[1]), 'mu must be a row vector'
    assert(x.shape[0] > x.shape[1]), 'x must be a row vector'
    assert(cov.shape[0] == cov.shape[1]), 'covariance matrix must be square'
    assert(mu.shape[0] == cov.shape[0]), 'cov_mat and mu_vec must have the same dimensions'
    assert(mu.shape[0] == x.shape[0]), 'mu and x must have the same dimensions'
    part1 = 1 / (((2 * numpy.pi)**(len(mu)/2)) * (numpy.linalg.det(cov)**(1/2)))
    part2 = (-1/2) * ((x-mu).T.dot(numpy.linalg.inv(cov))).dot((x-mu))
    return float(part1 * numpy.exp(part2))


def cluster(data, k, plusplus=False):
    """
    Perform GMM clustering on given data with given number of clusters.

    :param data: List of array data points of same dimensions
    :param k: Number of clusters
    :return:
    """
    gmm = GMM(data, k, plusplus)
    return gmm.find_clusters()
