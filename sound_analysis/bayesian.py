from osc_client import run_client
from osc_server import run_server
from process_audio import audio_to_array
import time
from emukit.core import ParameterSpace, ContinuousParameter
from emukit.experimental_design.model_free.random_design import RandomDesign
from GPy.models import GPRegression
from emukit.model_wrappers import GPyModelWrapper

# initial value list
value_list = [10, 20, 30, 40, 50, 60, 70, 80]

# send values to the synth and record its output
run_client(value_list)

# receive the values from the synth
run_server()
time.sleep(5)
a = audio_to_array("synth/synth_rec.wav")

parameter_space = ParameterSpace(
    [ContinuousParameter('x1', 0, 157), ContinuousParameter('x2', 0, 157), ContinuousParameter('x3', 0, 157),
     ContinuousParameter('x4', 0, 157), ContinuousParameter('x5', 0, 157), ContinuousParameter('x6', 0, 5999),
     ContinuousParameter('x7', 0, 999), ContinuousParameter('x8', 0, 699)])

design = RandomDesign(parameter_space) # Collect random points
num_data_points = 5
X = design.get_samples(num_data_points)
Y = f(X)
model_gpy = GPRegression(X,Y) # Train and wrap the model in Emukit
model_emukit = GPyModelWrapper(model_gpy)
