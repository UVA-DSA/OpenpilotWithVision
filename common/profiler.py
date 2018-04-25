import time

class Profiler(object):
  def __init__(self, enabled=False):
    self.enabled = enabled
    self.cp = {}
    self.cp_ignored = []
    self.iter = 0
    self.start_time = time.clock()
    self.last_time = self.start_time
    self.tot = 0.

  def reset(self, enabled=False):
    self.enabled = enabled
    self.cp = {}
    self.cp_ignored = []
    self.iter = 0
    self.start_time = time.clock()
    self.last_time = self.start_time

  def checkpoint(self, name, ignore=False):
    # ignore flag needed when benchmarking threads with ratekeeper
    if not self.enabled:
      return
    tt = time.clock()
    if name not in self.cp:
      self.cp[name] = 0.
      if ignore:
        self.cp_ignored.append(name)
    self.cp[name] += tt - self.last_time
    if not ignore:
      self.tot += tt - self.last_time
    self.last_time = tt

  def display(self):
    if not self.enabled:
      return
    self.iter += 1
    print "******* Profiling *******"
    for n in self.cp:
      ms = self.cp[n]
      if n in self.cp_ignored:
        print "%30s: %7.2f   perc: %1.0f" % (n, ms*1000.0, ms/self.tot*100), "  IGNORED"
      else:
        print "%30s: %7.2f   perc: %1.0f" % (n, ms*1000.0, ms/self.tot*100)
    print "Iter clock: %2.6f   TOTAL: %2.2f" % (self.tot/self.iter, self.tot)
