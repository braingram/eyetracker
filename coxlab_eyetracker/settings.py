
# these are the first settings loaded, they will be overwritten by:
#  1) default_config (in util/__init__.py)
#  2) ~/.eyetracker/config.ini
#
# within the .ini files section does NOT matter

global_settings = {"use_simulated": False,
                    "use_file_for_camera": False,
                    "calibration_path": '~/.eyetracker/calibration/'
                  }
