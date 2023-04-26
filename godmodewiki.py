import requests
from bs4 import BeautifulSoup
import re
import os
import time

start_time = time.time()

entry = input('Link with the character appearances: ')

response = requests.get(entry)

# find all the links in the page

soup = BeautifulSoup(response.text, 'html.parser')

links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href:
        links.append(href)

# find the index of the first link that ends with "/Gallery"

start_link_index = 0
for i, link in enumerate(links):
    if link.endswith("/Gallery"):
        start_link_index = i
        break

start_link_index = start_link_index+1

# find the index of the element that ends with "/wiki/Special:Categories"

end_link_index = links.index("/wiki/Special:Categories")-1

# filter the links according to those parameters

filtered_links = links[start_link_index:end_link_index+1]
unique_links = list(set(filtered_links))
unique_links = [link for link in unique_links if link.startswith('/wiki')]

# Add https://dc.fandom.com at the beginning of every element

for i in range(len(unique_links)):
    unique_links[i] = "https://dc.fandom.com" + unique_links[i]

# Create a list that contains the link plus its publication date

def date_extract(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    filtered_links = [link for link in links if link.startswith('/wiki/Category:20') or link.startswith('/wiki/Category:19')]
    filtered_links_2= [link for link in filtered_links if link.endswith('(Publication)')]
    if not filtered_links_2:
        return None
    cadena = filtered_links_2[1]
    patron = r"/wiki/Category:(\d{4}),_([a-zA-Z]+)_\(Publication\)"
    resultado = re.search(patron, cadena)
    if resultado:
        year = resultado.group(1)
        month = resultado.group(2)
        return year, month
    else:
        return None

links_with_dates = []

for link in unique_links:
    date = date_extract(link)
    if date is not None:
        links_with_dates.append((link, date))

# filter the links by month and year of publication

def get_month_number(month_str):
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    return months[month_str]

sorted_links = sorted(links_with_dates, key=lambda x: (int(x[1][0]), get_month_number(x[1][1])))

for index, value in enumerate(sorted_links):
    print(f"{index+1}. {value}")

end_time = time.time()

elapsed_time = end_time - start_time

print("The process took", elapsed_time, "seconds to complete.")

os.system("pause")