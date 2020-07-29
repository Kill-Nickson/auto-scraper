import logging
from time import strftime
from datetime import date, timedelta

from configparser import ConfigParser, NoSectionError, NoOptionError


def vars_init(path):
    config = ConfigParser()
    config.read(path)
    try:
        project_dir = config.get('Variables', 'project_dir')
        days_delta = config.get('Variables', 'days_delta')

        date_for_parsing = (date.today() - timedelta(days=int(days_delta)))
        formatted_yesterday = date_for_parsing.strftime("%d_%m_%Y")

        return project_dir,  date_for_parsing, formatted_yesterday
    except (NoSectionError, NoOptionError):
        logging.getLogger(__name__)
        logging.error(strftime('%Y-%m-%d %H:%M:%S') + ' - Occurred an error with a config file')
        exit()
