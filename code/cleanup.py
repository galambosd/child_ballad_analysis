import re
from sys import argv
import pprint
import pandas as pd

pp = pprint.PrettyPrinter(indent=4)

class ChildBallad(object):
    """docstring for ballad."""

    def __init__(self, number, variation, text, refrain,
                 date = None, origin = None):
        super(ChildBallad, self).__init__()
        self.number = number
        self.variation = variation
        self.reg_text = text
        self.refrain = refrain
        self.date = date
        self.origin = origin


def extractBallad(input, join_lines = True):
    '''
    Extract all ballad titles and ballad contents from the input file
    '''
    title_re = re.compile(r'Child\s(\d+)(\w)')
    refrain_lines_re = re.compile(r'##([^#]+)')
    reg_lines_re = re.compile(r'#([^#]+)\s')
    ballad_re = re.compile(r'@([^@]+)')
    outputList = []
    ballads = ballad_re.findall(input)
    for ballad in ballads:
        title = title_re.findall(ballad)[0]
        text = reg_lines_re.findall(ballad)
        refrain = refrain_lines_re.findall(ballad)
        if join_lines:
            text = str(''.join(text))
            refrain = str(''.join(refrain))
        new_ballad = ChildBallad(title[0], title[1],
                            text, refrain)
        outputList.append(new_ballad)

    return outputList

def cleanChars(input):
    '''
    Handle weird characters for escapes+corrections, etc
    '''
    # get rid of slashes, brackets, pluses
    slash_revision_re = re.compile(r'[\*\+\[\]\\]')
    clean = slash_revision_re.sub('', input)
    # reformat LBALLAD to @
    ballad_start_re = re.compile('LBALLADS ')
    clean = ballad_start_re.sub('@', clean)
    # reformat non-refrain lines to begin with #
    reg_line_start_re = re.compile(r'N\d\s')
    clean = reg_line_start_re.sub('#', clean)
    # reformat refrain lines to begin with ##
    refrain_line_start_re = re.compile(r'#([^#]+)\s*SBALLADS Child \d+\w\.\d+r',
                                       re.DOTALL)
    clean = refrain_line_start_re.sub(r'##\1', clean)
    # delete SBALLAD... suffix on all lines
    line_end_re = re.compile(r'SBALLADS\sChild\s\d+\w\.\d+')
    clean = line_end_re.sub('', clean)
    # Replace all newlines with spaces
    new_lines_re = re.compile(r'\n', re.DOTALL)
    clean = new_lines_re.sub(r' ', clean)
    return clean

def writeOutput(ballads, output_name = 'extracted_ballads.xlsx'):
    '''
    Write a list of ballad objects to an excel file that we can edit later
    '''
    num_list =[]
    var_list = []
    text_list = []
    for ballad in ballads:
        num = ballad.number
        var = ballad.variation
        text_and_refrain = str(ballad.reg_text) + '\n' + str(ballad.refrain)
        num_list.append(num)
        var_list.append(var)
        text_list.append(text_and_refrain)
    df = pd.DataFrame(
        {'num': num_list,
         'var': var_list,
         'text_refrain': text_list}
        )
    return df

def testExtraction(test):
    '''
    Print the extraction to see how it looks
    '''
    cleaned = cleanChars(test)
    ballads = extractBallad(cleaned, join_lines=False)
    for new in ballads:
        print(new.number, new.variation)
        pp.pprint(new.reg_text)
        print(new.refrain)
        print('-'*50)

def test_cleanup():
    file_name = argv[1]
    file = open(file_name)
    ballad_file = file.read()
    file.close()
    cleaned_ballad = cleanChars(ballad_file)
    extracted_ballads = extractBallad(cleaned_ballad)
    writeOutput(extracted_ballads)

if __name__ == '__main__':
    test_cleanup()
