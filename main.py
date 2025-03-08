import os

import pandas as pd

from data_analyzer import DataCleaner, DataAnalyzer, PronounCount
from data_scraping import DataScrapper


def main(input_file_url):
    input_df = None
    output_file_name = 'Output Data Structure.csv'          # output file path
    try:
        input_df = pd.read_csv(input_file_url)     # loading the input table dataframe
    except:
        print('Network error! Unable to load the input file.')
    else:
        print('Input file loaded successfully.')

    try:
        os.remove(output_file_name)               # delete the output file of previous run if exists
    except:
        print('Unable to delete old output file or file not present')
    else:
        print('Old output file cleared.')

    data_scrapper = DataScrapper()                # initializing the DataScrapper object
    data_cleaner = DataCleaner()                  # initializing the DataCleaner object
    data_analyzer = DataAnalyzer(data_cleaner)    # initializing the DataAnalyzer object
    for i in range(len(input_df)):                # Processing for each entry in input table
        url_id = None
        datarow = None
        try:
            # Performing the data scrapping using selenium
            url_id, text = data_scrapper.scrap(input_df.iloc[i, 0], input_df.iloc[i, 1])
            # data-row object that holds all the required data
            datarow = {'URL_ID': url_id, 'URL': input_df.iloc[i, 1]}
            # getting the cleaned tokenized words, word count, and avg word per sentence
            cleaned_words_text, word_count, words_per_sent = data_cleaner.RemoveStopwordsAndWordCount(text)
            # getting the pos, neg, polarity and subjectivity score
            ret_obj = data_analyzer.posneg_score(cleaned_words_text, word_count)
            datarow['POSITIVE SCORE'], datarow['NEGATIVE SCORE'] = ret_obj['POSITIVE SCORE'], ret_obj['NEGATIVE SCORE']
            datarow['POLARITY SCORE'], datarow['SUBJECTIVITY SCORE'] = (
                ret_obj['POLARITY SCORE'], ret_obj['SUBJECTIVITY SCORE'])
            datarow['AVG SENTENCE LENGTH'] = words_per_sent
            del ret_obj         # deleting the placeholder object
            # getting the complex word information and performing word level analysis
            ret_obj = data_analyzer.words_analysis(cleaned_words_text, word_count, words_per_sent)
            datarow['PERCENTAGE OF COMPLEX WORDS'] = ret_obj['PERCENTAGE OF COMPLEX WORDS']
            datarow['FOG INDEX'] = ret_obj['FOG INDEX']
            datarow['AVG NUMBER OF WORDS PER SENTENCE'] = words_per_sent
            datarow['COMPLEX WORD COUNT'] = ret_obj['COMPLEX WORD COUNT']
            datarow['WORD COUNT'] = word_count
            datarow['SYLLABLE PER WORD'] = ret_obj['SYLLABLE PER WORD']
            datarow['PERSONAL PRONOUNS'] = PronounCount(text)
            datarow['AVG WORD LENGTH'] = ret_obj['AVG WORD LENGTH']
            # creating DataFrame from the data-row dictionary
            output_row = pd.DataFrame([datarow])
            # saving the row to a local CSV file
            output_row.to_csv(output_file_name, index=False, header=not os.path.lexists(output_file_name), mode='a')

        except:
            print('Catastrophic error occurred! While processing for ', url_id)
        else:
            print(f'{url_id} processing complete')

    print('Program finished successfully.')   # To be executed at the end.
    print(f'Output is stored in {output_file_name} which can be found in project directory.')


if __name__ == '__main__':
    # The endpoint where the input data-table file is stored
    input_xlsx_url = ('https://docs.google.com/spreadsheets/d/1D7QkDHxUSKnQhR--q0BAwKMxQlUyoJTQ/export?format=csv&gid'
                      '=823090326')
    main(input_file_url=input_xlsx_url)
