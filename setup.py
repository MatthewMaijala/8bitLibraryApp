from setuptools import setup

APP = ['8bitLibrary.py']
OPTIONS = {
    'iconfile': '8bitLibrary.ico',
    'packages': ['mysql.connector', 'tkinter', 'hashlib', 'os', 'datetime'],
}

setup(
    app=APP,
    name='8bitLibrary',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

# This setup script is used to create a standalone application for the 8bitLibrary.py script using py2app.