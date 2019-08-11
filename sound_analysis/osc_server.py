import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
import sounddevice as sd
from scipy.io.wavfile import write
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
import serial

def send_synth_values(*args):
  #for i in args:
    #print(args[i])
  print(args)

# def record_audio():
#   fs = 44100  # Sample rate
#   seconds = 1  # Duration of recording
#
#   myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
#   sd.wait()  # Wait until recording is finished
#   write('output.wav', fs, myrecording)  # Save as WAV file

#dispatcher = dispatcher.Dispatcher()
#if __name__ == "__main__":

test_points = [143, 35, 72, 80, 29, 4488, 67, 429]

#def run_server():
# parser = argparse.ArgumentParser()
# parser.add_argument("--ip",
#                           default="127.0.0.1", help="The ip to listen on")
# parser.add_argument("--port",
#                           type=int, default=8000, help="The port to listen on")
# args = parser.parse_args()
#
# dispatcher = dispatcher.Dispatcher()
# #print(getattr(dispatcher, "dispatcher"))
# dispatcher.map("/synth_receive", send_synth_values)
#
# server = osc_server.ThreadingOSCUDPServer(
#       (args.ip, args.port), dispatcher)
# print("Serving on {}".format(server.server_address))
    #server.serve_forever()

dispatcher = Dispatcher()
#
#
# def set_filter(address: str, *args: List[Any]) -> None:
#     # We expect two float arguments
#     if not len(args) == 2 or type(args[0]) is not float or type(args[1]) is not float:
#         return
#
#     # Check that address starts with filter
#     if not address[:-1] == "/filter":  # Cut off the last character
#         return
#
#     value1 = args[0]
#     value2 = args[1]
#     filterno = address[-1]
#     print(f"Setting filter {filterno} values: {value1}, {value2}")
#
#
# dispatcher.map("/filter*", set_filter)  # Map wildcard address to set_filter function
# server = BlockingOSCUDPServer(("127.0.0.1", 8080), dispatcher)
# client = SimpleUDPClient("127.0.0.1", 8080)
#
# # Send message and receive exactly one message (blocking)
# client.send_message("/filter1", [1., 2.])
# server.handle_request()
#
# client.send_message("/filter8", [6., -2.])
# server.handle_request()

'''
dispatcher.map("/synth_receive", send_synth_values(test_points))  # Map wildcard address to set_filter function
server = BlockingOSCUDPServer(("127.0.0.1", 8000), dispatcher)

server.handle_request()


#run_server()

  # parser2 = argparse.ArgumentParser()
  # parser2.add_argument("--ip",
  #     default="127.0.0.1", help="The ip to listen on")
  # parser2.add_argument("--port",
  #     type=int, default=5050, help="The port to listen on")
  # args2 = parser2.parse_args()
  #
  # dispatcher2 = dispatcher.Dispatcher()
  # dispatcher2.map("/synth_receive", save_synth_values)
  #
  # server2 = osc_server.ThreadingOSCUDPServer(
  #     (args.ip, args.port), dispatcher2)
  # print("Serving on {}".format(server2.server_address))
  # server2.serve_forever()


# ser = serial.Serial('240')  # open serial port
# print(ser.name)         # check which port was really used
# ser.write(b'hello')     # write a string
# ser.close()             # close port

# with serial.Serial('a', 2400, timeout=1) as ser:
#     x = ser.read()          # read one byte
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     line = ser.readline()   # read a '\n' terminated line