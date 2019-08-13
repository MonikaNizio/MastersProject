from pythonosc import osc_message_builder
from pythonosc import udp_client
import numpy as np

def run_client(value_list):

    client = udp_client.SimpleUDPClient('localhost', 57110)

    msg = osc_message_builder.OscMessageBuilder(address = '/synth_values')

    #turn array into a list
    #value_list = np.ndarray.tolist(value_list)

    #turn nested list into a list
    #value_list = value_list[0]

    for i in value_list:
        msg.add_arg(i, arg_type='i')

    msg = msg.build()
    client.send(msg)