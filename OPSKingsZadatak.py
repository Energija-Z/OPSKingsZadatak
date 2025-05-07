import json
import requests
from requests.exceptions import ConnectionError

# Function to convert multiple rain times of a day into a string
def rainTimeInDay(rainDate, rainTime):
    if ", " in rainTime:
        rainTime = rainTime.split(", ")
        returnVal = ""
        for i in rainTime:
            returnVal += rainDate + ": " + i + "\n"
        return str(returnVal)
    else:
        return str(rainDate + ": " + rainTime + "\n")

url = "https://hook.eu2.make.com/7mfiayunbpfef8qlnielxli5ptoktz02"
urlAdd = "https://hook.eu2.make.com/76g53ebwgbestjsj1ikejbaicpnc5jro"

avgTemp = 0
rainDays = ""
cloudyDays = {
    "Cloudy": 0,
    "Foggy": 0,
    "Rainy": 0,
    "Sunny": 0,
    "Very Cloudy": 0,
}
holidayDays = ""

answer = False
k = 0

while k < 10:
    try:
        # Get response from first server
        answer = requests.get(url, timeout=1)

        # Try reaching server 10 times, otherwise throw exception
        answer = answer.json()

        # Get first degrees to compare with rest
        maxTemp = answer[0]["degrees_in_celsius"]
        minTemp = answer[0]["degrees_in_celsius"]

        answer2 = requests.get(urlAdd, None).json()
        answer2 = list(filter(lambda x: x["is_public_holiday"] == "yes", answer2))

        #Iterate through list
        for i in answer:
            temperature = i["degrees_in_celsius"]

            #Compare current temperature if it is higher or lower than compared
            if temperature > maxTemp:
                maxTemp = temperature
            elif temperature < minTemp:
                minTemp = temperature
            avgTemp += temperature

            #Add +1 to cloudy map
            skyStatus = i["sky"]
            match skyStatus:
                case "rainy": cloudyDays["Rainy"] += 1
                case "foggy": cloudyDays["Foggy"] += 1
                case "sunny": cloudyDays["Sunny"] += 1
                case "cloudy": cloudyDays["Cloudy"] += 1
                case "very cloudy": cloudyDays["Very Cloudy"] += 1
                case _: None

            #If day has multiple rain days, separate them and assign date
            if i["times_of_rain_showers"] != None:
                rainDays += rainTimeInDay(i["date"], i["times_of_rain_showers"])

            #Compare the cloudy dates to holiday dates
            for j in answer2:
                skyDate = j["date"]
                if skyDate == i["date"]:
                    holidayDays += skyDate + ": " + skyStatus + "\n"

        print("### scenario URL: https://github.com/Energija-Z/OPSKingsZadatak/blob/main/OPSKingsZadatak.py ###\n")
        print("Hi,\nhere are your San Francisco weather stats for 2022-11:")
        print("The max temperature was: " + str(maxTemp))
        print("The avg temperature was: " + str(avgTemp // len(answer)))
        print("The min temperature was: " + str(minTemp))
        print('\nOverview of unique "sky" values and their counts:')
        for i in cloudyDays:
            print(i + ": " + str(cloudyDays[i]))
        print("\nRain showers:\n" + rainDays)
        print('"Sky" statuses during holidays:')
        print(holidayDays)
        print("Have a nice day!")
        k = 10

    except:
        print("Server unreachable")
        k += 1
