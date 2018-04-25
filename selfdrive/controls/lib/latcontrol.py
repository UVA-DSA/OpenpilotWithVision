import math
import numpy as np

from selfdrive.controls.lib.pid import PIController
from selfdrive.controls.lib.lateral_mpc import libmpc_py
from common.numpy_fast import interp
from common.realtime import sec_since_boot
from selfdrive.swaglog import cloudlog

# 100ms is a rule of thumb estimation of lag from image processing to actuator command
ACTUATORS_DELAY = 0.1

_DT = 0.01    # 100Hz
_DT_MPC = 0.05  # 20Hz


def calc_states_after_delay(states, v_ego, steer_angle, curvature_factor, steer_ratio):
  states[0].x = v_ego * ACTUATORS_DELAY
  states[0].psi = v_ego * curvature_factor * math.radians(steer_angle) / steer_ratio * ACTUATORS_DELAY
  return states


def get_steer_max(CP, v_ego):
  return interp(v_ego, CP.steerMaxBP, CP.steerMaxV)


class LatControl(object):
  def __init__(self, VM):
    self.pid = PIController(VM.CP.steerKp, VM.CP.steerKi, k_f=VM.CP.steerKf, pos_limit=1.0)
    self.last_cloudlog_t = 0.0
    self.setup_mpc(VM.CP.steerRateCost)

  def setup_mpc(self, steer_rate_cost):
    self.libmpc = libmpc_py.libmpc
    self.libmpc.init(steer_rate_cost)

    self.mpc_solution = libmpc_py.ffi.new("log_t *")
    self.cur_state = libmpc_py.ffi.new("state_t *")
    self.mpc_updated = False
    self.cur_state[0].x = 0.0
    self.cur_state[0].y = 0.0
    self.cur_state[0].psi = 0.0
    self.cur_state[0].delta = 0.0

    self.last_mpc_ts = 0.0
    self.angle_steers_des = 0.0
    self.angle_steers_des_mpc = 0.0
    self.angle_steers_des_prev = 0.0
    self.angle_steers_des_time = 0.0

  def reset(self):
    self.pid.reset()

  def update(self, active, v_ego, angle_steers, steer_override, d_poly, angle_offset, VM, PL):
    cur_time = sec_since_boot()
    self.mpc_updated = False
    if self.last_mpc_ts < PL.last_md_ts:
      self.last_mpc_ts = PL.last_md_ts
      self.angle_steers_des_prev = self.angle_steers_des_mpc

      curvature_factor = VM.curvature_factor(v_ego)

      l_poly = libmpc_py.ffi.new("double[4]", list(PL.PP.l_poly))
      r_poly = libmpc_py.ffi.new("double[4]", list(PL.PP.r_poly))
      p_poly = libmpc_py.ffi.new("double[4]", list(PL.PP.p_poly))

      # account for actuation delay
      self.cur_state = calc_states_after_delay(self.cur_state, v_ego, angle_steers, curvature_factor, VM.CP.steerRatio)

      v_ego_mpc = max(v_ego, 5.0)  # avoid mpc roughness due to low speed
      self.libmpc.run_mpc(self.cur_state, self.mpc_solution,
                          l_poly, r_poly, p_poly,
                          PL.PP.l_prob, PL.PP.r_prob, PL.PP.p_prob, curvature_factor, v_ego_mpc, PL.PP.lane_width)

      delta_desired = self.mpc_solution[0].delta[1]
      self.cur_state[0].delta = delta_desired

      self.angle_steers_des_mpc = float(math.degrees(delta_desired * VM.CP.steerRatio) + angle_offset)
      self.angle_steers_des_time = cur_time
      self.mpc_updated = True

      #  Check for infeasable MPC solution
      nans = np.any(np.isnan(list(self.mpc_solution[0].delta)))
      t = sec_since_boot()
      if nans:
        self.libmpc.init(VM.CP.steerRateCost)
        self.cur_state[0].delta = math.radians(angle_steers) / VM.CP.steerRatio

        if t > self.last_cloudlog_t + 5.0:
          self.last_cloudlog_t = t
          cloudlog.warning("Lateral mpc - nan: True")

    if v_ego < 0.3 or not active:
      output_steer = 0.0
      self.pid.reset()
    else:
      # TODO: ideally we should interp, but for tuning reasons we keep the mpc solution
      # constant for 0.05s.
      #dt = min(cur_time - self.angle_steers_des_time, _DT_MPC + _DT) + _DT  # no greater than dt mpc + dt, to prevent too high extraps
      #self.angle_steers_des = self.angle_steers_des_prev + (dt / _DT_MPC) * (self.angle_steers_des_mpc - self.angle_steers_des_prev)
      self.angle_steers_des = self.angle_steers_des_mpc
      steers_max = get_steer_max(VM.CP, v_ego)
      self.pid.pos_limit = steers_max
      self.pid.neg_limit = -steers_max
      steer_feedforward = self.angle_steers_des * v_ego**2  # proportional to realigning tire momentum (~ lateral accel)
      output_steer = self.pid.update(self.angle_steers_des, angle_steers, check_saturation=(v_ego > 10), override=steer_override, feedforward=steer_feedforward)

    self.sat_flag = self.pid.saturated
    return output_steer
