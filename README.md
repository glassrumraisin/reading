# 読書ペース管理アプリ
#### Video Demo:  <URL https://youtu.be/tk4jnjZaoV8>
#### Description:
An application that allows you to manage your reading pace in two different ways
Languages used are python,flask,HTML,CSS
Book information is provided by openBD.
Link: https://api.openbd.jp

It has the following four HTML pages
1. A page displaying the database of books, if any (home page)
2. Enter the ISBN code of the book and if the book exists in the openBD database, it will be added to the database of this application.
3. Enter the date when you want to finish reading the book, and the number of pages read per day will be displayed.
4. When you enter the number of pages to be read per day, the date when you will finish reading the book is displayed.

Each element in the database has a delete button, which can be pressed to delete it from the database.
Information retrieved from openBD includes title, number of pages, author's name, and publisher's name.

Description of functions included in app.py
1. function create_conn for database creation and reference
Also used by reference to pass values to functions described below.
This function has the database as its return value.
2. function display for displaying the contents of the database on the screen
The return value is the total number of pages in the book and the database body, which is used for the functions described below.
3. function index for the top page
The database and the total number of pages are passed to the html page in order to accommodate updates to the database contents.
4. function search to search for books by the entered ISBN code and add them to the database
A database called openBD is used to search for books. The decisive factor is that the database includes the number of pages as an element.
The search function is designed to return an error if the ISBN does not exist in the database, if the page number is not listed in the database, or if the ISBN has already been searched.
5. function pages to input the expected end date of reading and calculate the number of pages
By entering the expected reading completion date (the deadline by which you want to finish reading the book), the number of pages to be read per day to finish reading the book on that date is displayed.
The function returns an error if the entered date is incorrect, if the total number of pages of a book is missing (database is empty), or if the entered date is in the past.
6. Function days to input the expected end date of reading and calculate the number of pages
By entering the number of pages to be read in a day, it is possible to know when the reading will be finished.
Returns an error if the input is incorrect, if the number of pages read in a day is less than 0, or if the total number of pages is incorrect (database is empty).
7. function delete to delete an element in the database
