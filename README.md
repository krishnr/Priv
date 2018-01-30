# Priv

## Chrome extension
Go to `chrome://extensions/`, click "Load Unpacked Extensions" and select directory that includes manifest.json file. In this case, it is the priv-extension directory.


## Server
In order to run the start script, you need both Python and Pip installed on your machines. All Macs come with Python pre-installed, visit [here](https://www.python.org/downloads/) for information on how to download Python onto your Linux or Windows machine.

To check if Python is installed, run `python --version`  
This should output something similar to: `python X.X.X`

To check if Pip is installed, run `which pip`  
If it is installed, it should show something similar to `path/to/your/python/version/bin/pip`

If Pip is not installed, visit [here](https://pip.pypa.io/en/stable/installing/)  
You can upgrade your pip installation by running `pip install -U pip`
 
To start server, simply run `./run.sh start`  
Use the `-h` or `--help` flags to view more information about the run script.