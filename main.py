#!/usr/bin/env python

import asyncio
import zmq
import zmq.asyncio
import signal
import struct
import sys

from chores import run

if (sys.version_info.major, sys.version_info.minor) < (3, 5):
		print("This example only works with Python 3.5 and greater")
		sys.exit(1)

port = 28332

class ZMQHandler():
		def __init__(self):
				self.loop = asyncio.get_event_loop()
				self.zmqContext = zmq.asyncio.Context()

				self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
				self.zmqSubSocket.setsockopt(zmq.RCVHWM, 0)
				self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
				self.zmqSubSocket.connect("tcp://127.0.0.1:%i" % port)

		async def handle(self) :
				topic, body, seq = await self.zmqSubSocket.recv_multipart()
				sequence = "Unknown"
				if len(seq) == 4:
						sequence = str(struct.unpack('<I', seq)[-1])
				if topic == b"hashblock":
						print('- HASH BLOCK ('+sequence+') -')
						# print(body.hex())
						run(body.hex())

				asyncio.ensure_future(self.handle())

		def start(self):
				self.loop.add_signal_handler(signal.SIGINT, self.stop)
				self.loop.create_task(self.handle())
				self.loop.run_forever()

		def stop(self):
				self.loop.stop()
				self.zmqContext.destroy()

daemon = ZMQHandler()
daemon.start()