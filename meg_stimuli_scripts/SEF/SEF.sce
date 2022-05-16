scenario = "SEF";
pcl_file = "SEF.pcl";

# These are always needed.
scenario_type = trials;
response_matching = simple_matching;

# Write port codes to the trigger port.
default_output_port = 1;
write_codes = true;
pulse_width = 25;

# Mouse click to end localization.
active_buttons = 1;
button_codes = 1;
response_port_output = false;

# Random defaults.
no_logfile = true;
default_text_color = 0, 0, 0;
default_background_color = 192, 192, 192;
default_font_size = 28;

begin;

picture {
   text { caption = "·"; font = "Symbol"; } fixation_mark;
   x = 0; y = 0;
} default;

trial {
   trial_duration = forever;
   trial_type = first_response;

   picture {
      text { caption = "Localizing head, please hold still..."; };
      x = 0; y = 0;
   };
   time = 0;
} localize_trial;

trial {
   trial_duration = forever;
   trial_type = first_response;

   picture {
      text { caption = "Done!"; };
      x = 0; y = 0;
   };
   time = 0;
} done_trial;

trial {
   stimulus_event {
      nothing {};
      time = 0;
      port = 2;
      port_code = 1;
   } st_stim;
} stim_trial;
