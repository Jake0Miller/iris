# Iris Webscraper for Sephora

## About

A short script to scrape product info from the popular makeup retailer Sephora.

## Setup

Written using Python 3.10.9 on MacOS 13.4

Data is stored in a PostgreSQL database. If not yet installed, run:

`brew install postgresql`

To start your PostgreSQL server, run:

`brew services start postgresql@14`

Create our database:
```
psql -d postgres
CREATE DATABASE iris;
```

Next we will set up our Python environment:
```
brew install pyenv-virtualenv
pyenv install 3.11.2
pyenv virtualenv 3.11.2 iris
pyenv local iris
```

Run `pyenv init` if necessary to debug a new install

To install all necessary libraries, run:

`pip install -r requirements.txt`

Lastly, make sure to update the `username` variable in `/scripts/webscraper.py` to your MacOS login.

## Usage

To run the script, simply run:

`python scripts/webscraper.py`

To check on the status of the `Products` table, run:

```
psql -d iris
SELECT COUNT(*) FROM products;
SELECT * FROM products;
```
