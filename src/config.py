import os
from dotenv import load_dotenv

import sys

def load_env_file():
    if getattr(sys, 'frozen', False):
        # If frozen, look in the same directory as the executable
        base_path = os.path.dirname(sys.executable)
    else:
        # If script, look in the parent directory (project root)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    env_path = os.path.join(base_path, '.env')
    load_dotenv(env_path)

load_env_file()

def get_config():
    companies = []
    for i in range(1, 7):  # Changed from 5 to 7 to support up to 6 companies

        name = os.getenv(f"COMPANY_{i}_NAME")
        username = os.getenv(f"COMPANY_{i}_USER")
        access_key = os.getenv(f"COMPANY_{i}_KEY")
        
        if name and username and access_key:
            companies.append({
                "id": i,
                "name": name,
                "username": username,
                "access_key": access_key
            })
    return companies
