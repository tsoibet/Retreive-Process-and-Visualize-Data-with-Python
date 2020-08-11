import sqlite3
import urllib.request
import urllib.parse
import json
import time
import os

serviceurl = "http://py4e-data.dr-chuck.net/json?"
parameter = dict()
parameter["key"] = os.environ.get("APIKEY")

conn = sqlite3.connect("finedata.sqlite")
cur = conn.cursor()
cur.execute('''SELECT full_address FROM WaterStations''')
result = cur.fetchall()

fhand = open('Map.js', 'w')
fhand.write("mapdata = [\n")

count = 0
for row in result:
    parameter["address"] = row[0]
    url = serviceurl + urllib.parse.urlencode(parameter)
    response = urllib.request.urlopen(url)
    print('Retrieving', url)
    data = response.read().decode()
    try:
        js = json.loads(data)
    except:
        print('Failure to retrieve. Data:')
        print(data)
        continue
    if 'status' not in js or js['status'] != 'OK':
        print('Failure to retrieve. Data:')
        print(data)
        continue
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0:
        continue
    print(row[0], lat, lng)
    count = count + 1
    if count > 1:
        fhand.write(",\n")
    fhand.write("["+str(lat)+","+str(lng)+",'"+row[0]+"']")

    if count % 10 == 0:
        time.sleep(5)
fhand.write("\n];")

fhand.close()
conn.close()

print(count, "records written to Map.js")
