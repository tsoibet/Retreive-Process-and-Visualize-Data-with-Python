import sqlite3

conn = sqlite3.connect("finedata.sqlite")
cur = conn.cursor()
# Number of water stations in each ward
ward_dict = dict()
cur.execute('''SELECT * FROM Wards''')
result = cur.fetchall()
ward_list = list()
for row in result:
    wardname = row[1]
    ward_list.append(wardname)
    cur.execute(
        '''SELECT COUNT(*) FROM WaterStations WHERE ward_id = ?''', (row[0], ))
    re = cur.fetchone()
    number_of_WS = re[0]
    ward_dict[wardname] = number_of_WS
print(ward_list, ward_dict)

conn.close()

fhand = open('Barchart.js', 'w')
fhand.write(
    "barchartdata = [ ['Ward', 'Number of water drinking stations']")
for ward in ward_list:
    number = ward_dict.get(ward)
    fhand.write(",\n['"+ward+"',"+str(number)+"]")

fhand.write(" ];")
fhand.close()

print("Data written to Barchart.js")
