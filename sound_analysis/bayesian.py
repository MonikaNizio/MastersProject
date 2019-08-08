from osc_client import run_client
from osc_server import run_server
from process_audio import audio_to_array
import time
import numpy as np
from emukit.test_functions import branin_function
from emukit.core import ParameterSpace, ContinuousParameter, DiscreteParameter
from emukit.experimental_design.model_free.random_design import RandomDesign
from GPy.models import GPRegression
from emukit.model_wrappers import GPyModelWrapper
from emukit.bayesian_optimization.acquisitions import ExpectedImprovement
from emukit.bayesian_optimization.loops import BayesianOptimizationLoop


def training_function(synth_values):
    # send values to the synth and record its output
    run_client(synth_values)
    time.sleep(5)
    audio_vector = audio_to_array("synth/synth_rec.wav")
    return audio_vector

syn1 = syn2 = syn3 = syn4 = syn5 = np.arange(158)
syn6 = np.arange(6000)
syn7 = np.arange(1000)
syn8 = np.arange(700)

# initial value list
# value_list = [10, 20, 30, 40, 50, 60, 70, 80]

# receive the values from the synth
# run_server()

# f, _ = branin_function()
# parameter_space = ParameterSpace(
#     [ContinuousParameter('x1', 0, 157), ContinuousParameter('x2', 0, 157), ContinuousParameter('x3', 0, 157),
#      ContinuousParameter('x4', 0, 157), ContinuousParameter('x5', 0, 157), ContinuousParameter('x6', 0, 5999),
#      ContinuousParameter('x7', 0, 999), ContinuousParameter('x8', 0, 699)])

parameter_space = ParameterSpace(
    [DiscreteParameter('x1', syn1), DiscreteParameter('x2', syn2), DiscreteParameter('x3', syn3),
     DiscreteParameter('x4', syn4), DiscreteParameter('x5', syn5), DiscreteParameter('x6', syn6),
     DiscreteParameter('x7', syn1), DiscreteParameter('x8', syn8)])

design = RandomDesign(parameter_space)  # Collect random points
num_data_points = 1
X = design.get_samples(num_data_points) # X is a (nested?) list
print(X)

# remove nesting
X = X[0]
print(X)

Y = training_function(X)
model_gpy = GPRegression(X, Y)  # Train and wrap the model in Emukit
model_emukit = GPyModelWrapper(model_gpy)
expected_improvement = ExpectedImprovement(model=model_emukit)
bayesopt_loop = BayesianOptimizationLoop(model=model_emukit,
                                         space=parameter_space,
                                         acquisition=expected_improvement,
                                         batch_size=1)

max_iterations = 10
bayesopt_loop.run_loop(Y, max_iterations)
results = bayesopt_loop.get_results()
