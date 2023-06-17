from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
import undetected_chromedriver as uc

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    name = Column(String, primary_key=True)
    brand = Column(String)
    price = Column(String)
    ingredients = Column(String)
    image = Column(String)

username = 'mtnblues'
password = ''
engine = create_engine(f'postgresql://{username}:{password}@localhost/iris')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

options = uc.ChromeOptions()
options.add_argument('--headless')
driver = uc.Chrome(options=options)

url = 'https://www.sephora.com/shop/makeup-cosmetics'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

products = soup.find('div', {'data-comp': 'ProductGrid '}).find_all('div', recursive=False)[1]

for product in products:
    try:
        if product['style'].endswith('start'):
            continue
        link = product.find('a')
        details = link.find_all('span', {'data-comp': 'StyledComponent BaseComponent '}, recursive=False)
        brand = details[0].text
        name = details[1].text
        price = link.find('span', class_='css-0').text
        image = link.find('img')['src']
        
        print(f'Name: {name}')
        print(f'Brand: {brand}')
        print(f'Price: {price}')
        print(f'Image: {image}')

        url = link['href']
        if 'sephora.com' not in url:
            url = 'https://www.sephora.com' + url
        print(f'URL: {url.split(" ")[0]}')

        driver.get(url)
        product_soup = BeautifulSoup(driver.page_source, 'html.parser')

        ingredients = product_soup.find('div', {'id': 'ingredients'}) or ''
        if ingredients:
            ingredients = ingredients.text

        print(f'Ingredients: {ingredients}\n')
        new_product = Product(
            name=name,
            brand=brand,
            price=price,
            ingredients=ingredients,
            image=image
        )
        session.add(new_product)
    except:
        session.commit()
        session.close()

session.close()