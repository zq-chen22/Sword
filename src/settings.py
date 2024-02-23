# config for main game
import os

WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
MAROON = '#800000'
BLACK = '#000000'
SALMON = '#FA8072'
SCARLET = "#FF2400"
IRON = '#48494B'
STEEL = '#777B7E'
GRAY = '#999999'
INK = '#C0C0C0'
CRIMSON = "#DC143C"
FIREBRICK = "#B22222"
MIDNIGHTBLUE = "#16264C"
DEEPBLUE = "#004C99"
SHALLOWBLUE = "#6D89DF"

PATH = os.path.dirname(os.path.dirname(__file__))
MODE = "webset"  # "webset"/"window"/"terminal"/"none"
PLAYERS = 2
PLAYERPOLICY = ["input", "random"]

LOCAL_IP = "127.0.0.1"
GLOBAL_IP = "127.0.0.1"
PORT = 7071