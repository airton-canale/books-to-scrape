from bs4 import BeautifulSoup
import requests
import re
from database import Book, Category

BASE_URL = 'https://books.toscrape.com/'

rating_star_translator = [
    'One',
    'Two',
    'Three',
    'Four',
    'Five'
]

def save_image(book_id, image_url):
    with open(f"images/book_{book_id}.jpg", "wb") as fp:
        image = requests.get(image_url)
        fp.write(image.content)
                

def get_books():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, features="html.parser")
    categories = soup.find('div', class_='side_categories').find_all('a')[1::]
    for category in categories:
        category_data = {
            "name": category.text.strip(),
            "url": f"{BASE_URL}{category.get('href')}",
        }
        created_category = Category.create(**category_data)
        print(f"Created category with id - {created_category.id} with name {created_category.name}")
        book_response = requests.get(f"{BASE_URL}{category.get('href')}")
        books = BeautifulSoup(book_response.text, features="html.parser").find_all('article', class_='product_pod')
        for book in books: 
            href = book.find('a').get('href').replace('../', '')
            url = f"{BASE_URL}catalogue/{href}"
            book_response = requests.get(url)
            book_html = BeautifulSoup(book_response.text, features="html.parser")
            book_name = book_html.find('h1').text
            book_data = {
                "name": book_name,
                "description": book_html.find('meta', { "name" : "description" }).get('content').strip(),
                "price": float(re.search(r'([0-9.]+)', book_html.find('p', class_='price_color').text)[0]),
                "rating": rating_star_translator.index(book_html.find('p', class_="star-rating").get('class')[1]) + 1,
                "category": created_category.id
            }
            created_book = Book.create(**book_data)
            image_url = f"{BASE_URL}/{book_html.find('img').get('src').replace('../', '')}"
            save_image(created_book.id, image_url)
            print(f"Created book with id - {created_book.id} with name {book_name}")
    
    soup.decompose()
get_books()