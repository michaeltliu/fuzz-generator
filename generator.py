import sys
from flask import Flask, request
from os import listdir
import random

app = Flask(__name__)
probs = dict()
probsInited = {0 : False}       # Janky fix, global state is not preserved if I just use a boolean

@app.route('/')
def returnFuzz():
    init = request.args.get("init", "")
    if not probsInited[0] and init != "false":
        directory = app.config['DIRECTORY']
        initProbabilities(directory)

    fuzz = ""

    file = open("out/fuzzOutput.txt", "w+", errors = "surrogateescape")

    print("Generating fuzz")

    d = dict(probs[""])
    d.pop("count")
    char = random.choices(list(d.keys()), weights = list(d.values()))
    if char[0] == "EOF":
        file.close()
        return fuzz
    fuzz += char[0]

    while True:
        d = dict(probs[fuzz[-1]])
        d.pop("count")
        char = random.choices(list(d.keys()), weights = list(d.values()))
        if char[0] == "EOF":
            file.write(fuzz)
            file.close()
            return fuzz
        fuzz += char[0]
        
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

    probsInited[0] = True

    return probs

@app.route('/live-update')
def liveUpdate():
    text = request.args.get("text", "")
    if len(text) == 0:
        return "Error: Training text is missing or has length 0"

    updateProbabilitiesWithString(text)
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

    for key in currProbs:
        # Normalizes weights to sum to 1
        m = currProbs[key]
        s = sum(m.values())
        for subkey in m:
            m[subkey] = m[subkey] / s
        
        # Adds currProbs into probs
        # Kind of a crap fest of code but this simplifies other areas
        temp = probs.get(key, dict())
        if len(temp) == 0:
            probs[key] = temp
        temp.update({"count" : temp.get("count", 0) + 1})
        for subkey in currProbs[key]:
            temp.update({subkey : (temp.get(subkey, 0) * (temp["count"] - 1) + currProbs[key][subkey]) \
                / temp["count"]})
        for subkey in temp:
            if subkey not in currProbs[key] and subkey != "count":
                temp.update({subkey : temp[subkey] * (temp["count"] - 1) / temp["count"]})

@app.route('/view-probs')
def viewProbs():
    return probs

if __name__ == '__main__':
    app.config['DIRECTORY'] = sys.argv[1]
    app.run()
