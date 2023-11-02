import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 40.341668 # Your latitude
MY_LONG = -74.660329 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    if abs(iss_latitude-MY_LAT) <= 5 and abs(iss_longitude-MY_LONG) <= 5:
        if time_now.hour > sunset or time_now.hour < sunrise:
            my_email = "marcos.jay.santos@gmail.com"
            my_password = "juzbbypwcsnzkppm"
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs="anishkataria69@yahoo.com",
                                    msg="Look up, the ISS is above you"
                                    )
                connection.close()
    time.sleep(60)

