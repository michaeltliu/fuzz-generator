# fuzz-generator
Generates fuzzing test inputs using a Markov chain model

## Dependencies:
- A virtual environment running Python 3 or above
- Flask and its default dependencies installed in the venv

## To run (Windows):
1. Get a virtual environment running with Flask installed
2. Run `export FLASK_APP=generator.py`
3. Run `python generator.py corpus`
4. Open/refresh the appropriate locally hosted port and the code will start running.

## Things to note:
- Contributions to training the Markov chain are weighted equally by **file**. Regardless of how large/small a file is, its weight in the probability dictionary is the same as any other file. This is so the resulting sample fuzz looks like an average file, not biased towards longer files.
- Opening the main page for the first time will take a while. The program has to parse through 1500 files! However, subsequent visits to the page should be much quicker.
- Send POST requests with url query strings e.g. `http://127.0.0.1:5000/live-update/<TEXT BLOB>`