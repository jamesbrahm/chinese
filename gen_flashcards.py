import unicodedata
import csv
import collections
import re


def get_hsk_data():
    hsk_data = []
    with open('data/hsk.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')
        for row in csvreader:
            row['Character'] = row['Character'].replace("（", "(")
            row['Character'] = row['Character'].replace("）", ")")
            row['Character'] = row['Character'].replace("、", ",")
            #row['Pinyin'] = row['Pinyin'].replace("\xa0", "")
            row['Pinyin'] = row['Pinyin'].replace("（", "(").replace("）",")")
            #row['Ascii'] = strip_accents(row['Pinyin'])
            row['HSK Set'] = int(row['HSK Set'])
            #row['TTL'] = TTL
            if row['HSK Set'] >2 and row['HSK Set'] <5:
                hsk_data.append(row)
    return hsk_data

hsk_data = get_hsk_data()

# Number of cards per page
cards_per_page = 10

# Generate HTML pages with flashcards
def generate_flashcard_pages(vocab_list, cards_per_page):
    # Initialize the HTML content
    html_content = """<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Chinese Vocabulary Flashcards</title><style>
        .page {
            width: 8.5in; /* Standard US letter size */
            height: 11in;
            margin: 0;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            page-break-after: always;
        }
        .card {
            border: 1.5px solid #ccc;
            padding: 0px;
            width: 50%; /* Each card takes up 33.33% of the page width */
            height: 20%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center; /* Center-align text within each card */
            align-items: center;
        }
        .character {
            font-size: 72px;
            font-weight: bold;
            padding: 0;
            line-height: 102%;
            word-spacing: -10%;
            letter-spacing: -10%;
        }
        .pinyin {
            font-size: 36px;
            color: #666;
            padding: -5px;
            line-height: 90%;
        }
        .definition {
            font-size: 28px;
            padding: 0;
            letter-spacing: -0.5px;
            word-spacing: -1px;
            line-height: 100%;
        }
        .hskset {
            font-size: 8pt;
            padding: 0;
            line-height: 100%;
        }
    </style></head><body>"""
    
    # Iterate over the vocabulary list
    for i in range(0, len(vocab_list), cards_per_page):
        # Start a new page
        html_content += "<div class='page'>"
        
        # Iterate over the vocabulary words on this page
        for j in range(i, min(i + cards_per_page, len(vocab_list))):
            word = vocab_list[j]
            print(word)
            
            # Create a flashcard
            html_content += f"<div class='card'><div class='character'>{word['Character']}<span class='hskset'>{word['HSK Set']}</span></div><div class='pinyin'>{word['Pinyin']}</div><div class='definition'>{word['Meaning']}</div></div>"
        
        # End the page
        html_content += "</div>"
    
    # Close the HTML tags
    html_content += "</body></html>"
    
    return html_content

# Generate the HTML for flashcard pages
flashcard_html = generate_flashcard_pages(hsk_data, cards_per_page)

# Save the HTML content to a file (you can customize the file name and path)
with open('flashcards.html', 'w', encoding='utf-8') as file:
    file.write(flashcard_html)

# Optionally, you can use a library like wkhtmltopdf to convert the HTML to PDF for printing.
# Install wkhtmltopdf: https://wkhtmltopdf.org/
# Example command to convert to PDF: wkhtmltopdf flashcards.html flashcards.pdf
