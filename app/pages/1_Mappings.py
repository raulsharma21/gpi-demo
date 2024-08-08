import streamlit as st
import pandas as pd
import os

# Sample data
if 'unmapped_df' not in st.session_state:

    # unmapped_data = {
    #     'Origin ID': [1, 2],
    #     'Origin City': ['New York', 'Los Angeles'],
    #     'Destination ID': [101, 102],
    #     'Destination City': ['Chicago', 'San Francisco'],
    #     'Profit Center Code': [''] * 2  # Initially empty
    # }
    unmapped_data = pd.read_excel('./app/data/unmapped.xlsx')
    st.session_state.unmapped_df = pd.DataFrame(unmapped_data)


mapped_data = {
        'Origin ID': [3, 4],
        'Origin City': ['Houston', 'Phoenix'],
        'Destination ID': [103, 104],
        'Destination City': ['Miami', 'Dallas'],
        'Profit Center Code': ['PC01', 'PC02']
}
mapped_df = pd.DataFrame(mapped_data)

st.title("Select Table")
option = st.radio(" ", ('Unmapped', 'Mapped'))

if option == 'Unmapped':
    st.header("Unmapped")

    # Display column headers
    cols = st.columns((1, 1, 1, 1, 1))
    headers = ['Origin ID', 'Origin City', 'Destination ID',
                  'Destination City', 'Profit Center Code']
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")

    # Display rows with text input for Profit Center Code
    for i in range(len(st.session_state.unmapped_df)):
        cols = st.columns((1, 1, 1, 1, 1))
        cols[0].write(st.session_state.unmapped_df.iloc[i, 0])
        cols[1].write(st.session_state.unmapped_df.iloc[i, 1])
        cols[2].write(st.session_state.unmapped_df.iloc[i, 2])
        cols[3].write(st.session_state.unmapped_df.iloc[i, 3])
        st.session_state.unmapped_df.at[i, 'Profit Center Code'] = cols[4].text_input(
            "Profit Center Code",
            st.session_state.unmapped_df.at[i, 'Profit Center Code'],
            key=f"pcc_{i}"
        )

else:
    st.header("Mapped")
    st.dataframe(mapped_df)


st.button("Submit")