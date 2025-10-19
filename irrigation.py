from datetime import datetime
from psycopg2 import sql
import sys
from connection import get_connection

def get_irrigation_and_et0_data(device_id, year, month, day, password):
    # Build date (YYYY-MM-DD)
    date_string = datetime(year, month, day).strftime("%Y-%m-%d")

    # Connect
    conn = get_connection(password)
    cursor = conn.cursor()

    # Irrigation (liters per irrigation)
    cursor.execute(
        sql.SQL("SELECT * FROM irrigation.fn_get_litre_per_irrigation(%s, %s);"),
        (device_id, date_string),
    )
    irrigation_data = cursor.fetchall()

    # Weather device id
    cursor.execute(
        sql.SQL("SELECT weather_device_id FROM fn_device_get_weather_device(%s)"),
        (device_id,),
    )
    weather_device_id_info = cursor.fetchall()
    weather_device_id = weather_device_id_info[0][0] if weather_device_id_info else None

    # Guard: missing weather device
    if weather_device_id is None:
        print("No weather device")
        cursor.close()
        conn.close()
        sys.exit(1)

    # ET0 & rain (daily)
    cursor.execute(
        sql.SQL(
            "SELECT * FROM utils.fn_get_daily_rain_et0(%s, %s::timestamp, now()::timestamp, 'Europe/Istanbul') "
            "ORDER BY c_tstamp"
        ),
        (weather_device_id, date_string),
    )
    et0_data = cursor.fetchall()

    # Close
    cursor.close()
    conn.close()

    # Return
    return irrigation_data, et0_data
