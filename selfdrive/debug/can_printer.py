#!/usr/bin/env python
import os
import sys
from collections import defaultdict
from common.realtime import sec_since_boot
import zmq
import selfdrive.messaging as messaging
from selfdrive.services import service_list


def can_printer(bus=0, max_msg=0x10000, addr="127.0.0.1"):
  context = zmq.Context()
  logcan = messaging.sub_sock(context, service_list['can'].port, addr=addr)

  start = sec_since_boot()
  lp = sec_since_boot()
  msgs = defaultdict(list)
  canbus = int(os.getenv("CAN", bus))
  while 1:
    can_recv = messaging.drain_sock(logcan, wait_for_one=True)
    for x in can_recv:
      for y in x.can:
        if y.src == canbus:
          msgs[y.address].append(y.dat)

    if sec_since_boot() - lp > 0.1:
      dd = chr(27) + "[2J"
      dd += "%5.2f\n" % (sec_since_boot() - start)
      for k,v in sorted(zip(msgs.keys(), map(lambda x: x[-1].encode("hex"), msgs.values()))):
        if k < max_msg:
          dd += "%s(%6d) %s\n" % ("%04X(%4d)" % (k,k),len(msgs[k]), v)
      print dd
      lp = sec_since_boot()

if __name__ == "__main__":
  if len(sys.argv) > 3:
    can_printer(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
  elif len(sys.argv) > 2:
    can_printer(int(sys.argv[1]), int(sys.argv[2]))
  elif len(sys.argv) > 1:
    can_printer(int(sys.argv[1]))
  else:
    can_printer()
  
