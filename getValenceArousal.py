import csv
import sys
import os
import logging
import setupLogging
from functools import reduce

logger1 = logging.getLogger('getValenceArousal')
#(tag, valence, arousal)
def findValArForTag(tag, values):
    return next(((val[1], val[2], val[5]) for val in values if val[1] == tag), (tag, 'n/a', 'n/a'))

#load tags
with open("uniqueFilteredTags.csv", 'r') as ut: 
    uniqueTags = ut.read().splitlines()
logger1.info("Currently found " + str(len(uniqueTags)) + " unique tags")

#load valuesList
with open("ArousalValenceCalculations.csv", 'r') as ut: 
    reader = csv.reader(ut, delimiter=';')
    next(reader, None)
    valuesList = [x for x in reader]
logger1.info("Currently found " + str(len(valuesList)) + " values")

tagsWithValAr = [findValArForTag(tag, valuesList) for tag in uniqueTags]

numberOfFoundValues = len([x for x in tagsWithValAr if x[1] != 'n/a'])
logger1.info("Values found for " + str(numberOfFoundValues) + " out of " + str(len(tagsWithValAr)) + " tags")

with open('valenceArousal.csv', 'w') as vAr:
    vAr.write("Tag; Valence; Arousal\n")
    for item in tagsWithValAr:
        vAr.write("{0};{1};{2}\n".format(item[0], item[1], item[2]))