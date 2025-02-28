import tempfile
import streamlit as st
import os
from PIL import Image
from api.gemini_api import analyze_check_with_gemini
from database.db_manager import store_cheque_data
from extract.extract_text import convert_pdf_to_images, save_images

import streamlit as st
st.set_page_config(page_title="Cheque Processing", page_icon="📄")

if st.button("🏠 Back to Home"):
    st.switch_page("home.py")

st.title("📄 Upload and Process a Cheque")
# (Rest of your cheque processing code here)

STORAGE_PATH = "stored_cheques"

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

def main():
    st.title("CheckMate: Automated Bank Cheque Processor")

    uploaded_file = st.file_uploader("Upload Cheque (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file:
        st.text("Processing cheque...")

        # ✅ Handle PDF upload
        if uploaded_file.type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.getbuffer())
                pdf_path = temp_pdf.name

            images = convert_pdf_to_images(pdf_path)  # ✅ Convert PDF to images
            image_paths = save_images(images)  # ✅ Save images to temp files

            if not image_paths:
                st.error("Failed to extract images from PDF.")
                return

            image_path = image_paths[0]  # ✅ Process only the first page for now

        else:
            # ✅ Save uploaded cheque image
            image_path = os.path.join(STORAGE_PATH, uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # ✅ Process cheque image with Gemini
        image = Image.open(image_path)
        structured_data = analyze_check_with_gemini(image_path=image_path)

        st.image(image, caption="Uploaded Cheque")
        st.write("Structured Data:", structured_data)

        # ✅ Store cheque details in database
        store_cheque_data(uploaded_file.name, structured_data)

        st.success("Cheque data saved successfully!")

if __name__ == "__main__":
    main()
