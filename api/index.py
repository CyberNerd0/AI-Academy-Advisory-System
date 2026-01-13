import os
import sys

# Force the current directory (api/) into the path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

# Vercel needs this to know where the app is. 
# It looks for a variable named 'app' or 'handler' in the file specified in vercel.json.
