import os
import sys

# Add the project root to the path so the 'app' package can be found
# The 'api' folder is inside the project root, so we add the parent of '__file__'
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from app import create_app

app = create_app()
