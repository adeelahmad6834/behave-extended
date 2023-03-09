# Parabank Testing Demo

Parabank quality assurance project.

## System Requirements

* Google Chrome
* chromedriver
* python
* virtualenv
* Xvfb

# Setup on Linux

### Google Chrome 

Install [Google Chrome](https://www.google.com/chrome/?brand=BNSD&gclid=CjwKCAiAjoeRBhAJEiwAYY3nDOed3lgWIqimA14HiaulGKpTN1vjcF75XHdXn5_cfovcevt3-QU2yhoCsbsQAvD_BwE&gclsrc=aw.ds)

### chromedriver 
Setup [chromedriver](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/)

### Install virtualenv

```bash
sudo pip3 install virtualenv
```

### Install Xvfb

```bash
sudo apt-get update -y 
sudo apt-get install -y xvfb 
```

### Create virtual environment and install application dependencies

Open a terminal at the root of the project and run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
## Setting up the directory for test execution

1. Please make sure, your local `behave.ini` file is updated, everytime you take a pull from develop.

## Running a single test with behave

Open a terminal at the root of the project and run the following commands:

```bash
source venv/bin/activate
cd features
behave -n "THE NAME OR NUMBER OF SCENARIO TO TEST"
deactivate
```
In order to enable logging for behave command add `--no-logcapture` at the end of the behave command.

## Running all tests with behave

Open a terminal at the root of the project and run the following commands:

```bash
source venv/bin/activate
cd features
behave
deactivate
```

## Running implemented tests with behave

We have a tag `@not-implemented` in place for the feature files that are not implemented yet. 

Run this behave command to exclude all such features. 

```bash
behave --tags ~@not-implemented
```

# Important notes for developers:

Behave does not allow duplicate step implementations.

More specifically, Behave parser looks for matching step definitions in all the files within the folder `/features/steps` - ignoring how the steps files are named - and if it finds a duplicate step, it raises AmbiguousStep Error. 

As a pre-requisite to prevent this situation, please run the following command:

```
behave --dry-run
```

If an AmbiguousStep Error occurs against a given step, then please **carefully** resolve the conflict. As it might be confusing to find which implementation of the duplicate step to keep and which one to remove.

## Running all the tests with Behave and generating data for test reports with Allure.

Open a terminal at the root of the project and run the following commands:

```bash
source venv/bin/activate
cd features
behave -f allure_behave.formatter:AllureFormatter -o ../public
deactivate
```