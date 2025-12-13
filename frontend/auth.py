"""
Authentication module for Microsoft SSO integration
"""
import os
import msal
import requests
import json
import base64
from typing import Optional, Dict
from datetime import datetime, timedelta

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

def save_session_to_cookie(user_data: Dict):
    """Save session data to browser cookie"""
    import streamlit as st
    from streamlit.components.v1 import html

    session_data = {
        'user': user_data,
        'login_time': datetime.now().isoformat(),
        'authenticated': True
    }

    # Encode session data
    session_json = json.dumps(session_data)
    session_b64 = base64.b64encode(session_json.encode()).decode()

    # Set cookie via JavaScript (expires in 8 hours)
    cookie_script = f"""
        <script>
            const date = new Date();
            date.setTime(date.getTime() + (8 * 60 * 60 * 1000)); // 8 hours
            document.cookie = "multiaceros_session={session_b64}; expires=" + date.toUTCString() + "; path=/; SameSite=Lax";
        </script>
    """
    html(cookie_script, height=0)

def load_session_from_cookie():
    """Load session data from browser cookie"""
    import streamlit as st
    from streamlit.components.v1 import html

    # Get cookie via JavaScript
    cookie_script = """
        <script>
            function getCookie(name) {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
            }
            const session = getCookie('multiaceros_session');
            if (session) {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: session}, '*');
            }
        </script>
    """

    result = html(cookie_script, height=0)

    if result:
        try:
            # Decode session data
            session_json = base64.b64decode(result).decode()
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
    from streamlit.components.v1 import html

    st.session_state['user'] = None
    st.session_state['authenticated'] = False
    if 'login_time' in st.session_state:
        del st.session_state['login_time']
    if 'last_activity' in st.session_state:
        del st.session_state['last_activity']

    # Clear cookie
    clear_cookie_script = """
        <script>
            document.cookie = "multiaceros_session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        </script>
    """
    html(clear_cookie_script, height=0)

def require_auth():
    """Decorator/function to require authentication"""
    import streamlit as st
    if not is_authenticated():
        st.warning("⚠️ Debes iniciar sesión para acceder a esta página")
        st.stop()
