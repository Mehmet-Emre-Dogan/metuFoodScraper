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

    # innerStart = '<div class="container">'
    # htmlDayText = f'<div class="row justify-content-md-center" > <div class=\"col col-2\"> <h2 style=\"font-family: Arial, Helvetica, sans-serif;\"> {day.strftime("%d/%m/%Y")} </h2> </div> </div>'
    # htmlLunchText = f'<div class="row justify-content-md-center" >' + "".join([f'<div class="col col-md-auto">{"".join(meal)} </div>' for meal in meals[0:4]]) + "</div>"
    # htmlLunch = f'<div class="row justify-content-md-center" >' + "".join([f'<div class="col col-md-auto">{image} </div>' for image in images[0:4]]) + "</div>"
    # htmlDinnerText = f'<div class="row justify-content-md-center" >' + "".join([f'<div class="col col-md-auto">{"".join(meal)} </div>' for meal in meals[4:]]) + "</div>"
    # htmlDinner = f'<div class="row justify-content-md-center" >' + "".join([f'<div class="col col-md-auto">{image} </div>' for image in images[4:]]) + "</div>"
    # innerEnd = '</div>'
    # return  innerStart +  htmlDayText + htmlLunchText + htmlLunch + "<br><br>" + htmlDinnerText + htmlDinner + innerEnd

    innerStart = '<div class="container">'
    htmlDayText = f'<div class="row justify-content-md-center" > <div class=\"col col-2\"> <h2 style=\"font-family: Arial, Helvetica, sans-serif;\"> {day.strftime("%d/%m/%Y")} </h2> </div> </div>'
    htmlLunch = f'<div class="row justify-content-md-center" >' + "".join([f'<div class="col col-md-auto">{"".join(meal)}<br>{image} </div>' for (meal, image) in zip(meals[0:4], images[0:4])]) + "</div>"
    htmlDinner = f'<div class="row justify-content-md-center" >' + "".join([f'<div class="col col-md-auto">{"".join(meal)}<br>{image} </div>' for (meal, image) in zip(meals[4:], images[4:])]) + "</div>"
    innerEnd = '</div>'
    
    return  innerStart +  htmlDayText + htmlLunch + "<br><br>"  + htmlDinner + innerEnd

with open("out.html", "w", encoding="UTF-8") as fptr:
    today = datetime.datetime.now() + datetime.timedelta(hours=constants.GMT_DELTA)
    dateStr =  today.strftime("%H:%M:%S %d.%m.%Y")
    timestampHtml = f'<br><br><br> <div class="row justify-content-md-center" > <div class=\"col-md-auto\"> <h4 style=\"font-family: Arial, Helvetica, sans-serif;\"> scraped @ {dateStr} </h4> </div> </div>'
    htmlCombined = constants.HTML_START +  getMeals(today) + "<br><br>"  + getMeals(today + datetime.timedelta(days=1)) + timestampHtml + constants.HTML_END
    fptr.write(htmlCombined)
    print()