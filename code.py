from adafruit_circuitplayground.express import cpx
import time
import board
import pulseio

"""
Project Summary: Star Wars Propel Wearable & Shooting Target

Background: For X-mas 2018, we found a deal for Propel Star Wars "battle"
drones on Massdrop. We purchased 2 sets (Tie Fighter & X-Wings) with the
intention of giving them away as X-mas gifts to my brother & brother-in-law
who each have a son. Turns out the drones were delivered past X-mas and we
had to revert to other gifts for the season.  Lucky for us, we had a chance
to play with the drones and quickly appreciated the fun of shooting at each
other in flight.  Although my son hadn't had much prior drone experience,
he quickly got a hang of the controlling the drone in flight [with some mishaps
- first flight, he didn't have much control and did a beeline directly at his
younger sister who had to Indiana Jones dive out of the way; and during one of
the battles against me, he lost control of the drone that flew
right into my chest - I still have the scar a week later.

Project Objectives:
 1. Design a target that can be stationary or wearable that can be shot
 by the drones
 2. Design a target that keeps count of the number hits
 3. Design a target that provides an indicator of hits (audible & visual)
 4. Other Features - can be reset, battery powered, small
 5. Can be switched to Rebels or Empire
Stretch Goal
 1. Design a target that can shoot back with visual/audible indicator
    NOTE: The CP Express has a IR send function - but will need to be
    "focused" so that it can be a more direct shot vs broad
 2. Design a target that can track the drones & shoot
 3. Design a target that can move defensively (i.e. positions that a more
    difficult to hit - i.e. simulating the quintessential Star Wars
    Deflector Shields)
 4. Design a target with varying levels of difficulty based on:
    a. Number of Hits
    b. Timer
    c. Sound of Drones
    d. Team State*
 5. Design the target to leverage Star Wars sound effects
    (cannon, laser blast, hits, etc.) DONE
 5b. Reuse the Propel sound bases to provide some sound color to be
    controlled by the target
 NOTE: The level of difficulty will be based on;
    - Number & Speed of Shots from the Target
    - Speed of Movement - tracking & defensive

1/13/19 UPDATE
 PHASE 1:
 - Number of hits up to 10 shots (LEDs on the CPE)
 - 2 Targets to be built - Rebellion & Republic
 - After 10 Shots - Indicator of winner/loser - Lights & Sound
 - To be built to be stationary target and can be moved around, small enough
   footprint to be on shelf mid-height location
 - Reset functionality to restart
 - External Powered Speaker
 - 3D design to house - speaker, CPE, switch, & battery, must allow reset.

1/21/19 UPDATE
 PHASE 1:
 - Add Reset functionality to be supported w/o button press - motion Y

"""


"""
Define the data length for the drone shot IR pulse
The data length of the shot is 100 - this was found in test.
There is a secondary pulse received, unsure if this is from the remote or drone
this pulse has a length of 44.  We may decode this later to determine if
it provides information on the drone that the shot originated from
(shot signature).
OI: Run a test on the drone shooting at itself against a mirror to determine
if the drone was developed with safeguards shooting against itself or teammates
on the same team - i.e. X-wing shooting X-wing or Tie Fighter shooting
Tie Fighter

"""

IR_SHOT = 100  # IR Shot Length in test
IR_SIG = 44  # IR Signature Length - TBD if can be used for future use for team

# Global values for target settings
hit_count = 0  # Number of hits - initialize to 0
hit_win_count = 10  # Number of hits to win - limited to 10 based on CPX
force = cpx.switch  # Toggle switch on CPX Force = 0 Empire & Force = 1 Rebel
shot = pulseio.PulseIn(board.IR_RX, maxlen=100, idle_state=True)
shot.clear()
shot.resume()
rebel_hit = (0, 0, 255)  # Color for Rebel Hit
rebel_color = (0, 0, 255)  # Color for Rebel Target
empire_hit = (255, 0, 0)  # Color for Empire Hit
empire_color = (255, 0, 0)  # Color for Empire Target
clear_color = (10, 10, 10)  # Clear Color - still want a little light
recovery_mode = 0  # Set to 1 for Recovery Mode (Future Feature)
reset_movement = 10  # Y Coordinate value for reset motion

# Circuit initialization values
cpx.pixels.brightness = 0.2  # Brightness value for LEDs
cpx.detect_taps = 10

# cpx.speaker_enable.value = True

# Define our reusable functions

# Set Up Initial State
if force:
    cpx.pixels.fill(rebel_color)
else:
    cpx.pixels.fill(empire_color)

while True:
    # IR HIT Function
    if force == 0 and hit_count < hit_win_count and len(shot) == 100:
        cpx.pixels[hit_count] = rebel_hit
        cpx.play_file("Explosion+1.wav")
        hit_count += 1
        shot.clear()
        shot.resume()
    elif force == 1 and hit_count < hit_win_count and len(shot) == 100:
        cpx.pixels[hit_count] = empire_hit
        cpx.play_file("Explosion+1.wav")
        hit_count += 1
        shot.clear()
        shot.resume()

    # Target Destroyed Function
    while hit_count > hit_win_count - 1:
        if force == 1:
            while cpx.play_file("Explosion+2.wav"):
                cpx.pixels.fill(rebel_color)
                time.sleep(.1)
                cpx.pixels.fill(empire_color)
                time.sleep(.1)
                cpx.pixels.fill(clear_color)
                time.sleep(.1)
                cpx.pixels.fill(empire_color)
                time.sleep(.1)
            hit_count -= 1
        elif force == 0:
            while cpx.play_file("Explosion+2.wav"):
                cpx.pixels.fill(rebel_color)
                time.sleep(.1)
                cpx.pixels.fill(empire_color)
                time.sleep(.1)
                cpx.pixels.fill(clear_color)
                time.sleep(.1)
                cpx.pixels.fill(empire_color)
                time.sleep(.1)
            hit_count -= 1

    # Button Reset Function
    if force == 0 and cpx.button_b:
        cpx.pixels.fill(empire_color)
        time.sleep(.3)
        cpx.pixels.fill(clear_color)
        time.sleep(.2)
        cpx.pixels.fill(empire_color)
        hit_count = 0
        cpx.play_file("imperial.wav")
    elif force == 1 and cpx.button_b:
        cpx.pixels.fill(rebel_color)
        time.sleep(.3)
        cpx.pixels.fill(clear_color)
        time.sleep(.2)
        cpx.pixels.fill(rebel_color)
        hit_count = 0
        cpx.play_file("starwars.wav")

    # Tap Reset Function
    if force == 0 and cpx.tapped:
        cpx.pixels.fill(empire_color)
        time.sleep(.3)
        cpx.pixels.fill(clear_color)
        time.sleep(.2)
        cpx.pixels.fill(empire_color)
        hit_count = 0
        # cpx.play_file("imperial.wav")
    elif force == 1 and cpx.tapped:
        cpx.pixels.fill(rebel_color)
        time.sleep(.3)
        cpx.pixels.fill(clear_color)
        time.sleep(.2)
        cpx.pixels.fill(rebel_color)
        hit_count = 0
        # cpx.play_file("starwars.wav")

    # Button Test Function
    if force == 0 and hit_count < hit_win_count and cpx.button_a:
        cpx.pixels[hit_count] = rebel_hit
        cpx.play_file("Explosion+1.wav")
        hit_count += 1
    elif force == 1 and hit_count < hit_win_count and cpx.button_a:
        cpx.pixels[hit_count] = empire_hit
        cpx.play_file("Explosion+1.wav")
        hit_count += 1