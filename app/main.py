import streamlit as st
import requests

def getAccessToken():
    client_id = st.secrets.client_id
    client_secret = st.secrets.client_secret
    tenant_id = st.secrets.tenant_id
    
    print(client_id)
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://dev.azuresynapse.net/.default'
    }

    response = requests.post(url, data=payload)
    access_token = response.json()['access_token']
    print("Access token:", access_token)

def triggerPipeline():
    print("triggered")
    workspace_name = 'usazr3-dmz-dev-syn-001-dwh'
    pipeline_name = 'pl_update_profit_centers'
    access_token = st.secrets.access_token

    url = f"https://{workspace_name}.dev.azuresynapse.net/pipelines/{pipeline_name}/createRun?api-version=2020-12-01"
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
    }
    payload = {}
    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)
    


def main():

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

    st.button("Get Access Code", on_click=getAccessToken)
    st.button("Trigger Pipline", on_click=triggerPipeline)


if __name__ == "__main__":
    main()