"""
program for creating the csv files for the deep learning part
"""

import csv
from scraping.destatis_scraper import DestatisScraper

URL = "https://www.destatis.de/EN/Themes/Economy/Foreign-Trade/Tables/lrahl01.html#242374"
scraper = DestatisScraper(URL)
scraper.scrape_content()
scraper.filter_for_columns([0, 1, 2]).convert_to_csv("exports-imports")

# prepare the imports data for the deep learning
imports = scraper.filter_for_columns([0, 2]).get_data()
# reversing the rows, because we want the rows in ascending order
imports.reverse()
imports_table = []
for imports_row in enumerate(imports):
    index = imports_row[0]
    # If we arrived to the last 4 rows, we know we have all the data we need
    if index >= len(imports) - 5:
        break
    row = [imports[index][1], imports[index + 1][1], imports[index + 2][1], imports[index + 3][1],
           imports[index + 4][1]]
    imports_table.append(row)
with open("imports.csv", "w", newline="", encoding="utf-8") as imports_file:
    csv_writer = csv.writer(imports_file)
    csv_writer.writerows(imports_table)

# prepare the exports data for the deep learning
exports = scraper.filter_for_columns([0, 1]).get_data()
# reversing the rows, because we want the rows in ascending order
exports.reverse()
exports_table = []
for export_row in enumerate(exports):
    index = export_row[0]
    # Same goes here. If we arrived to the last 4 rows, we know we have all the data we need
    if index >= len(exports) - 5:
        break
    row = [exports[index][1], exports[index + 1][1], exports[index + 2][1], exports[index + 3][1],
           exports[index + 4][1]]
    exports_table.append(row)
with open("exports.csv", "w", newline="", encoding="utf-8") as exports_file:
    csv_writer = csv.writer(exports_file)
    csv_writer.writerows(exports_table)
