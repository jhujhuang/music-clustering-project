# music-clustering-project
project for cs475 machine learning

## How to run
With music features already extracted, just run `clustering.py`.

Set directory constants in`clustering.py` to run on different data.



Otherwise, to get feature files (with Yaafe installed, and enviroment vars set):
- `cd musicFiles`
- `yaafe -r 44100 -c ../featureplan *.mp3 -b ../features/`

Or, with small set of data available in this github repository:
- `cd musicFiles/small`
- `yaafe -r 44100 -c ../../featureplan *.mp3 -b ../../features/small`
Remove existing feature files before getting new feature files.
