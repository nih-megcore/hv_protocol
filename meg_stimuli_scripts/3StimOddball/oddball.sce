scenario = "oddball";
scenario_type = trials;
pcl_file = "oddball.pcl";
response_matching = simple_matching;
active_buttons = 1;
button_codes = 1;
write_codes = true;
pulse_width = 25;
response_port_output = false;
default_text_color = 0, 0, 0;
default_font_size = 28;
no_logfile = true; 
default_background_color = 127, 127, 127;

begin;

sound { wavefile { filename = "std.wav"; }; attenuation = .15; } std;
sound { wavefile { filename = "targ.wav"; }; attenuation = .15; } targ;
sound { wavefile { filename = "white.wav"; }; } white;

picture {
   text { caption = "·"; font = "Symbol"; } fixation_mark;
   x = 0; y = 0;   
} default;

trial {
   trial_duration = forever;
   trial_type = first_response;
   
   picture {
      text { caption = "You will hear a series of brief sounds.
Two will be tones with different pitches
and one will sound like static. Your job is to
press the red button with your thumb when you
hear the higher pitched tone only. Ignore the
lower pitched tone and the static sound."; };
      x = 0; y = 0;
   };   
   time = 0;
} instruction_trial;

trial {
   trial_duration = forever;
   trial_type = first_response;
   
   picture {
      text { caption = "You will hear a series of brief sounds.
Two will be tones with different pitches
and one will sound like static. Your job is to
press the red button with your thumb when you
hear the higher pitched tone only. Ignore the
lower pitched tone and the static sound.
We will play you a sample now to test the sound level.
Please practice responding to the higher pitched tone
so that we will know you understand the task."; };
      x = 0; y = 0;
   };   
   time = 0;
} practice_trial;

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
   stimulus_event {
      sound std;
      time = 0;
      port = 1;
   } beep; 
} beep_trial;

trial {
   trial_duration = forever;
   trial_type = first_response;
   
   picture {
      text { caption = "Done!"; };
      x = 0; y = 0;
   };
   time = 0;
} done_trial;