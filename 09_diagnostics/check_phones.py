import sqlite3
conn = sqlite3.connect(r'c:\Users\maria\env\KALMIYA_System\kalmiya.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM user_memory WHERE key LIKE 'celular_%'")
rows = cursor.fetchall()
print(rows)
conn.close()
