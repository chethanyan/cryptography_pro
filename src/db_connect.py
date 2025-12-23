# mysql.connector → allows Python to communicate with MySQL database
import mysql.connector

# pandas → helps to read SQL data into table-like structure (DataFrame)
import pandas as pd


# -------------------- DATABASE CONNECTION --------------------

# Create a connection to the MySQL database
# This connection allows Python to send queries to MySQL
conn = mysql.connector.connect(
    host="localhost",          # Database is running on this machine
    user="root",               # MySQL username
    password="Chethu@1234",    # MySQL password
    database="clinical_trial"  # Database name
)


# -------------------- FETCH DATA FROM DATABASE --------------------

# Execute SQL query and store result in a Pandas DataFrame
# This reads all records from the 'patients' table
df = pd.read_sql("SELECT * FROM patients", conn)

# Print the data to verify database connection is successful
print(df)


# -------------------- CLOSE CONNECTION --------------------

# Close the database connection to free resources
conn.close()
