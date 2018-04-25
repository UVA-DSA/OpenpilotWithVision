#!/usr/bin/env python
import os
os.environ['OLD_CAN'] = '1'
os.environ['NOCRASH'] = '1'

import time
import unittest
import shutil
import matplotlib
matplotlib.use('svg')

from selfdrive.config import Conversions as CV, CruiseButtons as CB
from selfdrive.test.plant.maneuver import Maneuver
import selfdrive.manager as manager
from common.params import Params


def create_dir(path):
  try:
    os.makedirs(path)
  except OSError:
    pass

maneuvers = [
  Maneuver(
    'approaching a 40mph car while cruising at 60mph from 100m away',
    duration=30.,
    initial_speed = 60. * CV.MPH_TO_MS,
    #lead_relevancy=True, testvision = 1,  # original value True
    #lead_relevancy:HOOK#
    initial_distance_lead=100.,
    speed_lead_values = [40.*CV.MPH_TO_MS, 40.*CV.MPH_TO_MS],
    speed_lead_breakpoints = [0., 100.],
    cruise_button_presses = [(CB.DECEL_SET, 1.2), (0, 1.3)]
  )
]

#maneuvers = [maneuvers[-1]]

def setup_output():
  output_dir = os.path.join(os.getcwd(), 'out/longitudinal')
  if not os.path.exists(os.path.join(output_dir, "index.html")):
    # write test output header

    css_style = """
    .maneuver_title {
      font-size: 24px;
      text-align: center;
    }
    .maneuver_graph {
      width: 100%;
    }
    """

    view_html = "<html><head><style>%s</style></head><body><table>" % (css_style,)
    for i, man in enumerate(maneuvers):
      view_html += "<tr><td class='maneuver_title' colspan=5><div>%s</div></td></tr><tr>" % (man.title,)
      for c in ['distance.svg', 'speeds.svg', 'acceleration.svg', 'pedals.svg', 'pid.svg']:
        view_html += "<td><img class='maneuver_graph' src='%s'/></td>" % (os.path.join("maneuver" + str(i+1).zfill(2), c), )
      view_html += "</tr>"

    create_dir(output_dir)
    with open(os.path.join(output_dir, "index.html"), "w") as f:
      f.write(view_html)

class LongitudinalControl(unittest.TestCase):
  @classmethod
  def setUpClass(cls):

    setup_output()

    shutil.rmtree('/data/params', ignore_errors=True)
    params = Params()
    params.put("Passive", "1" if os.getenv("PASSIVE") else "0")
    params.put("IsFcwEnabled", "1")

    manager.gctx = {}
    manager.prepare_managed_process('radard')
    manager.prepare_managed_process('controlsd')
    manager.prepare_managed_process('visionInhouse')

    manager.start_managed_process('visionInhouse')
    pPool = '0'
    with open('parpool.txt','w') as writeLatMov:
      writeLatMov.write(str(pPool))
    while(1):
      with open('parpool.txt','r') as readFile:
        pPool = readFile.readline()
      if '1' in pPool:
        break
      
    time.sleep(5)
    manager.start_managed_process('radard')
    manager.start_managed_process('controlsd')

  @classmethod
  def tearDownClass(cls):
    manager.kill_managed_process('radard')
    manager.kill_managed_process('controlsd')
    manager.kill_managed_process('visionInhouse')
    time.sleep(5)

  # hack
  def test_longitudinal_setup(self):
    pass

WORKERS = 8
def run_maneuver_worker(k):
  output_dir = os.path.join(os.getcwd(), 'out/longitudinal')
  for i, man in enumerate(maneuvers[k::WORKERS]):
    score, plot = man.evaluate(output_dir)
    plot.write_plot(output_dir, "maneuver" + str(WORKERS * i + k+1).zfill(2))

for k in xrange(WORKERS):
  setattr(LongitudinalControl,
    "test_longitudinal_maneuvers_%d" % (k+1),
    lambda self, k=k: run_maneuver_worker(k))

if __name__ == "__main__":
  unittest.main()

