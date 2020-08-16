# fuzz-generator
Generates fuzzing test inputs using a Markov chain model

## Dependencies:
Install Flask and its default dependencies
Make sure you are running Python 3 and above

## To run (Windows):
`venv\Scripts\activate`
`export FLASK_APP=generator.py`
`python generator.py ../corpus`

Open/refresh the appropriate locally hosted port and the code will start running.

## Things to note:
- Contributions to training the Markov chain are weighted equally by **file**. Regardless of how large/small a file is, its weight in the probability dictionary is the same as any other file. This is so the resulting sample fuzz looks like an average file, not biased towards longer files.
- Opening the main page for the first time will take a while. The program has to parse through 1500 files! However, subsequent visits to the page should be much quicker.
- Send POST requests with url query strings e.g. http://127.0.0.1:5000/live-update/<TEXT BLOB>