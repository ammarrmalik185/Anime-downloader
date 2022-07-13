import requests
from bs4 import BeautifulSoup

def connecting(url, category, key, value):
    print("-------------------------------------------------")
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text , features=("html.parser"))
    for i in value:
        p = soup.findAll(category, {key:i})
        for i in range(0,len(p)):
            p1 = p[i].get_text()
            print(p1)
        print("-------------------------------------------------")

input_url = input("Enter URL :")
input_category = input("Enter category :")
input_key = input("Enter key :")
check = 1
value_list = []
while check != 0:
    input_value = input("Enter value :")
    value_list.append(input_value)
    check = int(input("Do you want to enter another value? 0 for no :"))

connecting(input_url, input_category, input_key, value_list)
input("")
