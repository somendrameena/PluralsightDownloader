# Pluralsight Scraper

Allows you to fetch & download the courses on PluralSight - MUST HAVE AN ACCOUNT IN ORDER TO DOWNLOAD

## Setup

1. Clone the repository

```
  git clone https://github.com/somendrameena/PluralsightDownloader.git
```

## Installation

1. Install Python

2. Install pip

3. Install packages from requirements.txt

```
  pip install -r requirements.txt
```

## Configure the tool

1. Edit config.py and add the following:
```python
    username = "Your PluralSight Email/Username"
    password = "Your PluralSight Password"
    link = "COURSE URL" 
    # Eg. https://app.pluralsight.com/library/courses/django-fundamentals-update/table-of-contents
```

## Run the script

```
  python launch.py
```
