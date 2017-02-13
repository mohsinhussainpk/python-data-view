#!python3
# -*- coding: UTF-8 -*-

import requests

import matplotlib.pyplot as plt
import matplotlib.dates as mdate

import numpy as np
import datetime as dt


### CONFIG SECTION
n = 1000
mac = '18:fe:34:de:a4:2c'

url_h = "https://www.terasyshub.io/api/v1/data/humidity/{}?order=desc&results={}".format(mac, n)
url_t = "https://www.terasyshub.io/api/v1/data/temperature/{}?order=desc&results={}".format(mac, n)
### END of config section


def get_data():
    """ Gets the data for temperature and humidity """
    # get the data
    r_t = requests.get(url_t)
    # check for errors
    if r_t.status_code != 200:
        print(r_t.status_code)
        exit()
    # extract data from JSON data, first timestamps
    ts = [l['timestamp'] for l in r_t.json()]
    # Convert to the correct format for matplotlib.
    temp_times = mdate.epoch2num(ts)
    # extract values from JSON
    temp_vals =  [l['value'] for l in r_t.json()]
    # same procedure for humidity
    r_h = requests.get(url_h)
    if r_h.status_code != 200:
        print(r_h.status_code)
        exit()
    ts = [l['timestamp'] for l in r_h.json()]
    hum_times = mdate.epoch2num(ts)
    hum_vals =  [l['value'] for l in r_h.json()]
    # return data for plotting
    return { 'temp' : [temp_times, temp_vals], 'hum': [hum_times, hum_vals]}
        

if __name__ == "__main__":
    # get the data
    data = get_data()

    ################### PLOT #########################
    # intialize plot
    fig, ax1 = plt.subplots()
    plt.xlabel("time [UTC]")
    plt.title("Last {} measured data of device {}".format(n,mac))
    plt.grid(True)

    # Plot the date using plot_date rather than plot
    #ax.plot_date(secs, vals)
    ax1.plot_date(*data['temp'], fmt="ro-")
    ax1.set_ylabel("Temperature [C]", color="r")
    ax1.tick_params("y", colors="r")
    
    ax2 = ax1.twinx()
    ax2.plot_date(*data['hum'], fmt="go-")
    ax2.set_ylabel("Humidity [%]", color="g")
    ax2.tick_params("y", colors="g")

    # Choose your xtick format string
    date_fmt = '%y-%m-%d %H:%M'

    # Use a DateFormatter to set the data to the correct format.
    date_formatter = mdate.DateFormatter(date_fmt)
    ax1.xaxis.set_major_formatter(date_formatter)

    # Sets the tick labels diagonal so they fit easier.
    fig.autofmt_xdate()

    # shows the plot
    plt.show()
