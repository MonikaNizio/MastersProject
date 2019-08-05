from osc_client import run_client
from osc_server import run_server
from process_audio import audio_to_array
import time

#initial value list
value_list = [10, 20, 30, 40, 50, 60, 70, 80]

#send values to the synth and record its output
run_client(value_list)

#receive the values from the synth
run_server()
time.sleep(5)
a = audio_to_array("synth/synth_rec.wav")