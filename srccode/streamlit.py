import streamlit as st
from pathlib import Path
import pandas as pd
from DatabaseConnection import cursor
from bizcard import processed_data, SingleUpload
import base64


st.set_page_config(layout="wide")

st.title("BIZ-CARD EXTRACTION USING STREAMLIT PYTHON")

# Create a sidebar with an options menu
selected_option = st.sidebar.selectbox(
    'Select an option',
    ('Home Page', 'Single Image Upload', 'Multiple Image Uploads', 'Modify Data', 'Delete Data')
)

if selected_option == "Home Page":
    st.subheader("Biz Card Data extraction")
    st.write("The goal of this project is to create an interactive Streamlit application enabling users to upload images of business cards for automated text extraction using EasyOCR. The extracted information includes critical details such as company name, cardholder name, designation, contact information, and address. Users can seamlessly store this extracted data into a MySQL database, supporting multiple entries. Additionally, they can perform read, update, and delete operations on the stored business card data through a user-friendly graphical interface. The emphasis is on a clean UI design and robust database management to ensure an intuitive experience and efficient data handling.")
    st.image("thumbnail.png")


elif selected_option == "Single Image Upload":
    st.title("Single Image Upload")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"])

    # Check if an image has been uploaded
    if uploaded_file is not None:
       
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

       
        img_bytes = uploaded_file.read()
        binary_data = base64.b64encode(img_bytes).decode('utf-8')

        data = SingleUpload(img_bytes)
        df = pd.DataFrame(processed_data(data))
        df['ImageBinary'] = binary_data
        st.write(df)

        if st.button("INSERT INTO MYSQL"):
            db, mycursor = cursor()
            mycursor.execute("""create table if not exists carddetails (
                            Name varchar(255), Designation varchar(255), PhoneNumbers varchar(255), 
                            emails varchar(255) primary key, website varchar(255), Area varchar(255), City varchar(255), State varchar(255),
                            pincodes varchar(255),CompanyName varchar(255), ImageBinary LONGTEXT
            )""")

            sql = (""" insert into carddetails (Name, Designation, PhoneNumbers, emails, website, Area, City, State, pincodes, 
                    CompanyName, ImageBinary) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    on duplicate key update
                    Name = values(Name), Designation = values(Designation), PhoneNumbers = values(PhoneNumbers),
                    website = values(website), Area = values(Area), City = values(City), State = values(State), pincodes = values(pincodes),
                    CompanyName = values(Companyname), ImageBinary = values(ImageBinary)
                    """)
            for i in df.to_records(index=False).tolist():
                    # st.write(i)
                    mycursor.execute(sql, i)
                


            db.commit()
            db.close()
            st.success("Data Inserted Successfully")

elif selected_option == "Multiple Image Uploads":
    st.title("Multiple Image Upload")

    uploaded_files = st.file_uploader("Choose multiple images...", type=["jpg", "png"], accept_multiple_files=True)

    # Check if images have been uploaded
    if uploaded_files is not None and len(uploaded_files) > 0:
        dfs = []  # List to store DataFrames for each uploaded file

        for uploaded_file in uploaded_files:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
            st.write("File Path:", uploaded_file.name)

            img_byte = uploaded_file.read()
            binary_data = base64.b64encode(img_byte).decode('utf-8')

            # Process the data and create a DataFrame
            data = SingleUpload(img_byte)
            df = pd.DataFrame(processed_data(data))

            # Add a new column "ImageBinary" with the binary data
            df['ImageBinary'] = binary_data

            # Append the DataFrame to the list
            dfs.append(df)

        # Concatenate DataFrames for each uploaded file
        final_df = pd.concat(dfs, ignore_index=True)

        # Display the resulting DataFrame
        st.write(final_df)

        if st.button("INSERT INTO MYSQL"):
            db, mycursor = cursor()
            mycursor.execute("""create table if not exists carddetails (
                            Name varchar(255), Designation varchar(255), PhoneNumbers varchar(255), 
                            emails varchar(255) primary key, website varchar(255), Area varchar(255), City varchar(255), State varchar(255),
                            pincodes varchar(255),CompanyName varchar(255), ImageBinary LONGTEXT
            )""")

            sql = (""" insert into carddetails (Name, Designation, PhoneNumbers, emails, website, Area, City, State, pincodes, 
                    CompanyName, ImageBinary) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    on duplicate key update
                    Name = values(Name), Designation = values(Designation), PhoneNumbers = values(PhoneNumbers),
                    website = values(website), Area = values(Area), City = values(City), State = values(State), pincodes = values(pincodes),
                    CompanyName = values(Companyname), ImageBinary = values(ImageBinary)
                    """)
            for i in final_df.to_records(index=False).tolist():
                    mycursor.execute(sql, i)


            db.commit()
            db.close()
            st.success("Data Inserted Successfully")

elif selected_option == "Modify Data":
    st.title("Modify Data")

    # Get email input from user
    new_email = st.text_input("Enter email:")

    with st.form(key="submit changes form"):
        db, mycursor = cursor()
        mycursor.execute("SELECT * FROM carddetails WHERE emails = %s", (new_email,))
        out = mycursor.fetchall()

        for row in out:
            new_name = st.text_input("Name", row[0], key="name")
            new_designation = st.text_input("Designation", row[1], key="designation")
            new_PhoneNumbers = st.text_input("PhoneNumbers", row[2], key="phonenumber")
            new_website = st.text_input("website", row[3], key="Website")
            new_Area = st.text_input("Area", row[5], key="area")
            new_City = st.text_input("City", row[6], key="city")
            new_State = st.text_input("State", row[7], key="state")
            new_pincodes = st.text_input("Pincodes", row[8], key="pincodes")
            new_CompanyName = st.text_input("CompanyName", row[9], key="companyname")
        if st.form_submit_button("Submit Changes"):
            # Update Statement with placeholders
            update_query = """
                UPDATE carddetails
                SET 
                    Name = COALESCE(%s, Name),
                    Designation = COALESCE(%s, Designation),
                    PhoneNumbers = COALESCE(%s, PhoneNumbers),
                    website = COALESCE(%s, website),
                    Area = COALESCE(%s, Area),
                    City = COALESCE(%s, City),
                    State = COALESCE(%s, State),
                    pincodes = COALESCE(%s, pincodes),
                    CompanyName = COALESCE(%s, CompanyName)
                    
                WHERE emails = %s"""
            
            db,mycursor = cursor()
            mycursor.execute(
                update_query,
                (
                    new_name or None,  # None if new_name is not provided
                    new_designation or None,  # None if new_designation is not provided
                    new_PhoneNumbers or None,  # None if new_PhoneNumbers is not provided
                    new_website or None,  # None if new_website is not provided
                    new_Area or None,  # None if new_Area is not provided
                    new_City or None,  # None if new_City is not provided
                    new_State or None,  # None if new_State is not provided
                    new_pincodes or None,  # None if new_pincodes is not provided
                    new_CompanyName or None,  # None if new_CompanyName is not provided
                    new_email,
                ),
            )

            # # Commit the changes to the database
            db.commit()
            mycursor.close()
            db.close()

            st.success("Changes Submitted Successfully")

elif selected_option == "Delete Data":
    st.title("Delete Data Using Email")

    # Get email input from user
    new_email = st.text_input("Enter email:")

    # Delete Statement with placeholders
    delete_query = """
        DELETE FROM carddetails
        WHERE emails = %s
    """
    with st.form(key="Delete Data form"):
        if st.form_submit_button("Delete Button"):
            # Execute the delete query with the input value
            db,mycursor = cursor()
            mycursor.execute(delete_query, (new_email,))

            # Commit the changes to the database
            db.commit()
            db.close()

            st.success("Deleted Data Successfully")







