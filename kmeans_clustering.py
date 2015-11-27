
import csv
import numpy
from os import listdir
from os.path import isfile, join
from shutil import copy

_FEATURE_DIR = './features/'
_MUSIC_DIR = './musicFiles'

K = 4  # Number of clusters


def read(filename):
    """
    Read all csv files for features associated with given filename.

    :param filename: String, name of file including '.mp3'
    :return: (object with) tuple representing features
    """
    files = [f for f in listdir(_FEATURE_DIR) if isfile(join(_FEATURE_DIR, f))
             and filename + '.' in f]
    t = ()
    print filename
    for csv_name in files:
        with open(join(_FEATURE_DIR, csv_name), 'rb') as csv_file:
            """csv_reader = csv.reader(csv_file)
            hi = True
            for row in csv_reader:
                if hi:
                    print row
                hi = False
            t = t + (csv_reader.line_num,)"""  # using numpy now
            csv_data = numpy.genfromtxt(csv_file, comments='%', delimiter=',')
            t = t + (numpy.average(csv_data), numpy.var(csv_data))
    return t  # TODO: return a feature tuple thing

# Get features for all input samples
musicFiles = [f for f in listdir(_MUSIC_DIR) if '.mp3' in f]
allInput = []
for musicFile in musicFiles:
    features = read(musicFile)
    allInput.append(features)

print allInput  # TODO: delete

# Clustering

# TODO: output files to clustered directories
# for f in musicFiles:
#     copy(join(_MUSIC_DIR, f), './testOut/')
