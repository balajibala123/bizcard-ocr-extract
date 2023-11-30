## Problem Statement

The goal of this project is to create an interactive Streamlit application enabling users to upload images of business cards for automated text extraction using EasyOCR. The extracted information includes critical details such as company name, cardholder name, designation, contact information, and address. Users can seamlessly store this extracted data into a MySQL database, supporting multiple entries. Additionally, they can perform read, update, and delete operations on the stored business card data through a user-friendly graphical interface. The emphasis is on a clean UI design and robust database management to ensure an intuitive experience and efficient data handling.

## Required Libraries

import streamlit as st
from pathlib import Path
import pandas as pd
from bizcard import processed_data, SingleUpload, cursor
import base64
import easyocr
import mysql.connector
import re

## Extract Data
Single Image Extract: Upload a single image to extract text data. Click to save the extracted data in the MYSQL database.
Multi Image Extract: Upload multiple images to extract text data and save it in the MYSQL database.

## Modify
Update Data: Modify the stored data in the MySQL database by selecting the Email Address.

## Delete
Delete Data: Remove specific data from the MySQL database by selecting the Email Address.

## Getting Started

To start with the Business Card Data Extraction project, follow these steps:

Clone the Repository:

Begin by cloning this GitHub repository to your local machine. Use the following command:
git clone 
Create the .env File for MySQL Connection:

Create a new file named .env within your project directory.
Enter the following details in the .env file, replacing the placeholder values with your MySQL connection details:

MYSQL_HOST_NAME = 'Enter Your MySQL Host Name'
MYSQL_USER_NAME = 'Enter Your MySQL User Name'
MYSQL_PASSWORD = 'Enter Your MySQL Password'
MYSQL_DATABASE_NAME = 'Enter Your MySQL Database Name'

Save the .env file once you've entered your actual MySQL database connection information.

Install Required Libraries:

Ensure you have the necessary Python libraries installed. You can find the required libraries in the "Required Libraries" section of this README. Use pip for installation.
Run the Business Card Extraction App:

Open your terminal or command prompt and navigate to the project directory.
Execute the command:
streamlit run main.py
This command will start the Streamlit application.
Utilize the Business Card Extraction App:

Once the app is launched, follow the instructions in the app for extracting data, modifying, deleting, and performing MySQL queries directly.

Now you're all set to use the Business Card Data Extraction app, managing and analyzing data from business cards with ease.