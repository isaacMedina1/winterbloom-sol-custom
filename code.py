"""
A sequencer with some parameters controlled by CC MIDI
and a Slew limiter on pitch output.

Based on "7_random.py" factory example.

Input CC
    CC16: Clock Division
    CC17: Octave

Output CV
    CV A: Pitch CV based on a random note
    CV B: Sine LFO
    Gate 1: Gate on/off for the note.
    Gate 2: Trigger on clock division

TODO: change array of notes, LFO frequency and trigger division with CC.

"""

import random

import winterbloom_sol as sol

# Declare a list of notes in intervals from root 0
notes = [
    0,
    2,
    3,
    5,
    7,
    8,
    10,
    12
]

# Declare a list of available subdivitions
# And get list length - 1
div_list = [2, 4, 6, 8, 16, 32]

div_len = len(div_list)-1

# Define a function to map CC
def map_cc(ctl, min, max):
    m = int(((ctl-0) * (max-min) / (1-0) + min))
    return m;

# Create a slew limiter
slew_limiter = sol.SlewLimiter(rate=0.1)  # Rate in seconds.

# Create LFO
sine_lfo = sol.SineLFO(0.5)

def loop(last, state, outputs):

    # Map cc(16) to integers for division selection
    cc_16 = map_cc(state.cc(16), 0, div_len)

    # Map cc(17) to integers for octave selection
    cc_17 = map_cc(state.cc(17), 2, 5)

    # Select octave from cc(17)
    octave = cc_17 * 12

    # Assign an item from 'div_list' to variable 'div'
    div = div_list[cc_16]

    if sol.should_trigger_clock(state, div):

        # Select a random note.
        note = octave + random.choice(notes)

        # Trigger the gate.
        outputs.trigger_gate_1()

        # Set slew_limiter target
        slew_limiter.target = sol.voct(note)

        # Set as output
        outputs.cv_a = slew_limiter.output

    # Otherwise, no need to have the gate on.
    else:
        outputs.gate_1 = False

    # Trigger on clock division
    if sol.should_trigger_clock(state, 2):
        outputs.trigger_gate_2()

    # Output LFO
    outputs.cv_b = sine_lfo.output * 1.0

sol.run(loop)
