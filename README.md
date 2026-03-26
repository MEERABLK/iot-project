# Smart Store IOT Project
Final Project for IOT

## venv setup
### Create venv
```
python -m venv .venv
```

### Activate venv
#### Windows
```
.venv\Scripts\activate
```
#### RaspberryPi
```
source .venv/bin/activate
```

#### If that didn't work, try running `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first

### Install packages
#### General requirements
```
pip install -r requirements.txt
```
#### RaspberryPi
If on RaspberryPi, also install
```
pip install -r requirements-rpi.txt
```

### Check your packages
Run
```
pip list
```
And verify you have required packages.

### Deactivate venv
To exit venv, run
```
deactivate
```
