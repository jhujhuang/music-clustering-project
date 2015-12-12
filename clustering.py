
import csv
from datetime import datetime
import numpy
from os import listdir, makedirs
from os.path import exists, isfile, join
from shutil import copy
import kmeans_lib

_FEATURE_DIR = './features/small'
_MUSIC_DIR = './musicFiles/small'

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
    return vector

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
clusters = kmeans_lib.cluster(allInput, K)

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
        directory = join('./testOut', run, str(key))
        if not exists(directory):
            makedirs(directory)
        copy(join(_MUSIC_DIR, get_filename(fv)), directory)

print '\nMusic files categorized successful!\n'
