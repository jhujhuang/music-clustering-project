from yaafelib import FeaturePlan


fp = FeaturePlan(44100)
fp.loadFeaturePlan('featureplan')  # Seems like not working, might just use command line

""" Note for using yaafe command line tool:

cd musicFiles
yaafe -r 44100 -c ../featureplan *.mp3 -b ../features/
"""