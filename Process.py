import sqlite3
import unicodedata

conn = sqlite3.connect("finedata.sqlite")
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS WaterStations''')
cur.execute('''DROP TABLE IF EXISTS Wards''')
cur.execute('''DROP TABLE IF EXISTS Charge''')

cur.execute('''CREATE TABLE WaterStations
(id INTEGER PRIMARY KEY, ward_id INTEGER, full_address TEXT UNIQUE, charge_id INTEGER)''')
cur.execute(
    '''CREATE TABLE Wards (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
cur.execute(
    '''CREATE TABLE Charge (id INTEGER PRIMARY KEY, charge TEXT UNIQUE)''')

raw_conn = sqlite3.connect("rawdata.sqlite")
raw_cur = raw_conn.cursor()

raw_cur.execute('''SELECT ward, address, building, charge FROM WaterStation''')
count = 0
for row in raw_cur:
    # Fill in table 'Wards' and get ward ID
    ward_name = row[0].strip()
    # Filter 'non-ward' regions in Tokyo
    if not ward_name.endswith("区"):
        continue
    cur.execute('INSERT OR IGNORE INTO Wards (name) VALUES ( ? )', (ward_name, ))
    conn.commit()
    cur.execute('SELECT id FROM Wards WHERE name = ?', (ward_name, ))
    ward_id = cur.fetchone()[0]

    # Fill in table 'Charge' and get charge ID
    charge_value = ""
    if row[3] == "":
        charge_value = "無料"
    elif "有料" in row[3]:
        charge_value = "有料"
    else:
        charge_value = row[3].strip()
    cur.execute(
        '''INSERT OR IGNORE INTO Charge (charge) VALUES ( ? )''', (charge_value, ))
    conn.commit()
    cur.execute('SELECT id FROM Charge WHERE charge = ?', (charge_value, ))
    charge_id = cur.fetchone()[0]

    # Make full address
    full_address = row[1].strip() + row[2].strip()
    full_address = unicodedata.normalize('NFKC', full_address)
    full_address = full_address.replace("−", "-")

    # Fill in all cleaned up data in table 'WaterStations'
    cur.execute('''INSERT OR IGNORE INTO WaterStations (ward_id, full_address, charge_id) 
    VALUES (?, ?, ?)''', (ward_id, full_address, charge_id))
    conn.commit()
    count = count + 1

raw_conn.close()

cur.execute('''SELECT Wards.name, WaterStations.full_address, Charge.charge FROM WaterStations JOIN Wards JOIN Charge ON WaterStations.ward_id = Wards.id and WaterStations.charge_id = Charge.id''')
for row in cur:
    print(row)
print(count, "records.")

conn.close()
