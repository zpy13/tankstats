# Project_tankstats
tankstats is a Flask application for retriveing tank stats from mulitiple pages related with WOT.
## Request package
  selenium, beautifulsoup, flask, sqlite3, request
### Install selenium webdriver
Check [url](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) to download webdriver for your browser.
## Usage
create cache file for tanks data by
```python
$ cache.py
```
create corresponding database by
```python
$ createdb.py
```
calculate number of parameters retrieved by
```python
$ params_cal.py
```
run flask application by
```python
$ app.py
```
your flask app should run at
```python
http://127.0.0.1:5000/
```
