import streamlit as st
import pandas as pd
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def fetch_cheques():
    """Fetch cheque data from the database."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, payee, amount_words, amount_digits, bank, ifsc_code,
               account_number, cheque_number, cheque_date, signature_verification, processed_at
        FROM cheques ORDER BY processed_at DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    columns = ["id", "filename", "payee", "amount_words", "amount_digits", "bank",
               "ifsc_code", "account_number", "cheque_number", "cheque_date",
               "signature_verification", "processed_at"]
    
    return pd.DataFrame(data, columns=columns)

def main():
    st.title("📊 Cheque Dashboard")
    st.subheader("Uploaded cheque records")
    
    cheques_df = fetch_cheques()
    
    if cheques_df.empty:
        st.warning("No cheques uploaded yet!")
        return

    # ✅ Display DataFrame in CSV format
    st.dataframe(cheques_df, use_container_width=True)

    # ✅ Provide a CSV download option
    csv = cheques_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="cheque_data.csv",
        mime="text/csv"
    )

    st.subheader("Uploaded cheques")

if __name__ == "__main__":
    main()
# import streamlit as st
# import pandas as pd
# import psycopg2
# from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# # Define the folder where cheque images are stored
# IMAGE_FOLDER = "uploads/"  # Adjust based on your storage path

# def fetch_cheques():
#     """Fetch cheque data from the database."""
#     conn = psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT
#     )
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT id, filename, payee, amount_words, amount_digits, bank, ifsc_code,
#                account_number, cheque_number, cheque_date, signature_verification, processed_at
#         FROM cheques ORDER BY processed_at DESC;
#     """)
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
    
#     columns = ["id", "filename", "payee", "amount_words", "amount_digits", "bank",
#                "ifsc_code", "account_number", "cheque_number", "cheque_date",
#                "signature_verification", "processed_at"]
    
#     return pd.DataFrame(data, columns=columns)

# def main():
#     st.title("📊 Cheque Dashboard")
    
#     cheques_df = fetch_cheques()
    
#     if cheques_df.empty:
#         st.warning("No cheques uploaded yet!")
#         return

#     # ✅ Display cheque images in a separate column
#     st.write("### Uploaded Cheques")

#     for index, row in cheques_df.iterrows():
#         image_path = IMAGE_FOLDER + row["filename"]
#         col1, col2 = st.columns([1, 3])

#         with col1:
#             st.image(image_path, caption=row["filename"], width=100)

#         with col2:
#             st.write(f"**Payee:** {row['payee']}")
#             st.write(f"**Amount:** {row['amount_words']} ({row['amount_digits']})")
#             st.write(f"**Bank:** {row['bank']}")
#             st.write(f"**Cheque Number:** {row['cheque_number']}")
#             st.write("---")

#     # ✅ Display full cheque data in table format
#     st.write("### Cheque Data (CSV View)")
#     st.dataframe(cheques_df, use_container_width=True)

#     # ✅ Provide a CSV download option
#     csv = cheques_df.to_csv(index=False).encode('utf-8')
#     st.download_button(
#         label="📥 Download CSV",
#         data=csv,
#         file_name="cheque_data.csv",
#         mime="text/csv"
#     )

# if __name__ == "__main__":
#     main()
