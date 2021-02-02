"""
# Unipolar Variable LFO v1.2

Two Unipolar LFOs with variable frequency whose shape bends from triangle to pulse.
[LFO a] can be influenced by [LFO b] for complex modulations.
[LFO b] gives a simple waveform output.
Both outputs as well as the influence parameter can be attenuated.

Input CC:
    CC 18: Shape a
    CC 19: Frequency a
    CC 20: Attenuator a-b
    CC 21: Shape b
    CC 22: Frequency b
    CC 23: Attenuator a
    CC 24: Attenuator b

Output:
    CV a: Unipolar Variable LFO - Complex (a-b)
    CV b: Unipolar Variable LFO - Simple (b)

Based on Partice Tarrabia and Bram de Jong's waveshaper algorithm
https://www.musicdsp.org/en/latest/Effects/46-waveshaper.html
"""

import winterbloom_sol as sol

# Define a function to map CC
def map_cc(ctl, min, max):
    m = ((ctl-0) * (max-min) / (1-0) + min)
    return m;

# Create two triangle LFOs
tri_lfo_a = sol.TriangleLFO(0.5)

tri_lfo_b = sol.TriangleLFO(0.5)

def loop(last, state, outputs):

    # Prevent CC to hit 1 for shape amounts
    shape_amt_a = state.cc(18) * 0.999

    shape_amt_b = state.cc(21) * 0.999

    # Get k from shape amount
    k_a = (shape_amt_a * 2) / (1 - shape_amt_a)

    k_b = (shape_amt_b * 2) / (1 - shape_amt_b)

    # Set LFO frequencies from CC
    freq_a = state.cc(19) + 0.01

    freq_b = state.cc(22) + 0.01

    tri_lfo_a.frequency = freq_a * 20.0

    tri_lfo_b.frequency = freq_b * 15.0

    # Map attenuators with CC up to 5V
    atten_a = map_cc(state.cc(23), 0.1, 5)

    atten_b = map_cc(state.cc(24), 0.1, 5)

    # Do the math for the waveshapers
    waveshaper_a = (1 + k_a) * tri_lfo_a.output / (1 + k_a * abs(tri_lfo_a.output))

    waveshaper_b = (1 + k_b) * tri_lfo_b.output / (1 + k_b * abs(tri_lfo_b.output))

    # Make them unipolar
    unipolar_a = ((waveshaper_a * 0.5) + 0.5)

    unipolar_b = ((waveshaper_b * 0.5) + 0.5)

    # Get a complex waveform by influencing a with b
    # Also use a CC to control attenuation
    complex = abs(unipolar_a - (unipolar_b * state.cc(20)))

    # Set LFO outputs and attenuate to taste
    outputs.cv_a = complex * atten_a

    outputs.cv_b = unipolar_b * atten_b

sol.run(loop)
