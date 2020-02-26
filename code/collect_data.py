import re
from sys import argv
import pprint as pp
import pandas as pd
from cleanup import *
from extract_metadata import *

def main():
    # extract all the ballads and stuff them into a dataframe
    ballad_text_file = open(argv[1])
    ballad_text = ballad_text_file.read()
    ballad_text_file.close()
    cleaned_ballad_text = cleanChars(ballad_text)
    extracted_ballads = extractBallad(cleaned_ballad_text)
    ballad_df = writeOutput(extracted_ballads)

    # extract all the metadata
    ballad_metadata_file = open(argv[2])
    ballad_metadata = ballad_metadata_file.read()
    ballad_metadata_file.close()
    search_term = r'\[Child (\d+)\]'
    dates, origins = extractMetadata(ballad_metadata, search_term)
    # add it to our dataframe
    ballad_df['date'] = ballad_df['num'].map(dates)
    ballad_df['origin'] = ballad_df['num'].map(origins)


    # save the dataframe a jsonlist
    # where each row is dictionary of column: value
    
    ballad_df.to_json('ballads.jsonl', orient='records')
    # pp.pprint(json_list[:500])
    # outfile = open('ballads.jsonl', 'w')
    # for entry in json_list:
    #     outfile.write(entry+'\n')
    # outfile.close()

if __name__ == '__main__':
    main()
