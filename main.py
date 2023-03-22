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


    with st.form("my_form"):
        book_name_id, author_name_id = st.columns(2)
        book_name_id.text_input("Book Name", value=book_title_name)
        author_name_id.text_input("Author Name", value=author_name)
        format_type_id, pages_id, new_flag_id = st.columns(3)
        format_type = format_type_id.selectbox("Format", ["Paperback", "Hardcover", "Kindle"], index=0)
        pages = pages_id.slider("Pages", min_value=10, max_value=3000, value=100, step=1)
        new_flag = new_flag_id.selectbox("New", ["New", "Preloved"], index=0)
        series_name_id, location_id = st.columns([2,1])
        series_name = series_name_id.text_input("Series Name")
        location = location_id.text_input("Buying Location")
        fiction_flag_id, purchase_date_id = st.columns(2)
        fiction_flag = fiction_flag_id.selectbox("Fiction", ["Fiction", "Non Fiction"], index=0)
        purchase_date = purchase_date_id.date_input("Enter Purchase Date")
        bl, add_id, bl = st.columns(3)

        add_submitted = add_id.form_submit_button("ADD")

    if add_submitted:
        insert_into_db(book_title_name, author_name, format_type, pages, new_flag, series_name, location, fiction_flag, purchase_date)
        st.success("BOOK ADDED SUCCESSFULLY !")


if nav_option == 'View Books':
    conn = sqlite3.connect('books_db.db')
    df = pd.read_sql("SELECT * FROM BOOKS", conn)
    st.write(df)