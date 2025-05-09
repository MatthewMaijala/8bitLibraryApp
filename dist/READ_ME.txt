This program has the MySQL connector hardcoded into it and therefore will not work for you should you choose to run it as is. To run the application, you must have PyInstaller installed in your python development environment, insert your specific database connection information to all files that use it (LoginScreen.py has two instances), then run the code provided below in the terminal.

pyinstaller --onefile --windowed --add-data "ManageBooks.py;." --add-data "ViewTables.py;." --add-data "SearchBooks.py;." --add-data "CheckoutBook.py;." --add-data "ReturnBook.py;." --add-data "MemberView.py;." --add-data "DatabaseAccounts.txt;." --add-data "user_activity.log;." --add-data "auth.py;." --icon=8bitLibrary.ico LoginScreen.py

doing this should allow you to generate the application (with your MySQL connection).

You CAN run this application without pyinstaller, you just need to run the LoginScreen.py file.