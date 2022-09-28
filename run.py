import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    """

    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",") #cant update spreadsheet values without converting into a list
        

        if validate_data(sales_data):
            print("Data Is Valid")
            break

    return sales_data


def validate_data(values):
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 Values required, you've provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again...\n")
        return False
    print(values)

    return True

def update_sales_worksheet(data): #This will add a new row in worksheeet with the data
    print('updating Sales Worksheet...\n')
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print('Sales worksheet updated Successfully.\n')

def calculate_surplus_data(sales_row):
    print('calculating surplus data...\n')
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(f"stock row:  {stock_row}")
    print(f"sales row:  {sales_row}")

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    print(surplus_data)
    return surplus_data

def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print('Welcome to Love Sandwhiches Data Automation')
main()