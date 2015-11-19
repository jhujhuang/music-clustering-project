
import csv
from os import listdir
from os.path import isfile, join

_FEATURE_DIR = './features/'


def read(filename):
    """
    Read all csv files for features associated with given filename.

    :param filename: String, name of file including '.mp3'
    :return: (object with) tuple representing features
    """
    files = [f for f in listdir(_FEATURE_DIR) if isfile(join(_FEATURE_DIR, f))
             and filename + '.' in f]
    for csv_name in files:
        with open(csv_name, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                pass

read('mozartG.mp3')
