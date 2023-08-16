import requests
import smtplib
import datetime as dt
import time

#----------------Constent variable------------------#
URL_ISS = 'http://api.open-notify.org/iss-now.json'
URL_SUNSET_SUNRISE = 'https://api.sunrise-sunset.org/json'
SENDER = input("Sender email: ")
PASSWORD = input("Password: ")
RECIVER = input("Send to: ")

MY_LNG =  int(input("LONG: "))
MY_LAT =  int(input("LAT: "))

#----------------Message system with smtplob------------------#
def message(message):
    with smtplib.SMTP('smtp.gmail.com',587,timeout=120) as connection:
        connection.starttls()
        connection.login(user=SENDER,password=PASSWORD)
        connection.sendmail(from_addr=SENDER,to_addrs=RECIVER,msg=message)
        print("Message send.")


#----------------Condition.------------------#
while True:
    current_hour = dt.datetime.now().hour
    iss_data = requests.get(url=URL_ISS).json()
    longitude = float(iss_data['iss_position']['longitude'])
    latitude = float(iss_data['iss_position']['latitude'])
    peremeter = {'lat':MY_LAT,'lng':MY_LNG,'formatted':0,}
    sunset_sunrise_data = requests.get(url=URL_SUNSET_SUNRISE,params=peremeter).json()
    sunrise = float(sunset_sunrise_data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = float(sunset_sunrise_data['results']['sunset'].split('T')[1].split(':')[0])
    if longitude + 5 >= MY_LNG or longitude -5 <= MY_LNG and latitude + 5 >= MY_LAT or latitude  -5 <= MY_LAT:
        if current_hour <= sunrise and current_hour >= sunset:
            msg =f"Subject:ISS Tracker\n\nDear{RECIVER},\n\nISS is currently over your location.It might be possiable to see it.\n\nYours Truly,\n{SENDER}."
            message(message=msg) 

    time.sleep(10)

