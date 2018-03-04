# Priv

## Chrome extension
Go to `chrome://extensions/`, click "Load Unpacked Extensions" and select directory that includes manifest.json file. In this case, it is the priv-extension directory.


## Deployment

To locally deploy the Chrome extension, you need Docker installed on your machine.

To check if you have Docker, run `docker --version`
This should output something similar to: `Docker version 17.12.0-ce, build c97c6d6`

Visit [here](https://store.docker.com/search?type=edition&offering=community) for instructions on how to install docker

Change the xhr request in `client/popup.js` from the `amazonaws.com` domain to `localhost:80/`


Once you have Docker installed, simply run `bash start.sh`

