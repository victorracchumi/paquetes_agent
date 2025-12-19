"""
Authentication module for Microsoft SSO integration
"""
import os
import msal
import requests
import json
from typing import Optional, Dict
from datetime import datetime, timedelta
try:
    import extra_streamlit_components as stx
except ImportError:
    stx = None

# Microsoft App Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

# MSAL Authority
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]

# Session timeout (8 hours)
SESSION_TIMEOUT_HOURS = 8

def get_msal_app():
    """Get MSAL Confidential Client Application"""
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )

def get_auth_url() -> str:
    """Generate Microsoft login URL"""
    app = get_msal_app()
    auth_url = app.get_authorization_request_url(
        SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return auth_url

def get_token_from_code(code: str) -> Optional[Dict]:
    """Exchange authorization code for access token"""
    app = get_msal_app()
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return result

def get_user_info(access_token: str) -> Optional[Dict]:
    """Get user information from Microsoft Graph"""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    return None

def get_cookie_manager():
    """Get cookie manager instance"""
    if stx is None:
        return None
    return stx.CookieManager()

def save_session_to_cookie(user_data: Dict):
    """Save session data to browser cookie"""
    import streamlit as st

    cookie_manager = get_cookie_manager()
    if cookie_manager is None:
        return

    session_data = {
        'user': user_data,
        'login_time': datetime.now().isoformat(),
        'authenticated': True
    }

    # Encode session data
    session_json = json.dumps(session_data)

    # Set cookie (expires in 8 hours = 28800 seconds)
    cookie_manager.set('multiaceros_session', session_json, max_age=28800)

def load_session_from_cookie():
    """Load session data from browser cookie"""
    import streamlit as st

    cookie_manager = get_cookie_manager()
    if cookie_manager is None:
        return False

    try:
        session_json = cookie_manager.get('multiaceros_session')

        if session_json:
            session_data = json.loads(session_json)

            # Check if session is still valid
            login_time = datetime.fromisoformat(session_data['login_time'])
            elapsed_time = datetime.now() - login_time

            if elapsed_time <= timedelta(hours=SESSION_TIMEOUT_HOURS):
                # Restore session to streamlit
                st.session_state['user'] = session_data['user']
                st.session_state['authenticated'] = True
                st.session_state['login_time'] = login_time
                return True
    except Exception as e:
        pass

    return False

def is_authenticated() -> bool:
    """Check if user is authenticated and session hasn't expired"""
    import streamlit as st

    # First check if we have session in streamlit
    if 'user' not in st.session_state or st.session_state['user'] is None:
        # Try to restore from cookie
        if not load_session_from_cookie():
            return False

    # Check session timeout
    if 'login_time' in st.session_state:
        login_time = st.session_state['login_time']
        elapsed_time = datetime.now() - login_time

        if elapsed_time > timedelta(hours=SESSION_TIMEOUT_HOURS):
            # Session expired
            logout()
            return False

    return True

def get_current_user() -> Optional[Dict]:
    """Get current authenticated user"""
    import streamlit as st
    return st.session_state.get('user')

def logout():
    """Clear session and logout user"""
    import streamlit as st

    st.session_state['user'] = None
    st.session_state['authenticated'] = False
    if 'login_time' in st.session_state:
        del st.session_state['login_time']
    if 'last_activity' in st.session_state:
        del st.session_state['last_activity']

    # Clear cookie
    cookie_manager = get_cookie_manager()
    if cookie_manager is not None:
        cookie_manager.delete('multiaceros_session')

def require_auth():
    """Decorator/function to require authentication"""
    import streamlit as st
    if not is_authenticated():
        st.warning("⚠️ Debes iniciar sesión para acceder a esta página")
        st.stop()
