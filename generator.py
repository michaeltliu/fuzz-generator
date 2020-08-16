import sys
from flask import Flask, request
from os import listdir
import random

app = Flask(__name__)
probs = dict()
probsInited = False

@app.route('/')
def returnFuzz():
    if not probsInited:
        directory = app.config['DIRECTORY']
        initProbabilities(directory)

    fuzz = ""

    return probs
        
# For every unique character to appear in the corpus (specified by param "directory"), 
# this returns a map of any character that has succeeded it along with its probability
# Return type: Map<String, Map<String, Float>>
def initProbabilities(directory):

    for f in listdir(directory):
        print(f)

        file = open(directory + "/" + f, errors = "replace")
        line = file.readline()

        # Reopens the file with the correct encoding if one is given
        # Otherwise, default encoding is used and characters that cause errors are replaced
        encodingIndex = line.find("encoding")
        if encodingIndex != -1:
            encoding = line[encodingIndex + 10 : line.find("\"", encodingIndex + 10)]
            file.close()
            file = open(directory + "/" + f, encoding = encoding, errors = "surrogateescape")
        else:
            file.close()
            file = open(directory + "/" + f, errors = "replace")

        s = file.read().replace("    ", "\t")

        if len(s) == 0:
            continue

        updateProbabilitiesWithString(s)

    # Normalizes
    for key in probs:
        m = probs[key]
        count = m["count"]
        for subkey in m:
            m[subkey] = m[subkey] / count
    
    probsInited = True

    return probs

@app.route('/live-update')
def liveUpdate():

    text = request.args.get("text")
    if len(text) == 0:
        return "Error: Training text has length 0"

    updateProbabilitiesWithString(text)
    # TODO: Renormalize probabilities after udpate
    return "Your training text has been successfully added. Return to the home page to view a new sample fuzz."

def updateProbabilitiesWithString(s):
                                # Probabilities for the current file only
    currProbs = dict()          # To be added to "probs"

    # Frequencies for the first character of the file
    temp = currProbs.get('', dict())
    if len(temp) == 0:
        currProbs[''] = temp
    temp.update({s[0] : temp.get(s[0], 0) + 1})

    for i in range(0, len(s) - 1):
        temp = currProbs.get(s[i], dict())
        if len(temp) == 0:
            currProbs[s[i]] = temp
        temp.update({s[i+1] : temp.get(s[i+1], 0) + 1})

    # Assigns a probability to the file ending
    temp = currProbs.get(s[-1], dict())
    if len(temp) == 0:
        currProbs[s[-1]] = temp
    temp.update({"EOF" : temp.get("EOF", 0) + 1})

    # Normalizes weights to sum to 1
    for key in currProbs:
        m = currProbs[key]
        s = sum(m.values())
        for subkey in m:
            m[subkey] = m[subkey] / s
        
        # Adds currProbs into probs
        temp = probs.get(key, dict())
        if len(temp) == 0:
            probs[key] = temp
        for subkey in currProbs[key]:
            temp.update({subkey : temp.get(subkey, 0) + currProbs[key][subkey]})
        temp.update({"count" : temp.get("count", 0) + 1})

if __name__ == '__main__':
    app.config['DIRECTORY'] = sys.argv[1]
    app.run()
