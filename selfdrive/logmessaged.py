#!/usr/bin/env python
import zmq
from logentries import LogentriesHandler
from selfdrive.services import service_list
import selfdrive.messaging as messaging

def main(gctx):
  # setup logentries. we forward log messages to it
  le_token = "e8549616-0798-4d7e-a2ca-2513ae81fa17"
  le_handler = LogentriesHandler(le_token, use_tls=False, verbose=False)

  le_level = 20 #logging.INFO

  ctx = zmq.Context()
  sock = ctx.socket(zmq.PULL)
  sock.bind("ipc:///tmp/logmessage")

  # and we publish them
  pub_sock = messaging.pub_sock(ctx, service_list['logMessage'].port)

  while True:
    dat = ''.join(sock.recv_multipart())

    # print "RECV", repr(dat)

    levelnum = ord(dat[0])
    dat = dat[1:]

    if levelnum >= le_level:
      # push to logentries
      le_handler.emit_raw(dat)

    # then we publish them
    msg = messaging.new_message()
    msg.logMessage = dat
    pub_sock.send(msg.to_bytes())

if __name__ == "__main__":
  main(None)
