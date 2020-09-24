from faces import person_name


import gspread

from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('project_secret_key.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Employee attendance system').sheet1



zaposleni = ['nebojsatutic']

if person_name in zaposleni:
    row = []
    time = datetime.now().strftime("%H:%M:%S, %m/%d/%Y")
    row_one = 'Name: ' + person_name + " time: " + time
    row.append(row_one)
    index = 1
    sheet.insert_row(row, index)
    index+1
else:
    print('Osoba ' + person_name + ' se ne nalazi na spiski zaposlenih! ')


# while True:
#     row = []
#     name = person_name
#     time = datetime.now().strftime("%H:%M:%S, %m/%d/%Y")
#     row_one = name + " time: " + time
#     row.append(row_one)
#     index = 1
#     sheet.insert_row(row, index)
#     index+1

