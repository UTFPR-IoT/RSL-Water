import os

from math import isnan
from sys import argv, exit

import pandas as pd

class BibEntry(object):
    def __init__(self):
        self.Item_Title = None
        self.Publication_Title = None
        self.Book_Series_Title = None
        self.Journal_Volume = None
        self.Journal_Issue = None
        self.Item_DOI = None
        self.Authors = None
        self.Publication_Year = None
        self.URL = None
        self.Content_Type = None
        self.Abstract = None

    def generate_bib(self, header_id: str) -> str:
        """
        Based on its members, returns
        a string in .bib format entry
        """
        header = "@article{"+header_id+",\n\t" 
        author = "author = {"+self.Authors+"},\n\t"#Authors
        title = "title = {"+self.Item_Title+"},\n\t"  #Item Title
        journal_book = "journal = {"+self.Publication_Title+"},\n\t" #Publication Title
        volume = "volume = {"+str(self.Journal_Volume)+"},\n\t" #Journal Volume
        number = "number = {"+str(self.Journal_Issue)+"},\n\t" #Journal Issue
        year = "year = {"+str(self.Publication_Year)+"},\n\t" #Publication Year
        content_type = "type = {"+str(self.Content_Type)+"},\n\t" #Content Type
        url = "url = {"+str(self.URL)+"},\n\t" #URL
        abstract = "abstract = {"+str(self.Abstract)+"},\n\t" #URL
        doi = "doi = {"+str(self.Item_DOI)+"}\n}\n\n" #Item DOI
        return header+author+title+journal_book+volume+number+year+content_type+url+abstract+doi





def _get_bibentries(filepath: str) -> list:
    if os.path.exists(filepath):
        bibentries = []
        springer_csv = pd.read_csv(filepath)
        springer_csv.fillna('', inplace=True)
        for index, row in springer_csv.iterrows():
            bibentry = BibEntry()
            bibentry.Authors = row['Authors']
            bibentry.Book_Series_Title = row['Book Series Title']
            bibentry.Content_Type = row['Content Type']
            bibentry.Item_DOI = row['Item DOI']
            bibentry.Item_Title = row['Item Title']
            bibentry.Journal_Issue = row['Journal Issue']
            bibentry.Journal_Volume = row['Journal Volume']
            bibentry.Publication_Title = row['Publication Title']
            bibentry.Publication_Year = row['Publication Year']
            bibentry.Abstract = row['Abstract']
            bibentry.URL = row['URL']
            bibentries.append(bibentry.generate_bib(str(index)))
        return bibentries
    else:
        print("{0} not found!".format(filepath))
        return []


def convert_csv2bib(filepath: str) -> bool:
    """
    It converts a .csv in SpringerLink format
    to a valid .bib with the same name, just 
    changing extension.

    ATTENTION: if a .bib file with the same name aready exists,
    it will be appended!

    :param filepath: a path to a .csv file
    :return: True if .bib file was created, False otherwise.
    """
    bibentries = _get_bibentries(filepath)
    bibfile = filepath.split(".")[0] + ".bib"
    for bib in bibentries:
        with open(bibfile, 'a', encoding="utf-8") as f:
            f.write(bib)


if __name__ == "__main__":
    try:
        filepath = argv[1]
    except:
        print("Usage: python springer_csv2bib <filepath.csv>")
        exit(0)
    convert_csv2bib(filepath=argv[1])
