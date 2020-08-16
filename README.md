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

## URL routes:
- '/' routes to the main page which outputs the randomly generated fuzz (see note below about the output). Running this page for the first time will also initialize the Markov chain using the corpus data. This should take less than a minute. Subsequent visits to this page should be instantaneous. 
	- You may optionally set the "init" parameter to "false" in order to prevent the Markov chain from initializing with corpus data. So, only data from live updates would be used. 
- '/live-update' allows you to post a request to the server. You must specify a url query string with parameter "text" e.g. `http://127.0.0.1:5000/live-update?text=<TRAINING_BLOB>`
- '/view-probs' routes to a page containing all the probability information of the Markov chain formatted as a plain Python dictionary.

## Things to note:
- **IMPORTANT**: The output returned on the web app is almost always not what the true fuzz string really looks like. The string is technically printed, but various limitations with Unicode encoding in Chrome (coupled with my incompetence) make many characters invisible. However, the fuzz string is also piped to the text file `out\fuzzOutput.txt`. This file contains the accurate visualization of the fuzz.
	- If you plan on refreshing the main page a lot, it helps to use a text editor like VS Code or Atom that will automatically `fuzzOutput.txt`.
- Contributions to the training of the Markov chain are weighted equally by **file**. Regardless of how large/small a file is, its weight in the probability dictionary is the same as any other file. This was more difficult to implement, but now, the resulting sample fuzz looks like an average file, not biased towards longer files.

## Known exceptions:
- Sometimes the main page `'\'` will throw a `UnicodeEncodeError`. This occurs when we run into foreign Unicode characters when piping our output to `out\fuzzOutput.txt`. These Unicode characters were properly **decoded** when reading the training data, because much of the data included their encoding in their xml header. However, once they go into the Markov chain, I don't keep track of their encodings, so when one happens to get pulled out again, it looks like a completely foreign object. 
	- Quick note: I actually handle a good chunk of the weird Unicode characters by using "surrogateescape" error handling when file writing. Still, a small amount slip through.