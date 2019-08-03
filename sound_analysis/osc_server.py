import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
import sounddevice as sd
from scipy.io.wavfile import write

def save_synth_values(*args):
  #for i in args:
    #print(args[i])
  print(args)

def record_audio():
  fs = 44100  # Sample rate
  seconds = 1  # Duration of recording

  myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
  sd.wait()  # Wait until recording is finished
  write('output.wav', fs, myrecording)  # Save as WAV file

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/synth_receive", save_synth_values)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()


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



