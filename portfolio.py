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

    with st.expander("Terms of Use"):
        st.write("""
                Last Updated: 01/09/2023

                1. Acceptance of Terms: 
                By accessing or using this website, applications, and services (hereinafter referred to as "Services"), you agree to comply with and be bound by these Terms of Use.
                Within these terms, "I" or "me" refers to Colin Pons, the creator of this web app. Additionally the term "you" refers to you the user of this web app.
                Any reference to external data providers / sources specifically related to modules will be referenced with the applicable module.
                
                2. Changes to Terms: 
                I reserves the right to change, modify, or revise these Terms at any time. All changes will be effective immediately upon posting to the Services. Your continued use of the Services will signify your acceptance of any changes.

                3. Privacy Policy: 
                I do not record any personal information from the user, I may collect data which is input into the web app and record results for development purposes.
                Your use of the Services is also governed by the platform provider Steamlit.io Privacy Policy, which can be accessed here https://streamlit.io/privacy-policy.

                4. User Conduct: 
                You agree not to use the Services for any illegal or unethical activities.

                5. Limitation of Liability: 
                I shall not be liable for any indirect, incidental, or consequential damages arising out of your use or inability to use the Services.

                6. Governing Law: 
                These Terms shall be governed by the laws of the United Kingdom.

                7. Termination: 
                We reserve the right to terminate or suspend access to these Services at our sole discretion, without notice, for conduct that we believe violates these Terms or is harmful to other users of the Services, us, or third parties, or for any other reason.

                8. Contact Information: 
                For any questions about these Terms, please contact me at colin.pons@outlook.com.
                """)

if __name__ == "__main__":
    main()