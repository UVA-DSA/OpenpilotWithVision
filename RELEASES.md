Version 0.4.2 (2018-02-05)
==========================
 * Add alpha support for 2017 Lexus RX Hybrid
 * Add alpha support for 2018 ACURA RDX
 * Updated fingerprint to include Toyota Rav4 SE and Prius Prime
 * Bugfixes for Acura ILX and Honda Odyssey

Version 0.4.1 (2018-01-30)
==========================
 * Add alpha support for 2017 Toyota Corolla
 * Add alpha support for 2018 Honda Odyssey with Honda Sensing
 * Add alpha support for Grey Panda
 * Refactored car abstraction layer to make car ports easier
 * Increased steering torque limit on Honda CR-V by 30%

Version 0.4.0.2 (2018-01-18)
==========================
 * Add focus adjustment slider
 * Minor bugfixes

Version 0.4.0.1 (2017-12-21)
==========================
 * New UI to match chffrplus
 * Improved lateral control tuning to fix oscillations on Civic
 * Add alpha support for 2017 Toyota Rav4 Hybrid
 * Reduced CPU usage
 * Removed unnecessary utilization of fan at max speed
 * Minor bug fixes

Version 0.3.9 (2017-11-21)
==========================
 * Add alpha support for 2017 Toyota Prius
 * Improved longitudinal control using model predictive control
 * Enable Forward Collision Warning
 * Acura ILX now maintains openpilot engaged at standstill when brakes are applied

Version 0.3.8.2 (2017-10-30)
==========================
 * Add alpha support for 2017 Toyota RAV4
 * Smoother lateral control
 * Stay silent if stock system is connected through giraffe
 * Minor bug fixes

Version 0.3.7 (2017-09-30)
==========================
 * Improved lateral control using model predictive control
 * Improved lane centering
 * Improved GPS
 * Reduced tendency of path deviation near right side exits
 * Enable engagement while the accelerator pedal is pressed
 * Enable engagement while the brake pedal is pressed, when stationary and with lead vehicle within 5m
 * Disable engagement when park brake or brake hold are active
 * Fixed sporadic longitudinal pulsing in Civic
 * Cleanups to vehicle interface

Version 0.3.6.1 (2017-08-15)
============================
 * Mitigate low speed steering oscillations on some vehicles
 * Include board steering check for CR-V

Version 0.3.6 (2017-08-08)
==========================
 * Fix alpha CR-V support
 * Improved GPS
 * Fix display of target speed not always matching HUD
 * Increased acceleration after stop
 * Mitigated some vehicles driving too close to the right line

Version 0.3.5 (2017-07-30)
==========================
 * Fix bug where new devices would not begin calibration
 * Minor robustness improvements

Version 0.3.4 (2017-07-28)
==========================
 * Improved model trained on more data
 * Much improved controls tuning
 * Performance improvements
 * Bugfixes and improvements to calibration
 * Driving log can play back video
 * Acura only: system now stays engaged below 25mph as long as brakes are applied

Version 0.3.3  (2017-06-28)
===========================
  * Improved model trained on more data
  * Alpha CR-V support thanks to energee and johnnwvs!
  * Using the opendbc project for DBC files
  * Minor performance improvements
  * UI update thanks to pjlao307
  * Power off button
  * 6% more torque on the Civic

Version 0.3.2  (2017-05-22)
===========================
  * Minor stability bugfixes
  * Added metrics and rear view mirror disable to settings
  * Update model with more crowdsourced data

Version 0.3.1  (2017-05-17)
===========================
  * visiond stability bugfix
  * Add logging for angle and flashing

Version 0.3.0  (2017-05-12)
===========================
  * Add CarParams struct to improve the abstraction layer
  * Refactor visiond IPC to support multiple clients
  * Add raw GPS and beginning support for navigation
  * Improve model in visiond using crowdsourced data
  * Add improved system logging to diagnose instability
  * Rewrite baseui in React Native
  * Moved calibration to the cloud

Version 0.2.9  (2017-03-01)
===========================
  * Retain compatibility with NEOS v1

Version 0.2.8  (2017-02-27)
===========================
  * Fix bug where frames were being dropped in minute 71

Version 0.2.7  (2017-02-08)
===========================
  * Better performance and pictures at night
  * Fix ptr alignment issue in boardd
  * Fix brake error light, fix crash if too cold

Version 0.2.6  (2017-01-31)
===========================
  * Fix bug in visiond model execution

Version 0.2.5  (2017-01-30)
===========================
  * Fix race condition in manager

Version 0.2.4  (2017-01-27)
===========================
  * OnePlus 3T support
  * Enable installation as NEOS app
  * Various minor bugfixes

Version 0.2.3  (2017-01-11)
===========================
  * Reduce space usage by 80%
  * Add better logging
  * Add Travis CI

Version 0.2.2  (2017-01-10)
===========================
  * Board triggers started signal on CAN messages
  * Improved autoexposure
  * Handle out of space, improve upload status

Version 0.2.1  (2016-12-14)
===========================
  * Performance improvements, removal of more numpy
  * Fix boardd process priority
  * Make counter timer reset on use of steering wheel

Version 0.2  (2016-12-12)
=========================
  * Car/Radar abstraction layers have shipped, see cereal/car.capnp
  * controlsd has been refactored
  * Shipped plant model and testing maneuvers
  * visiond exits more gracefully now
  * Hardware encoder in visiond should always init
  * ui now turns off the screen after 30 seconds
  * Switch to openpilot release branch for future releases
  * Added preliminary Docker container to run tests on PC

Version 0.1  (2016-11-29)
=========================
  * Initial release of openpilot
  * Adaptive cruise control is working
  * Lane keep assist is working
  * Support for Acura ILX 2016 with AcuraWatch Plus
  * Support for Honda Civic 2016 Touring Edition
