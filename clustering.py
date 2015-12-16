
import csv
from datetime import datetime
from matplotlib.pyplot import scatter, title, savefig, clf
import numpy
from os import listdir, makedirs
from os.path import exists, isfile, join
from shutil import copy
from sklearn.metrics import silhouette_score
import tsne
import gmm_lib
import kmeans_lib

_FEATURE_DIR = './features'
_MUSIC_DIR = './musicFiles'
_OUT_DIR = './testOut'

K = 4  # Number of clusters


def read(filename):
    """
    Read all csv files for features associated with given filename.

    :param filename: String, name of file including '.mp3'
    :return: (object with) tuple representing features
    """
    files = [f for f in listdir(_FEATURE_DIR) if isfile(join(_FEATURE_DIR, f))
             and filename + '.' in f]
    vector = []
    print filename
    for csv_name in files:
        with open(join(_FEATURE_DIR, csv_name), 'rb') as csv_file:
            """csv_reader = csv.reader(csv_file)
            hi = True
            for row in csv_reader:
                if hi:
                    print row
                hi = False
            t = t + (csv_reader.line_num,)"""  # using numpy & list now
            csv_data = numpy.genfromtxt(csv_file, comments='%', delimiter=',')
            vector.append(numpy.average(csv_data))
            vector.append(numpy.var(csv_data))
    return vector  # [0:6] for a smaller dimension for gaussian density computing

samples = []  # For storing which features is from which file

# Get features for all input samples
musicFiles = [f for f in listdir(_MUSIC_DIR) if '.mp3' in f]
allInput = []
for musicFile in musicFiles:
    features = numpy.array(read(musicFile))
    allInput.append(features)
    samples.append((features, musicFile,))
print allInput  # TODO: delete

# Clustering
method = 'kmeans++'
# clusters = kmeans_lib.cluster(allInput, K)  # Kmeans
clusters = kmeans_lib.cluster(allInput, K, True)  # Kmeans++
# clusters = gmm_lib.cluster(allInput, K, True)  # GMM with Kmeans++: have to decrease dimension!

def get_filename(feature_vector):
    for (fv, name) in samples:
        if numpy.array_equal(fv,feature_vector):
            return name

for key in clusters:
    print '\n' + str(key) + ':\n'
    for fv in clusters[key]:
        print get_filename(fv)
        # Output files to clustered directories
        now = datetime.today()
        run = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute)
        directory = join(_OUT_DIR, run, str(key))
        if not exists(directory):
            makedirs(directory)
        copy(join(_MUSIC_DIR, get_filename(fv)), directory)

print '\nMusic files categorized successful!\n'

X = []
y = []
for key in clusters:
    for fv in clusters[key]:
        X.append(fv)
        y.append(key)
X = numpy.array(X)
y = numpy.array(y)

#  Plot data points
for i in range(5):
    X_2d = tsne.bh_sne(X, perplexity=5)
    scatter(X_2d[:, 0], X_2d[:, 1], c=y)
    title(method + " with k = " + str(K))
    savefig('testOut/' + run + str(i) + '.png')
    clf()

#  Calculate silhouette score
silhouette_avg = silhouette_score(X, y)
print 'The average silhouette score is: ', silhouette_avg
