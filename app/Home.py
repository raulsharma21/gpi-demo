import streamlit as st
import pandas as pd

from pipeine import triggerPipeline

from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

def mapLocally():
    report = pd.read_excel("./app/data/Qlik file.xlsx")
    mappings = pd.read_excel("./app/data/mappings.xlsx")

    mappings['Clean PC'] = mappings['Plant/Profit Center Name'].str.split('Sales/COS',1).str[0]
    mappings['Clean PC'] = mappings['Clean PC'].str.split('-',1).str[0]
    mappings['Clean PC'] = mappings['Clean PC'].str.strip()

    print(mappings)
    # undefined = report[report['Profit Center'] == "Undefined"]

def main():

    st.set_page_config(
    page_title="Profit Center POC",
    )

    
    st.title("Profit Center Mapping")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    st.header("Proof Of Concept")

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    st.text("Once the report file has been uploaded to cloud storage:")

    if st.button('Match Existing Profit Centers'):
        # triggerPipeline()
        mapLocally()
        nav_page("Mappings")


    

    

if __name__ == "__main__":
    main()
