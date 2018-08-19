# Zotero-Hypothesis Importer #

## Introduction ##

This program scans through a [Zotero](https://zotero.com) library and checks
each URL for [Hypothesis](https://hypothes.is) annotations. If annotations are
found it imports them into the Zotero library as note objects with their
associated tags.

## Installation ##

### Windows ###

Coming soon.

### Linux ###

At the command line, do the following:

Navigate to the directory where you'd like to install the program:

    cd /home/my_username/my_software_folder/

Git clone this repository:

    git clone https://github.com/JD-P/hypothesis-zotero

Change directory to the cloned repository:

    cd hypothesis-zotero

Create a virtual environment for the programs dependencies to go:

    virtualenv --python=python3 venv

Activate the virtualenvironment using the 'source' command:

    source venv/bin/activate

Use setuptools to install the program dependencies:

    python3 setup.py install

Run the program:

    python3 hypothesis_zotero.py

Then move on to the "Use" sections for instructions on how to use the program.

## Use & Operation ##

You need 4 pieces of information to run the program:

- The userID for your Zotero API usage, [available here](https://www.zotero.org/settings/keys).
- A developer API key for Zotero, [you can make one here](https://www.zotero.org/settings/keys/new).
- Your Hypothesis username, which should just be the username you use to access
the service.
- Your Hypothesis Developer API key, [available here](https://hypothes.is/account/developer).

Once you have these four things you put them into the appropriate slots in the
programs interface. You also need to specify how many items back in your personal
library the program should search through, the default is fifty but it's possible
to specify more. (Note: In version 0.1 this will actually crash the program, but
in future versions it shouldn't.)

After you've put all the information in, you should probably press 'save settings'
so that the transfer settings will be saved to a file for your next session. This
will save you time when you want to use the program again later.

Finally, press 'grab' and the transfer will begin. A progress indicator shows
how far along the program is in your document set. Once it's finished the progress
indicator will read 'done' and you can begin using your notes in Zotero.