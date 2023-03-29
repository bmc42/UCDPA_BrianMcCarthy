""" --------------------------------------------------------------------------------------------------------
File:		Extract Bellwether stocks 
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-16
Descr		The purpose of this script is to use webscrapping to determine the 
            list of bellwether stocks from specified websites.
            
            Using two websites, extract five bellwether stocks and add them to
            an array. Finally, write the array to the CSV file called 
            'targetStock.csv'.

"""

# import the Python Libraries
import pandas as pd	              # library for pandas
import requests                   # Library for requests
from bs4 import BeautifulSoup     # BS library

# setup the array for the stock listing
stockListingArray = []

#
#   URL:    https://www.morningstar.co.uk/uk/news/180953/5-uk-stocks-on-the-global-income-bellwether-list.aspx
#   
#   This URL lists the top five bellwether stocks from the london stock exchange
#
#   Using Scraping looking for a combinaton of html tags (as listed below) to get 
#   the character id of the stock exchange listing. It is noted that the html 
#   is not tagged with specific IDs
#
#   <h3>
#       <strong>
#           <a>
#
#   The stock ID is the text for the anchor html tag (<a>)
#

# set the URL
URL = "https://www.morningstar.co.uk/uk/news/180953/5-uk-stocks-on-the-global-income-bellwether-list.aspx"

# Load the Page
page = requests.get(URL)

# Process the page using beautiful soup
soup = BeautifulSoup(page.content, "html.parser")

# Html Elements
HTMLElementsH3 = soup.find_all("h3" )
for HTMLElements in HTMLElementsH3:
    HTMLElementsStrong = HTMLElements.find("strong")
    if ( HTMLElementsStrong != 'None'):
        HTMLElementsAnchor = HTMLElementsStrong.find("a")
        if ( HTMLElementsAnchor != 'None'):
            #print(HTMLElementsAnchor.prettify())
            # grab the text of the anchor and replace and dots ("."). 
            # Also need to add ".XLON" to the text.
            HTMLElementsAnchor = HTMLElementsAnchor.contents[0].replace(".", "")+'.XLON'
            stockListingArray.append (HTMLElementsAnchor)

#
#   URL:    https://www.dividend.com/how-to-invest/5-stocks-that-are-bellwethers-for-the-u-s-economy/
#   
#   This URL lists the top five bellwether stocks from the NYSE stock exchange
#
#   Using scraping looking for a combinaton of html tags (as listed below) to get 
#   the character id of the stock exchange listing. It is noted that the html 
#   is not tagged with specific IDs
#
#   <h2 class="n-text__section_heading t-text-gray-725">
#
#   The stock ID is the text for the header2 tag <h2>
#

# set the URL
URL = "https://www.dividend.com/how-to-invest/5-stocks-that-are-bellwethers-for-the-u-s-economy/"

# Load the Page
page = requests.get(URL)

# Process the page using beautiful soup
soup = BeautifulSoup(page.content, "html.parser")

# Html Elements
HTMLElementsH2 = soup.find_all("h2", class_="n-text__section_heading t-text-gray-725" )
for HTMLElements in HTMLElementsH2:
    HTMLElements = HTMLElements.contents[0]
    #print (HTMLElements)
    st = HTMLElements.find ("(")
    if ( st != -1 ) :
        en = HTMLElements.find(")")
        if ( en != -1 ):
            stockListingArray.append (HTMLElements[(st+1):(en)].strip())

print (stockListingArray)

# store the list of targeted stock listings as a file called target.csv
stockListingArrayDF = pd.DataFrame(stockListingArray)
stockListingArrayDF.to_csv( '../Data/targetStocks.csv', encoding='utf-8', header=False )
