import logging
from os.path import exists
from time import sleep, strftime

from check_time import is_time_between
from init_config_variables import vars_init
from collect_games_data import matches_parse, check_internet_connection
from interact_database import table_init, table_update


def main():
    logging.basicConfig(filename='D:\\Pets\\parser_with_timer\\logs\\main.log', level=logging.INFO, filemode='a')

    while True:
        if is_time_between([5, 00], [6, 00]) and check_internet_connection():
            logging.info(strftime('%Y-%m-%d %H:%M:%S') + ' - Started collecting')

            if exists('D:/Pets/parser_with_timer/configs/config.ini'):

                # Initialise main variables
                project_dir, date_for_parsing, formatted_date_for_parsing = \
                    vars_init(path=r'D:\Pets\parser_with_timer\configs\config.ini')

                # Parse new matches data
                matches = matches_parse(date_for_parsing)
                logging.info(strftime('%Y-%m-%d %H:%M:%S') + ' - Collected new matches')

                if not exists(project_dir + '/databases/' + formatted_date_for_parsing + '.db'):

                    # Initialise a matches table if not exists
                    table_init(project_dir, formatted_date_for_parsing)

                    # Update matches table with the matches
                    table_update(project_dir, formatted_date_for_parsing, matches)
                    logging.info(strftime('%Y-%m-%d %H:%M:%S') + ' - Updated a matches table')

            logging.info(strftime('%Y-%m-%d %H:%M:%S') + ' - Took a break')
            
            # Break for 20 hours
            sleep(72000)
        else:
            # Break for 5 minutes
            sleep(300)


if __name__ == '__main__':
    main()
