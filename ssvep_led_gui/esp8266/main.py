import json
from machine import Pin
from utime import ticks_ms, sleep
import urequests


def tick():
	# return time in seconds with flots until milliseconds
	return ticks_ms() / 1000


def update_led_config():

	#res = urequests.get("http://10.42.0.1:8888/esp8266")
	#config = res.json()
	
	config = {"n_trial": 5,
		 "t_trial": 5,
		"interval": 2,
		"leds": {
		1: {"pin": 16, "on": 1, "freq": 1, "duty": 50},
		2: {"pin": 4, "on": 1, "freq": 2,  "duty": 50}, 
		3: {"pin":14, "on": 1, "freq": 4,  "duty": 50}, 
		4: {"pin": 15, "on": 1,"freq": 8,  "duty": 50}}}
	
	pins = list()
	times = list()
	d_cycle = list()
	
	
	for k, v in config['leds'].items():   # k stores tha number of the leds(1,2,3...), while v stores the led info (pin, on/off, freq)
		if v['on']:
			period = 1 / v['freq']   
			pins.append(Pin(v['pin'], Pin.OUT))
			times.append(period)
			d_cycle.append(v['duty']/100)

		# store values on/off of leds
	vals = [True for _ in range(len(pins))]   #True for those pins with state = "on"
		# execute the number of trials
	for _ in range(config['n_trial']):
		now = tick()
		counts = [tick() for _ in range(len(pins))]

		while (tick() - now) < config['t_trial']:  

			for i in range(len(pins)):

				if (tick() - counts[i] <= times[i]*d_cycle[i] and tick()-counts[i] < times[i]):
					pins[i].value(1) 

				elif(tick() - counts[i]) >= times[i]:
					counts[i] = tick()

				else:
					pins[i].value(0)

		# turn off all leds
		[p.value(0) for p in pins]

		sleep(config['interval'])          # interval between trials

		#res.close()     # connection needs to close


if __name__ == "__main__":
    
	while True:
	
		button = Pin(5, Pin.IN)
		get_state = button.value()
		sleep(0.01)
		if not get_state:
			update_led_config()
		
# set push button to finish app


#		btn_finish = Pin(12, Pin.IN, Pin.PULL_UP)
#		finish = btn_finish.value()
#		#set push button to update app
#		btn_update = Pin(13, Pin.IN, Pin.PULL_UP)
#		first = btn_update.value()
#		sleep(0.01)
#		second = btn_update.value()
#		# control the update
#		if not first and second:
#		update_led_config()
		# control the finish app
#		if not finish:
#			print('Application finished!')
#			break

