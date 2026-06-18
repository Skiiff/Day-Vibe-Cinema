def get_events():
    output = []
    from datetime import date

    month = int(date.today().month)
    day = int(date.today().day)

    import sqlite3 as sql

    db_event = sql.connect("Recom_Parameters.db")
    conn = db_event.cursor()

    events = conn.execute("SELECT id,title_ru,importance FROM events WHERE month = ? AND day = ?",(month, day))
    events = conn.fetchall()
    
    event_genres = conn.execute("SELECT genre FROM event_genres WHERE event_id = ?",(events[0][0],))
    event_genres = conn.fetchall()
    
    for m in event_genres:
        output.append(m[0])
    output.append(events[0][-1])

    db_event.close()
    
    return output
