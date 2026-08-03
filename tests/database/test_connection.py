"""
============================================================
Test PostgreSQL Connection
============================================================
"""

from database.connection import get_connection


def main():
    conn = None

    try:
        conn = get_connection()

        print("\n====================================")
        print(" PostgreSQL Connection Successful")
        print("====================================")

        print(f"Database : {conn.info.dbname}")
        print(f"Host     : {conn.info.host}")
        print(f"Port     : {conn.info.port}")
        print(f"User     : {conn.info.user}")

    except Exception as e:
        print("\nConnection Failed")
        print(e)

    finally:
        if conn:
            conn.close()
            print("\nConnection Closed")


if __name__ == "__main__":
    main()