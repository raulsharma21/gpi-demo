import streamlit as st
import pandas as pd
import os
from Home import mapLocally

# button functionality
def updateReportFile():
    report = pd.read_excel("./app/data/Freight Analytics Export.xlsx")
    # print(report.sort_values(by='Profit Center'))

    for i in range(len(report)):
        # print(report.iloc[i]['Profit Center'])
        if(report.iloc[i]['Profit Center']=='Undefined'):
            shipment_num = report.iloc[i]['Shipment Num']

            rows =  st.session_state.mapped_df[st.session_state.mapped_df['Shipment Num'] == shipment_num]
            if len(rows) == 0:
                continue
                # print("No mapping")

            elif len(rows) == 1:
                print(shipment_num, rows['Profit Center Code'].values[0])
                # st.session_state.mapped_df.loc[report.iloc[i]['Shipment Num']]
                report.at[i, 'Profit Center'] = rows['Profit Center Code'].values[0]
            else:
                continue
                # print("Shippment Num overlap")

    # print(report.sort_values(by='Profit Center'))
    report.to_excel("./app/data/updated data.xlsx", index=False)

def addMappings():
    old_mappings = pd.read_excel("./app/data/Profit Center Overrides.xlsx")
#  print(old_mappings.columns.to_list)

    # print(st.session_state.unmapped_data['edited_rows'])
    # print(st.session_state.unmapped_df.columns.to_list)
    
    new_mappings = []
    row = []
    for i in st.session_state.unmapped_data['edited_rows']:
        row.append(st.session_state.unmapped_data['edited_rows'][i]['Profit Center Code'])
        row.append(st.session_state.unmapped_df.at[i, 'Dest ID'])
        row.append(st.session_state.unmapped_df.at[i, 'Dest City'])
        new_mappings.append(row)
        

        # print(st.session_state.unmapped_df.at[i, 'Profit Center Code'])
        
    new_mappings_df = pd.DataFrame(new_mappings)
    new_mappings_df.columns = ['Profit Center Code', 'Load Reference ID', 'Plant/Profit Center Name']

    old_mappings = pd.concat([old_mappings, new_mappings_df])
    old_mappings.to_excel("./app/data/Profit Center Overrides.xlsx", index=False)

def updateMappingSheet():
    old_mappings = pd.read_excel("./app/data/Profit Center Overrides.xlsx")\

    for i in st.session_state.error_data['edited_rows']:
        # print(st.session_state.error_data['edited_rows'][i])
        LR_ID = st.session_state.errors_df.at[i, 'Load Reference ID']
        
        new_city_value = st.session_state.error_data['edited_rows'][i]['Clean PC']

        old_mappings.loc[old_mappings['Load Reference ID'] == LR_ID, 'Plant/Profit Center Name'] = new_city_value

    old_mappings.to_excel("./app/data/Profit Center Overrides.xlsx", index=False)


# Check for data
if 'unmapped_df' not in st.session_state:
    print("Unmapped not in session")

if 'mapped_df' not in st.session_state:
    print("Mapped not in session")

if 'errors_df' not in st.session_state:
    print("Errors not in session")


st.title("Result")
option = st.radio(" ", ('Mapped', 'Unmapped', 'Errors'))


if option == 'Unmapped':
    st.header("Unmapped")

    edited = st.data_editor(st.session_state.unmapped_df,
                            key="unmapped_data",
                            column_order=['Profit Center Code','Dest City','Dest ID'],
                            disabled=['Dest City','Dest ID'])

    if st.button("Add Mappings"):
        addMappings()
    if st.button("Add Mappings and Rerun"):
        addMappings()
        mapLocally()
        

elif option == 'Mapped':
    st.header("Mapped")
    st.dataframe(st.session_state.mapped_df,
                 column_order=['Origin ID', 'Origin City', 'Dest ID', 'Dest City', 'Profit Center Code', 'Legacy PC'])

    if st.button("Update Report File"):
        updateReportFile()

elif option == 'Errors':
    st.header("Errors")
    st.text("Profit Centers were matched based on Load Reference ID.")
    st.text("These records have matching Load Reference IDs but differing City Names.")

    # st.session_state.errors_df['Selected'] = False
    st.data_editor(st.session_state.errors_df,
                   key='error_data',
                   column_order=['Load Reference ID', 'Dest City', 'Clean PC', 'Profit Center Code', 'Selected'],
                   column_config={'Dest City':'City in Export',
                                  'Clean PC': 'City in Mapping Sheet'},
                                  )

    if st.button("Save Selected Changes to Mapping Sheet and Remap"):
        updateMappingSheet()
        mapLocally()
    # st.button("Approve Mapping for Selected Rows")


