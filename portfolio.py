import streamlit as st, base64
from modules import MODULES

def get_pdf_download_link(pdf_path: str, pdf_name: str) -> str:
    """Generates a link allowing the user to download the PDF."""

    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    href = f'<a href="data:file/pdf;base64,{base64_pdf}" download="{pdf_name}">Download {pdf_name}</a>'
    return href

def main():
    st.title("Colin Pons")
    st.write("""
             I am a dedicated professional with a passion for utilising product master data to drive value for organisations. 
             I strongly believe in the power of scalable, simple, and accurate data. 
             Having transitioned from retail management to an office-based role, I have developed robust self-management skills and a proficiency in Python. 

             """)
    
    linkedin_link = "https://www.linkedin.com/in/colin-pons/"
    st.markdown(linkedin_link, unsafe_allow_html=True)

    pdf_link = get_pdf_download_link("pdfs/Colin Pons CV.pdf", "Colin Pons CV.pdf")
    st.markdown(pdf_link, unsafe_allow_html=True)

    modules = ["Home"] + list(MODULES.keys())
    selected_module = st.selectbox("Choose a module to explore", modules)

    if selected_module in MODULES and selected_module != "Home":
        MODULES[selected_module]()

    
if __name__ == "__main__":
    main()