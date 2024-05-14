import argparse
import random
from datetime import date, datetime, timedelta
from time import strftime

def generate_fake_routes(route_times, notrain, nobus, noblabla) -> list:
    transport_base = ["Train", "Bus", "Blablacar"]
    selected = [notrain, nobus, noblabla]
    transport = [x for x,y in zip(transport_base, selected) if y]
    timeskips = [20, 60, 120, 150]
    payload = []
    for x in timeskips:
        tmp = {}
        duration = random.randrange(100, 140) 
        tmp["start"] = route_times + timedelta(minutes= random.randrange(x-10, x+10))
        tmp["end"] = tmp["start"] + timedelta(minutes=duration)
        tmp["timetravel"] = duration
        tmp["transport"] = random.choice(transport)
        payload.append(tmp)
    return payload

def draw_timetable(payload, params):
    LINESIZE = 60
    # drawing header
    dest = f"|{params.start} -> {params.to}|" 
    rest = LINESIZE - len(dest)
    _size = rest // 2
    pre = "".join(["-" for x in range(_size)])
    post = pre
    if rest%2 != 0:
        post = pre+"-"
    
    print(f"{pre}{dest}{post}")
    # draw columns 
    for x in payload:
        print(f"| {x['start']} - {x['end']} | {x['transport']} | {x['timetravel']}")




def main(args: argparse.Namespace) -> None:
    time_parsed = f"{args.date} {args.time}"
    time_parsed = datetime.strptime(time_parsed, "%d/%m/%Y %H:%M:%S")
    print(time_parsed)
    payload = generate_fake_routes(time_parsed, args.ignore_trains, args.ignore_buses, args.ignore_blablacar)
    draw_timetable(payload, args)


if __name__ == "__main__":
    today = date.today()
    parser = argparse.ArgumentParser(
            description="Znajdź swoją ulubioną trasę!"
            )

    parser.add_argument("--start", default="WRO", type=str, help="Ustaw miasto początkowe")
    
    parser.add_argument("--to", default="WWA", type=str, help="Ustaw miasto końcowe")
    parser.add_argument("--time", default=today.strftime("%H:%M:%S"), type=str, help="Podaj czsa planowanego wyjazdu w formacie HH:MM:SS")
    parser.add_argument("--date", default=today.strftime("%d/%m/%Y"), type=str, help="Podaj datę wyjazdu w formacie DD/MM/YYYY")
    parser.add_argument("--ignore_trains", action="store_false", help="Ignoruj połączenia pociągiem")
    parser.add_argument("--ignore_blablacar", action="store_false", help="Ignoruj połaczenia ")
    parser.add_argument("--ignore_buses", action="store_false", help="Ignoruj połaczenia ")
    args = parser.parse_args()
    print(args)
    main(args)
