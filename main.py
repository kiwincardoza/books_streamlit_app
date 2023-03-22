import streamlit as st
import requests
import xmltodict
import sqlite3
import pandas as pd



CONSUMER_KEY = 'MAqh1xHyjdG3G1wea58H5Q'
CONSUMER_SECRET = 'QQ02V9neX62kgybmbkJpXlO3GcmF3EKW1YU7qKL5A'

@st.cache_data
def search_book_in_goodreads(book_name, author_name):
    try:
        response_obj = requests.get("https://www.goodreads.com/search/index.xml", params={'key':CONSUMER_KEY, 'page': '1', 'q': book_name, 'search': 'title'})
        data_dict = xmltodict.parse(response_obj.text)

        for book_obj in data_dict['GoodreadsResponse']['search']['results']['work']: 
            if book_obj['best_book']['author']['name'] == author_name:
                return book_obj['best_book']['title']
    except Exception as e:
        st.write("Cannot find the book name!")
        return "NULL"
    
    st.write("Cannot find the author name!")
    return "NULL"


def insert_into_db(book_title_name, author_name, format_type, pages, new_flag, series_name, location,
                fiction_flag, purchase_date):
    conn = sqlite3.connect('books_db.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        AUTHOR_NAME TEXT NOT NULL,
        FORMAT TEXT NOT NULL,
        PAGES INT NOT NULL,
        NEW_FLAG CHAR(50) NOT NULL,
        SERIES_NAME TEXT,
        BUYING_LOCATION TEXT,
        FICTION_FLAG CHAR(50) NOT NULL,
        PURCHASE_DATE DATE);''')
    
    st.write("Created Table")
    conn.execute(f"INSERT INTO BOOKS(NAME, AUTHOR_NAME, FORMAT, PAGES, NEW_FLAG, SERIES_NAME, BUYING_LOCATION, FICTION_FLAG, PURCHASE_DATE) VALUES ('{book_title_name}', '{author_name}', '{format_type}', {pages}, '{new_flag}', '{series_name}', '{location}', '{fiction_flag}', {purchase_date})");
    conn.commit()

    st.write("Inserted into table")

    conn.close()


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
    book_name_id, author_name_id = st.columns(2)
    book_name = book_name_id.text_input("Book Name")
    author_name = author_name_id.text_input("Author Name")
    book_title_name = "NULL"
    bl, submit, bl = st.columns(3)
    if submit.button("Search"):
        book_title_name = search_book_in_goodreads(book_name, author_name)

    book_title_name = search_book_in_goodreads(book_name, author_name).replace("'", "''")

    with st.form("my_form"):
        book_name_id, author_name_id = st.columns(2)
        book_name_1 = book_name_id.text_input("Book Name", value=book_title_name)
        author_name_id.text_input("Author Name", value=author_name)
        
        
        pages = st.slider("Pages", min_value=10, max_value=2000, value=100, step=1)
        
        series_name_id, location_id, format_type_id = st.columns([1,2,1])
        series_name = series_name_id.text_input("Series Name")
        location = location_id.text_input("Buying Location")
        format_type = format_type_id.selectbox("Format", ["Paperback", "Hardcover", "Kindle"], index=0)
        fiction_flag_id, purchase_date_id, new_flag_id = st.columns(3)
        fiction_flag = fiction_flag_id.selectbox("Fiction", ["Fiction", "Non Fiction"], index=0)
        purchase_date = purchase_date_id.date_input("Enter Purchase Date")
        new_flag = new_flag_id.selectbox("New", ["New", "Preloved"], index=0)
        bl, add_id, bl = st.columns(3)

        add_submitted = add_id.form_submit_button("ADD")

    if add_submitted:
        insert_into_db(book_name_1, author_name, format_type, pages, new_flag, series_name, location, fiction_flag, purchase_date)
        st.success(f"BOOK {book_name_1} ADDED SUCCESSFULLY !")


if nav_option == 'View Books':
    conn = sqlite3.connect('books_db.db')
    my_books_df = pd.read_sql("SELECT * FROM BOOKS", conn)

    read_book_lst = get_read_books_list()

    read_flag = st.selectbox('Select Read/Unread/ALL', ['All', 'Read', 'Unread'], index=2)
    start_page, end_page = st.select_slider(
                'Select a range of pages',
                options=[10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800],
                value=(200, 400))
    author_name = st.text_input("Author Name")
    format = st.selectbox("Format", ["Paperback", "Hardcover", "Kindle"], index=0)
    series_name = st.text_input("Series Name")
    new_flag = st.selectbox("New/Preloved", ["New", "Preloved"], index=0)
    fiction_flag = st.selectbox("Fiction/Non Fiction", ["Fiction", "Non Fiction"], index=0)

    if read_flag == 'Read':
        my_books_df = my_books_df[my_books_df['NAME'].isin(read_book_lst)]
    elif read_flag == 'Unread':
        my_books_df = my_books_df[~my_books_df['NAME'].isin(read_book_lst)]
    
    my_books_filtered_df = my_books_df[(my_books_df['PAGES']>=start_page) & (my_books_df['PAGES']<=end_page) |
                                       (my_books_df['AUTHOR_NAME'] == author_name) |
                                       (my_books_df['FORMAT'] == format) |
                                       (my_books_df['SERIES_NAME'] == series_name) |
                                       (my_books_df['NEW_FLAG'] == new_flag) |
                                       (my_books_df['FICTION_FLAG'] == fiction_flag)
                                       ]

    st.write(read_book_lst)
    st.write(my_books_filtered_df)