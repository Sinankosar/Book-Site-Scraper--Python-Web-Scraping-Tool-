import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1



is_on = True
books_dict = {}
while is_on:
    url = f"https://books.toscrape.com/catalogue/page-{str(current_page)}.html"
    data = requests.get(url=url).text
    soup = BeautifulSoup(data,"html.parser")
    if soup.title.text == "404 Not Found":
        is_on=False
    else:
       
        books = soup.find_all("article", class_ = "product_pod")
        for i in books:
            book_name = i.find("h3").find("a").text
            book_price = i.find("div", class_ = "product_price").find("p").text[2:] #.replace("Â","").strip()
           
            book_stock = i.find("div", class_= "product_price").find("p",class_= "instock availability").text.strip()

            rating_value = i.find("p").get("class")[-1]

            books_dict[book_name] = {
            "price": book_price,
            "stock": book_stock,
            "rating": rating_value
}
            
        print(f"Scrape complated.\nCurrent page : {current_page}")    
        current_page+=1
        

df = pd.DataFrame.from_dict(books_dict, orient="index")
df.index.name = "Book Name"
df.reset_index(inplace=True)
df.to_excel("books.xlsx", index=False)


