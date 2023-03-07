import requests
from bs4 import BeautifulSoup
import datetime
import re

url = "https://kafeterya.metu.edu.tr/"

htmlResponse = requests.get(url)
print(htmlResponse.content)

today = datetime.datetime.now()
currDay = today
header = {"Content-Type": "application/json; charset=utf-8"}
requ = {"date_filter[value][date]": f"{currDay.day}/{currDay.month}/{currDay.year}"}
htmlResponse = requests.post(url=url, data=requ, headers=header)
soup = BeautifulSoup(htmlResponse.content, 'html.parser')
images = soup.find_all("img", class_="img-responsive")
names = soup.find_all("h2")
print(names)

htmlStart= f"""
<html lang="en" class="p-3 mb-2 bg-dark text-white">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meal List</title>
    <link rel='icon' href='favicon.png' type='image/x-icon' sizes="16x16" />
    
<!-- BOOTSTRAP CSS only -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<!-- JavaScript Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<link href="./css/idBasedStyles.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

</head>
<body class="p-3 mb-2 bg-dark text-white">
      <div class="container" id="0">
"""
htmlEnd="""      <br>
    </div> 
</body>
</html>
"""

starterChar= '">'
enderChar= '</a>'

names = names[0:8]
meals = [re.findall(">([\w|\s]+)<", str(name)) for name in names]
print(meals)
for txt in meals:
    print(txt)
htmlLunchText = f'<div class="row" >' + "".join([f'<div class="col col-2">{meal} </div>' for meal in meals[0:4]]) + "</div>"
htmlLunch = f'<div class="row" >' + "".join([f'<div class="col col-2">{image} </div>' for image in images[0:4]]) + "</div>"
htmlDinnerText = f'<div class="row" >' + "".join([f'<div class="col col-2">{meal} </div>' for meal in meals[4:]]) + "</div>"
htmlDinner = f'<div class="row" >' + "".join([f'<div class="col col-2">{image} </div>' for image in images[4:]]) + "</div>"
# htmlCombined = htmlStart + f'<div class="row" ><div class="col col-2">{images} </div></div>' + htmlEnd
htmlCombined = htmlStart + htmlLunchText + htmlLunch + "<br><br>" + htmlDinnerText + htmlDinner + htmlEnd
with open("out.html", "w", encoding="UTF-8") as fptr:
    fptr.write(htmlCombined)