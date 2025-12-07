import os
from dotenv import load_dotenv
import streamlit as st

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
    for i in range(1, 7):  # Support up to 6 companies
        
        # Keys to look for
        key_name = f"COMPANY_{i}_NAME"
        key_user = f"COMPANY_{i}_USER"
        key_access = f"COMPANY_{i}_KEY"
        
        # 1. Try OS Environment (Local .env)
        name = os.getenv(key_name)
        username = os.getenv(key_user)
        access_key = os.getenv(key_access)
        
        # 2. Fallback to Streamlit Secrets (Cloud)
        # Check if keys exist in the root of st.secrets
        if name is None and key_name in st.secrets:
            name = st.secrets[key_name]
        if username is None and key_user in st.secrets:
            username = st.secrets[key_user]
        if access_key is None and key_access in st.secrets:
            access_key = st.secrets[key_access]
            
        if name and username and access_key:
            companies.append({
                "id": i,
                "name": name,
                "username": username,
                "access_key": access_key
            })
    return companies
