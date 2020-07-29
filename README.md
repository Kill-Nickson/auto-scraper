# auto_scraper

#### Reason of creating:
Once I got a need to scrape data from a web-source and then store the data daily  while I will not get enough.

#### Project's modules:
 * **check_time** - helps to detect time between two timestamps, main part was borrowed and slightly editter (source: shorturl.at/jtFJP)
 * **init_config_vars** - opens a configuration file and initialize several required variables.
 * **collect_games_data** - its main purpose is to analyze the syntax of a web-source and return list of required data (contains only a template of how it might look).
 * **interact_database** - initializes table if it does not exist and updates it with newly collected data.
 * **main** - the module whose main function combines the functions of all other modules and implements an endless loop that collects new data at a specified time.


#### Quick start:

###### Edit configs/config.ini file

Edit config.ini file:
* days_delta: a day for collecting data (0 - today, 1 - yesterday, ...)
* project_dir: an absolute path to the project directory
* base_url: a link to a scraping web-source
```
[Variables]
days_delta = 1
project_dir = ***
base_url = https://******
```

###### Set up venv

Install the dependencies from requirements.txt

* cd to the directory where requirements.txt is located
* activate your venv
* run:
    ```
    pip install -r requirements.txt
    ```

###### Ways to run:
* Run main.py script and leave let it waork in the background;
* By using pyinstaller create an executable file and put it into a Startup folder of your OS, command to compile:
    ```
    pyinstaller -F -w main.py
    ```
