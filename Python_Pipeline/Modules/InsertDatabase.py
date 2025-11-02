import json
import mysql.connector
from Pipeline.Individual_Items import NewsItem

# ----------------------------------------
# Persistent Database Connection (once)
# ----------------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",           # change if needed
        database="voxpulse"     # your database name
    )
    cursor = conn.cursor()
    print("✅ Database connected successfully.")
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    conn = None
    cursor = None


# ----------------------------------------
# Core Function: Save a NewsItem
# ----------------------------------------
def save_news_to_db(item: NewsItem):
    """
    Inserts a NewsItem into the 'news_items' table.
    Uses the persistent connection established at import.
    """
    if not conn or not cursor:
        print("⚠️ No active database connection.")
        return

    try:
        sql = """
            INSERT INTO news_items
            (title, reference_links, content_text, audio_file_path, category)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            item.title,
            json.dumps(item.url, ensure_ascii=False),
            item.content,
            item.audio_file,
            item.category
        )

        cursor.execute(sql, values)
        conn.commit()
        print(f"🗄️ Inserted '{item.title}' successfully (ID: {cursor.lastrowid})")

    except mysql.connector.Error as err:
        print(f"❌ Database error while inserting '{item.title}': {err}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")


# ----------------------------------------
# Optional: Close Connection (for orchestrator shutdown)
# ----------------------------------------
def close_connection():
    """Close the global connection cleanly when done."""
    global conn, cursor
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("🔌 Database connection closed.")
    except Exception as e:
        print(f"⚠️ Error closing connection: {e}")
