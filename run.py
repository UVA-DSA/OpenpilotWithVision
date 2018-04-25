import os
import os.path
import numpy as np
import time
from sys import argv


def insert_fault_code(fileLoc, faultLoc, codeline):
    brk = 0
    bkupFile = fileLoc+'.bkup'
    if os.path.isfile(bkupFile) != True:
      cmd = 'cp ' + fileLoc + ' ' + bkupFile
      os.system(cmd)
    else:
      print 'Bkup file already exists!!'

    src_fp = open(fileLoc, 'w')
    bkup_fp = open(bkupFile, 'r')

    for line in bkup_fp:
      src_fp.write(line)
      if brk>0:
        for i in range(1, leadSp+1):
          src_fp.write(' ')
        src_fp.write('else:'+'\n')
        for l in np.arange(brk,len(codeline)):
            for i in range(1, leadSp+3):
              src_fp.write(' ')
            src_fp.write(codeline[l]+'\n')

      brk = 0

      if faultLoc in line:
        leadSp = len(line) - len(line.lstrip(' ')) # calculate the leading spaces

        for i in range(1, leadSp+1):
          src_fp.write(' ')
        src_fp.write(codeline[0]+'\n')

        for l in np.arange(1,len(codeline)):
          if codeline[l] != 'none\n':
            for i in range(1, leadSp+3):
              src_fp.write(' ')
            src_fp.write(codeline[l]+'\n')
          else:
            brk=l+1
            for i in range(1,3):
              src_fp.write(' ')
            break

    src_fp.close()
    bkup_fp.close()

def handleH2LdRel(tag, codeline):
  fileLoc = 'selfdrive/test/tests/plant/test_longitudinal.py'
  faultLoc = '#lead_relevancy:HOOK#'
  bkupFile = fileLoc + '.bkup'

  if tag == 'start':
    if os.path.isfile(bkupFile) != True:
      cmd = 'cp ' + fileLoc + ' ' + bkupFile
      os.system(cmd)
    else:
      print 'Bkup file already exists!!'
    src_fp = open(fileLoc, 'w')
    bkup_fp = open(bkupFile, 'r')

    for line in bkup_fp:
      src_fp.write(line)

      if faultLoc in line:
        leadSp = len(line) - len(line.lstrip(' ')) # calculate the leading spaces

        for i in range(1, leadSp+1):
          src_fp.write(' ')
        src_fp.write(codeline+'\n')

    src_fp.close()
    bkup_fp.close()

  else:
    cmd = 'cp ' + bkupFile + ' ' + fileLoc
    os.system(cmd)
    cmd = 'rm ' + bkupFile
    os.system(cmd)


def inject_fault(fileName):
    in_file = fileName+'.txt'
    outfile_path = 'selfdrive/test/tests/plant/out/longitudinal/'
    sceneLine  = fileName.split('_')
    sceneNum = sceneLine[len(sceneLine)-1]

    recFaultTime="//fltTime=open(\'out/longitudinal/fault_times.txt\',\'a+\')//fltTime.write(str(sec_since_boot())+\'||\')//fltTime.close()"

    with open(in_file, 'r') as fp:
        print in_file
        line = fp.readline() # title line
        tLine = line.split('-')
        hz = tLine[len(tLine)-1].replace('\n','')
        title_num = line.split(':')
        scene_num = title_num[1].split('_')

        if hz=='H2':
          handleH2LdRel('start','lead_relevancy=False,  testvision = 0,')
        else:
          if int(scene_num[0]) >= 35 and int(scene_num[0])<= 38:
            handleH2LdRel('start','lead_relevancy=True,  testvision = 1,')
          elif int(scene_num[0]) >= 43 and int(scene_num[0])<= 47:
            handleH2LdRel('start','lead_relevancy=True,  testvision = 1,')
          else:
            handleH2LdRel('start','lead_relevancy=True,  testvision = 0,')

        title = line.split(':')
        title[1] = title[1].replace('\n','')

        if os.path.isdir('../output_files/'+title[1]) != True:
          os.makedirs('../output_files/'+title[1])

        hazardFile = open('../output_files/'+title[1]+'/Hazards.txt','w')
        alertFile = open('../output_files/'+title[1]+'/Alerts.txt','w')
        summFile = open('../output_files/'+title[1]+'/summary.csv','w')

        summLine = 'Scenario#,Fault#,Fault-line,Alerts,Hazards,T1,T2,T3\n'
        summFile.write(summLine)

        hazardFile.close()
        alertFile.close()
        summFile.close()

        hazardFile = open('../output_files/'+title[1]+'/Hazards.txt','a+')
        alertFile = open('../output_files/'+title[1]+'/Alerts.txt','a+')
        summFile = open('../output_files/'+title[1]+'/summary.csv','a')

        line = fp.readline() # fault location line
        lineSeg = line.split('//')
        fileLoc = lineSeg[1]
        faultLoc = lineSeg[2]

        for line in fp:
          line = line + recFaultTime
          lineSeg = line.split('//')
          startWord = lineSeg[0].split(' ')
          del lineSeg[0]

          if startWord[0]=='fault':
            print "+++++++++++"+title[1]+"++++++++++++++"
            insert_fault_code(fileLoc, faultLoc, lineSeg)
            #os.system('./run_standalone.sh') # run the openpilot simulator
            #os.system('./run_docker_tests.sh') # run the openpilot simulator

            output_dir = '../output_files/'+title[1]+'/'+startWord[1]
            if os.path.isdir(output_dir) != True:
              os.makedirs(output_dir)

            '''Copy all output files in a common directory'''
            #cmd = 'cp -a ' + outfile_path+'/.' + ' ' + output_dir
            #os.system(cmd)


            '''Write all alerts in single file '''
            alertMsg = 'N/A'
            alertTime = 'N/A'
            startTime = 0.0
            with open(output_dir+'/alerts.txt') as alFile:
              alLine = alFile.readline()  # first line
              alertFile.write('\nAlerts for fault '+startWord[1]+'::\n')
              for alLine in alFile:
                alertFile.write(alLine)
                if alLine.find('Enable/') >= 0:
                  strTime = alLine.split('=')
                  startTime = float(strTime[len(strTime)-1])
                elif startTime>0.0:
                  strTime = alLine.split('=')
                  strAlert = alLine.split('||')
                  if float(strTime[len(strTime)-1])-startTime < (28.0*10.) and alertMsg.find(strAlert[1])<0:
                    if alertMsg == 'N/A':
                      alertMsg = strAlert[1]
                      alertTime = str(float(strTime[len(strTime)-1])-startTime)
                    else:
                      alertMsg = alertMsg +'||'+ strAlert[1]
                      alertTime = alertTime+'||'+ str(float(strTime[len(strTime)-1])-startTime)
            if startTime==0.0:
              alertMsg = 'Comma unavailable'
              alertTime = str(startTime)


            '''Write all hazards in single file '''
            hazardMsg = 'N/A'
            hazardTime = 'N/A'
            with open(output_dir+'/hazards.txt') as hzFile:
              hazLine = hzFile.readline()  # first line
              hazardFile.write('\nHazards for fault '+startWord[1]+'::\n')
              for hazLine in hzFile:
                hazardFile.write(hazLine)
                hzTime = hazLine.split('=')
                hzTime = hzTime[len(hzTime)-1]
                hzTime = hzTime.replace('\n','')
                hzMsg = hazLine.split('||')
                if hazardMsg=='N/A':
                  hazardMsg = hzMsg[1]
                  hazardTime = str(float(hzTime) - startTime)
                else:
                  hazardMsg = hazardMsg +'||'+ hzMsg[1]
                  hazardTime = hazardTime +'||'+  str(float(hzTime) - startTime)


            faultTime = 'N/A'
            with open(output_dir+'/fault_times.txt') as fltFile:
              fltLine = fltFile.readline()  # first line
              fltTime = fltLine.split('||')
              tm = float(fltTime[0]) - startTime
              if tm < 0:
                faultTime = '0'
              else:
                faultTime = str(tm)


            # delete the recFaultTime codes, don't want to store it in summary.csv
            del lineSeg[len(lineSeg)-1]
            del lineSeg[len(lineSeg)-1]
            del lineSeg[len(lineSeg)-1]

            faultLine = '||'.join(lineSeg)
            faultLine = faultLine.replace('\n','')
            summLine = '%d,%d,"%s",%s,%s,%s,%s,%s\n' %(int(sceneNum),int(startWord[1]),faultLine,alertMsg,hazardMsg,faultTime,alertTime,hazardTime)
            summFile.write(summLine)

            #break

        hazardFile.close()
        alertFile.close()
        summFile.close()
        
        print 'Fault injection and execution done !!!'
        bkupFile = fileLoc+'.bkup'
        refFile = fileLoc+'.reference'       
        cmd = 'cp ' + fileLoc + ' ' + refFile
        os.system(cmd)
        cmd = 'cp ' + bkupFile + ' ' + fileLoc
        os.system(cmd)
        cmd = 'rm ' + bkupFile
        os.system(cmd)
        handleH2LdRel('stop','')
        print 'Original file restored'
    cmd = 'cp '+in_file + ' ' +'../output_files/'+title[1]
    os.system(cmd)

start = time.time()

if len(argv)>1:
  inject_fault(argv[1])
else:
  print 'Fault library filename is missing, pass the filename as argument'

print '\n\n Total runtime: %f seconds' % (time.time()-start)

