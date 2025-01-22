import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="rightmove_houses",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

# Create a cursor
cur = conn.cursor()
# cur.execute("""CREATE TABLE houses (
#             id SERIAL PRIMARY KEY,
#             url VARCHAR(300),
#             image_text text);""")

# # Insert data into the table
# ur = """http://49.13.238.251:8000/download-image/?request=https%3A%2F%2Fmedia.rightmove.co.uk%2F23k%2F22317%2F154980638%2F22317_TOT240172_FLP_00_0000.jpeg"""
# text = """Image text is Approximate Gross Internal Area 1695 sq ft - 160 sqm"""
# cur.execute(f"""INSERT INTO houses (id, url, image_text) VALUES ({2}, {ur}, {text});""")



res = cur.execute("SELECT * from houses;")
print(res)
# Commit changes and close connection
conn.commit()
cur.close()
conn.close()
