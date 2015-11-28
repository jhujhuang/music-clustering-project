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


def cluster(data, k):
    """
    Perform k-means clustering on given data.

    :param data: List of array data points of same dimensions
    :param k: Number of clusters
    :return: A dictionary of (0 ... k-1) to clusters
    """
    # Initialize to k random centers
    old_mu = None
    mu = random.sample(data, k)
    while not has_converged(mu, old_mu):
        # Assign all points to clusters
        clusters = e_step(data, mu)
        # Reevaluate means
        old_mu = mu
        mu = m_step(clusters)
    return clusters
