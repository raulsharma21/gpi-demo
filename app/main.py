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

from azure.identity import ClientSecretCredential
from azure.mgmt.synapse import SynapseManagementClient
from azure.mgmt.synapse.models import CreateRunResponse

# Replace these values with your service principal and workspace details
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
tenant_id = 'YOUR_TENANT_ID'
subscription_id = 'YOUR_SUBSCRIPTION_ID'
resource_group_name = 'YOUR_RESOURCE_GROUP_NAME'
workspace_name = 'YOUR_WORKSPACE_NAME'
pipeline_name = 'YOUR_PIPELINE_NAME'

# Authenticate using the service principal
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

# Initialize Synapse management client
synapse_client = SynapseManagementClient(credentials, subscription_id)

# Run the pipeline
response = synapse_client.pipeline_runs.create(
    resource_group_name=resource_group_name,
    workspace_name=workspace_name,
    pipeline_name=pipeline_name,
    parameters={}  # Add pipeline parameters here if needed
)

# Output the run ID
print(f'Pipeline run initiated. Run ID: {response.run_id}')
