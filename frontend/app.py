"""
Login page with Microsoft SSO
"""
import streamlit as st
import os
from auth import get_auth_url, get_token_from_code, get_user_info, is_authenticated

st.set_page_config(page_title="Login - Recepción de Paquetes", page_icon="🔐", layout="centered")

# CSS for login page
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary-color: #6366f1;
        --primary-hover: #4f46e5;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --border-color: rgba(148, 163, 184, 0.1);
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Inter', sans-serif;
    }

    .main .block-container {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        border: 1px solid var(--border-color);
        max-width: 500px;
        backdrop-filter: blur(10px);
    }

    h1 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 1rem 0;
        text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
    }

    .stButton > button {
        background: var(--primary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
        width: 100%;
    }

    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
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
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>🔐 Iniciar Sesión</h1>
        <p style='color: #4299e1; font-size: 1.1rem; font-weight: 500;'>Sistema de Recepción de Paquetes</p>
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
                    # Save to session
                    st.session_state['user'] = {
                        'name': user_info.get('displayName'),
                        'email': user_info.get('mail') or user_info.get('userPrincipalName'),
                        'access_token': token_result['access_token']
                    }
                    st.session_state['authenticated'] = True

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
        <div style='text-align: center; padding: 2rem 0;'>
            <p style='color: var(--text-secondary); margin-bottom: 2rem;'>
                Inicia sesión con tu cuenta de Microsoft para acceder al sistema
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Generate auth URL
    auth_url = get_auth_url()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button(
            "🔑 Iniciar sesión con Microsoft",
            auth_url,
            use_container_width=True
        )

    st.divider()

    st.markdown("""
        <div style='text-align: center;'>
            <p style='color: var(--text-muted); font-size: 0.875rem;'>
                🔒 Autenticación segura mediante Microsoft Azure AD
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("💡 Sistema de Recepción de Paquetes - Multiaceros S.A.")
