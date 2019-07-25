

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for x in range(10):
        client.send_message("/filter", random.random())
        time.sleep(1)

from pythonosc import osc_message_builder
from pythonosc import udp_client

client = udp_client.SimpleUDPClient('localhost', 57110)

amplitude = 0.5 # just adding one amplitude
phase = 0.5 # just adding one phase

msg = osc_message_builder.OscMessageBuilder(address = '/s_new')
msg.add_arg(100, arg_type='i')
msg.add_arg(1, arg_type='i')
msg.add_arg(1, arg_type='i')
msg.add_arg('oscBank512', arg_type='s')
msg.add_arg('amplitude', arg_type='s')
msg.add_arg(amplitude, arg_type='f')
msg.add_arg('phase', arg_type='s')
msg.add_arg(phase, arg_type='f')
msg.add_arg('attackSynth', arg_type='s')
msg.add_arg(0.1, arg_type='f')
msg.add_arg('releaseSynth', arg_type='s')
msg.add_arg(0.5, arg_type='f')
msg = msg.build()
client.send(msg)