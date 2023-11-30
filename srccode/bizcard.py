import easyocr
from pathlib import Path
import mysql.connector
from tabulate import tabulate
import pandas as pd
import re


def SingleUpload(path):
    # path = "../BIZ_IMAGES/2.png"
    data =[]
    reader = easyocr.Reader(['en'])
        
    result = reader.readtext(path, detail=0)
    data.append(result)

    return data


def processed_data(data):
# path = "../BIZ_IMAGES"

    lis = []
    for j in data:
        data1 = j[2:]
        info = {}
        info['Name'] = j[0]
        info['Designation'] = j[1]

        nums = ""
        address = ""
        website = ""
        companyName = ""
        
        for i in data1:
            # phone numbers
            if re.findall(r'\+\d{1,}-\d{3,}-\d{4,}', i) or re.findall(r'\d{1,}-\d{3,}-\d{4,}', i):
                nums = nums+ " " +i
                info['PhoneNumbers'] = nums


            elif re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', i):
                info['emails'] = i

            # Extracting website address
            elif  re.findall(r'\bwww\b',i, re.IGNORECASE) or re.findall(r'\b.com\b', i) and not re.findall(r'\bglobal\s*\d+', i):
                website = website+i
            
            # Extracting address
            elif re.findall(r'\d{6}', i) or re.findall(r'\d{3}', i) or 'Erode' in i or 'St' in i:
                numbers = ''.join(char for char in i if char.isdigit())
                characters = ''.join(char for char in i if not char.isdigit()) 
                address = address+i
            
            # Extacting company name
            else:
                companyName = companyName+ " " +i
            

        if website:
            website = website.replace('www', 'www.')
            website = website.replace('WWW', 'WWW.')
            website = website.replace('com', '.com')
            website = website.replace('..', '.')
            website = website.replace(' ', '')
            info['website'] = website

        if address:
            updated_address =  re.sub(r'(global)(\w+)', r'\1 St ,\2', address) 
            updated_address = re.sub(r'St\s*,\s*$', '', updated_address)
            updated_address = re.sub(r'(\D|^)(\d{6})', r'\1, \2', updated_address, 1)
            updated_address = re.sub(r',', r', ', updated_address, 1) 


            if 'global' in updated_address:
                info['Area'] = updated_address.split(',')[0]
                info['City'] = updated_address.split(',')[1]
                info['State'] = updated_address.split(',')[2]
                info['Pincodes'] = updated_address.split(',')[-1].strip()

            elif ',,' in address or ";" in address or " " in address:
                
                address = re.sub(r'(\D|^)(\d{6})', r'\1, \2', updated_address, 1)
                address = address.replace(',,', ',')
                address = address.replace(';', ',')
                address = address.replace(', ,', ',')
                info['Area'] = address.split(',')[0]
                info['City'] = address.split(',')[1]
                info['State'] = address.split(',')[2]
                info['Pincodes'] = address.split(',')[-1].strip()

        if companyName:
            info['CompanyName'] = companyName


        lis.append(info)

    return lis

# def cursor():
#     db = mysql.connector.connect(
#         host = 'localhost',
#         user = 'root',
#         password = 'balaji',
#         database = 'bizcard'
#     )

#     mycursor = db.cursor(buffered= True)
#     print(mycursor)
#     db.commit()

#     return db, mycursor


      

    