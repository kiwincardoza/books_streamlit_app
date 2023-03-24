import streamlit as st
import requests
import xmltodict
import sqlite3
import pandas as pd
from PIL import Image
import math



CONSUMER_KEY = 'MAqh1xHyjdG3G1wea58H5Q'
CONSUMER_SECRET = 'QQ02V9neX62kgybmbkJpXlO3GcmF3EKW1YU7qKL5A'



'''
Updates:
    Author name populated on own - selected button
    Downloadable excel/csv/pdf - final table
    Watermark/Logo - 
    Error handling
'''


@st.cache_data
def search_book_in_goodreads(book_name, author_name, book_id):
    try:
        if (book_name == '') & (author_name == '') & (book_id == ''):
            st.error("Enter some values to search")
            return "NULL", "NULL", 0, 0, 0, "NULL", "NULL", 0
        response_obj1 = requests.get("https://www.goodreads.com/book/show", params={'key': CONSUMER_KEY, 'id': book_id, 'format': 'xml'})
        data_dict1 = xmltodict.parse(response_obj1.text)
        if data_dict1:
            st.success("Found the book from Goodreads Book ID")
            if data_dict1['GoodreadsResponse']['book']['series_works']:
                return data_dict1['GoodreadsResponse']['book']['title'], book_id, int(data_dict1['GoodreadsResponse']['book']['num_pages']), int(data_dict1['GoodreadsResponse']['book']['publication_year']), float(data_dict1['GoodreadsResponse']['book']['average_rating']), data_dict1['GoodreadsResponse']['book']['image_url'], data_dict1['GoodreadsResponse']['book']['series_works']['series_work']['series']['title'], int(data_dict1['GoodreadsResponse']['book']['series_works']['series_work']['series']['primary_work_count'])
            else:
                return data_dict1['GoodreadsResponse']['book']['title'], book_id, int(data_dict1['GoodreadsResponse']['book']['num_pages']), int(data_dict1['GoodreadsResponse']['book']['publication_year']), float(data_dict1['GoodreadsResponse']['book']['average_rating']), data_dict1['GoodreadsResponse']['book']['image_url'], "NULL", 0
        else:
            st.warning("Did not find by Goodreads ID... Try by Name and Author")

        response_obj = requests.get("https://www.goodreads.com/search/index.xml", params={'key':CONSUMER_KEY, 'page': '1', 'q': book_name, 'search': 'title'})
        data_dict = xmltodict.parse(response_obj.text)

        for book_obj in data_dict['GoodreadsResponse']['search']['results']['work']: 
            if book_obj['best_book']['author']['name'] == author_name:
                st.success("Found the book by book name and author name")
                return book_obj['best_book']['title'], book_obj['best_book']['id']['#text'], 0, 0, 0, book_obj['best_book']['image_url'], "NULL", 0
    except Exception as e:
        st.error(f"Cannot find the book name - {e}!")
        return "NULL", "NULL", 0, 0, 0, "NULL", "NULL", 0 
    
    st.error("Cannot find the author name!")
    return "NULL", "NULL", 0, 0, 0, "NULL", "NULL", 0


def insert_into_db(book_title_name, book_id_1, author_name, format_type, pages, new_flag, series_name, location,
                fiction_flag, purchase_date, image_url, publication_year, average_rating, total_in_series):
    conn = sqlite3.connect('books_db.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        BOOK_ID VARCHAR NOT NULL, 
        AUTHOR_NAME TEXT NOT NULL,
        FORMAT TEXT NOT NULL,
        PAGES INT NOT NULL,
        NEW_FLAG CHAR(50) NOT NULL,
        SERIES_NAME TEXT,
        BUYING_LOCATION TEXT,
        FICTION_FLAG CHAR(50) NOT NULL,
        PURCHASE_DATE DATE, 
        IMAGE_URL TEXT,
        PUBLICATION_YEAR INT,
        AVERAGE_RATING FLOAT,
        TOTAL_IN_SERIES INT);''')
    
    st.write("Created Table")
    conn.execute(f"INSERT INTO BOOKS(NAME, BOOK_ID, AUTHOR_NAME, FORMAT, PAGES, NEW_FLAG, SERIES_NAME, BUYING_LOCATION, FICTION_FLAG, PURCHASE_DATE, IMAGE_URL, PUBLICATION_YEAR, AVERAGE_RATING, TOTAL_IN_SERIES) VALUES ('{book_title_name}', '{book_id_1}', '{author_name}', '{format_type}', {pages}, '{new_flag}', '{series_name}', '{location}', '{fiction_flag}', {purchase_date}, '{image_url}', '{publication_year}', {average_rating}, {total_in_series})");
    conn.commit()

    st.write("Inserted into table")

    conn.close()




@st.cache_data
def get_read_books_list():
    user_id = '101611214'
    shelf = 'read'
    sort = 'title'

    response_obj = requests.get("https://www.goodreads.com/review/list", params={'key':CONSUMER_KEY, 'id': user_id, 'shelf': shelf, 'sort': sort, 'v':2, 'per_page': '200'})
    data_dict = xmltodict.parse(response_obj.text)

    book_title_lst = []
    for book in data_dict['GoodreadsResponse']['reviews']['review']:
        book_title_lst.append(book['book']['title'])
    return book_title_lst


st.title("Kiwin's Books")
nav_option = st.sidebar.radio("Navigation", ["Add Books", "View Books"])

if nav_option == 'Add Books':
    book_name_id, author_name_id, book_id_id = st.columns(3)
    book_name = book_name_id.text_input("Book Name")
    author_name = author_name_id.text_input("Author Name")
    book_id = book_id_id.text_input("Goodreads Book ID")
    book_title_name = "NULL"
    bl, submit, bl = st.columns(3)
    if submit.button("Search"):
        book_title_name, book_id_1, num_pages, publication_year, average_rating, image_url, series_name_1, total_in_series = search_book_in_goodreads(book_name, author_name, book_id)

    book_title_name, book_id_1, num_pages, publication_year, average_rating, image_url, series_name_1, total_in_series = search_book_in_goodreads(book_name, author_name, book_id)
    book_title_name = book_title_name.replace("'", "''")

    with st.form("my_form"):
        book_name_id, author_name_id, book_id_id = st.columns(3)
        book_name_1 = book_name_id.text_input("Book Name", value=book_title_name)
        author_name_1 = author_name_id.text_input("Author Name", value=author_name)
        book_id_id.text_input("Goodreads Book ID", value=book_id_1)
        
        
        pages = st.slider("Pages", min_value=10, max_value=2000, value=num_pages, step=1)
        
        series_name_id, location_id, format_type_id = st.columns([1,2,1])
        series_name = series_name_id.text_input("Series Name", value=series_name_1)
        location = location_id.text_input("Buying Location")
        format_type = format_type_id.selectbox("Format", ["Paperback", "Hardcover", "Kindle"], index=0)
        fiction_flag_id, purchase_date_id, new_flag_id = st.columns(3)
        fiction_flag = fiction_flag_id.selectbox("Fiction", ["Fiction", "Non Fiction"], index=0)
        purchase_date = purchase_date_id.date_input("Enter Purchase Date")
        new_flag = new_flag_id.selectbox("New", ["New", "Preloved"], index=0)

        publication_year_id, average_rating_id = st.columns(2)
        publication_year = publication_year_id.text_input("Publication Year", value=publication_year)
        average_rating = average_rating_id.number_input("Average Rating", value=average_rating)

        image_url_id, total_in_series_id = st.columns([2,1])
        image_url = image_url_id.text_input("Image URL", value=image_url)
        total_in_series = total_in_series_id.number_input("Total Books in Series", value=total_in_series)

        bl, add_id, bl = st.columns(3)
        add_submitted = add_id.form_submit_button("ADD")

    if add_submitted:
        insert_into_db(book_name_1, book_id_1, author_name_1, format_type, pages, new_flag, series_name, location, fiction_flag, purchase_date,
                       image_url, publication_year, average_rating, total_in_series)
        st.success(f"BOOK {book_name_1} ADDED SUCCESSFULLY !")


if nav_option == 'View Books':
    conn = sqlite3.connect('books_db.db')
    my_books_df = pd.read_sql("SELECT * FROM BOOKS", conn)

    series_name_lst = list(my_books_df['SERIES_NAME'].unique())
    author_name_lst = list(my_books_df['AUTHOR_NAME'].unique())

    series_name_lst.append("All")
    author_name_lst.append("All")

    read_book_lst = get_read_books_list()

    read_flag = st.selectbox('Select Read/Unread/ALL', ['All', 'Read', 'Unread'], index=2)
    start_page, end_page = st.select_slider(
                'Select a range of pages',
                options=[10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800],
                value=(200, 400))
    start_rating, end_rating = st.select_slider(
                'Select a range of rating',
                options=[1,2,3,4,5],
                value=(3,5))
    author_name = st.selectbox("Author Name", author_name_lst, index=0)
    format_1 = st.selectbox("Format", ["All", "Paperback", "Hardcover", "Kindle"], index=0)
    series_name = st.selectbox("Series Name", series_name_lst, index=0)
    new_flag = st.selectbox("New/Preloved", ["All", "New", "Preloved"], index=0)
    fiction_flag = st.selectbox("Fiction/Non Fiction", ["Fiction", "Non Fiction"], index=0)

    if read_flag == 'Read':
        my_books_df = my_books_df[my_books_df['NAME'].isin(read_book_lst)]
    elif read_flag == 'Unread':
        my_books_df = my_books_df[~my_books_df['NAME'].isin(read_book_lst)]
    
    if author_name == "All":
        authors_condition = (my_books_df['AUTHOR_NAME'] != "None")
    else:
        authors_condition = (my_books_df['AUTHOR_NAME'] == author_name)

    if series_name == "All":
        series_name_condition = (my_books_df['SERIES_NAME'] != "None")
    else:
        series_name_condition = (my_books_df['SERIES_NAME'] == series_name)

    if format_1 == "All":
        format_condition = (my_books_df['FORMAT'] != "None")
    else:
        format_condition = (my_books_df['FORMAT'] == format_1)

    if new_flag == "All":
        new_flag_condition = (my_books_df['NEW_FLAG'] != "None")
    else:
        new_flag_condition = (my_books_df['NEW_FLAG'] == new_flag)
    

    my_books_filtered_df = my_books_df[(my_books_df['PAGES']>=start_page) & (my_books_df['PAGES']<=end_page) &
                                       (my_books_df['AVERAGE_RATING']>=start_rating) & (my_books_df['AVERAGE_RATING']<=end_rating) &
                                       (authors_condition) &
                                       (format_condition) &
                                       (series_name_condition) &
                                       (new_flag_condition) &
                                       (my_books_df['FICTION_FLAG'] == fiction_flag)
                                       ]

    st.table(my_books_filtered_df)

    
    books_in_one_segment = 3
    no_of_books = len(my_books_filtered_df)
    no_of_segments = math.ceil(no_of_books/books_in_one_segment)

    image_container_lst = []
    for segment in range(no_of_segments):
        image_container_lst.append(st.columns(books_in_one_segment))

    
    for index, row in my_books_filtered_df.iterrows():
        #image = Image.open(row['IMAGE_URL'])
        #real_index = index + 1

        st.image(row['IMAGE_URL'], caption=row['NAME'])
    