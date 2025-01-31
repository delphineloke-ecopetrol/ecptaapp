import pathlib
import streamlit as st
import pandas as pd
import os

root_start_path = pathlib.Path.home()
file_path = r"data\summaries.csv"
csv_path = os.path.join(root_start_path, file_path)

df = pd.read_csv(csv_path)
df['Date'] = pd.to_datetime(df['Date'], format='mixed').dt.date
counterparties = df['Counterparty'].unique()
 
# Streamlit App Setup
st.set_page_config(page_title="Meetings Summary Repository", page_icon="📝", layout="wide")
st.title("Meetings Summary Repository 📝")
st.write(" ### Create, update and delete meeting summary entries here!")
# Display DataFrame
st.dataframe(df)

# Main Options
option = st.selectbox(
    "Do you want to create a new entry, update an existing entry, or delete an existing entry?",
    ("Create New", "Update Existing", "Delete Existing")
)

if "attendees" not in st.session_state:
    st.session_state.attendees = []

def add_attendee():
    st.session_state.attendees.append([name, designation, contact, email])
    st.session_state.namewidget = ""
    st.session_state.designationwidget = ""
    st.session_state.contactwidget = ""
    st.session_state.emailwidget = ""
    
if option == "Delete Existing":
    summ_id = st.number_input("Enter Summary ID to delete", step=1, value=None)
    if summ_id in df['Summary ID'].values:
        row_index = df[df['Summary ID'] == summ_id].index[0]
        filtered_row = df.iloc[[row_index]]
        st.write("Entry to delete:")
        st.dataframe(filtered_row)
 
        if st.button("Delete Entry"):
            df.drop(index=row_index, inplace=True)
            df.to_csv(csv_path, index=False)
            st.success(f"Successfully deleted entry with Summary ID {summ_id}!")
    else:
        if summ_id != None:
            st.warning("Summary ID not found in the dataset!")

elif option == "Create New":
    
    new_date = st.date_input("Date:")
    new_counterparty = st.text_input("Enter Counterparty Name:")
    summary = st.text_area("Meeting Summary:")
    st.write("Add new Attendee")

    name = st.text_input("Enter Counterparty Attendees:", key="namewidget")
    designation = st.text_input("Enter Counterparty Designations:", key="designationwidget")
    contact = st.text_input("Enter Counterparty Contact Numbers:", key="contactwidget")
    email = st.text_input("Enter Counterparty Emails:", key="emailwidget")
    
    if st.button("Add Attendee", on_click=add_attendee):
        st.dataframe(pd.DataFrame(st.session_state.attendees, columns=["Name", "Designation", "Contact", "Email"]))
        st.success("Attendee added.")

    if st.button("Add Entry"):
        new_attendees = []
        for particulars in st.session_state.attendees:
            new_attendees.append(", ".join(particulars))
        new_attendees = " | ".join(new_attendees)
        new_entry = {
            "Summary ID": df["Summary ID"].max() + 1 if not df.empty else 1,
            "Date": new_date,
            "Counterparty": new_counterparty,
            "Summary": summary,
            "Attendee(s) Details": new_attendees
        }

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        st.success("Successfully added new entry!")
        st.dataframe(df)
 
elif option == "Update Existing":
    summ_id = st.number_input("Enter Summary ID to edit", step=1, value=None)
    if summ_id in df['Summary ID'].values:
        row_index = df[df['Summary ID'] == summ_id].index[0]
        selected_row = df.loc[row_index]
 
        st.write("Current Entry:")
        st.dataframe(selected_row.to_frame().T)
 
        # Allow Updates
        new_date = st.date_input("New Date:", value=selected_row['Date'])
        new_counterparty = st.text_input("New Counterparty Name:", value=selected_row['Counterparty'])
        summary = st.text_area("New Meeting Summary:", value=selected_row['Summary'])
        attendees = st.text_input("New Attendee(s) Details :", value=selected_row['Attendee(s) Details'])

        if st.button("Update Entry"):
            df.loc[row_index, "Date"] = new_date
            df.loc[row_index, "Counterparty"] = new_counterparty
            df.loc[row_index, "Summary"] = summary
            df.loc[row_index, "Attendee(s) Details"] = attendees

            df.to_csv(csv_path, index=False)
            st.success(f"Successfully updated entry with Summary ID {summ_id}!")
            st.dataframe(df)
    else:
        if summ_id != None:
            st.warning("Summary ID not found in the dataset!")
