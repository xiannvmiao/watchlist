from dotenv import load_dotenv
import os

dot_env = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dot_env):
    load_dotenv(dot_env)

from watchlist import app



