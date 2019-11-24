# Write your code here :-)
import pulseio
from adafruit_circuitplayground.express import cpx
import time
import array
import board
import audioio
import digitalio

# Required for CircuitPlayground Express
# speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
# speaker_enable.switch_to_output(value=True)

# f = open("cplay-5.1-16bit-16khz.wav", "rb")
# a = audioio.AudioOut(board.A0, f)

""" print("playing")
a.play()
while a.playing:
  pass
print("stopped")
"""

pwm = pulseio.PWMOut(board.IR_TX, duty_cycle=2 ** 15, frequency=20000, variable_frequency=False)
pulse = pulseio.PulseOut(pwm)
#
pulses = array.array('H', [5500, 1000, 1000, 500, 500, 500, 500, 500,
  500, 500, 500, 1000, 1000, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 5500, 1000,
  1000, 500, 500, 500, 500, 500, 500, 500,
  500, 1000, 1000, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 5500, 1000, 1000, 500,
  500, 500, 500, 500, 500, 500, 500, 1000,
  1000, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 5500, 1000, 1000, 500, 500, 500,
  500, 500, 500, 500, 500, 1000, 1000, 500,
  500, 500, 500, 500, 500, 500, 500, 500,
  5500, 1000, 1000, 500, 500, 500, 500, 500,
  500, 500, 500, 1000])

pulse2 = array.array('H', [1000, 500, 500, 500, 500, 500,
  500, 500, 500, 1000, 1000, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 5500, 1000,
  1000, 500, 500, 500, 500, 500, 500, 500,
  500, 1000, 1000, 500, 500, 500, 500, 500,
  500, 500, 500, 1000])

pulse3 = array.array('H', [5401, 1054, 932, 583, 416, 578, 410, 609,
  389, 577, 411, 1079, 907, 608, 380, 587,
  412, 582, 406, 1000])

while True:
    if cpx.button_a:
        pulse.send(pulses)
        time.sleep(0.1)
        pulse.send(pulse2)
        time.sleep(0.1)
        pulse.send(pulses)
        time.sleep(0.1)
        pulse.send(pulses)
        time.sleep(0.1)
        pulse.send(pulse2)

# Modify the array of pulses.
# pulses[0] = 200
# pulse.send(pulses)