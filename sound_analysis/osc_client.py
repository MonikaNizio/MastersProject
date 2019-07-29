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

value_list = [10, 20, 30, 40, 50, 60, 70, 80]

client = udp_client.SimpleUDPClient('localhost', 57110)

msg = osc_message_builder.OscMessageBuilder(address = '/synth_values')

for i in value_list:
    msg.add_arg(i, arg_type='i')

msg = msg.build()
client.send(msg)