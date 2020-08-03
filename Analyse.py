import sqlite3

conn = sqlite3.connect("finedata.sqlite")
cur = conn.cursor()

# Number of water stations in each ward
ward_dict = dict()
cur.execute('''SELECT * FROM Wards''')
result = cur.fetchall()
for row in result:
    wardname = row[1]
    cur.execute(
        '''SELECT COUNT(*) FROM WaterStations WHERE ward_id = ?''', (row[0], ))
    re = cur.fetchone()
    number_of_WS = re[0]
    ward_dict[wardname] = number_of_WS
print(ward_dict)


conn.close()
