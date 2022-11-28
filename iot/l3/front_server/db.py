import sqlite3

def est_conn():
    con = sqlite3.connect("servers.db")
    cur = con.cursor()
    return cur, con

def insert_new_server(id: str, name: str, method: str, port: str, interval: int, source: str, channel: str, server: str, lh: int):
    cur, con = est_conn()
    cur.execute("""
                INSERT INTO servers VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """, (id, name, method, port, interval, source, channel, server))
    cur.execute("INSERT INTO connections VALUES (?,?)", (name, lh))
    con.commit()

def get_all_connections():
    cur, con = est_conn()
    res = cur.execute("""
                SELECT * FROM connections
                """)
    return res.fetchall()

def get_all_servers():
    cur, con = est_conn()
    res = cur.execute("""
                SELECT * FROM servers
                """)
    print()
    print(res)
    return res.fetchall()

def get_server_info(name: str):
    cur, con = est_conn()
    res = cur.execute("""
                SELECT port FROM connections WHERE id = ?

                """, (name,))
    return res.fetchall()

def edit_server(data: tuple):
    cur, con = est_conn()
    sql = ''' UPDATE servers 
        SET method= ? ,
        port = ? ,
        inverval = ?,
        source = ?,
        channel = ?,
        server = ?
        WHERE name = ?'''
    cur.execute(sql, data)
    con.commit()

def main():
    cur, con = est_conn()
    # cur.execute("""
    #             CREATE TABLE servers(
    #                 id text,
    #                 name text,
    #                 method text,
    #                 port text,
    #                 inverval int,
    #                 source text,
    #                 channel text,
    #                 server text
    #                 )
    #             """)
    # cur.execute(
    #         """
    #         CREATE TABLE connections(
    #             id text,
    #             port text
    #             )
    #         """
    #         )
    print("exe")
    print(get_all_connections())

def clear_server():
    cur, con = est_conn()
    cur.execute("DELETE FROM servers")
    cur.execute("DELETE FROM connections")
    con.commit()
    return True

if __name__ == "__main__":
    main()
