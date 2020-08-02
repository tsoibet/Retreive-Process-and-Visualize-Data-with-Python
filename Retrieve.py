import sqlite3
import urllib.request
import urllib.error
import ssl
import csv
import io

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect("rawdata.sqlite")
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS WaterStation''')
cur.execute('''CREATE TABLE WaterStation
(id INTEGER PRIMARY KEY, ward TEXT, building TEXT, address TEXT, location TEXT, charge TEXT, drinktype TEXT)''')

dataurl = "https://www.opendata.metro.tokyo.lg.jp/waterworks/2019tokyowaterdrinkingstation.csv"
try:
    response = urllib.request.urlopen(dataurl, None, 30, context=ctx)
    if response.getcode() != 200:
        print("Error code: ", response.getcode())
    text = response.read().decode(encoding='SHIFT_JIS')
    csvdata = csv.reader(io.StringIO(initial_value=text))
    count = 0
    for row in csvdata:
        print(row)
        ward = row[0]
        building = row[1]
        address = row[2]
        location = row[3]
        charge = row[4]
        drinktype = row[5]
        cur.execute('''INSERT OR IGNORE INTO WaterStation (ward, building, address, location, charge, drinktype)
                       VALUES (?, ?, ?, ?, ?, ?)''', (ward, building, address, location, charge, drinktype))
        count = count+1
    print(count, "records.")
    conn.commit()
except KeyboardInterrupt:
    print("\nProgram interrupted by user...")
except Exception as e:
    print("Unable to retrieve data...")
    print("Error message: ", e)
conn.commit()
cur.close()
