import streamlit as st
import sqlite3
import pandas as pd

# Establish connection to SQLite database
conn = sqlite3.connect("data1.db", check_same_thread=False)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL
    )
""")
conn.commit()

def create_record(id, name, phone, address):
    try:
        # Convert ID to integer
        id = int(id)

        # Check if the ID already exists
        cur.execute("SELECT id FROM records WHERE id=?", (id,))
        existing_id = cur.fetchone()
        if existing_id:
            st.error("Record with this ID already exists!")
            return False
        
        # Convert phone to integer
        phone = int(phone)

        # Check if the phone number already exists
        cur.execute("SELECT phone FROM records WHERE phone=?", (phone,))
        existing_phone = cur.fetchone()
        if existing_phone:
            st.error("Record with this Phone number already exists!")
            return False
        
        # Check if the address already exists
        cur.execute("SELECT address FROM records WHERE address=?", (address,))
        existing_address = cur.fetchone()
        if existing_address:
            st.error("Record with this Address already exists!")
            return False
        
        # Check if the phone number is less than 15 characters
        if len(str(phone)) >= 15:
            st.error("Phone number should be less than 15 characters")
            return False
        
        # If ID, phone number, and address pass validation, insert the record
        cur.execute("INSERT INTO records (id, name, phone, address) VALUES (?, ?, ?, ?)", (id, name, phone, address))
        conn.commit()
        return True
    except ValueError:
        st.error("ID and Phone number should be integers")
        return False
    except sqlite3.Error as e:
        st.error(f"Failed to create record: {e}")
        return False


def update_record(id, name, phone, address):
    try:
        # Convert ID to integer
        id = int(id)

        # Check if the provided ID already exists for a different record
        cur.execute("SELECT id FROM records WHERE id=? AND id!=?", (id, id))
        existing_id = cur.fetchone()
        if existing_id:
            st.error("ID already exists for another record!")
            return False
        
        # Convert phone to integer
        phone = int(phone)

        # Check if the phone number already exists for a different record
        cur.execute("SELECT id FROM records WHERE phone=? AND id!=?", (phone, id))
        existing_id = cur.fetchone()
        if existing_id:
            st.error("Phone number already exists for another record!")
            return False
        
        # Check if the address already exists for a different record
        cur.execute("SELECT id FROM records WHERE address=? AND id!=?", (address, id))
        existing_id = cur.fetchone()
        if existing_id:
            st.error("Address already exists for another record!")
            return False
        
        # If all checks pass, update the record
        cur.execute("UPDATE records SET name=?, phone=?, address=? WHERE id=?", (name, phone, address, id))
        conn.commit()
        return True
    except ValueError:
        st.error("ID and Phone number should be integers")
        return False
    except sqlite3.Error as e:
        st.error(f"Failed to update record: {e}")
        return False


def read_records():
    cur.execute("SELECT * FROM records")
    return cur.fetchall()

# def update_record(id, name, phone, address):
#     try:
#         # Check if the provided ID already exists for a different record
#         cur.execute("SELECT id FROM records WHERE id=? AND id!=?", (id, id))
#         existing_id = cur.fetchone()
#         if existing_id:
#             st.error("ID already exists for another record!")
#             return False
        
#         # Check if the phone number already exists for a different record
#         cur.execute("SELECT id FROM records WHERE phone=? AND id!=?", (phone, id))
#         existing_id = cur.fetchone()
#         if existing_id:
#             st.error("Phone number already exists for another record!")
#             return False
        
#         # Check if the address already exists for a different record
#         cur.execute("SELECT id FROM records WHERE address=? AND id!=?", (address, id))
#         existing_id = cur.fetchone()
#         if existing_id:
#             st.error("Address already exists for another record!")
#             return False
        
#         # If all checks pass, update the record
#         cur.execute("UPDATE records SET name=?, phone=?, address=? WHERE id=?", (name, phone, address, id))
#         conn.commit()
#         return True
#     except sqlite3.Error as e:
#         st.error(f"Failed to update record: {e}")
#         return False

def delete_record(id):
    try:
        cur.execute("DELETE FROM records WHERE id=?", (id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Failed to delete record: {e}")
        return False

def page1():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "root":
            st.success("Logged in successfully!")
            st.session_state["page"] = "page2"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def page2():
    background = """
                <style>
                    [data-testid=stAppViewContainer] {
                        background-image: url('wel.jpeg');
                        background-size: cover;
                        text-align: center;
                        border-radius: 30px     
                        }
                        [data-testid=StyledLinkIconContainer]{
                        margin: -20px;
                        margin-left: 20px             
                        }
                </style>
                """

    st.markdown(background, unsafe_allow_html=True)

    st.image('well.png')
    if st.button("Continue"):
        st.session_state["page"] = "page3"
        st.experimental_rerun()

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "page1"

    if st.session_state["page"] == "page1":
        page1()
    elif st.session_state["page"] == "page2":
        page2()
    elif st.session_state["page"] == "page3":
        # Display Options for CRUD Operations
        option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete"))

        # Perform Selected CRUD Operations
        if option == "Create":
            st.subheader("Create a Record")
            id = st.text_input("Enter ID")
            name = st.text_input("Enter Name")
            phone = st.text_input("Enter Phone")
            address = st.text_input("Enter Address")
            if st.button("Create"):
                if create_record(id, name, phone, address):
                    st.success("Record Created Successfully!!!")

        elif option == "Read":
            st.subheader("Read Records")
            records = read_records()
            if not records:
                st.write("No records to display")
            else:
                column_names = ["ID", "Name", "Phone", "Address"]  # Define column names
                df = pd.DataFrame(records, columns=column_names)
                st.dataframe(df)

        elif option == "Update":
            st.subheader("Update a Record")
            id = st.text_input("Enter ID")
            name = st.text_input("Enter New Name")
            phone = st.text_input("Enter New Phone")
            address = st.text_input("Enter New Address")
            if st.button("Update"):
                if update_record(id, name, phone, address):
                    st.success("Record Updated Successfully!!!")

        elif option == "Delete":
            st.subheader("Delete a Record")
            id = st.text_input("Enter ID")
            if st.button("Delete"):
                if delete_record(id):
                    st.success("Record Deleted Successfully!!!")

if __name__ == "__main__":
    main()
