import sqlite3
import urllib.request
import urllib.error
import re
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dataurl = "https://www.opendata.metro.tokyo.lg.jp/waterworks/2019tokyowaterdrinkingstation.csv"
try:
    response = urllib.request.urlopen(dataurl, None, 30, context=ctx)
    text = response.read().decode(encoding="SHIFT-JIS")
    if response.getcode() != 200:
        print("Error code: ", response.getcode())
    print(len(text), "characters retrieved.")
    # print(text)
except KeyboardInterrupt:
    print("\nProgram interrupted by user...")
except Exception as e:
    print("Unable to retrieve data...")
    print("Error message: ", e)
