import sqlite3

def est_conn():
    con = sqlite3.connect("servers.db")
    cur = con.cursor()
    return cur, con

def insert_new_server(id: str, source: str, method: str):
    cur, con = est_conn()
    cur.execute("""
                INSERT INTO servers VALUES(?, ?, ?)
                """, (id, source, method))
    con.commit()

def get_all_servers():
    cur, con = est_conn()
    res = cur.execute("""
                SELECT * FROM servers

                """)
    return res.fetchall()

def main():
    cur, con = est_conn()
    cur.execute("""
                CREATE TABLE servers(
                    id text,
                    source text,
                    method text
                    )
                """)
    print("exe")



if __name__ == "__main__":
    main()
