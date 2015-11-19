
import csv
from os import listdir
from os.path import isfile, join

_FEATURE_DIR = './features/'
_MUSIC_DIR = './musicFiles'


def read(filename):
    """
    Read all csv files for features associated with given filename.

    :param filename: String, name of file including '.mp3'
    :return: (object with) tuple representing features
    """
    files = [f for f in listdir(_FEATURE_DIR) if isfile(join(_FEATURE_DIR, f))
             and filename + '.' in f]
    for csv_name in files:
        with open(join(_FEATURE_DIR, csv_name), 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                pass
    return ()  # TODO: return a feature tuple thing

musicFiles = [f for f in listdir(_MUSIC_DIR) if '.mp3' in f]
allInput = []
for musicFile in musicFiles:
    features = read(musicFile)
    allInput.append(features)

print allInput  # TODO: delete
