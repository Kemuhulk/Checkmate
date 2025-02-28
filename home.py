import streamlit as st

st.set_page_config(page_title="CheckMate - Home", page_icon="🏦")

st.title("🏦 CheckMate: Automated Bank Cheque Processor")
st.subheader("Welcome! Choose an option below:")

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Process a New Cheque"):
        st.switch_page("pages/1_📄_Cheque_Processing.py")

with col2:
    if st.button("📊 View Cheque Dashboard"):
        st.switch_page("pages/2_📊_Cheque_Dashboard.py")

st.markdown(
    """
    ---
    **CheckMate** is a tool that extracts and verifies cheque details using AI.  
    - Upload a cheque to extract details.
    - View processed cheques in the dashboard.
    """
)
