#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip", default="127.0.0.1",
#                         help="The ip of the OSC server")
#     parser.add_argument("--port", type=int, default=5005,
#                         help="The port the OSC server is listening on")
#     args = parser.parse_args()
#
#     client = udp_client.SimpleUDPClient(args.ip, args.port)
#
#     for x in range(10):
#         client.send_message("/filter", random.random())
#         time.sleep(1)

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