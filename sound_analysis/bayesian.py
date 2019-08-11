from osc_client import run_client
#from osc_server import run_server
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
import pdb


def get_synth_output(synth_values):
    # send values to the synth and record its output
    run_client(synth_values)
    time.sleep(3)
    audio_vector = audio_to_array("synth/synth_rec.wav")
    return audio_vector

def user_sample_conversion(audio):
    user_audio_vector = audio_to_array(audio)
    return user_audio_vector

def training_function(X):
    #vector_array = np.zeros((num_data_points, 8))
    vector_array = [0] * num_data_points  # here will be stored audio vectors of synth outputs for given X
    for row in X:
        x_list = row.tolist()
        vector_array[row] = np.linalg.norm(user_sample_vector - get_synth_output(x_list))

    #vector_array = [0] * num_data_points  # here will be stored audio vectors of synth outputs for given X
    #print(vector_array)
    # for i in range(num_data_points):
    #     vector_array[i] = np.linalg.norm(user_sample_vector - get_synth_output(x_list[i]))
    #     #vector_array[i] = get_synth_output(Xlist[i])
    #     print(i)
    #     print(vector_array)
    vector_array = np.asarray(vector_array)
    vector_array = vector_array.reshape(num_data_points,1)
    return vector_array

# def placeholder(X):
#     training_function

def process_user_sample(user_sample):
    user_sample_vector = user_sample_conversion(user_sample)
    user_sample_vector = np.asarray(user_sample_vector)
    return user_sample_vector

user_sample_vector = process_user_sample("audio_samples/rain01.wav")

syn1 = syn2 = syn3 = syn4 = syn5 = np.arange(158)
syn6 = np.arange(6000)
syn7 = np.arange(1000)
syn8 = np.arange(700)

parameter_space = ParameterSpace(
    [DiscreteParameter('x1', syn1), DiscreteParameter('x2', syn2), DiscreteParameter('x3', syn3),
     DiscreteParameter('x4', syn4), DiscreteParameter('x5', syn5), DiscreteParameter('x6', syn6),
     DiscreteParameter('x7', syn1), DiscreteParameter('x8', syn8)])

design = RandomDesign(parameter_space)  # Collect random points
num_data_points = 5
#pdb.set_trace()
X = design.get_samples(num_data_points) # X is a numpy array ##lista punktów
print("X=", X)

#Y = get_synth_output(X) ##tu trzeba zrobić liste wynikow czyli wektorow
#pdb.set_trace()
# Y = placeholder(X)
Y = training_function(X)

print(Y)
model_gpy = GPRegression(X, Y)  # Train and wrap the model in Emukit

model_emukit = GPyModelWrapper(model_gpy)
expected_improvement = ExpectedImprovement(model=model_emukit)
bayesopt_loop = BayesianOptimizationLoop(model=model_emukit,
                                         space=parameter_space,
                                         acquisition=expected_improvement,
                                         batch_size=1)

max_iterations = 10
bayesopt_loop.run_loop(training_function, max_iterations)
results = bayesopt_loop.get_results()
