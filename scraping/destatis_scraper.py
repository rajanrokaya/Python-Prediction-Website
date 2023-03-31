""""
A csv data scraper specific for sites from destatis (Statistisches Bundesamt)
Use this class to extract the table content from destatis statistics
A site must comply with:
    - The URL must begin with https://www.destatis.de/
    - Site must have at least one structured table with multiple entries
It's still not guaranteed that every site is scrapable with this tool
"""

import re
import sys

import os.path
import csv
import requests
from bs4 import BeautifulSoup

from requests import HTTPError


class DestatisScraper:
    """" A data scraper specific for sites from destatis """

    def __init__(self, url, soup=None, data=None):
        """ The initial constructor for the DestatisScraper class """
        # container for storing a beautifulsoup object
        self.__soup = soup
        # container for storing the csv data
        self.__data = [] if data is None else data
        self.__URL = url
        # extract the name of the html file
        self.__HTML_FILENAME = re.search(r"[a-zA-Z0-9-_]*.html", self.__URL).group()

    def __str__(self):
        return self.__data

    def request_site(self, url, save_path="./"):
        """
        Function for fetching and saving the html site to the local disk drive
        """
        print(f"Requesting the site from {self.__URL}")
        req = requests.get(url, timeout=2.50)
        try:
            req.raise_for_status()
        except HTTPError:
            print(f"Following Error occurred during requesting "
                  f"the site: {sys.exc_info()}")
            return None
        self.__soup = BeautifulSoup(req.content, 'html.parser')
        html = self.__soup.prettify("utf-8")
        with open(save_path + self.__HTML_FILENAME, "wb") as html_file:
            html_file.write(html)
        print(f"Saving the site as {self.__HTML_FILENAME}")
        return self.__soup

    def scrape_content(self, look_for_existing_file=True, path="./"):
        """
        Function for extracting the table content from the html site
        Returns a BeautifulSoup object
        """
        # If we already have the site saved, we just load there content
        if look_for_existing_file \
                and os.path.exists(path + self.__HTML_FILENAME):
            with open(self.__HTML_FILENAME, "rb") as html_file:
                self.__soup = BeautifulSoup(html_file, 'html.parser')
        # otherwise we load the html site from the server
        elif self.request_site(self.__URL) is None:
            return None
        # extracting all <tr>...</tr> elements from the first table to a list
        tables = self.__soup.select("div.c-toggle__entry > table")
        tr_list = tables[0].select("tbody > tr")
        # for each tablerow element we're extracting the data
        # and saving it in the self.__data
        for tbl_row in tr_list:
            row = []
            tbl_header = tbl_row.select("th")
            row.append(tbl_header[len(tbl_header) - 1].text.strip())
            for tbl_data in tbl_row.select("td"):
                row.append(tbl_data.text.strip().replace(",", ""))
            self.__data.append(row)
        return self.__data

    def filter_for_columns(self, keep):
        """
        filters for specific rows and returns a new DestatisScraper
        object for further processing.
        use it as follows:
            my_scraper.filter_for_columns([1,4,5])
        this will filter for the columns 1,4,5
        """
        # if no data was scraped or no argument was passed, we return self
        if (keep is None) or (not len(self.__data)):
            return self
        data = []
        # run through every tablerow and filter the corresponding columns
        for row in self.__data:
            new_row = []
            for column in keep:
                new_row.append(row[column])
            data.append(new_row)
        # make a copy with different data by creating a new instance
        return DestatisScraper(self.__URL, self.__soup, data)

    def convert_to_csv(self, filename, seperator=","):
        """
        Converts and saves the table content to a .csv file.
        You can optionally pass a filename as an argument and a
        different seperator
        """
        # if no data was scraped, we return nothing
        if not len(self.__data):
            return False
        if filename is None:
            filename = self.__HTML_FILENAME
        with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as file:
            csv_writer = csv.writer(file, delimiter=seperator)
            for row in self.__data:
                csv_writer.writerow(row)
        return True

    def get_data(self):
        """ getter function for the data """
        return self.__data

    def is_empty(self):
        """ method for checking if the scraper is empty """
        return self.__data == []
