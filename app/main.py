import streamlit as st

st.header("GPI Streamlit Demo")
st.write("App is hosted on Azure") 

if 'flag' not in st.session_state:
    st.session_state['flag'] = False

def set_flag():
    st.session_state['flag'] = not st.session_state['flag']

st.button("Click me", on_click=set_flag)

st.write(f"Flag state: {st.session_state['flag']}")

if st.session_state['flag']:
    st.error("### Popup Message")
    st.code("This is a simulated popup message displayed when the button is pressed.")