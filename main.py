import requests
import xmltodict


CONSUMER_KEY = 'MAqh1xHyjdG3G1wea58H5Q'
CONSUMER_SECRET = 'QQ02V9neX62kgybmbkJpXlO3GcmF3EKW1YU7qKL5A'
user_id = '101611214'
shelf = 'read'
sort = 'title'

response_obj = requests.get("https://www.goodreads.com/review/list", params={'key':CONSUMER_KEY, 'id': user_id, 'shelf': shelf, 'sort': sort, 'v':2, 'per_page': '200'})
data_dict = xmltodict.parse(response_obj.text)

print(data_dict['GoodreadsResponse']['reviews']['review'][0]['book']['title'])


book_title_lst = []
for book in data_dict['GoodreadsResponse']['reviews']['review']:
    book_title_lst.append(book['book']['title'])

print(len(book_title_lst))