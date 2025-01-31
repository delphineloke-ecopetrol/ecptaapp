import streamlit as st
import pandas as pd
import datetime as dt

ta_database_path = "data/ta_database.csv"
daily_ta_path = "data/daily_ta.csv"

ta_database = pd.read_csv(ta_database_path).sort_values(by=["start_date", "end_date"], ascending=[False, False])
ta_database['start_date'] = pd.to_datetime(ta_database['start_date'], format='mixed').dt.date
ta_database['end_date'] = pd.to_datetime(ta_database['end_date'], format='mixed').dt.date
daily = pd.read_csv(daily_ta_path, low_memory=False)
ref_lst = ta_database["Name"].sort_values(ascending=True).unique()

def get_ref_id(refinery, col):
    row_index = ta_database[ta_database['Name'] == refinery].index[0]
    id = ta_database.at[row_index, col]
    return id

def make_daily_ta(ta_database_path, daily_ta_path):
    expanded_rows = []
    outages_grouped_df = pd.read_csv(ta_database_path)
    for _, row in outages_grouped_df.iterrows():
        date_range = pd.date_range(start=row["start_date"], end=row["end_date"])
        for date in date_range:
            expanded_rows.append({
                "Outage ID": row["Outage ID"],
                "Platts Outage ID": row["Platts Outage ID"],
                "ECPTA ID": row["ECPTA ID"],
                "Name": row["Name"],
                "Country": row["Country"],
                "Planning Status": row["Planning Status"],
                "Unit": row["Unit"],
                "Date": date,
                "Volume": row["Volume"]
            })
    
    expanded_df = pd.DataFrame(expanded_rows)
    expanded_df.to_csv(daily_ta_path, index=False)

# Streamlit App
st.set_page_config(page_title="Turnarounds Database 🏭", page_icon="🏭", layout="wide")
st.title("Turnarounds Database 🏭")
st.write(" ### Create, update and delete refinery turnaround entries here!")

# Display DataFrame (optional)
st.write("Initial Database")
st.dataframe(ta_database)

st.subheader("Search by Refinery")
refinery_name = st.selectbox("Select Refinery: ", ref_lst)

if refinery_name in ta_database['Name'].values:
        filtered_grouped = ta_database[(ta_database['Name'] == refinery_name)]
        st.dataframe(filtered_grouped)
else:
     st.error("Refinery not found.")

st.subheader("Update Refinery Turnaround Entries")
option = st.selectbox("Do you want to create a new entry, update an existing entry, or delete an existing entry for this refinery?", 
                      ("Create New", "Update Existing", "Delete Existing"))
entries = []
# Create New Entry
if option == "Create New":
    new_start_date = st.date_input("Start Date: ", "today", format="YYYY-MM-DD")
    new_end_date = st.date_input("End Date: ", "today", format="YYYY-MM-DD")
    new_status = st.selectbox("Planning Status: ", ("Planned", "Unplanned"))
    new_unit = st.selectbox("Unit: ", ("CDU", "HCU", "FCU", "Coker", "Reformer"))
    new_volume = st.number_input("Outage Volume (KBD): ", value=None)
    new_outage_id = max(ta_database['Outage ID']) + 1
    new_ref_id = get_ref_id(refinery_name, 'ECPTA ID')
    new_country = get_ref_id(refinery_name, 'Country')

    row ={'Outage ID': new_outage_id, 'Platts Outage ID': '', 'ECPTA ID': new_ref_id, 'Name': refinery_name, 'Country': new_country, 'Planning Status': new_status, 'Unit': new_unit, 
           'start_date': new_start_date, 'end_date':new_end_date, 'Volume': new_volume, 'Edited': 'Yes'}
    entries.append(row)

    if st.button("Add Turnaround to Database"):
        entries_df = pd.DataFrame(entries, columns=['Outage ID', 'Platts Outage ID', 'ECPTA ID', 'Name', 'Country', 'Planning Status', 'start_date', 'end_date',
                                                                          'Volume', 'Edited'])
        if new_end_date >= new_start_date:
            st.dataframe(entries_df)   
            ta_database = pd.concat([ta_database, entries_df])  
            st.success("Entry successfully inserted into Database!")

            ta_database.to_csv(ta_database_path, index=False)
            make_daily_ta(ta_database_path, daily_ta_path)

# Delete Existing Entry
elif option == "Delete Existing":
    outage_id = st.number_input("Enter Outage ID to delete", step=1, value=None)
    if outage_id in ta_database["Outage ID"].values:
        row_index = ta_database[ta_database['Outage ID'] == outage_id].index[0]
        filtered_row = ta_database.loc[row_index]
        st.write("Entry to delete:")
        st.dataframe(filtered_row)
        
        if st.button("Delete Entry"):
            ta_database.drop(index=row_index, inplace=True)
            ta_database.to_csv(ta_database_path, index=False)
            st.success(f"Successfully deleted entry with Outage ID {outage_id}!")
    else:
        if outage_id != None:
            st.warning("Summary ID not found in the dataset!")

# Update Existing Entry
else:
    outage_id = st.number_input("Enter Outage ID to replace", step=1, value=None)
    
    if outage_id in ta_database['Outage ID'].values:
        row_index = ta_database[ta_database['Outage ID'] == outage_id].index[0]
        selected_row = ta_database.loc[row_index]

        st.write("Current Entry:")
        st.dataframe(selected_row.to_frame().T)

        new_status = st.selectbox("Planning Status: ", ("Planned", "Unplanned"))
        new_unit = st.selectbox("Unit: ", ("CDU", "HCU", "FCU", "Coker", "Reformer"))
        new_start_date = st.date_input("Start Date: ", "today", format="YYYY-MM-DD")
        new_end_date = st.date_input("End Date: ", "today", format="YYYY-MM-DD")
        new_volume = st.number_input("Outage Volume (KBD): ", value=selected_row['Volume'])

        if st.button("Update Entry"):
        
                ta_database.at[row_index, 'start_date'] = new_start_date
                ta_database.at[row_index, 'end_date'] = new_end_date
                ta_database.at[row_index, 'Volume'] = new_volume
                ta_database.at[row_index, 'Edited'] = 'Yes'
                filtered_grouped = ta_database[(ta_database['Name'] == refinery_name)]
                filtered_grouped = filtered_grouped.sort_values(by=['start_date', 'end_date', 'Outage ID', 'Edited'], ascending=[ False, False, True, False])
                st.success("Existing entry updated in database!")
                st.dataframe(filtered_grouped)

                ta_database.to_csv(ta_database_path, index=False)
                make_daily_ta(ta_database_path, daily_ta_path)
    else:
        if outage_id != None:
            st.warning("Summary ID not found in the dataset!")

    
