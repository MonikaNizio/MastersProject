from osc_client import run_client
#from osc_server import run_server
from process_audio import audio_to_array
import time
import numpy as np
from emukit.core import ParameterSpace, ContinuousParameter, DiscreteParameter
from emukit.experimental_design.model_free.random_design import RandomDesign
from GPy.models import GPRegression
from emukit.model_wrappers import GPyModelWrapper
from emukit.bayesian_optimization.acquisitions import ExpectedImprovement
from emukit.bayesian_optimization.loops import BayesianOptimizationLoop
from emukit.core.loop.user_function import UserFunction, UserFunctionWrapper
from emukit.benchmarking.loop_benchmarking.benchmark_plot import BenchmarkPlot
from emukit.core.loop.loop_state import LoopState
from emukit.core.loop.loop_state import create_loop_state
from emukit.core.loop.user_function_result import UserFunctionResult
import pdb


def get_synth_output(synth_values): #transform the synth output into a data vector
    #send values to the synth and record its output
    run_client(synth_values)
    #allow time to record
    time.sleep(3)
    #convert to a data vector
    audio_vector = audio_to_array("synth/synth_rec.wav")
    return audio_vector

def training_function(X): #return the difference between the user sample and the test sample

    i = 0
    vector_array = [0] * np.size(X,0)  # used for storing audio vectors of synth outputs for the given X
    #process recordings for the given set of X
    for row in X:
        print("processing set of synth settings from the row #", i, " in X:", row)
        #Euclidean distance between the target sample and the test sample
        vector_array[i] = np.linalg.norm(user_sample_vector - get_synth_output(row))
        print("result:", vector_array[i])
        i += 1
    vector_array = np.asarray(vector_array)
    #print("training function result", vector_array)
    vector_array = vector_array.reshape(num_data_points, 1)
    print("training function results for the given set of X:", vector_array)
    return vector_array

def process_user_sample(user_sample):
    user_sample = audio_to_array(user_sample)
    #user_sample = np.asarray(user_sample)
    return user_sample

#1. user sample into a data vector
user_sample_vector = process_user_sample("audio_samples/rain02.wav")
#print("user sample", user_sample_vector)

#2. ranges of the synth parameters
syn1 = syn2 = syn3 = syn4 = syn5 = np.arange(158)
syn6 = np.arange(6000)
syn7 = np.arange(1000)
syn8 = np.arange(700)

#2. synth paramters ranges into an 8D parameter space
parameter_space = ParameterSpace(
    [DiscreteParameter('x1', syn1), DiscreteParameter('x2', syn2), DiscreteParameter('x3', syn3),
     DiscreteParameter('x4', syn4), DiscreteParameter('x5', syn5), DiscreteParameter('x6', syn6),
     DiscreteParameter('x7', syn1), DiscreteParameter('x8', syn8)])

#3. collect random points
design = RandomDesign(parameter_space)
num_data_points = 3
X = design.get_samples(num_data_points) #X is a numpy array
print("X=", X)

UserFunction.evaluate(training_function, X)
results = UserFunctionWrapper(training_function).evaluate(X)

#[is this needed?]
#loop_state = create_loop_state(X, Y)

#4. define training_function as Y
Y = training_function(X)

#5. train and wrap the model in Emukit
model_gpy = GPRegression(X, Y)

model_emukit = GPyModelWrapper(model_gpy)
expected_improvement = ExpectedImprovement(model=model_emukit)
bayesopt_loop = BayesianOptimizationLoop(model=model_emukit,
                                         space=parameter_space,
                                         acquisition=expected_improvement,
                                         batch_size=3)

max_iterations = 3
bayesopt_loop.run_loop(training_function, max_iterations)

#results = bayesopt_loop.get_results()
bayesopt_loop.loop_state.X
print("X: ", bayesopt_loop.loop_state.X)
print("Y: ", bayesopt_loop.loop_state.Y)
print("cost: ", bayesopt_loop.loop_state.cost)



