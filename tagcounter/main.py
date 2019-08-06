### main program

import argparse
import pkg_resources
from tagcounter.udf import init_logging, read_sites_synonyms_from_yaml, run_console, run_ui
from tagcounter.db import init_db_session

def run():
    ## parse args provided in command line
    ap = argparse.ArgumentParser(prog='tagcounter', description='Count html tags in a web page.')
    ap.add_argument("--get", required=False,
                    help="Program will get html tags for the web page specified by this parameter.")
    ap.add_argument("--view", required=False,
                    help="Program will show from database the html tags for the web page specified by this parameter.")
    # argv = ['--get', 'ggl']
    # args = vars(ap.parse_args(argv))
    args = vars(ap.parse_args())
    # print(args)

    ## app 'hard-coded' params
    file_dict_synoms = pkg_resources.resource_filename(__name__, 'data/dictionary_websites.yml')
    file_logs = pkg_resources.resource_filename(__name__, 'data/logs.log')
    file_db_sqlite = pkg_resources.resource_filename(__name__, 'data/tagcounts_sqlite.db')

    #file_dict_synoms = 'data/dictionary_websites.yml'
    #file_logs = 'data/logs.log'
    #file_db_sqlite = 'data/tagcounts_sqlite.db'

    init_logging(file_logs)
    db_session = init_db_session(file_db_sqlite)
    dict_sites = read_sites_synonyms_from_yaml(file_dict_synoms)

    if args['get'] or args['view']:
        run_console(args, dict_sites, db_session)
    else:
        run_ui(db_session)

# run()
