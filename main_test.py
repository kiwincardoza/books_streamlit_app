import requests
import xmltodict
import json


CONSUMER_KEY = 'MAqh1xHyjdG3G1wea58H5Q'
CONSUMER_SECRET = 'QQ02V9neX62kgybmbkJpXlO3GcmF3EKW1YU7qKL5A'
user_id = '101611214'
shelf = 'read'
sort = 'owned'

'''
response_obj = requests.get("https://www.goodreads.com/review/list", params={'key':CONSUMER_KEY, 'id': user_id, 'shelf': shelf, 'sort': sort, 'v':2, 'per_page': '200'})
data_dict = xmltodict.parse(response_obj.text)

#print(data_dict['GoodreadsResponse']['reviews']['review'][0]['book']['title'])



book_title_lst = []
book_obj_lst = []
for book in data_dict['GoodreadsResponse']['reviews']['review']:
    #book_title_lst.append(book['book']['title'])
    if "The Innocent" in book['book']['title']:
        book_obj_lst.append(book['book'])

print(book_obj_lst)
'''


#12849385


search_author = "David Baldacci"
search_book = "The Innocent"
response_obj = requests.get("https://www.goodreads.com/search/index.xml", params={'key':CONSUMER_KEY, 'page': '1', 'q': search_book, 'search': 'title'})
data_dict = xmltodict.parse(response_obj.text)

for book_obj in data_dict['GoodreadsResponse']['search']['results']['work']: 
    if book_obj['best_book']['author']['name'] == search_author:
        print(book_obj['best_book'])


'''
#12583831, 848455, 33808483
response_obj = requests.get("https://www.goodreads.com/book/show", params={'key': CONSUMER_KEY, 'id': '3380849999983', 'format': 'xml'})
data_dict = xmltodict.parse(response_obj.text)
print(data_dict['GoodreadsResponse']['book']['publication_year'])
print(data_dict['GoodreadsResponse']['book']['series_works'])
print(data_dict['GoodreadsResponse']['book']['num_pages'])
print(data_dict['GoodreadsResponse']['book']['average_rating'])
print(data_dict['GoodreadsResponse']['book']['image_url'])
'''