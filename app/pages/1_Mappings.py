import streamlit as st
import pandas as pd
import os

# button functionality
def updateReportFile():
    report = pd.read_excel("./app/data/Qlik file.xlsx")
    print(report.sort_values(by='Profit Center'))

    for i in range(len(report)):
        # print(report.iloc[i]['Profit Center'])
        if(report.iloc[i]['Profit Center']=='Undefined'):
            shipment_num = report.iloc[i]['Shipment Num']

            rows =  st.session_state.mapped_df[st.session_state.mapped_df['Shipment Num'] == shipment_num]
            if len(rows) == 0:
                print("No mapping")

            elif len(rows) == 1:
                print(shipment_num, rows['Legacy PC'].values[0])
                # st.session_state.mapped_df.loc[report.iloc[i]['Shipment Num']]
                report.at[i, 'Profit Center'] = rows['Legacy PC'].values[0]
            else:
                print("Shippment Num overlap")

    print(report.sort_values(by='Profit Center'))
    report.to_excel("./app/data/updated report.xlsx", index=False)



# Check for data
if 'unmapped_df' not in st.session_state:
    print("Unmapped not in session")

if 'mapped_df' not in st.session_state:
    print("Unmapped not in session")

if 'errors_df' not in st.session_state:
    print("Errors not in session")


st.title("Result")
option = st.radio(" ", ('Mapped', 'Unmapped', 'Errors'))


if option == 'Unmapped':
    st.header("Unmapped")

    edited = st.data_editor(st.session_state.unmapped_df,
                            column_order=['Profit Center Code','Dest City','Dest ID'],
                            disabled=['Dest City','Dest ID'])

    st.button("Update Mappings")
    st.button("Update Mappings and Rerun")

elif option == 'Mapped':
    st.header("Mapped")
    st.dataframe(st.session_state.mapped_df,
                 column_order=['Origin ID', 'Origin City', 'Dest ID', 'Dest City', 'Profit Center Code', 'Legacy PC'])

    if st.button("Update Report File"):
        updateReportFile()

elif option == 'Errors':
    st.header("Errors")
    st.text("Profit Centers were matched based on Dest ID.")
    st.text("These records have the same Dest ID but different Profit Center Names.")
    st.data_editor(st.session_state.errors_df,
                   column_order=['Origin ID', 'Origin City', 'Dest ID', 'Dest City', 'Profit Center Code', 'Legacy PC'])

    st.button("Save Corrections")


