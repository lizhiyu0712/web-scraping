# ----- 1. Use the requests module to download the html for URL.

import requests
import json
import csv
from bs4 import BeautifulSoup

requestURL = 'https://ca.trustpilot.com/review/www.gucci.com?languages=all'
csvFileName = "Test_WebScraping_AS1.csv"
html = requests.get(requestURL)

soup = BeautifulSoup(html.text, 'html.parser')
print(soup.title)

# ----- 2. Extract the total number of reviews."""

data = json.loads(soup.body.script.get_text())# return a python dict
print("The total number of reviews are " + 
      str(data["props"]["pageProps"]
                    ["businessUnit"]["numberOfReviews"]))

# From the first page data, 
# we get the total number of review page inorder to get the full data
pages = data["props"]["pageProps"]["filters"]["pagination"]["totalPages"]

DataArrayAsJson = []

for idx in range(pages):
    newURL = requestURL + "&page=" + str(idx + 1)
    currentHTMLRequest = requests.get(newURL)
    newSoup = BeautifulSoup(currentHTMLRequest.text, 'html.parser')
    CurrentDataInJson = json.loads(newSoup.body('script', 
                                                id="__NEXT_DATA__", 
                                                type="application/json")
                                                [0].get_text())
    DataArrayAsJson.append(CurrentDataInJson)

print(len(DataArrayAsJson))

# ----- 3. Iterate over the review pages.

# get the html
resp = requests.get(requestURL)

# check what the response contains
type(resp)

# This is the html source
html_code = resp.text

# ----- 4. From each page extract the reviews.

comapnyName = data["props"]["pageProps"]["businessUnit"]["displayName"]
datePublishedArray = []
ratingValueArray = []
reviewBodyArray = []

for DataInThisPage in DataArrayAsJson:
    currentReviewsArray = DataInThisPage["props"]["pageProps"]["reviews"]
    for currentReviewsObject in currentReviewsArray:
        datePublishedArray.append(currentReviewsObject["dates"]
                                  ["publishedDate"])
        ratingValueArray.append(currentReviewsObject["rating"])
        reviewBodyArray.append(currentReviewsObject["text"])

# ----- 5. Store companyName, datePublished, ratingValue, reviewBody
# ----- to the CSV file

# open a new file as follows:
with open(csvFileName, 'w', encoding="utf-8", newline='') as f:
    # close it with f.close()
    # start a csv writer object:
    writer = csv.writer(f, delimiter=',')
    # write a row, this writes the header
    writer.writerow(["CompanyName", "DataPublished", 
                     "RatingValue", "ReviewBody"])

    for idx in range(len(datePublishedArray)):
        writer.writerow([comapnyName, datePublishedArray[idx], 
                         ratingValueArray[idx], reviewBodyArray[idx]])

    f.close()
