"""This program outputs square waves

Output mapping:
-CV A: A pulse LFO at a given frequency.
-CV B: Same pulse LFO as CV A but phase shifted by 50%.
"""

import winterbloom_sol as sol

saw_lfo = sol.SawtoothLFO(0.25)


def loop (last, state, outputs):

  # Make unipolar pulse waves out of the saw_lfo
  outputs.cv_a = (((saw_lfo.output + 1) / 2) > 0.5) * 5.0
  
  outputs.cv_b = (((saw_lfo.output + 1) / 2) < 0.5) * 5.0
  
 sol.run(loop)
