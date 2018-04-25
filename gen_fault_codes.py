import os
import numpy as np
import random


def gen_add_code(trigger_code, trigger, t1, t2, variable, stuck_value, additional_code):
    assert(len(variable) == len(stuck_value))
    if trigger_code:
      code = trigger_code
    else:
      code = 'if %s>=%s and %s<=%s:' % \
            (trigger, t1, trigger, t2)
    for v, s in zip(variable, stuck_value):
        l = '//%s+=%s' % (v,s)
        code = code + l
    code = code + additional_code
    return code

def gen_sub_code(trigger_code, trigger, t1, t2, variable, stuck_value, additional_code):
    assert(len(variable) == len(stuck_value))
    if trigger_code:
      code = trigger_code
    else:
      code = 'if %s>=%s and %s<=%s:' % \
            (trigger, t1, trigger, t2)
    for v, s in zip(variable, stuck_value):
        l = '//%s-=%s' % (v,s)
        code = code + l
    code = code + additional_code
    return code

def gen_none_code(trigger_code, trigger, t1, t2, additional_code):
    if trigger_code:
      code = trigger_code
    else:
      code = 'if %s>=%s and %s<=%s:' % \
            (trigger, t1, trigger, t2)
    l = '//none'
    code = code + l
    code = code + additional_code
    return code

def gen_uniform_rand_code(trigger_code, trigger, t1, t2, variable, d1, d2, additional_code):
    if trigger_code:
      code = trigger_code
    else:
      code = 'if %s>=%s and %s<=%s:' % \
            (trigger, t1, trigger, t2)
    for i in range(len(variable)):
      delta = random.uniform(d1,d2) + (i*3.7)
      l = '//%s+=(%s)' % (variable[i],str(delta))
      code = code + l
    code = code + additional_code
    return code

def gen_stuck_code(trigger_code, trigger, t1, t2, variable, stuck_value, additional_code):
    assert(len(variable) == len(stuck_value))
    if trigger_code:
      code = trigger_code
    else:
      code = 'if %s>=%s and %s<=%s:' % \
            (trigger, t1, trigger, t2)
    for v, s in zip(variable, stuck_value):
        l = '//%s=%s' % (v,s)
        code = code + l
    code = code + additional_code
    return code


### Write codes to fault library file
def write_to_file(fileName, code, param, exp_name, target_file, faultLoc):
    if os.path.isdir('fault_library') != True:
      os.makedirs('fault_library')
    fileName = 'fault_library/scenario_'+str(sceneNum)
    out_file = fileName+'.txt'
    param_file = fileName+'_params.csv'

    with open(out_file, 'w') as outfile:
        print out_file
        outfile.write('title:' + exp_name + '\n')
        outfile.write('location//' + target_file+ '//'+faultLoc + '\n')
        for i, line in enumerate(code):
            outfile.write('fault ' + str(i+1) + '//' + line + '\n')
        outfile.write('Total number of fault cases: '+str(i+1))

    with open(param_file, 'w') as outfile:
        for i, line in enumerate(param):
            outfile.write(str(i) + ',' + line + '\n')

    with open('run_fault_inject_campaign.sh', 'a+') as runFile:
        runFile.write('python run.py '+fileName+'\n')

### Write codes to fault library file -- for vision effects
def write_to_vision_file(fileName, code, param, exp_name, target_file, faultLoc):
    if os.path.isdir('fault_library') != True:
      os.makedirs('fault_library')
    effect = fileName
    fileName = 'fault_library/scenario_'+str(sceneNum)
    out_file = fileName+'.txt'
    param_file = fileName+'_params.csv'

    with open(out_file, 'w') as outfile:
        print out_file
        outfile.write('title:' + exp_name + '\n')
        outfile.write('location//' + target_file+ '//'+faultLoc + '\n')
        for i, line in enumerate(code):
            outfile.write('fault ' + str(i+1) + '//' + line + '\n')
        outfile.write('Total number of fault cases: '+str(i+1))

    with open(param_file, 'w') as outfile:
        for i, line in enumerate(param):
            outfile.write(str(i) + ',' + line + '\n')


    with open('run_fault_inject_campaign.sh', 'a+') as runFile:
      for thickness in range(1,11):
        if os.path.isdir('../output_files/'+str(sceneNum)+'_vision_'+effect+'/'+str(thickness)) != True:
          os.makedirs('../output_files/'+str(sceneNum)+'_vision_'+effect+'/'+str(thickness))
        runFile.write('./run_matlab_openpilot.sh '+effect+' '+str(thickness)+'\n')
        runFile.write('python run.py '+fileName+'\n')
        runFile.write('cp -R '+'../output_files/'+exp_name+' '+'../output_files/'+str(sceneNum)+'_vision_'+effect+'/'+str(thickness)+'/\n')



### d_rel-add-incRADAR-H1
def gen_rel_dist_add_fault_plant(sceneNum):
    title = str(sceneNum)+'_d_rel-add-incRADAR-H1'
    faultLibFile = 'fault_library/dRelPlantRad'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#radar_dRel:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = ['radar_dRel']
    deltaRange = np.arange(15,255,10)
    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d in deltaRange:
          delta = random.randint(d,d+9)
          #code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-add-incVision-H1
def gen_vision_dRel_add_fault_plant(sceneNum):
    title = str(sceneNum)+'_d_rel-add-incVision-H1'
    faultLibFile = 'fault_library/dRelPlantVis'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#vision_dRel:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = ['vision_dRel']
    deltaRange = np.arange(15,255,10)
    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d in deltaRange:
          delta = random.randint(d,d+9)
          #code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-add-incRadVis-H1
def gen_RadVis_dRel_add_fault_plant(sceneNum):
    title = str(sceneNum)+'_d_rel-add-incRadVis-H1'
    faultLibFile = 'fault_library/dRelPlantRadVis'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#RadVis_dRel:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = ['d_rel']
    deltaRange = np.arange(15,255,10)
    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d in deltaRange:
          delta = random.randint(d,d+9)
          #code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-sub-incRADAR-H2
def gen_rel_dist_sub_fault_plant(sceneNum):
    title = str(sceneNum)+'_d_rel-sub-incRADAR-H2'
    faultLibFile = 'fault_library/dRelPlantRad'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#radar_dRel:HOOK#'
    trigger = 'radar_dRel'
    trigger_code = 'if not self.lead_relevancy:'
    code = []
    param = []
    variable = ['radar_dRel']
    deltaRange = np.arange(10,255,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [200]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          code.append(gen_sub_code(trigger_code,trigger, t1, t2, variable, [delta], '//if '+variable[0]+'<0:'+'//  '+variable[0]+'= 0'))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-sub-incVision-H2
def gen_vision_dRel_sub_fault_plant(sceneNum):
    title = str(sceneNum)+'_d_rel-sub-incVision-H2'
    faultLibFile = 'fault_library/dRelPlantVis'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#vision_dRel:HOOK#'
    trigger = 'vision_dRel'
    trigger_code = 'if not self.lead_relevancy:'
    code = []
    param = []
    variable = ['vision_dRel']
    deltaRange = np.arange(10,255,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [200]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          code.append(gen_sub_code(trigger_code,trigger, t1, t2, variable, [delta], '//if '+variable[0]+'<0:'+'//  '+variable[0]+'= 0'))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-sub-incRadVis-H2
def gen_RadVis_dRel_sub_fault_plant(sceneNum):
    title = str(sceneNum)+'_d_rel-sub-incRadVis-H2'
    faultLibFile = 'fault_library/dRelPlantRadVis'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#RadVis_dRel:HOOK#'
    trigger = 'd_rel'
    trigger_code = 'if not self.lead_relevancy:'
    code = []
    param = []
    variable = ['d_rel']
    deltaRange = np.arange(10,255,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [200]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          code.append(gen_sub_code(trigger_code,trigger, t1, t2, variable, [delta], '//if '+variable[0]+'<0:'+'//  '+variable[0]+'= 0'))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)



### v_rel-add-incRADAR-H1
def gen_rel_vel_add_fault_plant(sceneNum):
    title = str(sceneNum)+'_v_rel-add-incRADAR-H1'
    faultLibFile = 'fault_library/vRelPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#radar_dRel:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = ['v_rel']
    deltaRange = np.arange(10,61,10)
    
    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d in deltaRange:
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### v_rel-sub-incRADAR-H2
def gen_rel_vel_sub_fault_plant(sceneNum):
    title = str(sceneNum)+'_v_rel-sub-incRADAR-H2'
    faultLibFile = 'fault_library/vRelPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#radar_dRel:HOOK#'
    trigger = 'radar_dRel'
    trigger_code = 'if not self.lead_relevancy and self.current_time()>0:'
    code = []
    param = []
    variable = ['v_rel']
    deltaRange = np.arange(10,61,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [200]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_sub_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### radar-none-incRADAR-H1
def gen_radar_jamming_fault_plant_H1(sceneNum):
    title = str(sceneNum)+'_radar-none-incRADAR-H1'
    faultLibFile = 'fault_library/radJamPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#radar_none:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = []

    for t1 in [2.0]:
      for dt in [30.0]:
        t2 = dt
        code.append(gen_none_code(trigger_code, trigger, t1, t2, ''))
        param.append(','.join(['radar jamming',str(t1),str(dt),'none']))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### radar-none-incRADAR-H2
def gen_radar_jamming_fault_plant_H2(sceneNum):
    title = str(sceneNum)+'_radar-none-incRADAR-H2'
    faultLibFile = 'fault_library/radJamPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#radar_none:HOOK#'
    trigger = 'radar_dRel'
    trigger_code = 'if not self.lead_relevancy and self.current_time()<=3:'
    code = []
    param = []
    variable = []

    for t1 in [50]:
      for dt in [200]:
        t2 = dt
        code.append(gen_none_code(trigger_code, trigger, t1, t2, ''))
        param.append(','.join(['radar jamming',str(t1),str(dt),'none']))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-add-incProcRad-H1
def gen_rel_dist_add_fault_radard(sceneNum):
    title = str(sceneNum)+'_d_rel-add-incProcRad-H1'
    faultLibFile = 'fault_library/dRelRadard'
    fileLoc = 'selfdrive/controls/radard.py'
    faultLoc = '#d_rel:HOOK#'
    #trigger = 'tracks[ids].dRel'
    trigger = 'pt.dRel'
    trigger_code = ''
    code = []
    param = []
    #variable = ['tracks[ids].dRel']
    variable = ['pt.dRel']
    deltaRange = np.arange(15,255,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### d_rel-sub-incProcRad-H2
def gen_rel_dist_sub_fault_radard(sceneNum):
    title = str(sceneNum)+'_d_rel-sub-incProcRad-H2'
    faultLibFile = 'fault_library/dRelRadard'
    fileLoc = 'selfdrive/controls/radard.py'
    faultLoc = '#d_rel:HOOK#'
    #trigger = 'tracks[ids].dRel'
    trigger = 'pt.dRel'
    trigger_code = 'if '+trigger+'>=200.0:'
    code = []
    param = []
    #variable = ['tracks[ids].dRel']
    variable = ['pt.dRel']
    deltaRange = np.arange(10,256,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [200]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          code.append(gen_sub_code(trigger_code,trigger, t1, t2, variable, [delta], '//if '+variable[0]+'<0:'+'//  '+variable[0]+'= 0'))
          param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### v_rel-add-incProcRad-H1
def gen_rel_vel_add_fault_radard(sceneNum):
    title = str(sceneNum)+'_v_rel-add-incProcRad-H1'
    faultLibFile = 'fault_library/vRelRadard'
    fileLoc = 'selfdrive/controls/radard.py'
    faultLoc = '#d_rel:HOOK#'
    trigger = 'pt.dRel'
    trigger_code = ''
    code = []
    param = []
    variable = ['pt.vRel']
    deltaRange = np.arange(10,61,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### v_rel-sub-incProcRad-H2
def gen_rel_vel_sub_fault_radard(sceneNum):
    title = str(sceneNum)+'_v_rel-sub-incProcRad-H2'
    faultLibFile = 'fault_library/vRelRadard'
    fileLoc = 'selfdrive/controls/radard.py'
    faultLoc = '#d_rel:HOOK#'
    trigger = 'pt.dRel'
    trigger_code = 'if '+trigger+'>=200.0:'
    code = []
    param = []
    variable = ['pt.vRel']
    deltaRange = np.arange(10,61,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [200]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_sub_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['relative speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### curr_sp-sub-incProcPlant-H1
def gen_curr_sp_sub_fault_plant(sceneNum):
    title = str(sceneNum)+'_curr_sp-sub-incProcPlant-H1'
    faultLibFile = 'fault_library/vCurrSpPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#speed:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = ['speed2send']
    deltaRange = np.arange(10,61,10)
    
    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d in deltaRange:
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_sub_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'<0:'+'//  '+variable[0]+'= 0'))
          param.append(','.join(['current speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### curr_sp-add-incProcPlant-H2
def gen_curr_sp_add_fault_plant(sceneNum):
    title = str(sceneNum)+'_curr_sp-add-incProcPlant-H2'
    faultLibFile = 'fault_library/vCurrSpPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#speed:HOOK#'
    trigger = 'radar_dRel'
    trigger_code = 'if not self.lead_relevancy and self.current_time()>2.0:'
    code = []
    param = []
    variable = ['speed2send']
    deltaRange = np.arange(10,61,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=85.0:'+'//  '+variable[0]+'= 85.0'))
          param.append(','.join(['current speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### md-rand-incProcPlant-H3
def gen_md_rand_val_plant(lane,sceneNum):
    title = str(sceneNum)+'_'+lane+'Lane-rand-incProcPlant-H3'
    faultLibFile = 'fault_library/mdPlant_'+lane
    fileLoc = 'selfdrive/test/plant/maneuver.py'
    faultLoc = '#md:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    if lane.lower()=='left':
      variable = ['self.lLane']
    elif lane.lower()=='right':
      variable = ['self.rLane']
    else:
      variable = ['self.lLane','self.rLane']
    deltaRange = np.arange(-2.5,2.5,0.5)

    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d1 in deltaRange:
          d2 = d1+1
          code.append(gen_uniform_rand_code(trigger_code, trigger, t1, t2, variable, d1, d2, ''))
          param.append(','.join(['path model',str(t1),str(dt),str(d1),str(d2)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### angSteer-add-incProcPlant-H3
def gen_angle_steer_add_plant(sceneNum):
    title = str(sceneNum)+'_angSteer-add-incProcPlant-H3'
    faultLibFile = 'fault_library/angSteerPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#angle_steer:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = ['angle_steer2send']
    deltaRange = np.arange(-45,46,10)

    for t1 in [0]:
      for dt in [2.0]:
        t2 = t1+dt
        for d in deltaRange:
          delta = random.randint(d,d+9)
          if d > 45:
            alpha = 45*3.1416/180.0
          else:
            alpha = delta*3.1416/180.0
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, ['('+str(alpha)+')'], ''))
          param.append(','.join(['steer angle',str(t1),str(dt),str(alpha)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### brake-stuck0-incProcCarcontroller-H1
def gen_brake_stuck0_Carcontroller(sceneNum):
    title = str(sceneNum)+'_brake-stuck0-incProcCarcontroller-H1'
    faultLibFile = 'fault_library/brakeStuckCC'
    fileLoc = 'selfdrive/car/honda/carcontroller.py'
    faultLoc = '#apply_brake:HOOK#'
    trigger = '(frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['apply_brake']
    deltaRange = [0]
    for d in deltaRange:
      for t1 in [7]:
        for dt in [23]:
          t2 = t1+dt
          code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, [d], ''))
          param.append(','.join(['apply_brake',str(t1),str(dt),str(d)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### gas-stuckV-incProcCarcontroller-H1
def gen_gas_stuckV_Carcontroller(sceneNum):
    title = str(sceneNum)+'_gas-stuckV-incProcCarcontroller-H1'
    faultLibFile = 'fault_library/gasStuckCC'
    fileLoc = 'selfdrive/car/honda/carcontroller.py'
    faultLoc = '#apply_gas:HOOK#'
    trigger = '(frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['apply_gas']
    deltaRange = np.arange(0,1004,100)
    for d in deltaRange:
      for t1 in [7]:
        for dt in [23]:
          t2 = t1+dt
          delta = random.randint(d,d+99)
          if delta > 1003:
            delta = 1003
          code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['apply_gas',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### brake-stuckV-incProcCarcontroller-H2
def gen_brake_stuckV_Carcontroller(sceneNum):
    title = str(sceneNum)+'_brake-stuckV-incProcCarcontroller-H2'
    faultLibFile = 'fault_library/gasStuckCC'
    fileLoc = 'selfdrive/car/honda/carcontroller.py'
    faultLoc = '#apply_brake:HOOK#'
    trigger = '(frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['apply_brake']
    deltaRange = np.arange(0,256,25)
    for d in deltaRange:
      for t1 in [3]:
        for dt in [27]:
          t2 = t1+dt
          delta = random.randint(d,d+24)
          if delta > 255:
            delta = 255
          code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['apply_brake',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### gas-stuck0-incProcCarcontroller-H2
def gen_gas_stuck0_Carcontroller(sceneNum):
    title = str(sceneNum)+'_gas-stuck0-incProcCarcontroller-H2'
    faultLibFile = 'fault_library/gasStuckCC'
    fileLoc = 'selfdrive/car/honda/carcontroller.py'
    faultLoc = '#apply_gas:HOOK#'
    trigger = '(frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['apply_gas']
    deltaRange = [0]
    for d in deltaRange:
      for t1 in [3]:
        for dt in [27]:
          t2 = t1+dt
          code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, [d], ''))
          param.append(','.join(['apply_gas',str(t1),str(dt),str(d)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### steer-stuckV-incProcCarcontroller-H3
def gen_steer_stuckV_Carcontroller(sceneNum):
    title = str(sceneNum)+'_steer-stuckV-incProcCarcontroller-H3'
    faultLibFile = 'fault_library/steerStuckCC'
    fileLoc = 'selfdrive/car/honda/carcontroller.py'
    faultLoc = '#apply_steer:HOOK#'
    trigger = '(frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['apply_steer']
    deltaRange = np.arange(0,13,1)
    for d in deltaRange:
      for t1 in [3]:
        for dt in [27]:
          for ang_dir in [-1,1]:
            t2 = t1+dt
            delta = ang_dir*(2**d)
            code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, ['('+str(delta)+')'], ''))
            param.append(','.join(['apply_steer',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### a_target-add-faultContProc-H1
def gen_a_target_add_fault_adaptCruise(sceneNum):
    title = str(sceneNum)+'_a_target-add-faultContProc-H1'
    faultLibFile = 'fault_library/aTargetAdaptCruise'
    fileLoc = 'selfdrive/controls/lib/adaptivecruise.py'
    faultLoc = '#a_target:HOOK#'
    trigger = 'l1.dRel'
    trigger_code = ''
    code = []
    param = []
    variable = ['a_target']
    deltaRange = np.arange(0,1.6,0.1)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = d
          if delta > 1.5:
            delta = 1.5
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//a_target = np.clip(a_target, a_lim[0], a_lim[1])'))
          param.append(','.join(['target acceleration',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### v_target-add-faultContProc-H1
def gen_v_target_add_fault_longControl(sceneNum):
    title = str(sceneNum)+'_v_target-add-faultContProc-H1'
    faultLibFile = 'fault_library/vTargetLongControl'
    fileLoc = 'selfdrive/controls/lib/longcontrol.py'
    faultLoc = '#v_target:HOOK#'
    trigger = ''
    trigger_code = 'if v_target<(v_cruise * CV.KPH_TO_MS):'
    code = []
    param = []
    variable = ['v_target']
    deltaRange = np.arange(10,61,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//v_target = min(v_target, v_cruise * CV.KPH_TO_MS)'))
          param.append(','.join(['target speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### output_gb-add-faultContProc-H1
def gen_output_gb_add_fault_longControl(sceneNum):
    title = str(sceneNum)+'_output_gb-add-faultContProc-H1'
    faultLibFile = 'fault_library/outputGbLongControl'
    fileLoc = 'selfdrive/controls/lib/longcontrol.py'
    faultLoc = '#output_gb:HOOK#'
    trigger = ''
    trigger_code = 'if v_target<(v_cruise * CV.KPH_TO_MS):'
    code = []
    param = []
    variable = ['output_gb']
    deltaRange = np.arange(0.2,2.2,0.2)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = d
          if delta > 2.0:
            delta = 2.0
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['final gas brake',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### a_target-sub-faultContProc-H2
def gen_a_target_sub_fault_adaptCruise(sceneNum):
    title = str(sceneNum)+'_a_target-sub-faultContProc-H2'
    faultLibFile = 'fault_library/aTargetAdaptCruise'
    fileLoc = 'selfdrive/controls/lib/adaptivecruise.py'
    faultLoc = '#a_targetH2:HOOK#'
    trigger = 'l1.dRel'
    trigger_code = 'if l1 is not None and l1.status is False:'
    code = []
    param = []
    variable = ['a_target']
    deltaRange = np.arange(0.2,3.2,0.2)
    for d in deltaRange:
      for t1 in [200]:
        for dt in [100]:
          t2 = t1+dt
          delta = d
          if delta > 3.0:
            delta = 3.0
          code.append(gen_sub_code(trigger_code, trigger, t1, t2, variable, [delta], '//a_target = np.clip(a_target, a_lim[0], a_lim[1])'))
          param.append(','.join(['target acceleration',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### v_target-sub-faultContProc-H2
def gen_v_target_sub_fault_longControl(sceneNum):
    title = str(sceneNum)+'_v_target-sub-faultContProc-H2'
    faultLibFile = 'fault_library/vTargetLongControl'
    fileLoc = 'selfdrive/controls/lib/longcontrol.py'
    faultLoc = '#v_target:HOOK#'
    trigger = ''
    trigger_code = 'if v_target>=(v_cruise * CV.KPH_TO_MS):'
    code = []
    param = []
    variable = ['v_target']
    deltaRange = np.arange(10,61,10)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 60:
            delta = 60
          delta = delta*0.44704    # 1MPH = 0.44704 m/s
          code.append(gen_sub_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'<0:'+'//  '+variable[0]+'= 0'))
          param.append(','.join(['target speed',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### output_gb-sub-faultContProc-H2
def gen_output_gb_sub_fault_longControl(sceneNum):
    title = str(sceneNum)+'_output_gb-sub-faultContProc-H2'
    faultLibFile = 'fault_library/outputGbLongControl'
    fileLoc = 'selfdrive/controls/lib/longcontrol.py'
    faultLoc = '#output_gb:HOOK#'
    trigger = ''
    trigger_code = 'if v_target>=(v_cruise * CV.KPH_TO_MS):'
    code = []
    param = []
    variable = ['output_gb']
    deltaRange = np.arange(0.2,2.2,0.2)
    for d in deltaRange:
      for t1 in [0]:
        for dt in [50]:
          t2 = t1+dt
          delta = d
          if delta > 2.0:
            delta = 2.0
          code.append(gen_sub_code(trigger_code, trigger, t1, t2, variable, [delta], ''))
          param.append(','.join(['final gas brake',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### plrd_poly-rand-faultContProcPP-H3
def gen_plrd_poly_rand_val_pathPlanner(lane,sceneNum):
    title = str(sceneNum)+'_'+lane+'Poly-rand-faultContProcPP-H3'
    faultLibFile = 'fault_library/plrdPolyPathPlanner_'+lane
    fileLoc = 'selfdrive/controls/lib/pathplanner.py'
    if lane.lower()=='d_path':
      faultLoc = '#d_poly:HOOK#'
    else:
      faultLoc = '#plr_poly:HOOK#'
    trigger = '(md.model.frameId/100)'
    trigger_code = ''
    code = []
    param = []
    if lane.lower()=='left':
      variable = ['l_poly[3]']
    elif lane.lower()=='right':
      variable = ['r_poly[3]']
    elif lane.lower()=='p_path':
      variable = ['p_poly[3]']
    else:
      variable = ['self.d_poly[3]']
    deltaRange = np.arange(-5,5,1)

    for d1 in deltaRange:
      for t1 in [3]:
        for dt in [27]:
          t2 = t1+dt
          d2 = d1+1
          code.append(gen_uniform_rand_code(trigger_code, trigger, t1, t2, variable, d1, d2, ''))
          param.append(','.join(['path poly',str(t1),str(dt),str(d1),str(d2)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### angSteerDes-add-faultContProcLaC-H3
def gen_angle_steer_des_add_LaC(sceneNum):
    title = str(sceneNum)+'_angSteerDes-add-faultContProcLaC-H3'
    faultLibFile = 'fault_library/angSteerDesLaC'
    fileLoc = 'selfdrive/controls/lib/latcontrol.py'
    faultLoc = '#angle_steers_des:HOOK#'
    trigger = '(PL.PP.frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['self.angle_steers_des']
    deltaRange = np.arange(-45,55,10)
    for d in deltaRange:
      for t1 in [3]:
        for dt in [27]:
          t2 = t1+dt
          delta = random.randint(d,d+9)
          if delta > 45:
            delta = 45
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, ['('+str(delta)+')'], ''))
          param.append(','.join(['steer angle des',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)


### output_steer-add-faultContProcLaC-H3
def gen_output_steer_add_LaC(sceneNum):
    title = str(sceneNum)+'_output_steer-add-faultContProcLaC-H3'
    faultLibFile = 'fault_library/outSteerLaC'
    fileLoc = 'selfdrive/controls/lib/latcontrol.py'
    faultLoc = '#output_steer:HOOK#'
    trigger = '(PL.PP.frame/100)'
    trigger_code = ''
    code = []
    param = []
    variable = ['output_steer']
    deltaRange = np.arange(-1.0667,1.2667,0.2)
    for d in deltaRange:
      for t1 in [3]:
        for dt in [27]:
          t2 = t1+dt
          delta = d
          if delta > 1.0667:
            delta = 1.0667
          code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, ['('+str(delta)+')'], ''))
          param.append(','.join(['output steer',str(t1),str(dt),str(delta)]))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### vision-none-miscommVisPlant-H3
def gen_vision_miscomm_fault_plant(sceneNum):
    title = str(sceneNum)+'_vision-none-miscommVisPlant-H3'
    faultLibFile = 'fault_library/visMiscommPlant'
    fileLoc = 'selfdrive/test/plant/plant.py'
    faultLoc = '#md_none:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    variable = []

    for t1 in [2.0]:
      for dt in [30.0]:
        t2 = t1+dt
        code.append(gen_none_code(trigger_code, trigger, t1, t2, ''))
        param.append(','.join(['vision miscomm',str(t1),str(dt),'none']))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

### vision-effect-noisyInputManeuver-H3
def gen_vision_noisyInput_fault_Maneuver(effect, sceneNum):
    title = str(sceneNum)+'_vision-effect-noisyInputManeuver-H3'
    faultLibFile = ''
    fileLoc = 'selfdrive/test/plant/maneuver.py'
    faultLoc = '#visionFault:HOOK#'
    trigger = 'self.frameIdx'
    trigger_code = ''
    code = []
    param = []
    #variable = ['left_line','right_line']
    #deltaRange = ['lanes[0]','lanes[1]']
    variable = ['self.effect', 'self.thickness']

    if effect <7:
      range_th = range(1,11)
    elif effect == 7:
      range_th = range(3,7)
    elif effect == 8:
      range_th = [3,5,7]
    elif effect == 9:
      range_th = [3,5]

    for t1 in [500.0]:
      for dt in [2500.0]:
        for th in range_th:
          t2 = t1+dt
          code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, [str(effect), str(th)], ''))
          param.append(','.join(['vision noisyInput',str(t1),str(dt),'none']))

    write_to_file(faultLibFile, code, param, title, fileLoc, faultLoc)

'''
def gen_vision_noisyInput_fault_Maneuver(effect, sceneNum):
    title = str(sceneNum)+'_vision-effect-noisyInputManeuver-H3'
    faultLibFile = effect.lower()
    fileLoc = 'selfdrive/test/plant/maneuver.py'
    faultLoc = '#visionFault:HOOK#'
    trigger = 'self.headway_time'
    trigger_code = ''
    code = []
    param = []
    #variable = ['left_line','right_line']
    #deltaRange = ['lanes[0]','lanes[1]']
    variable = ['lanes']
    deltaRange = ['lanesFl[l_ind]']


    for t1 in [0]:
      for dt in [30.0]:
        t2 = t1+dt
        code.append(gen_stuck_code(trigger_code, trigger, t1, t2, variable, deltaRange, ''))
        param.append(','.join(['vision noisyInput',str(t1),str(dt),'none']))

    write_to_vision_file(faultLibFile, code, param, title, fileLoc, faultLoc)
'''


###_main_###

with open('run_fault_inject_campaign.sh', 'w') as runFile:
    runFile.write('#Usage: python run.py target_fault_library\n')

scenarios = {
## Incorrect RADAR input
1 : gen_rel_dist_add_fault_plant,
2 : gen_rel_vel_add_fault_plant,
3 : gen_rel_dist_sub_fault_plant,
4 : gen_rel_vel_sub_fault_plant,
5 : gen_radar_jamming_fault_plant_H1,
6 : gen_radar_jamming_fault_plant_H2,
## Incorrect Process Model
7 : gen_rel_dist_add_fault_radard,
8 : gen_rel_vel_add_fault_radard,
9 : gen_curr_sp_sub_fault_plant,
10 : gen_rel_dist_sub_fault_radard,
11 : gen_rel_vel_sub_fault_radard,
12 : gen_curr_sp_add_fault_plant,
13 : gen_md_rand_val_plant,
14 : gen_md_rand_val_plant,
15 : gen_md_rand_val_plant,
16 : gen_angle_steer_add_plant,
17 : gen_brake_stuck0_Carcontroller,
18 : gen_gas_stuckV_Carcontroller,
19 : gen_brake_stuckV_Carcontroller,
20 : gen_gas_stuck0_Carcontroller,
21 : gen_steer_stuckV_Carcontroller,
## Faulty Control Algorithm
22 : gen_a_target_add_fault_adaptCruise,
23 : gen_v_target_add_fault_longControl,
24 : gen_output_gb_add_fault_longControl,
25 : gen_a_target_sub_fault_adaptCruise,
26 : gen_v_target_sub_fault_longControl,
27 : gen_output_gb_sub_fault_longControl,
28 : gen_plrd_poly_rand_val_pathPlanner,
29 : gen_plrd_poly_rand_val_pathPlanner,
30 : gen_plrd_poly_rand_val_pathPlanner,
31 : gen_plrd_poly_rand_val_pathPlanner,
32 : gen_angle_steer_des_add_LaC,
33 : gen_output_steer_add_LaC,
34 : gen_vision_miscomm_fault_plant,
35 : gen_vision_noisyInput_fault_Maneuver,
36 : gen_vision_noisyInput_fault_Maneuver,
37 : gen_vision_noisyInput_fault_Maneuver,
38 : gen_vision_noisyInput_fault_Maneuver,
39 : gen_vision_dRel_add_fault_plant,
40 : gen_vision_dRel_sub_fault_plant,
41 : gen_RadVis_dRel_add_fault_plant,
42 : gen_RadVis_dRel_sub_fault_plant,
43 : gen_vision_noisyInput_fault_Maneuver,
44 : gen_vision_noisyInput_fault_Maneuver,
45 : gen_vision_noisyInput_fault_Maneuver,
46 : gen_vision_noisyInput_fault_Maneuver,
47 : gen_vision_noisyInput_fault_Maneuver
}

lanes = ['left','right','both']  # 'left','right','both'
poly = ['p_path','left','right','d_path']  # 'p_path','left','right','d_path'
#effects = ['rain', 'fog', 'snow', 'occlusion']
effects = [1,2,3,4,5,6,7,8,9]

#for sceneNum in range(35,39):
#for sceneNum in [13,14,15,16,21,28,29,30,31,32,33,34]:
#for sceneNum in [1,2,5,9,13,14,15,16,34,35,36,37,38,39,40,41,42]: # for testing HWT trigger (H1 and H3)
#for sceneNum in [3,4,6,12]: # for testing HWT trigger (H2)
#for sceneNum in [1,2,3,4,5,6,9,12,13,14,15,16,34,35,36,37,38,39,40,41,42,43,44,45,46,47]: # for testing the faults in inputs
for sceneNum in [35,36,37,38,43,44,45,46,47]:
  print sceneNum
  if sceneNum >= 13 and sceneNum <=15:
    scenarios[sceneNum](lanes[sceneNum-13],sceneNum)
  elif sceneNum >= 28 and sceneNum <=31:
    scenarios[sceneNum](poly[sceneNum-28],sceneNum)
  elif sceneNum >= 35 and sceneNum <=38:
    scenarios[sceneNum](effects[sceneNum-35],sceneNum)
  elif sceneNum >= 43 and sceneNum <=47:
    scenarios[sceneNum](effects[sceneNum+4-43],sceneNum)
  else:
    scenarios[sceneNum](sceneNum)








