
import csv
from os import listdir
from os.path import isfile, join

_FEATURE_DIR = './features/'

def read(filename):
    csv_files = [f for f in listdir(_FEATURE_DIR)
                 if isfile(join(_FEATURE_DIR, f))
                 and filename + '.' in f]
    for csv_name in csv_files:
        with open(csv_name, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                pass
