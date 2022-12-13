import psycopg2

class Queries:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
                dbname = "main",
                user="user",
                password="admin",
                host="0.0.0.0",
                port=54320
                )
        self.cur = conn.cursor()

    def insert_config(self, config) ->bool:
        q = """INSERT INTO public.sender_configs(
                name, method, sender_port, channel, server
                VALUES ()
                )"""
    
    def insert_val(self, data) -> bool:
        q = """INSERT INTO public.recv_data
        """


if __name__ == "__main__":
    data = Queries()
