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
        open = f"""
            select distinct on (date_trunc(%s, time)) bid
            from public.recv_data WHERE walor = %s
            order by date_trunc(%s, time), time
            """
        close = f"""
            select distinct on (date_trunc(%s, time)) bid
            from public.recv_data WHERE walor = %s
            order by date_trunc(%s, time), time DESC
            """
        time_concat = str(time_val)+" " + time_unit
        self.cur.execute(q, (time_concat, instrument))
        data = self.cur.fetchall()
        self.cur.execute(open, (time_unit, instrument, time_unit))
        open_data = self.cur.fetchall()
        self.cur.execute(close, (time_unit, instrument, time_unit))
        close_data = self.cur.fetchall()

        return [data, open_data, close_data]

    def tools(self):
        q = """
        SELECT walor FROM public.recv_data GROUP BY walor
        """
        self.cur.execute(q)
        data = self.cur.fetchall()
        return data

def generate_ohlc_values(instrument, time_unit, time_val):
    q = Queries()
    data = q.ohlc(instrument, time_unit, time_val)
    parsed = []
    for x in range(len(data[0])):
        val = [int(dict(data[0][x])["candle"].timestamp()), [dict(data[1][x])["bid"], dict(data[0][x])["max"], dict(data[0][x])["min"], dict(data[2][x])["bid"]]]
        if val:
            parsed.append(val)
    return {"instrument": instrument, "values": parsed}

def all_tools() -> list:
    q = Queries()
    data = [dict(x) for x in q.tools()]
    return data

if __name__ == "__main__":
    test = generate_ohlc_values('USDPLN', 'hours', 1)
    print(test)
    # all_tools()
