from __future__ import division
import random
import numpy
import kmeans_lib

_CONVERGE_ORDER = 2.2

class GMM(object):

    def __init__(self, data, k, plusplus=False):
        self.num_samples = len(data)
        self.data = data
        self.k = k
        # Initialize centers with/without kmeans++ option
        self.mu = self._initialize_centers(plusplus)
        # Initialize covariance as identity matrices
        m = len(data[0])
        self.cov = [numpy.identity(m)] * k
        # Initialize pi as equally likely
        self.pi = numpy.ones(k) / k
        self.first_check_increase = None

    def find_clusters(self):
        old_log_ll = None
        log_ll = self._find_log_likelihood()
        print log_ll, "       IS LOG LIKEL"
        # Run EM until convergence
        while not self._has_converged(log_ll, old_log_ll):
            # E Step
            resp = self._get_current_responsibilities()
            # M Step
            self._update_parameters(resp)

            old_log_ll = log_ll
            log_ll = self._find_log_likelihood()

        # associate each point with the most likely cluster
        clusters = {}
        resp = self._get_current_responsibilities()
        for i in range(self.num_samples):
            cluster_found = max(range(self.k), key=lambda kk:resp[i][kk])
            if cluster_found in clusters.keys():
                clusters[cluster_found].append(self.data[i])
            else:
                clusters[cluster_found] = [self.data[i]]
        return clusters

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
                [self.pi[k] * pdf_multivariate_gauss(xx, self.mu[k], self.cov[k]) for k in range(self.k)]
            )) for xx in self.data]
        )

    def _get_current_responsibilities(self):
        resp = [numpy.zeros(self.k)] * self.num_samples
        # TODO: DEBUG!!!!!!
        for i in range(self.num_samples):
            for k in range(self.k):
                print "pdf is ", pdf_multivariate_gauss(self.data[i], self.mu[k], self.cov[k])
                resp[i][k] = self.pi[k] * pdf_multivariate_gauss(self.data[i], self.mu[k], self.cov[k])
            print resp[i], i, self.pi
            sum_resp = sum([resp[i][k] for k in range(self.k)])
            resp[i] = [r / sum_resp for r in resp[i]]  # Normalize
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
            self.cov[k] = numpy.array([[0.0]*len(self.data[0])] * len(self.data[0]))
            for i in range (1, self.num_samples):
                diff = self.data[i] - self.mu[k]
                add = numpy.transpose(numpy.matrix(diff)).dot(numpy.matrix(diff))# / big_n[k]
                self.cov[k] += add / big_n[k]

        # Update pi
        self.pi = [nk / float(self.num_samples) for nk in big_n]


def pdf_multivariate_gauss(x, mu, cov):
    """ This helper method was edited from the example from
        https://www.reddit.com/r/Python/comments/236odt/is_there_really_no_good_library_for_a/

        Calculate the multivariate normal density (pdf)

        Keyword arguments:
            x = numpy array of a "d x 1" sample vector
            mu = numpy array of a "d x 1" mean vector
            cov = "numpy array of a d x d" covariance matrix
    """
    assert(cov.shape[0] == cov.shape[1]), 'covariance matrix must be square'
    assert(mu.shape[0] == cov.shape[0]), 'cov_mat and mu_vec must have the same dimensions'
    assert(mu.shape[0] == x.shape[0]), 'mu and x must have the same dimensions'
    part1 = 1 / (((2 * numpy.pi)**(len(mu)/2)) * (numpy.linalg.det(cov)**(1/2)))
    diff = numpy.transpose(numpy.matrix(x - mu))

    trans = numpy.transpose(diff)
    cov_inv = numpy.matrix(numpy.linalg.inv(cov))
    transtimescovinv = numpy.matrix(trans.dot(cov_inv))
    part2 = (-1/2) * transtimescovinv.dot(diff)
    result = part1 * numpy.exp(part2)
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
