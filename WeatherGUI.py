import tkinter as tk
import requests
from bs4 import BeautifulSoup

url = 'https://weather.com/en-IN/weather/today/l/32355ced66b7ce3ab7ccafb0a4f45f12e7c915bcf8454f712efa57474ba8d6c8'

root = tk.Tk()
root.title("Weather")
root.config(bg = 'white')

def getWeather():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    location = soup.find('h1',class_="_1Ayv3").text
    temperature = soup.find('span',class_="_3KcTQ").text
    airquality = soup.find('text',class_='k2Z7I').text
    airqualitytitle = soup.find('span',class_='_1VMr2').text
    sunrise = soup.find('div',class_='_2ATeV').text
    sunset = soup.find('div',class_='_2_gJb _2ATeV').text
    humidity = soup.find('div',class_='_23DP5').text
    wind = soup.find('span',class_='_1Va1P undefined').text
    pressure = soup.find('span',class_='_3olKd undefined').text
    locationlabel.config(text=(location))
    templabel.config(text = temperature+"C")
    WeatherText = "Sunrise : "+sunrise+"\n"+"SunSet : "+sunset+"\n"+"Pressure : "+pressure+"\n"+"Wind : "+wind+"\n"
    weatherPrediction.config(text=WeatherText)
    airqualityText = airquality + " "*5 + airqualitytitle + "\n"
    airqualitylabel.config(text = airqualityText)
    
    weatherPrediction.after(120000,getWeather)
    root.update()
    

locationlabel= tk.Label(root, font = ('Calibri bold',20), bg = 'white')
locationlabel.grid(row = 0,column = 1, sticky='N',padx=20,pady=40)

templabel = tk.Label(root, font = ('Caliber bold', 40), bg="white")
templabel.grid(row=0,column = 0,sticky="W",padx=17)

weatherPrediction = tk.Label(root, font = ('Caliber', 15), bg="white")
weatherPrediction.grid(row=2,column=1,sticky="W",padx=40)

tk.Label(root,text = "Air Quality", font = ('Calibri bold',20), bg = 'white').grid(row = 1,column = 2, sticky='W',padx=20)
airqualitylabel = tk.Label(root, font = ('Caliber bold', 20), bg="white")
airqualitylabel.grid(row=2,column=2,sticky="W")

getWeather()
root.mainloop()

##################################################################################################################################################

# There is actually a better api to use rather than this one
#Try the code below to get weather is any city

import tkinter as tk
import requests
from PIL import Image, ImageTk

app = tk.Tk()

HEIGHT = 500
WIDTH = 600

def format_response(weather_json):
    try:
        city = weather_json['name']
        conditions = weather_json['weather'][0]['description']
        temp = weather_json['main']['temp']
        final_str = 'City: %s \nConditions: %s \nTemperature (°F): %s' % (city, conditions, temp)
    except:
        final_str = 'There was a problem retrieving that information'
    #final_str = 'hello'
    return final_str


def get_weather(city):
    # you have to go to the site to get your API key
    weather_key = 'edffd1bf975a74d5d10e58c5ac8be2d3'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': 'edffd1bf975a74d5d10e58c5ac8be2d3', 'q': city, 'units':'imperial'}
    response = requests.get(url, params=params)
    print(response.json())
    weather_json = response.json()

    results['text'] = format_response(response.json())

    icon_name = weather_json['weather'][0]['icon']
    open_image(icon_name)

def open_image(icon):
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw', image=img)
    weather_icon.image = img

C = tk.Canvas(app, height=HEIGHT, width=WIDTH)
background_image= tk.PhotoImage(file='./landscape.png')
background_label = tk.Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

C.pack()

frame = tk.Frame(app,  bg='#42c2f4', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
#frame_window = C.create_window(100, 40, window=frame)

textbox = tk.Entry(frame, font=40)
textbox.place(relwidth=0.65, relheight=1)

submit = tk.Button(frame, text='Get Weather', font=40, command=lambda: get_weather(textbox.get()))
#submit.config(font=)
submit.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(app, bg='#42c2f4', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

bg_color = 'white'
results = tk.Label(lower_frame, anchor='nw', justify='left', bd=4)
results.config(font=40, bg=bg_color)
results.place(relwidth=1, relheight=1)

weather_icon = tk.Canvas(results, bg=bg_color, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)






app.mainloop()
