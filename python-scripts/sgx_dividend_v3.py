import traceback

import requests,re
import datetime
import pytz
import pyodbc

tzz = pytz.timezone('Asia/Singapore')
asia_time = datetime.datetime.now(tzz)

columns=('Security Name,Type,Date,Record date,Payment date,Particulars,currency,details,symbol'
         ',short_name,symbol_curr,exchange_rate,link,market,FetchDate').split(',')
date_columns = ['Date', 'Record date', 'Payment date']

tbl = requests.get('https://links.sgx.com/FileOpen/{}%20{}%20{}.ashx?App=ISINCode&FileID=1'.format(
    datetime.datetime.today().day, datetime.datetime.now().strftime("%b"), datetime.datetime.today().year)).text

#########################


map={
'GBP'	:'GBP',
'USD'	:'USD',
'SGD'	:'SGD',
'A$'	:'AUD',
'US$'	:'USD',
'SG$'	:'SGD',
'S$'	:'SGD',
'EUR'	:'EUR',
'CNY'	:'CNY',
'HK$'	:'HKD',
'MYR'	:'MYR',
'THB'	:'THB'}



server = '139.99.20.45'
database = 'fundamental'
username = 'fundamental_admin'
password = 'ADLYWIJJxbwBffgg&sca'
table = 'corporate_action'


columns_to_add = {
    "Security Name": "VARCHAR(255)",  # Change data type as needed
    "Record date": "DATETIME",
    "Payment date": "DATETIME",
    "Particulars": "VARCHAR(255)",
    "short_name": "VARCHAR(100)",
    "symbol_curr": "VARCHAR(50)",
    "exchange_rate": "FLOAT",
    "link": "VARCHAR(255)"
}

try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    for column_name, column_type in columns_to_add.items():
        # Check if the column exists
        check_column_query = f"""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table}' AND COLUMN_NAME = '{column_name}'
        """
        cursor.execute(check_column_query)
        column_exists = cursor.fetchone()[0]

        # If the column does not exist, add it
        if column_exists == 0:
            add_column_query = f"""
            ALTER TABLE {table}
            ADD [{column_name}] {column_type} NULL
            """
            cursor.execute(add_column_query)
            print(f"Added column: {column_name} ({column_type})")
        else:
            print(f"Column already exists: {column_name}")
        conn.commit()
except:
    traceback.print_exc()
finally:
    conn.close()



try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # Fetch existing links from the database
    sql = f"SELECT link FROM {table}"
    cursor.execute(sql)

    old_links = []
    myresult = cursor.fetchall()
    for tup in myresult:
            try:
                old_links.append(tup[0])
            except:
                pass

    for page in range(3):
        resp = requests.get(
            'https://api.sgx.com/corporateactions/v1.0?pagestart={}&pagesize=100&params=id%2CanncType%2CdatePaid%2CexDate%2Cname%2Cparticulars%2CrecDate'.format(
                page)).json()

        for r in resp['data']:
            row = {}
            row[columns[0]] = r['name']
            row[columns[1]] = r['anncType']
            row[columns[2]] = r['exDate']
            row[columns[3]] = r['recDate']
            row[columns[4]] = r['datePaid']

            try:
                row[columns[2]] = datetime.datetime.fromtimestamp(
                    int(str(row[columns[2]])[:10]), tz=tzz).date()
            except:
                pass
            try:
                row[columns[3]] = datetime.datetime.fromtimestamp(
                    int(str(row[columns[3]])[:10]), tz=tzz).date()
            except:
                pass
            try:
                row[columns[4]] = datetime.datetime.fromtimestamp(
                    int(str(row[columns[4]])[:10]), tz=tzz).date()
            except:
                pass

            row[columns[5]] = r['particulars']

            if row['Type'] == 'DIVIDEND' and 'Rate: NA NA' in row['Particulars']:
                continue
            if row['Type'] == 'DIVIDEND' and row['Payment date'] == '-':
                continue

            if len(re.findall(r"[0-9] Cash Options", row['Particulars'])) > 0:
                for line in requests.get(
                        'https://links.sgx.com/1.0.0/corporate-actions/{}'.format(r['id'])).text.splitlines():
                    if 'Declared Rate:' in line:
                        row['Particulars'] = line.strip().split('<br />')[0]
                        break

            for key, value in row.items():
                if str(value) == 'None' and key != 'Security Name': row[key] = '-'
            row['symbol'] = '-'
            row['short_name'] = '-'
            for lin in tbl.splitlines():
                if row['Security Name'] in lin:
                    cells = lin.split('      ')
                    row['symbol'] = cells[-2].strip()
                    row['short_name'] = cells[-1].strip()
            row['symbol_curr'] = 'SGD'
            row['currency'] = '-'
            row['details'] = '-'
            row['exchange_rate'] = '-'
            if 'Per Security' in row['Particulars'] or 'Declared Rate:' in row['Particulars']:
                row['currency'] = row['Particulars'].split(':')[1].split()[0]
                row['details'] = row['Particulars'].split(':')[1].split()[1]
            for key, value in map.items():
                if key in row['short_name'].split() or value in row['short_name'].split():
                    row['symbol_curr'] = value
            if row['symbol_curr'] == row['currency']:
                row['exchange_rate'] = '1'
            else:
                if row['symbol_curr'] != '-':
                    try:
                        rte = float(row['details'])
                        curr = requests.get(
                            'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{}.json'.format(
                                row['currency'].lower())).json()[row['currency'].lower()][row['symbol_curr'].lower()]
                        row['exchange_rate'] = curr
                    except:
                        pass

            row['link'] = 'https://links.sgx.com/1.0.0/corporate-actions/{}'.format(r['id'])
            row['market'] = 'SES'  # Static value for market

            row['FetchDate'] = asia_time.strftime('%Y-%m-%d')
            row['Date'] = row['Date'].strftime('%Y-%m-%d') if isinstance(row['Date'], datetime.date) else row[
                'Date']
            row['Record date'] = row['Record date'].strftime('%Y-%m-%d') if isinstance(row['Record date'],
                                                                                       datetime.date) else row[
                'Record date']
            row['Payment date'] = row['Payment date'].strftime('%Y-%m-%d') if isinstance(row['Payment date'],
                                                                                         datetime.date) else row[
                'Payment date']
            # Handle '-' and format valid dates
            for col in date_columns:
                if row[col] == '-':  # Replace '-' with None
                    row[col] = None
                elif row[col] and isinstance(row[col], datetime.date):  # Format valid date objects
                    row[col] = row[col].strftime('%Y-%m-%d')

            # Clean and validate 'exchange_rate'
            if row['exchange_rate'] in ['-', None]:  # Replace invalid values
                row['exchange_rate'] = None
            else:
                try:
                    row['exchange_rate'] = float(row['exchange_rate'])  # Convert valid values to float
                except ValueError:
                    row['exchange_rate'] = None  # Handle non-convertible values

            if row['symbol'] != '-' and not row['symbol'].endswith('.SI'):
                row['symbol'] += '.SI'

            tul = tuple(row[col] for col in columns)

            # Insert new records into MSSQL database
            if row['link'] not in old_links:
                sql = f"""
                INSERT INTO {table} 
                ([Security Name], [Type], [date], [Record date], [Payment date], [Particulars], [currency], [details], 
                [symbol], [short_name], [symbol_curr], [exchange_rate], [link], [market], [FetchDate]) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                try:
                    cursor.execute(sql, tul)
                except:
                    traceback.print_exc()
                    conn.rollback()
                    pass
                conn.commit()
            else:
                print('OLD --> ' + str(tul))

except:
    traceback.print_exc()
finally:
    conn.close()