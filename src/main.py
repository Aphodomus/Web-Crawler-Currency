import datetime
from utils.util import *
from models.currency import *

def main():
    now = datetime.datetime.now()
    last_register = read_last_register()

    # If you read the page TODAY you don't do it again
    if str(now.day) != last_register:
        # Scrap page and return information like a list
        create_html()
        write_new_register()

    scrap_page()

if __name__ == '__main__':
    main()