import requests
from bs4 import BeautifulSoup
import datetime
import re
import constants

def getMeals(day):
    getPayload = f"?date_filter[value][date]={day.day}/{day.month}/{day.year}"
    htmlResponse = requests.get(url=constants.URL + getPayload)
    print(htmlResponse.status_code)
    soup = BeautifulSoup(htmlResponse.content, 'html.parser')
    images = soup.find_all("img", class_="img-responsive")
    names = soup.find_all("h2")
    # print(names)
    names = names[0:8]
    meals = [re.findall(">([\w|\s|.]+)<", str(name)) for name in names]
    # print(meals)
    for txt in meals:
        print(txt)
    htmlDayText = f'<div class="row" > <h2 style=\"font-family: Arial, Helvetica, sans-serif;\"> {day.strftime("%d/%m/%Y")} </h2> </div>'
    htmlLunchText = f'<div class="row" >' + "".join([f'<div class="col col-2">{"".join(meal)} </div>' for meal in meals[0:4]]) + "</div>"
    htmlLunch = f'<div class="row" >' + "".join([f'<div class="col col-2">{image} </div>' for image in images[0:4]]) + "</div>"
    htmlDinnerText = f'<div class="row" >' + "".join([f'<div class="col col-2">{"".join(meal)} </div>' for meal in meals[4:]]) + "</div>"
    htmlDinner = f'<div class="row" >' + "".join([f'<div class="col col-2">{image} </div>' for image in images[4:]]) + "</div>"

    return constants.HTML_START + htmlDayText + htmlLunchText + htmlLunch + "<br><br>" + htmlDinnerText + htmlDinner + constants.HTML_END

with open("out.html", "w", encoding="UTF-8") as fptr:
    today = datetime.datetime.now()
    htmlCombined = getMeals(today) + "<br><br>"  + getMeals(today + datetime.timedelta(days=1))
    fptr.write(htmlCombined)