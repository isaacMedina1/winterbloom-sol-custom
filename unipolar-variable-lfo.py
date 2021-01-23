"""
# Unipolar Variable LFO

An Unipolar LFO with variable frequency
whose shape bends from triangle to pulse.
Output can be also attenuated.

Input CC:
    CC 18: LFO Shape
    CC 19: LFO Frequency
    CC 20: Attenuator

Output:
    CV A: Unipolar Variable LFO

Based on Partice Tarrabia and Bram de Jong's waveshaper algorithm
https://www.musicdsp.org/en/latest/Effects/46-waveshaper.html
"""

import winterbloom_sol as sol

# Define a function to map CC
def map_cc(ctl, min, max):
    m = ((ctl-0) * (max-min) / (1-0) + min)
    return m;

# Create triangle LFO
tri_lfo = sol.TriangleLFO(0.5)

def loop(last, state, outputs):

    # Prevent CC to hit 1 for shape_amt
    shape_amt = state.cc(18) * 0.999

    # Get k from shape_amt
    k = (shape_amt * 2) / (1 - shape_amt)

    # Set LFO frequency from CC
    freq = state.cc(19) + 0.01

    tri_lfo.frequency = freq * 20.0

    # Map an attenuator with CC up to 5V
    atten = map_cc(state.cc(20), 0.1, 5)

    # Do the math for the waveshaper
    waveshaper = (1 + k) * tri_lfo.output / (1 + k * abs(tri_lfo.output))

    # Set LFO output as unipolar and attenuate to taste
    outputs.cv_a = ((waveshaper * 0.5) + 0.5) * atten

sol.run(loop)
