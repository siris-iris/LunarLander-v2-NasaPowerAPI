import requests
from datetime import datetime, timedelta, timezone


# Get wind speed from NASA Power Api
def get_wind_speed(date, lat, long):
    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    parameters = {
        "parameters": "WS10M",
        "start": date,
        "end": date,
        "latitude": lat,
        "longitude": long,
        "community": "RE",
        "format": "JSON"
    }

    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        try:
            return response.json()["properties"]["parameter"]["WS10M"]
        except KeyError:
            return None
    return None


# check if data is available for user-input hour
def hours_available(available_hours):
    hours_set = set(available_hours)
    input_hour = input("Enter an hour between 0 and 23: ").strip()
    while input_hour not in hours_set:
        print(f"Invalid hour or no data is available at {input_hour}. Try a different time")
        input_hour = input("Enter an hour between 0 and 23: ").strip()
    return input_hour


# Get day and
def get_hourly_data(lat, long, selected_hour=None):
    wind_data = None
    valid_date = None
    for i in range(1, 31):
        ugly_date = (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y%m%d")
        wind_data = get_wind_speed(ugly_date, lat, long)
        if wind_data and any(v != -999.0 for v in wind_data.values()):
            valid_date = ugly_date
            break
    if not wind_data:
        print("No valid wind data available in the past 30 days at this location")
        return None
    
    # make the date formatting nicer
    yyyymmdd_format = datetime.strptime(valid_date, "%Y%m%d")
    nice_date = yyyymmdd_format.strftime("%B %d, %Y")
    print(f"Using wind data from {nice_date}")

    available_hours = [k[-2:] for k in wind_data.keys() if wind_data[k] != -999.0]

    if selected_hour is None:
        new_hour = hours_available(available_hours)
    else:
        selected_hour = selected_hour.zfill(2)
        if selected_hour not in available_hours:
            print(f"Provided hour {selected_hour} is not available. Defaulting to {available_hours[0]}")
            new_hour = available_hours[0]
        else:
            new_hour = selected_hour

    full_key = next(k for k in wind_data.keys() if k.endswith(new_hour))
    wind_speed = wind_data[full_key]

    print(f"Wind speed on {nice_date} at {new_hour} is {wind_speed:.2f} m/s")
    return wind_speed

    
# calling the function
#lat = float(input("Enter the latitude: "))
#long = float(input("Enter the longitude: "))
#wind_speed = get_hourly_data(lat, long)
#if wind_speed is not None:
#    print(f"Wind speed is {wind_speed:.2f} m/s")
#else:
#    print("Could not retrieve wind speed")