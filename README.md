# fuzz-generator
Generates fuzzing test inputs using a Markov chain model

## Dependencies:
- A virtual environment running Python 3 or above
- Flask and its default dependencies installed in the venv

## To run (Windows):
1. Get a virtual environment running with Flask installed
2. Run `export FLASK_APP=generator.py`
3. Run `python generator.py corpus` or `python generator.py mini_corpus`
4. Open/refresh the appropriate locally hosted port and the code will start running.

## URL routes:
- `'/'` routes to the main page which outputs the randomly generated fuzz (see note below about output). Running this page for the first time will also initialize the Markov chain using the corpus data. This should take less than a minute. Subsequent visits to this page should be instantaneous. 
	- You may optionally set the "init" parameter to "false" in order to prevent the Markov chain from initializing with corpus data. Only data from live updates would be used. 
	- `http://127.0.0.1:5000/?init=false`
- `'/live-update'` allows you to post a request to the server. You must specify a url query string with parameter "text" e.g. `http://127.0.0.1:5000/live-update?text=<TRAINING_BLOB>`
- `'/view-probs'` routes to a page containing all the probability information of the Markov chain formatted as a plain Python dictionary.

## Things to note:
- **IMPORTANT**: The output returned on the web app is almost always not what the true fuzz string really looks like. The string is technically printed, but various limitations with Unicode encoding in Chrome (coupled with my incompetence) make many characters invisible. As a workaround, the fuzz string is also piped to the text file `out\fuzzOutput.txt`. This file contains the accurate visualization of the fuzz.
	- If you plan on refreshing the main page a lot, it helps to use a text editor like VS Code or Atom that will automatically refresh `fuzzOutput.txt`.
- I've included a `mini-corpus`. You may find it easier to look at a smaller data set at first.
- Contributions to the training of the Markov chain are weighted equally by **file**. Regardless of how large/small a file is, its weight in the probability dictionary is the same as any other file. This was hairier to implement, but now, the resulting sample fuzz looks like an average file, not biased towards longer files.

## Known exceptions:
- Sometimes the main page `'\'` will throw a `UnicodeEncodeError`. This occurs when we run into foreign Unicode characters when piping our output to `out\fuzzOutput.txt`. These Unicode characters were properly **decoded** when reading the training data because much of the data included their encoding in their xml header. However, once they go into the Markov chain, I don't keep track of their encodings, so when one happens to get pulled out again, it looks like a completely foreign object. 
	- Quick note: I actually handle a good chunk of the weird Unicode characters by using "surrogateescape" error handling when file writing. Still, a small amount slip through.

## Mutational fuzzing thoughts:
I think the most basic way to mutate inputs is to make some small adjustment to the probabilities/Markov chain. Think of the Markov chain as a directed graph with weighted edges that represent the probability of going from one particular letter to another particular letter. I think the least effective thing you can do to introduce mutations is alter the weights on the edges. Instead, you should create new edges (succeed a character by another character it's never been succeeded by), or even better, create entirely new vertices (use a new character). For new characters, you could try using new Unicode characters or even flip a bit in the string's byte encoding. In general, creating these new branches in the Markov chain should occasionally result in new behavior -- something that has never happened before in all of the training data.

For the implementation, the main page could take in a parameter from a url query string that specifies if the user wants to mutate inputs. If so, the program could have a large predetermined set of unique characters, choose a few from there that are not already in the Markov chain, and connect them to a few other random characters.