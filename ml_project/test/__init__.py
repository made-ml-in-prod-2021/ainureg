import sys
from pathlib import Path

this = Path(__file__).resolve()
system_path = str(this.parent.parent.resolve())
#ml_project folder
sys.path.insert(0, system_path)
from src.data import datagenerate, read_pipeline_params
from src.utils import setup_logging
from src import app