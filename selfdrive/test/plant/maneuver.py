from maneuverplots import ManeuverPlot
from plant import Plant
from common.realtime import sec_since_boot
import numpy as np
import os


class Maneuver(object):
  def __init__(self, title, duration, **kwargs):
    # Was tempted to make a builder class
    self.distance_lead = kwargs.get("initial_distance_lead", 200.0)
    self.speed = kwargs.get("initial_speed", 0.0)
    self.lead_relevancy = kwargs.get("lead_relevancy", 0) 

    self.grade_values = kwargs.get("grade_values", [0.0, 0.0])
    self.grade_breakpoints = kwargs.get("grade_breakpoints", [0.0, duration])
    self.speed_lead_values = kwargs.get("speed_lead_values", [0.0, 0.0])
    self.speed_lead_breakpoints = kwargs.get("speed_lead_breakpoints", [0.0, duration])

    self.cruise_button_presses = kwargs.get("cruise_button_presses", [])

    self.duration = duration
    self.title = title

    self.frameIdx = 0  # added by Hasnat
    self.pathOffset = 0.0  # added by Hasnat
    self.lLane = -1.85  # added by Hasnat
    self.rLane = 1.85  # added by Hasnat
    self.dPath = 0.0  # added by Hasnat
    self.headway_time = 30.0  # added by Hasnat
    self.testvision = kwargs.get('testvision', 0)  # added by Hasnat

    self.effect = 0  # added by Hasnat
    self.thickness = 0  # added by Hasnat

  def evaluate(self, output_dir):
    ############# added by Hasnat
    '''Create files to record the outputs and alerts/hazards -- Hasnat'''
    out_file = output_dir + '/outputs.csv'
    hazard_file = output_dir + '/hazards.txt'
    alert_file = output_dir + '/alerts.txt'
    fault_file = output_dir + '/fault_times.txt'

    outfile = open(out_file, 'w')
    outfile.write('frameIdx, distance(m), speed(m/s), acceleration(m/s2), angle_steer, gas, brake, steer_torque, d_rel(m), v_rel(m/s), c_path(m)\n')

    hazardfile = open(hazard_file, 'w')
    hazardfile.write('*********Hazards generated in this test run**********\n')

    alertfile = open(alert_file, 'w')
    alertfile.write('*********Alerts generated in this test run**********\n')
    alertfile.close()

    faultfile = open(fault_file, 'w')
    faultfile.close()
    fwriteFile = open('frameId.txt','w')
    fwriteFile.close()

    visionLane = 1  # use path model from matlab output
    angle_steer = 0.0
    prev_distance = 0.0
    prev_angle_steer = 0.0
    delta_lane = 0.0
    thetaFactor = 0.1067  # this value has been derived empirically
    '''
    if visionLane==1:
      visionFile = os.path.join(os.getcwd(),'laneData.dat')
      with open(visionFile, 'r') as visionfile:
        line = visionfile.readline()
        lanes = line.split(',')
        lanes = [float(i) for i in lanes]
    '''
    lanesCl=[]
    lanesFl = []

    # for clean images
    if visionLane==1:
      visionFile = os.path.join(os.getcwd(),'laneData.dat')
      with open(visionFile, 'r') as visionfile:
        for line in visionfile:
          lanesStr = line.split(',')
          lanesCl.append( [float(i) for i in lanesStr])

    # for noisy images
    '''
    if visionLane==1:
      visionFile = os.path.join(os.getcwd(),'laneData_noisy.dat')
      with open(visionFile, 'r') as visionfile:
        for line in visionfile:
          lanesStr = line.split(',')
          lanesFl.append( [float(i) for i in lanesStr])

    cPathPoint = [];
    with open('centerPath.dat','r') as cPathFile:
      for line in cPathFile:
        line = line.replace('\n','');
        if self.testvision > 0:
          cPathPoint.append(float(line))
        else:
          cPathPoint.append(0.0) 
    '''
    ######## -- check frame updates from vision
    prevLlane = self.lLane
    prevRlane = self.rLane
    frameUpdate = 0.
    cpPoint = 0.
    #########

    l_ind = 0
    lanes = lanesCl[l_ind]
    left_line = lanes[0]
    right_line = lanes[1]

    reportHazardH1 = True
    reportHazardH2 = True
    reportHazardH3 = True
    
    """runs the plant sim and returns (score, run_data)"""
    plant = Plant(
      lead_relevancy = self.lead_relevancy,
      speed = self.speed,
      distance_lead = self.distance_lead
    )

    last_live100 = None
    plot = ManeuverPlot(self.title)

    buttons_sorted = sorted(self.cruise_button_presses, key=lambda a: a[1])
    current_button = 0
    while plant.current_time() < self.duration:
      while buttons_sorted and plant.current_time() >= buttons_sorted[0][1]:
        current_button = buttons_sorted[0][0]
        buttons_sorted = buttons_sorted[1:]
        print "current button changed to", current_button
    
      grade = np.interp(plant.current_time(), self.grade_breakpoints, self.grade_values)
      speed_lead = np.interp(plant.current_time(), self.speed_lead_breakpoints, self.speed_lead_values)

      self.frameIdx = self.frameIdx + 1    # added by Hasnat
      if self.frameIdx == 120:
        with open('procImages.txt','w') as procImFile:
          procImFile.write('1');


      #print self.frameIdx

      distance, speed, acceleration, distance_lead, brake, gas, steer_torque, fcw, live100, angle_steer, reportHazardH1, reportHazardH2, reportHazardH3, self.headway_time = plant.step(reportHazardH1, reportHazardH2, reportHazardH3, outfile, hazardfile, speed_lead, current_button, grade, self.frameIdx, self.pathOffset, self.lLane, self.rLane, delta_lane) # angle_steer (return parameter), outfile, hazardfile, self.frameIdx, self.pathOffset, lLane, rLane added by Hasnat

      ############ lateral change w.r.t. angle_steer -- added by Hasnat
      delta_lane = (angle_steer-prev_angle_steer)/thetaFactor
      #print delta_lane
      #self.lLane -= delta_lane
      #self.rLane -= delta_lane
      self.dPath += delta_lane
      #print self.lLane
      #print self.rLane
      #print self.dPath

      if self.testvision > 0:
        ### Incorrect/noisy camera input
        #visionFault:HOOK#
        
        with open('latMov.txt','w') as writeLatMov:
          writeLatMov.write(str(self.effect)+','+str(self.thickness)+','+str(self.dPath))

      if self.testvision > 0:
        with open('laneData.dat','r') as readLanes:
          readL = readLanes.read()
          readL = readL.split(',')
          if len(readL)>1:
            readL[1] = readL[1].replace('\n','')
            self.lLane = float(readL[0])
            self.rLane = float(readL[1])

        #print '++++++++++++++++++++++++++++'
        #print self.lLane
        #print self.rLane
        if (prevLlane != self.lLane) and (prevRlane != self.rLane):
          #cpPoint = cPathPoint[int(frameUpdate)]
          with open('frameId.txt','a') as fwriteFile:
            fwriteFile.write(str(self.frameIdx*10.)+'ms\n')
          frameUpdate += 1.

        prevLlane = self.lLane
        prevRlane = self.rLane


      '''
      if self.frameIdx % 10 == 0:
        if l_ind < len(lanesCl)-1:
          l_ind += 1
        lanes = lanesCl[l_ind]

        ### Incorrect/noisy camera input
        #visionFault:HOOK#
        
        if self.testvision > 0:
          #print angle_steer
          self.lLane = lanes[0] - self.dPath
          self.rLane = lanes[1] - self.dPath
      '''


      ### Incorrect Process Model
      #md:HOOK#

      prev_angle_steer = angle_steer
      prev_distance = distance


      #########################


      if live100:
        last_live100 = live100[-1]

      d_rel = distance_lead - distance if self.lead_relevancy else 200. 
      v_rel = speed_lead - speed if self.lead_relevancy else 0. 

      if last_live100:
        # print last_live100
        #develop plots
        plot.add_data(
          time=plant.current_time(),
          gas=gas, brake=brake, steer_torque=steer_torque,
          distance=distance, speed=speed, acceleration=acceleration,
          up_accel_cmd=last_live100.upAccelCmd, ui_accel_cmd=last_live100.uiAccelCmd,
          uf_accel_cmd=last_live100.ufAccelCmd,
          d_rel=d_rel, v_rel=v_rel, v_lead=speed_lead,
          v_target_lead=last_live100.vTargetLead, pid_speed=last_live100.vPid,
          cruise_speed=last_live100.vCruise,
          jerk_factor=last_live100.jerkFactor,
          a_target=last_live100.aTarget,
          fcw=fcw)
    
    print "maneuver end"
    print (frameUpdate*100.)/float(self.frameIdx - 130)

    return (None, plot)


