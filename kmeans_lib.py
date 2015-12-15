import random
import numpy


def e_step(samples, mu):
    clusters = {}
    for x in samples:
        cluster_found = min(enumerate(mu), key=lambda tt: numpy.linalg.norm(x-tt[1]))[0]
        if cluster_found in clusters.keys():
            clusters[cluster_found].append(x)
        else:
            clusters[cluster_found] = [x]
    return clusters


def m_step(clusters):
    new_mu = []
    for k in sorted(clusters.keys()):
        new_mu.append(numpy.mean(clusters[k], axis=0))
    return new_mu


def has_converged(mu1, mu0):
    if not mu0:
        return False
    return set([tuple(t) for t in mu1]) == set([tuple(t) for t in mu0])


def get_kmeans_plusplus(data, k):
    # Get first center at random
    mu = random.sample(data, 1)
    n = len(data)

    def find_nearest_center_distance(x):
        return min(abs(numpy.linalg.norm(x - center)) for center in mu)

    while len(mu) < k:
        # Compute all D(x)
        distance_prob = [pow(find_nearest_center_distance(x), 2) for x in data]
        # Normalize probabilities
        sum_distance_square = sum(distance_prob)
        distance_prob = [p / sum_distance_square for p in distance_prob]
        # Choose one new center
        choice = numpy.random.choice(range(n), p=distance_prob)
        mu.append(data[choice])
    return mu


def cluster(data, k, plusplus=False):
    """
    Perform k-means clustering on given data.

    :param data: List of array data points of same dimensions
    :param k: Number of clusters
    :param plusplus: Whether or not to use kmeans++ initialization
    :return: A dictionary of (0 ... k-1) to clusters
    """
    # Initialize to k random centers
    old_mu = None
    if plusplus:
        mu = get_kmeans_plusplus(data, k)
    else:
        mu = random.sample(data, k)

    # Run EM until convergence
    while not has_converged(mu, old_mu):
        # Assign all points to clusters
        clusters = e_step(data, mu)
        # Reevaluate means
        old_mu = mu
        mu = m_step(clusters)
    return clusters
