from app.model.model import Base, engine, get_db, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
import psycopg2
Base.metadata.create_all(bind=engine)

# Đọc nội dung file SQL
with open("data_insert_query.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

try:
    # Kết nối đến database
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    cur = conn.cursor()

    # Thực thi script SQL
    cur.execute(sql_script)
    conn.commit()

    print("Database đã được khởi tạo thành công!")
except Exception as e:
    print(f"Lỗi: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()