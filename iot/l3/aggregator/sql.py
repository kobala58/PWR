import psycopg2

class Queries:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
                dbname = "main",
                user="admin",
                password="admin",
                host="0.0.0.0",
                port=54320
                )
        self.cur = self.conn.cursor()

    def insert_config(self, config) ->bool:
        q = """INSERT INTO public.sender_configs(
                name, method, sender_port, channel, server
                VALUES ()
                )"""
    
    def insert_val(self, data: set) -> bool:
        q = """INSERT INTO public.recv_data (walor, time, bid, ask) VALUES (%s, %s, %s, %s)"""
        self.cur.execute(q, data)
        self.conn.commit()
        return True
    
    def select_top_walor(self, walor, top):
        q = """SELECT MIN(bid),MAX(bid), AVG(bid) FROM public.recv_data WHERE walor = %s LIMIT %s"""
        self.cur.execute(q, (walor, top))
        return self.cur.fetchone()



if __name__ == "__main__":
    data = Queries()
