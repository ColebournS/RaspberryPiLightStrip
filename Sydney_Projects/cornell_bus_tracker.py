# cornell_bus_tracker.py helps you to make the cornell bus on time!
# - web scrapes tompkins tcat (aka cornell university bus) website that has real time information
# - outputs departure time and minutes until departure and updates every 20 seconds
# - controls leds connected to raspberry pi to show minutes until departure
#   - color slowly changes from blue to red as departure time approaches
#   - number of pixels lit up in a row = number of minutes until departure time
#   - at 5 minutes until departure, flashes leds on and off

import re
import time
import board
import neopixel
import requests
from bs4 import BeautifulSoup
import arrow 
import json

tcat_url = 'https://realtimetcatbus.availtec.com/InfoPoint/Minimal/'

pause_time = 20.0

wait_time = 0.001

flash_time = 1

pixel_pin = board.D18

num_pixels = 300

ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# controls leds
def bus_lights(num, wait):
    for i in range(num_pixels):
        if (num > 300):
            num = 0
        if (i % (num + 1) == 0):
            pixels[i] = (0,0,0)
        else:
            color_num = (max(min(num, 15), 5) - 5) * 25
            pixels[i] = (255-color_num,0,color_num)
        pixels.show()
        if (num == 5):
            for i in range(num_pixels):
                pixels[i] = (255,0,0)
            pixels.show()
            time.sleep(flash_time)
            for i in range(num_pixels):
                pixels[i] = (0,0,0)
            pixels.show()
            time.sleep(flash_time)
        time.sleep(wait)

# web scrapes route info from tcat website
def get_route(stop_id, route_name):
    r = requests.get(tcat_url + 'Departures/ForStop?stopId=' + stop_id)
    soup = BeautifulSoup(r.content, 'html.parser')
    route = soup.find('div', text=re.compile(route_name)) 
    return route

# web scrapes stop info from tcat website
def get_stop(route_num, stop_name):
    r = requests.get(tcat_url + 'Stops/ForRoute?routeId=' + route_num)
    soup = BeautifulSoup(r.content, 'html.parser')
    stop = soup.find('a', text=re.compile(stop_name)) 
    return stop

# web scrapes next stop info from tcat website
def get_next_stop(stop, stop_name):
    next_stop = stop.find_next('a', text=re.compile(stop_name))
    return next_stop

# web scrapes departure info from tcat website
def get_departure(departure, departure_num):
    while (departure_num > 0 and departure != None):
        if (departure.text == 'Done'):
            break
        departure = departure.find_next('div', class_='departure')
        departure_num -= 1
    return departure

# gets departure time from current time and departure info
def get_departure_time(now, departure_text):
    departure_time = arrow.get(departure_text + ' -04:00', 'h:mm A ZZ')
    departure_time = departure_time.shift(years=(now.year - 1), months=(now.month - 1), days=(now.day - 1))
    return departure_time

# uses inputs to web scrape tcat website, display info, and control leds
def show_results(stop_id, next_stop_id, direction, route_name, departure_num):
    if (direction != None):
        route_name = route_name + direction

    route = get_route(stop_id, route_name)
    
    if (route == None and next_stop_id != None):
        route = get_route(next_stop_id, route_name)

    departure = get_departure(route, departure_num)

    if (route == None or departure == None):
        return

    print(route.text)
    print(departure.text)

    diff_time = 0
    if (departure.text != 'Done'):
        current_time = arrow.now()
        departure_time = get_departure_time(current_time, departure.text)

        diff = departure_time.humanize(current_time, granularity='minute')
        print(diff)
        
        diff_time = (int)((departure_time - current_time).seconds / 60)
        bus_lights(diff_time, wait_time)

# gets route mapper using info from route.json
def get_route_mapper():
    route_mapper = None
    with open('routes.json', 'r') as openfile:
        route_mapper = json.load(openfile)
    return route_mapper

# gets route inputs from user
def get_route_input(route_mapper):
    route_num = None
    route_name = None
    while (route_name == None):
        route_num = input('Route Number: ')
        for route in route_mapper['routes']:
            if (int(route['num']) == int(route_num)):
                route_name = route['name']
    return route_num, route_name

# gets direction inputs from user
def get_direction_input():
    direction = input('Inbound or Outbound: ')
    direction = ' - ' + direction
    return direction

# gets stop inputs from user
def get_stop_input(route_num):
    stop_id = None
    next_stop_id = None
    direction = None
    while(stop_id == None):
        stop_name = input('Stop Name: ')
        stop = get_stop(route_num, stop_name)
        if (stop != None):
            stop_id = stop.attrs['stopid']
            next_stop = get_next_stop(stop, stop_name)
            if (next_stop != None):
                next_stop_id = next_stop.attrs['stopid']
                direction = get_direction_input()
    return stop_id, next_stop_id, direction

# gets departure inputs from user
def get_departure_input():
    departure_num = None
    while (departure_num == None):
        input_num = input('Departure Number: ')
        if (input_num.isnumeric()):
            departure_num = int(input_num)
    return departure_num

# pauses code
def sleep(start_time):
    time.sleep(pause_time - ((time.time() - start_time) % pause_time))


start_time = time.time()

route_mapper = get_route_mapper()

route_num, route_name = get_route_input(route_mapper)    

stop_id, next_stop_id, direction = get_stop_input(route_num)

departure_num = get_departure_input()
    
while True:
    show_results(stop_id, next_stop_id, direction, route_name, departure_num)
    sleep(start_time)