'''pubmed_journals_by_year.py




'''

__title__ = 'pubmed_journals_by_year.py'
__version__ = '1.0.0'
__author__ = 'Toby C. Cornish, MD, PhD'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2020'

import os
import sys
import csv
from collections import defaultdict
from configparser import ConfigParser

from Bio import Entrez
from Bio import Medline

input_file_path = os.path.abspath(r'pmid_results.csv')
journal_output_file_path = os.path.abspath(r'journal_counts.csv') 

start_year = 1913
end_year = 2021

def main():
    '''Main function'''
    # read our config file
    config = read_config_file('config.ini')
    if not config['use_api_key']:
        config['api_key'] = None
    print(config)
    
    # Read the journals to search from the input file
    journals = read_file(input_file_path)

    # Read the journals we have finsihed with from the output file
    finished = read_progress_from_file(journal_output_file_path)

    # remove the finished files from the journals list 
    journals = [j for j in journals if j not in finished]

    print('='*40)
    for journal in journals:
        print(f'{journal}')
        result = []
        for year in range(start_year,end_year+1):
            search_string = f'''"{journal}" [Journal] AND "{year}"[PPDAT]'''
            print(f'  {year} : {search_string}')
            count = search(search_string,config['email'],config['api_key']).get('count')
            print(f'    Found {count} publications.')
            result.append(count)
        write_journal_result(journal,result)
 
def search(query, email, api_key=None):
    '''Use Entrez.esearch to identify all publications in a journal'''

    Entrez.email = email
    if api_key:
        Entrez.api_key = api_key

    # see https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch for information on parameters
    # of note: To retrieve more than 100,000 UIDs, submit multiple esearch requests while incrementing the value of retstart
    print("  Retrieving PMIDs ...")
    query_result = {
        'term' : query,
        'pmids' : [],
        'query_translation' : None,
        'quoted_phrase_found' : False,
        'count' : 0
    }
    pmids = []
    retstart = 0
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='100000',
                            retstart=retstart,
                            retmode='xml',
                            term=query
    )
    results = Entrez.read(handle)

    # populate part of the query_result
    query_result['query_translation'] = results['QueryTranslation']
    query_result['count'] = int(results['Count'])

    # if the quoted phrase isn't found we get whacko results
    if quoted_phrase_found(results):
        pmids.extend(results['IdList'])
        query_result['quoted_phrase_found'] = True
    else:
        query_result['quoted_phrase_found'] = False
        print("    The quoted phrase wasn't found (0 results).")

    print("    Done.")
    query_result['pmids'] = pmids
    return query_result

def quoted_phrase_found(results):
    '''If the quoted phrase was found return True'''
    if 'WarningList' in results:
        if 'QuotedPhraseNotFound' in results['WarningList']:
            return False
        else:
            return True
    else:
        return True

def read_file(file_path):
    '''Read the input file and return a list of unique journals, sorted''' 
    with open(file_path,'r') as f:
        reader = csv.DictReader(f)
        return sorted(list(set([row['TA'] for row in reader if row['TA'] != ''])))

def read_progress_from_file(file_path):
    '''Read the output file and return a list of journals that are done''' 
    with open(file_path,'r') as f:
        reader = csv.DictReader(f)
        return [row['journal'] for row in reader] 

def write_journal_result(journal,result):
    '''Append our results to the output file'''
    file_exists = os.path.isfile(journal_output_file_path) # if it doesn't exist, we are creating it and need to write a header

    fieldnames = ['journal',]
    fieldnames.extend(list(range(start_year,end_year+1)))

    with open(journal_output_file_path,'a', newline='') as f: # mode is 'append'
        csv_writer = csv.writer(f, dialect='excel')

        if not file_exists:
            csv_writer.writerow(fieldnames)

        data = [journal,]
        data.extend(result)
        csv_writer.writerow(data)

def delete_if_exists(file_path):
    '''Delete the file if it exists'''
    if os.path.exists(file_path):
        os.remove(file_path)

def read_config_file(config_file_path):
    '''Read the INI style configuration file into a dict'''
    config = {}
    parser = ConfigParser()
    parser.read(config_file_path)

    try:
        # read Entrez section
        config['email'] = parser.get('Entrez', 'email')
        config['api_key'] = parser.get('Entrez', 'api_key')
        config['use_api_key'] = parser.getboolean('Entrez', 'use_api_key')
    except Exception as e:
        print("An error occurred reading the config file.")
        print("  error: %s" % e)  
        sys.exit()

    return config

if __name__ == '__main__':
    main()