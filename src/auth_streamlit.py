import streamlit as st
import time

def check_password():
    """Returns `True` if the user had a correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if "username" in st.session_state and "password" in st.session_state:
            usr = st.session_state["username"]
            pwd = st.session_state["password"]
            
            # Safe access to secrets
            try:
                creds = st.secrets["credentials"]
                if usr in creds["usernames"]:
                    index = creds["usernames"].index(usr)
                    if pwd == creds["passwords"][index]:
                        st.session_state["password_correct"] = True
                        st.session_state["user_name"] = creds["names"][index]
                        # Clean up inputs
                        del st.session_state["password"]
                        del st.session_state["username"]
                        return
            except Exception as e:
                # Fallback if secrets structure is wrong
                st.error(f"Error de configuración: {e}")
                
            # Failed
            st.session_state["password_correct"] = False
        else:
            st.session_state["password_correct"] = False

    # Return True if already authenticated
    if st.session_state.get("password_correct", False):
        return True

    # Show Login Form if not authenticated
    # Split Screen Login Design
    st.markdown("""
    <style>
        /* Force Full Screen & Remove Padding */
        .stApp {
            background-color: white !important;
            overflow: hidden !important; /* NO SCROLL ALLOWED */
        }
        [data-testid="stAppViewContainer"] {
            background-color: white !important;
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden !important;
            height: 100vh !important;
        }
        [data-testid="stHeader"] {
            display: none !important; /* Hide header strip */
        }
        [data-testid="stSidebar"] {
            display: none !important; 
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
            overflow: hidden !important;
        }
        /* Remove Streamlit's vertical gap */
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
        }
        
        /* Left Panel Style */
        .left-panel {
            background-color: #183C30;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        
        /* Right Panel Style */
        .right-panel {
            height: 100vh !important;
            display: flex !important;
            align-items: center !important; /* Horiz Center */
            justify-content: center !important; /* Vert Center */
            flex-direction: column !important;
            padding: 20px;
            margin-top: -50px; /* Counteract streamlit top padding */
        }
        
        /* Form Styling */
        .login-title {
            font-family: 'Inter', sans-serif;
            color: #1E3A2F;
            font-weight: 800;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .login-subtitle {
             color: #666;
             margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- ABSOLUTE POSITIONING STRATEGY ---
    import base64
    def get_base64_image(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
             return ""

    logo_b64 = get_base64_image("src/assets/logo.png")

    # Full Screen Layout CSS
    st.markdown(f"""
    <style>
        /* RESET STREAMLIT CONTAINERS */
        .stApp {{
            background-color: white !important;
        }}
        [data-testid="stAppViewContainer"] {{
            background-color: white !important;
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden !important;
        }}
        [data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stToolbar"] {{
            display: none !important;
        }}
        .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }}
        [data-testid="stVerticalBlock"] {{
            gap: 0 !important;
            padding: 0 !important;
        }}
        /* LEFT PANEL (Green Overlay) */
        .split-left {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 50% !important;
            max-width: 50% !important; /* Strict limit */
            height: 100vh !important;
            background-color: #183C30 !important;
            z-index: 10 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
        
        /* FORM CONTAINER - TARGETING STREAMLIT NATIVE FORM DIRECTLY */
        [data-testid="stForm"] {{
            position: fixed !important;
            top: 50% !important; /* True Center */
            left: 75% !important; 
            transform: translate(-50%, -50%) !important;
            width: 100% !important; 
            max-width: 360px !important; /* 20% larger */
            height: auto !important; /* Define height by content */
            min-height: unset !important;
            z-index: 9999 !important;
            background: white !important;
            padding: 40px !important; /* Visual breathing room */
            border-radius: 16px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1) !important;
            border: 1px solid #E5E7EB !important;
        }}
        
        /* Hide the submit button's default container padding if any */
        /* Hide the submit button's default container padding if any */
        [data-testid="stForm"] > div {{
             padding-bottom: 0 !important;
        }}

        /* BUTTON SPACING */
        [data-testid="stFormSubmitButton"] {{
             margin-top: 20px !important;
        }}
        [data-testid="stFormSubmitButton"] button {{
             border-radius: 8px !important;
             border: none !important;
        }}

        /* HIDE "Press Enter to submit" HINT - AGGRESSIVE */
        [data-testid="stForm"] small, 
        [data-testid="stForm"] .streamlit-small-text, 
        [data-testid="inputInstructions"],
        div[data-testid="stForm"] div[data-testid="stMarkdownContainer"] p small {{
             display: none !important;
             opacity: 0 !important;
             visibility: hidden !important;
             height: 0 !important;
        }}

        /* ERROR MESSAGE POSITIONING */
        .login-error {{
            position: fixed !important;
            top: 82% !important; /* Low enough to clear the form */
            left: 75% !important;
            transform: translate(-50%, -50%) !important;
            width: 360px !important; /* Match form width */
            z-index: 10000 !important;
            text-align: center !important;
        }}
        
        .login-error [data-testid="stAlert"] {{
             width: 100% !important;
        }}
    </style>
    
    <!-- LEFT PANEL CONTENT -->
    <div class="split-left">
         <img src="data:image/png;base64,{logo_b64}" style="width: 50%; max-width: 300px; filter: brightness(0) invert(1);" />
    </div>
    """, unsafe_allow_html=True)

    # FORM CONTENT
    with st.form("login_form"):
        st.text_input("Correo electrónico", key="username", placeholder="user@origenbotanico.com") 
        # Note: changing label to hidden might improve minimalist look but user didn't ask. 
        # Kept visible as per screenshot but "Correo electrónico"
        
        # User screenshot shows "Correo electrónico" label. I will verify if I need to change anything there. 
        # Current code uses label="Correo electrónico". Correct.
        
        st.text_input("Contraseña", type="password", key="password", placeholder="••••••••")
        submitted = st.form_submit_button("INGRESAR", type="primary", use_container_width=True)
        
        if submitted:
             password_entered()
             if st.session_state.get("password_correct", False):
                st.rerun()

    # ERROR MESSAGE (Floating below form)
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
         st.markdown(
             """
             <div class="login-error">
             """, unsafe_allow_html=True
         )
         st.error("Credenciales incorrectas")
         st.markdown("</div>", unsafe_allow_html=True)
    
    return False

def logout():
    st.session_state["password_correct"] = False
    st.rerun()
