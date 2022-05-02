# Importing the required libraries for the web scraping
import re
import requests
from bs4 import BeautifulSoup

# Fetching the Required URL


def get_url(number_of_pages):
    book_url = []
    for index in range(1, number_of_pages):
        headers = {'Accept-Language': 'en-US,en;q=0.8'}
        # Sends get request to the targeted url and as a response we are getting the information required
        goodreads_page = requests.get(
            "https://www.goodreads.com/list/show/5.Best_Books_of_the_Decade_2000s?page="+str(index), headers=headers)
        #  soup parses all the infromation from the html document
        soup = BeautifulSoup(goodreads_page.content, "html.parser")
        for a in soup.find_all('a', class_="bookTitle", href=True):
            book_url.append("http://www.goodreads.com"+a['href'])
    return book_url


def get_title(soup):
    # itemprop is the attribute to add the properties to an elment and every element can have this property.
    book_title = soup.find("h1", {'itemprop': 'name'}).text.strip()
    return book_title


def get_author(soup):
    book_author = soup.find("span", {'itemprop': 'name'}).text.strip()
    return book_author


def get_reviews(soup):
    # extracting the information from the meta elements with content atrributes
    num_reviews = soup.find('meta', {'itemprop': 'reviewCount'})[
        'content'].strip()
    return num_reviews


def get_ratings(soup):
    num_ratings = soup.find('meta', {'itemprop': 'ratingCount'})[
        'content'].strip()
    return num_ratings


def get_avg_rating(soup):
    avg_rating = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
    return avg_rating


def get_num_pages(soup):
    # Regex Pattern numbers between 0-9 and of either 3 or 4 digits and group to extract the matched value
    num_pages = soup.find('span', {'itemprop': 'numberOfPages'})
    if num_pages:
        return re.search('([0-9]{1,4})', num_pages.text).group(1)


def get_year_first_published(soup):
    # Books having two dates (Published date and first published dates)
    year_first_published = soup.find('nobr', {'class': 'greyText'})
    if year_first_published:
        # year_first_published = year_first_published.string
        # Regex Pattern numbers between 0-9 and of 4 digits and group to extract the matched value
        return re.search('([0-9]{4})', year_first_published.text).group(1)
    else:
        # item_content = soup.find_all('div', class_='leftContainer')
        item_content = soup.find_all('div', {'class': 'uitext darkGreyText'})
        #original_publish_year = item_content[0].find_all("div", class_="row")[1].text.replace("\n"," ").strip().split(" ")
        original_publish_year = item_content[0].find_all("div", class_="row")[
            1]
        return re.search('([0-9]{4})', original_publish_year.text).group(1)


def get_genres(soup):
    genres = []
    current_genres = soup.find_all(
        'a', {'class': 'actionLinkLite bookPageGenreLink'})
    # Filtering the first three genres
    for g in current_genres[:3]:
        g = g.text
        if g.strip():
            genres.append(g)
    return genres


def get_series(soup):
    book_series = soup.find_all('div', class_="infoBoxRowTitle")
    # checking if the book belongs to the series or not by looping through the text of elements with class infoBoxRowTitle
    list_of_inner_text = [x.text for x in book_series]
    book_series = True if 'Series' in list_of_inner_text else False
    return book_series


def get_awards(soup):
    book_awards = soup.find("div", {'itemprop': 'awards'})
    if book_awards:
        book_awards = book_awards.text.replace("\n", "").replace(
            "...more", ",").replace("...less", "").strip()
        book_awards = book_awards.split(",")
    return book_awards


def get_places(soup):
    book_places = soup.find_all('div', class_="infoBoxRowTitle")
    settings = []
    for ind, values in enumerate(book_places):
        # If the location is given then extract the location (Setting)
        if values.text == 'Setting':
            places = soup.find_all("div", class_="infoBoxRowItem")
            # The index of the location varies i.e different books can have different location index
            # If values.text == "Settings" if we find the settings then take the index of that element
            places = places[ind].find_all('a')
            for item in places:
                settings.append(item.text)
    return settings
