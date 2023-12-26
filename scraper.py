import requests
from bs4 import BeautifulSoup
import pandas as pd


EXCEL_FILE_PATH = 'uralic_dict.xlsx' 
MAX_RETRY = 5

uralic_dict = pd.DataFrame()
for idx, page_no in enumerate(range(1, 1899, 20)):
    print(f'Scrapping page: {idx+1}...')

    dict_entries = []
    i = 0
    while not dict_entries and i < MAX_RETRY:
        if i: print(f'Retrying page: {idx+1}')

        url = f'https://starlingdb.org/cgi-bin/response.cgi?root=config&morpho=0&basename=\\data\\uralic\\uralet&first={page_no}'

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        dict_entries = soup.find_all('div', class_='results_record')
        i += 1

    for _idx, entry in enumerate(dict_entries):
        word = entry.find('span', string='Proto:').find_next_sibling('span').get_text()
        word = word.strip()
        eng_meaning_span = entry.find('span', string='English meaning:')
        if eng_meaning_span:
            eng_meaning = eng_meaning_span.find_next_sibling('span').get_text()
            eng_meaning = eng_meaning.strip()
        else:
            eng_meaning = None

        df_entry = pd.DataFrame({
            'Word': [word],
            'English Meaning': [eng_meaning]
        }, index=[page_no+_idx])
        uralic_dict = pd.concat([uralic_dict, df_entry])
    
    uralic_dict.to_excel(EXCEL_FILE_PATH)

print('Done')