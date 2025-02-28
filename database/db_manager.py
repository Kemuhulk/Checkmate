import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def connect_db():
    """Establish connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_cheque_table():
    """Creates a table to store cheque images and their extracted data."""
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cheques (
                id SERIAL PRIMARY KEY,
                filename TEXT UNIQUE,
                payee TEXT,
                amount_words TEXT,
                amount_digits TEXT,
                bank TEXT,
                ifsc_code TEXT,
                account_number TEXT,
                cheque_number TEXT,
                cheque_date TEXT,
                signature_verification TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Cheque table is ready.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error creating table: {e}")

def store_cheque_data(filename, check_data):
    """Stores cheque details and image filename in the database."""
    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # ✅ Debugging: Print the received data before inserting
            print("Storing Cheque Data:", check_data)

            query = """
            INSERT INTO cheques (
                filename, payee, amount_words, amount_digits, bank, ifsc_code,
                account_number, cheque_number, cheque_date, signature_verification
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                filename,
                check_data.get("Payee Name", "Not Found"),  # ✅ Match exact Gemini API keys
                check_data.get("Amount in Words", "Not Found"),
                check_data.get("Amount in Digits", "Not Found"),
                check_data.get("Bank Name", "Not Found"),
                check_data.get("IFSC Code", "Not Found"),
                check_data.get("Account Number", "Not Found"),
                check_data.get("Cheque Number", "Not Found"),
                check_data.get("Date", "Not Found"),
                check_data.get("Signature Verification", "Not Found")
            )

            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Cheque data for {filename} stored successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error storing cheque data: {e}")
