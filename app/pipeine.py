import requests
import streamlit as st

def getAccessToken():
    client_id = st.secrets.client_id
    client_secret = st.secrets.client_secret
    tenant_id = st.secrets.tenant_id

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://dev.azuresynapse.net/.default'
    }

    response = requests.post(url, data=payload)
    access_token = response.json().get('access_token')
    
    if access_token:
        return access_token
        # st.success("Access token retrieved successfully")
    else:
        st.error("Failed to retrieve access token")
        return ""


def triggerPipeline():
    workspace_name = 'usazr3-dmz-dev-syn-001-dwh'
    pipeline_name = 'pl_update_profit_centers'
    access_token = getAccessToken()

    if not access_token:
        st.error("Access token not available. Please get the access token first.")
        return

    url = f"https://{workspace_name}.dev.azuresynapse.net/pipelines/{pipeline_name}/createRun?api-version=2020-12-01"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        st.success("Pipeline triggered successfully")
    else:
        st.error(f"Failed to trigger pipeline: {response.status_code} - {response.text}")