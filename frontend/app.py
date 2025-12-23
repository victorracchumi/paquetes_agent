"""
Login page with Microsoft SSO
"""
import streamlit as st
import os
from datetime import datetime
from auth import get_auth_url, get_token_from_code, get_user_info, is_authenticated

st.set_page_config(page_title="Login - Recepción de Paquetes", page_icon="🔐", layout="centered")

# CSS for login page
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        box-shadow: 0 25px 80px rgba(0,0,0,0.25);
        max-width: 480px;
        margin-top: 2rem;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    h1, h2, h3 {
        color: #2d3748 !important;
        font-family: 'Poppins', sans-serif !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
        width: 100% !important;
        text-transform: none !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
    }

    .stMarkdown p {
        color: #4a5568;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Check if already authenticated
if is_authenticated():
    st.success("✅ Ya has iniciado sesión")
    if st.button("Ir a la aplicación"):
        st.switch_page("pages/Dashboard.py")
    st.stop()

# Login page content
st.markdown("""
    <div style='text-align: center; padding: 0 0 1.5rem 0;'>
        <div style='margin-bottom: 1.5rem;'>
            <h2 style='font-size: 2.5rem; font-weight: 700; color: #2d3748; margin: 0; letter-spacing: -0.5px;'>
                <span style='color: #4a5568;'>MULTI</span><span style='color: #e53e3e;'>ACEROS</span>
            </h2>
            <p style='color: #48bb78; font-size: 0.85rem; font-weight: 600; margin: 0.25rem 0 0 0; letter-spacing: 1px;'>
                FUERTE EN SERVICIO
            </p>
        </div>
        <div style='font-size: 3.5rem; margin-bottom: 0.75rem;'>📦</div>
        <h1 style='font-size: 1.85rem; margin: 0.5rem 0; font-weight: 600; color: #1a202c;'>
            Bienvenido
        </h1>
        <p style='color: #2d3748; font-size: 0.95rem; font-weight: 500; margin-top: 0.5rem;'>
            Sistema de Recepción de Paquetes
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Handle OAuth callback
query_params = st.query_params

if "code" in query_params:
    code = query_params["code"]

    # Clear query params to prevent reuse
    st.query_params.clear()

    with st.spinner("🔄 Autenticando..."):
        try:
            # Exchange code for token
            token_result = get_token_from_code(code)

            if "access_token" in token_result:
                # Get user info
                user_info = get_user_info(token_result["access_token"])

                if user_info:
                    # Save to session with login time
                    user_data = {
                        'name': user_info.get('displayName'),
                        'email': user_info.get('mail') or user_info.get('userPrincipalName'),
                        'access_token': token_result['access_token']
                    }
                    st.session_state['user'] = user_data
                    st.session_state['authenticated'] = True
                    st.session_state['login_time'] = datetime.now()
                    st.session_state['last_activity'] = datetime.now()

                    # Redirect to dashboard immediately
                    st.switch_page("pages/Dashboard.py")
                else:
                    st.error("❌ Error al obtener información del usuario")
            else:
                error_desc = token_result.get("error_description", "Error desconocido")
                st.error(f"❌ Error de autenticación: {error_desc}")

        except Exception as e:
            st.error(f"❌ Error durante el login: {str(e)}")
else:
    # Show login button
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0 2rem 0;'>
            <p style='color: #2d3748; font-size: 0.95rem; line-height: 1.6; font-weight: 400;'>
                Inicia sesión con tu cuenta corporativa de Microsoft<br/>
                para acceder al sistema de gestión de paquetes
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Generate auth URL
    auth_url = get_auth_url()

    st.link_button(
        "Iniciar sesión con Microsoft",
        auth_url,
        use_container_width=True,
        type="primary"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(102, 126, 234, 0.15);'>
            <p style='color: #718096; font-size: 0.8rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;'>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                Autenticación segura mediante Microsoft Azure AD
            </p>
            <p style='color: #a0aec0; font-size: 0.7rem; margin-top: 1rem;'>
                © 2025 Multiaceros S.A. | Versión 1.0.0
            </p>
        </div>
    """, unsafe_allow_html=True)
