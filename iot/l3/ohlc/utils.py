import psycopg2
from pydantic import main
from psycopg2.extras import RealDictCursor

class Queries:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
                dbname = "main",
                user="user",
                password="admin",
                host="0.0.0.0",
                port=54320
                )
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    
    
    def ohlc(self, instrument, time_unit, time_val):
        q = """
        SELECT walor,
        round( avg(bid)::numeric , 4) AS avg,
        min(bid),
        max(bid),
        date_bin(%s,time,'2000-01-01') as candle 
        FROM public.recv_data
        where walor = %s
        GROUP BY walor, candle ORDER BY candle
        """
        time_concat = str(time_val)+" " + time_unit
        self.cur.execute(q, (time_concat, instrument))
        data = self.cur.fetchall()
        return data

def generate_ohlc_values(instrument, time_unit, time_val):
    q = Queries()
    data = [dict(x) for x in q.ohlc(instrument, time_unit, time_val)]
    return data


if __name__ == "__main__":
    generate_ohlc_values('USDPLN', 'hours', 1)
