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

def run_server():
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
                            default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
                            type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  #print(getattr(dispatcher, "dispatcher"))
  dispatcher.map("/synth_receive", send_synth_values)

  server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()