import random
import numpy
import kmeans_lib


class GMM(object):

    def __init__(self, data, k, plusplus=False):
        self.data = data
        self.k = k
        # Initialize centers with/without kmeans++ option
        self.mu = self._initialize_centers(plusplus)
        # Initialize covariance as identity matrices
        m = len(data[0])
        self.cov = numpy.identity(m) * k
        # Initialize pi as equally likely
        self.pi = numpy.ones(k) / k

    def _initialize_centers(self, pp):
        if pp:
            return kmeans_lib.get_kmeans_plusplus(self.data, self.k)
        else:
            return random.sample(self.data, self.k)

    def find_clusters(self):
        # Run EM until convergence
        while not self._has_converged():
            pass  # TODO

    def _has_converged(self):
        pass


def cluster(data, k, plusplus=False):
    """
    Perform GMM clustering on given data with given number of clusters.

    :param data: List of array data points of same dimensions
    :param k: Number of clusters
    :return:
    """
    gmm = GMM(data, k, plusplus)
    return gmm.find_clusters()
