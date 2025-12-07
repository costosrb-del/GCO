import streamlit as st
import time

def check_password():
    """Returns `True` if the user had a correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if "username" in st.session_state and "password" in st.session_state:
            usr = st.session_state["username"]
            pwd = st.session_state["password"]
            
            if usr in st.secrets["credentials"]["usernames"]:
                index = st.secrets["credentials"]["usernames"].index(usr)
                if pwd == st.secrets["credentials"]["passwords"][index]:
                    st.session_state["password_correct"] = True
                    st.session_state["user_name"] = st.secrets["credentials"]["names"][index]
                    # Clean up
                    del st.session_state["password"]
                    del st.session_state["username"]
                    return
            
            # Failed
            st.session_state["password_correct"] = False
        else:
            st.session_state["password_correct"] = False

    # Return True if already authenticated
    if st.session_state.get("password_correct", False):
        return True

    # Show Login Form if not authenticated
    st.markdown("""
    <style>
        /* Login Page Specific Styles */
        [data-testid="stAppViewContainer"] {
            background-color: #F0F2F5;
        }
        [data-testid="stSidebar"] {
            display: none;
        }
        .login-container {
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            max-width: 400px;
            margin: auto;
        }
        .login-header {
            font-family: 'Inter', sans-serif;
            color: #1E3A2F;
            font-weight: 700;
            font-size: 24px;
            margin-bottom: 8px;
        }
        .login-sub {
            font-family: 'Inter', sans-serif;
            color: #666;
            font-size: 14px;
            margin-bottom: 24px;
        }
        .stTextInput input {
            background-color: #F9FAFB;
            border: 1px solid #E5E7EB;
            color: #000000;
        }
        .stButton button {
            background-color: #1E3A2F !important;
            color: white !important;
            font-weight: 600;
            border-radius: 8px;
            height: 45px;
        }
        .forgot-password {
            text-align: center;
            margin-top: 16px;
            font-size: 13px;
        }
        .forgot-password a {
            color: #1E3A2F;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

    # Centered Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>" * 2, unsafe_allow_html=True)
        
        # Header without broken container wrapper
        st.markdown('<h2 style="text-align: center; color: #1E3A2F; margin-bottom: 0;">🌿 Origen Botánico</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666; font-size: 14px; margin-top: 5px; margin-bottom: 30px;">Ingresa tus credenciales para continuar</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("Correo electrónico", key="username", placeholder="nombre@empresa.com")
            st.text_input("Contraseña", type="password", key="password", placeholder="••••••••")
            
            # Form submit button
            submitted = st.form_submit_button("Continuar", type="primary", use_container_width=True)
            
            if submitted:
                password_entered()
        
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("Usuario o contraseña incorrectos")
            
        st.markdown('<div class="forgot-password"><a href="#">¿Olvidaste tu contraseña?</a></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
    return False

def logout():
    st.session_state["password_correct"] = False
    st.rerun()
