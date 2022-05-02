import pandas as pd
from scraper.scraper import *

no_pages = 20

book_url = get_url(no_pages)

books = []

for book_no, url in enumerate(book_url):
    print(f'Printing Page')
    my_page = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.8'})
    soup = BeautifulSoup(my_page.content, "html.parser")
    try:
        book_title = get_title(soup)
    except:
        book_title = 'None'
    try:
        book_author = get_author(soup)
    except:
        book_author = 'None'
    try:
        num_reviews = get_reviews(soup)
    except:
        num_reviews = 'None'

    try:
        num_ratings = get_ratings(soup)
    except:
        num_ratings = 'None'
    try:
        avg_rating = get_avg_rating(soup)
    except:
        avg_rating = 'None'
    try:
        num_pages = get_num_pages(soup)
    except:
        num_pages = 'None'
    try:
        original_publish_year = get_year_first_published(soup)
    except:
        original_publish_year = 'None'
    try:
        book_series = get_series(soup)
    except:
        book_series = 'None'
    try:
        genres = get_genres(soup)
    except:
        genres = 'None'
    try:
        settings = get_places(soup)
    except:
        settings = 'None'
    try:
        book_awards = get_awards(soup)
    except:
        book_awards = 'None'

    books.append({
        'url': url,
        'title': book_title,
        'author': book_author,
        'num_reviews': num_reviews,
        'num_ratings': num_ratings,
        'avg_rating': avg_rating,
        'num_pages': num_pages,
        'original_publish_year': original_publish_year,
        'series': book_series,
        'genres': genres,
        'awards': book_awards,
        'places': settings})

    print('Book_'+str(book_no)+'\n')

    time.sleep(3)

    df = pd.DataFrame.from_dict(books)

    df.to_csv('dataset.csv', index=False)
