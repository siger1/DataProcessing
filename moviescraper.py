#!/usr/bin/env python
# Name: Siger de Vries
# Student number: 10289321
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""
import re
import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_\
votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """
    movies=[]
    for element in dom.find_all("div", class_="lister-item mode-advanced"):
        # titles
        movies.append(element.find('img').get('alt'))
        #print(element.find('img').get('alt'))
        # rating
        movies.append(element.find("div", "ratings-bar").find('strong').string)
        #print(element.find("div", "ratings-bar").find('strong').string)
        # year
        year = element.find('span', 'lister-item-year text-muted unbold').string
        year = re.sub('[()]', '', year)
        year = re.sub('[I]', '', year)
        movies.append(year)
        # actors/acresses
        l=[]
        if element.find("div", "lister-item-content").find_all("p")[2].find("span") != None:
            for a in element.find("div", "lister-item-content").find_all("p")[2].find("span").next_siblings:
                if a.string[0] != ' ' and len(a.string) > 4 :
                    l.append(a.string)
        movies.append(l)
        # runtime
        movies.append(element.find('span','runtime').string)
        #print(element.find('span','runtime').string)
    #print(titles, ratings, years, actors, runtimes)

    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    return movies  # REPLACE THIS LINE AS WELL IF APPROPRIATE


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])
    for i in range(0, 249, 5):
        writer.writerow([movies[i], movies[i+1], movies[i+2], movies[i+3], movies[i+4]])

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
