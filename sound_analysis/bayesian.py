from osc_client import run_client
# from osc_server import run_server
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
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor


num_data_points = 5
user_sample_vector = 0

def get_synth_output(vector_array):  # transform the synth output into a data vector
    #vector_array = np.array([synth_values[0], 0, 0, 0, 0, 5999, 0, 0])

    # send values to the synth and record its output
    run_client(vector_array)
    # allow time to record
    time.sleep(3)
    # convert to a data vector
    audio_vector = audio_to_array("synth/synth_rec.wav")
    return audio_vector

def training_function(X): #return the difference between the user sample and the test sample

    i = 0
    vector_array = [0] * np.size(X, 0)  # used for storing audio vectors of synth outputs for the given X
    # process recordings for the given set of X
    for row in X:
        print("processing set of synth settings from the row #", i, " in X:", row)
        # Euclidean distance between the target sample and the test sample
        vector_array[i] = np.linalg.norm(user_sample_vector - get_synth_output(row.astype(int)))
        # vector_array[i] = np.linalg.norm(user_sample_vector - get_synth_output(row.astype(int)))
        print("result:", vector_array[i])
        i += 1
    vector_array = np.asarray(vector_array)
    # print("training function result", vector_array)
    vector_array = vector_array.reshape(-1, 1)
    print("training function results for the given set of X:", vector_array)
    return vector_array

# def process_user_sample(user_sample):
#     user_sample = audio_to_array(user_sample)
#     # user_sample = np.asarray(user_sample)
#     return user_sample

def main_loop(file_name):
    # 1. user sample into a data vector
    global user_sample_vector
    user_sample_vector = audio_to_array(file_name)
    # print("user sample", user_sample_vector)
    bayesian_opt()


def bayesian_opt():

    # 2. ranges of the synth parameters
    syn1 = syn2 = syn3 = syn4 = syn5 = np.arange(158)
    syn6 = np.arange(6000)
    syn7 = np.arange(1000)
    syn8 = np.arange(700)

    # 2. synth paramters ranges into an 8D parameter space
    # parameter_space = ParameterSpace(
    #     [ContinuousParameter('x1', 0., 157.)])

    # parameter_space = ParameterSpace(
    #     [DiscreteParameter('x8', syn8)])

    parameter_space = ParameterSpace(
        [ContinuousParameter('x1', 0., 157.), ContinuousParameter('x2', 0., 157.), ContinuousParameter('x3', 0., 157.),
         ContinuousParameter('x4', 0., 157.), ContinuousParameter('x5', 0., 157.), ContinuousParameter('x6', 0., 5999.),
         ContinuousParameter('x7', 0., 999.), ContinuousParameter('x8', 0., 699.)])

    # parameter_space = ParameterSpace(
    #     [DiscreteParameter('x1', syn1), DiscreteParameter('x2', syn2), DiscreteParameter('x3', syn3),
    #      DiscreteParameter('x4', syn4), DiscreteParameter('x5', syn5), DiscreteParameter('x6', syn6),
    #      DiscreteParameter('x7', syn1), DiscreteParameter('x8', syn8)])

    # 3. collect random points
    design = RandomDesign(parameter_space)

    X = design.get_samples(num_data_points)  # X is a numpy array
    print("X=", X)

    # [is the below needed?]
    # UserFunction.evaluate(training_function, X)
    # I put UserFunctionWrapper in line 94

    # 4. define training_function as Y
    Y = training_function(X)

    # [is this needed?]
    # loop_state = create_loop_state(X, Y)

    # 5. train and wrap the model in Emukit
    model_gpy = GPRegression(X, Y, normalizer=True)

    model_emukit = GPyModelWrapper(model_gpy)
    expected_improvement = ExpectedImprovement(model=model_emukit)
    bayesopt_loop = BayesianOptimizationLoop(model=model_emukit,
                                             space=parameter_space,
                                             acquisition=expected_improvement,
                                             batch_size=5)

    max_iterations = 15
    bayesopt_loop.run_loop(training_function, max_iterations)
    model_gpy.plot()
    plt.show()
    results = bayesopt_loop.get_results()
    # bayesopt_loop.loop_state.X
    print("X: ", bayesopt_loop.loop_state.X)
    print("Y: ", bayesopt_loop.loop_state.Y)
    print("cost: ", bayesopt_loop.loop_state.cost)
