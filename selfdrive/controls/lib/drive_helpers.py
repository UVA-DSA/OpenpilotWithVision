from common.numpy_fast import clip
from cereal import car


class EventTypes:
  ENABLE = 'enable'
  PRE_ENABLE = 'preEnable'
  NO_ENTRY = 'noEntry'
  WARNING = 'warning'
  USER_DISABLE = 'userDisable'
  SOFT_DISABLE = 'softDisable'
  IMMEDIATE_DISABLE = 'immediateDisable'
  PERMANENT = 'permanent'


def create_event(name, types):
  event = car.CarEvent.new_message()
  event.name = name
  for t in types:
    setattr(event, t, True)
  return event


def get_events(events, types):
  out = []
  for e in events:
    for t in types:
      if getattr(e, t):
        out.append(e.name)
  return out


def rate_limit(new_value, last_value, dw_step, up_step):
  return clip(new_value, last_value + dw_step, last_value + up_step)


def learn_angle_offset(lateral_control, v_ego, angle_offset, c_poly, c_prob, angle_steers, steer_override):
  # simple integral controller that learns how much steering offset to put to have the car going straight
  # while being in the middle of the lane
  min_offset = -5.  # deg
  max_offset =  5.  # deg
  alpha = 1./36000. # correct by 1 deg in 2 mins, at 30m/s, with 50cm of error, at 20Hz
  min_learn_speed = 1.

  # learn less at low speed or when turning
  slow_factor = 1. / (1. + 0.02 * abs(angle_steers) * v_ego)
  alpha_v = alpha * c_prob * (max(v_ego - min_learn_speed, 0.)) * slow_factor

  # only learn if lateral control is active and if driver is not overriding:
  if lateral_control and not steer_override:
    angle_offset += c_poly[3] * alpha_v
    angle_offset = clip(angle_offset, min_offset, max_offset)

  return angle_offset
