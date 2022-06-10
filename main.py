from bs4 import BeautifulSoup
import requests
import os
import time
import csv
import json
def get_all_pages():
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    # req = requests.get("https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/",headers)

    # if not os.path.exists("Dynamic_Web/data"):
    #     os.mkdir("Dynamic_Web/data")
    # with open("Dynamic_Web/data/index.html","w",encoding="utf-8") as file:
    #     file.write(req.text)
    with open("Dynamic_Web/data/index.html",encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src,"lxml")
    pages_count = len(soup.find("div",class_="bx-pagination-container").find_all("a"))
    for  i in range(1,pages_count + 1):
        url = f"https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}"
        req = requests.get(url,headers)
        with open(f"Dynamic_Web/data/page_{i}.html","w",encoding="utf-8") as file:
            file.write(req.text)
        time.sleep(2)
    return pages_count +1
    
def collect_data(pages_count):
    with open("Dynamic_Web/data/watches.csv","w",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("Бренд","Модель","Ціна"))
    watches_json = []
    for i in range(1,pages_count):
        with open(f"Dynamic_Web/data/page_{i}.html",encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src,"lxml")
        watches = soup.find_all("div",class_="product-item")
        for watch in watches:
            watch_brand = "G-SHOCK"
            watch_model = watch.find("p",class_="product-item__articul").text
            watch_model = watch_model.replace("\n","").strip()
            watch_price = watch.find("p",class_="product-item__price").find("span",class_="rouble").next_element.next_element.next_element.text
            watches_json.append({"Бренд":watch_brand,"Модель":watch_model,"Ціна":watch_price})
            with open("Dynamic_Web/data/watches.csv","a",encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow((watch_brand,watch_model,watch_price))
    with open("Dynamic_Web/data/watches.json","a",encoding="utf-8") as file:
        json.dump(watches_json, file,indent=4,ensure_ascii=False)
    print("File processed")


def main():
    pages_count = get_all_pages()
    collect_data(pages_count)
if __name__ == "__main__":
    main()