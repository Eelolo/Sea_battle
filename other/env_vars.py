import os
from dotenv import load_dotenv
import json


def load_variable(var_name: str):
    load_dotenv()
    return json.loads(os.getenv(var_name))
