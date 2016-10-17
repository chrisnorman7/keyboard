import pyglet, libaudioverse as lav, sys # Main imports
from pyglet.window import key # Pyglet key definitions.

lav.initialize() # Initialise Libaudioverse

volume = 0.4 # The initial volume.

keys = { # List of keys which will play tones.
 key.A: -9,
 key.W: -8,
 key.S: -7,
 key.E: -6,
 key.D: -5,
 key.F: -4,
 key.T: -3,
 key.G: -2,
 key.Y: -1,
 key.H: 0,
 key.U: 1,
 key.J: 2,
 key.K: 3,
 key.O: 4,
 key.L: 5,
 key.P: 6,
 key.SEMICOLON: 7,
 key.APOSTROPHE: 8,
 key.BRACKETRIGHT: 9,
 key.HASH: 10
}

class NodeList(object): # Store nodes.
 def __init__(self, type, difference = 1.0, play = True):
  self.type = type # A wave generator class to be initialised.
  self.play = play # True of False for whether or not nodes should be played when keys are pressed.
  self.nodes = dict() # Put all the nodes into this list.
  for k, v in keys.items(): # Could be expanded by just changing the list of keys.
   n = self.type(Server) # Create the wave generator.
   n.mul.value = volume # Set the volume.
   n.state.value = lav.NodeStates.paused # Pause the node so it doesn't play when connected.
   n.frequency.value = difference * semi(v) # Set the frequency to be the frequency of the note which will be played.
   n.connect(0, fx, 0) # Connect it to the FX node.
   n.connect(0,Server) # Connect the dry signal to the Server.
   self.nodes[k] = n # Finally add the new node to the nodes dictionary.

def semi(semitones, frequency = 440.0):
 a = 2.0 ** (1.0/12.0)
 return frequency * (a**semitones)

def set_volume(value):
 value -= 48
 if not value:
  value = 100.0
 else:
  value *= 10.0
 value = value * 0.01
 print(value)
 for n in nodes:
  for v in n.nodes.values():
   v.mul.value = value

def get_nodes(value):
 res = []
 for n in nodes:
  if n.play and value in n.nodes:
   res.append(n.nodes[value])
 return res

Server = lav.Server()
Server.set_output_device()

fx = lav.FdnReverbNode(Server)
fx.mul.value = 0.1
fx.cutoff_frequency.value = 10000.0
fx.density.value = 1.0
fx.delay_modulation_frequency.value = 100.0
fx.connect(0,Server)

nodes = []
nodes.append(NodeList(lav.SineNode, difference = 0.5))
nodes.append(NodeList(lav.AdditiveSquareNode, difference = 0.5))
nodes.append(NodeList(lav.AdditiveSawNode, difference = 0.5))
nodes.append(NodeList(lav.AdditiveTriangleNode, difference = 0.5))

window = pyglet.window.Window(caption = 'Keyboard')

pressed_keys = [] # The keys which are currently pressed.

@window.event
def on_close():
 lav.shutdown()

@window.event
def on_key_press(single, mods): # A key was pressed.
 if single in keys:
  pressed_keys.append(single)
  for n in get_nodes(single):
   n.state.value = lav.NodeStates.playing
 else:
  toggle_node_keys = [key.F1, key.F2, key.F3, key.F4]
  if single in toggle_node_keys:
   node = nodes[toggle_node_keys.index(single)]
   node.play = not node.play
   for k, n in node.nodes.items():
    if node.play and k in pressed_keys:
     n.state.value = lav.NodeStates.playing
    else:
     n.state.value = lav.NodeStates.paused
  elif single in [key._1, key._2, key._3, key._4, key._5, key._6, key._7, key._8, key._9, key._0]:
   set_volume(single)

@window.event
def on_key_release(single, mods):
 if single in pressed_keys:
  pressed_keys.remove(single)
 for n in get_nodes(single):
  n.state.value = lav.NodeStates.paused

if __name__ == '__main__':
 pyglet.app.run()
