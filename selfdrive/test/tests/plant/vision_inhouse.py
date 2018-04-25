
import matlab.engine



def update_laneData(lLane, rLane):
    with open('laneData.dat', 'w') as writefile:
      writefile.write(str(lLane)+','+str(rLane))
    with open('latMov.txt','w') as writeLatMov:
      writeLatMov.write(str(0)+','+str(0)+','+str(0.0))

def vision_thread(gctx, laneDetectorEng, rate=100):
  ind = 1
  effect = ''
  thickness = 0
  lat_mov = 0
  while 1:
    lLane,rLane = laneDetectorEng.detectLaneMarker(nargout=2)
    #update_laneData(lLane, rLane)
    with open('latMov.txt','r') as latMovfile:
      latL = latMovfile.read()
      latL = latL.split(',')
      effect = latL[0]
      thickness = float(latL[1])
      lat_mov = float(latL[2])
      '''
      print '=============================='
      print effect
      print thickness
      print lat_mov
      '''
    ind+=1
 

def main(gctx=None):
  update_laneData(-1.85, 1.85)
  laneDetectorEng = matlab.engine.start_matlab()
  vision_thread(gctx, laneDetectorEng, 10)

if __name__ == "__main__":
  main()
