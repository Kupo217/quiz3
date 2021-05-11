# This is a program to get photos made by mars rover(API is provided by NASA)
import requests
import json
import sqlite3

# Date when the photo was made(Earth date)
# Not all the dates work, for instance, you can use 2015-5-16(Already checked date)

earth_date = input("Enter a date in format YYYY-MM-DD: ")
payload = {'api_key': '57siWL3kv2YqgleQ7nnpmuedl7wGrrAuSELHuRRs', 'earth_date': earth_date}
r = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos', params=payload)

# Each result returns 25 photos
print(f'Status Code of get request: {r.status_code}\n')
print(f'Information about data type: {r.headers}\n')
result = json.loads(r.text)
print(json.dumps(result, indent=4))

# Here you enter a number of photos that you want to get, not to get all 25 photos
i = 0
photo_set = set()

num_photo = int(input("Enter a number of photos(max. 25): "))
while i < num_photo:
    img_src = result['photos'][i]['img_src']
    photo_set.add(img_src)
    i += 1

# Getting images

name = 'mri1'
index = 2
for each in photo_set:
    r_img = requests.get(each)
    with open(f'{name}.jpg', 'wb') as f:
        f.write(r_img.content)
    name = 'mri'
    name += str(index)
    index += 1

# Creating database to store img url and the date when the photo was made

con = sqlite3.connect('mri.db')
cur = con.cursor()

cur.execute('''CREATE TABLE "mars_images" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	img_src TEXT(150),
	date TEXT(30)
);''')

for url in photo_set:
    cur.execute("INSERT INTO mars_images(img_src, date) VALUES (?, ?)", (url, earth_date))

con.commit()

con.close()
