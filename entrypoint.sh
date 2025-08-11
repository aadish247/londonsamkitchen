#!/bin/bash
set -e

# Print Python and package versions for debugging
python -c "import sys; print(f'Python version: {sys.version}')"
python -c "import numpy as np; print(f'NumPy version: {np.__version__}')"
python -c "import pandas as pd; print(f'Pandas version: {pd.__version__}')"

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:${PORT:-8080} app:app