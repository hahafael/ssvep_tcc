import json
from machine import Pin
from utime import ticks_ms, sleep
import urequests


def tick():
    # return time in seconds with flots until milliseconds
    return ticks_ms() / 1000


def update_led_config():
    res = urequests.get("http://10.42.0.1:8888/esp8266")
    config = res.json()
    pins = list()
    times = list()
    for k, v in config['leds'].items():   # k stores tha number of the leds(1,2,3...), while v stores the led info (pin, on/off, freq)
        if v['on']:
            freq = 1 / v['freq'] / 2   # should be:  period_high = 1/v['freq']*duty_cycle
            # store the active pin classes
            pins.append(Pin(v['pin'], Pin.OUT))
            # time calculated by "1/f" and divides by 2 (half time on/off)
            times.append(freq)
    # store values on/off of leds
    vals = [True for _ in range(len(pins))]   #True for those pins with state = "on"
    # execute the number of trials
    for _ in range(config['n_trial']):
        now = tick()
        counts = [tick() for _ in range(len(pins))]
        # control the time of each trial
        while (tick() - now) < config['t_trial']: #do while the difference (time passed) is lower than the trial time. 
            # control the frequency of each led
            for i in range(len(pins)):
                if (tick() - counts[i]) >= times[i]: #swaps the logic level of the led if the passed time is greater than the  half-period defined. 
                    pins[i].value(vals[i])
                    vals[i] = not vals[i]
                    counts[i] = tick() #update the refential time for the next leds. 
        # turn off all leds
        [p.value(0) for p in pins]

        sleep(config['interval'])          # interval between trials

    res.close()     # connection needs to close


if __name__ == "__main__":
    
    print('Application started!')
    while True:
        # set push button to finish app
        btn_finish = Pin(12, Pin.IN, Pin.PULL_UP)
        finish = btn_finish.value()
        # set push button to update app
        btn_update = Pin(13, Pin.IN, Pin.PULL_UP)
        first = btn_update.value()
        sleep(0.01)
        second = btn_update.value()
        # control the update
        if not first and second:
            update_led_config()
        # control the finish app
        if not finish:
            print('Application finished!')
            break

