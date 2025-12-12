import os
import sys
import streamlit as st

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import is_authenticated, get_current_user, logout

st.set_page_config(page_title="Recepción de Paquetes", page_icon="📦", layout="wide")

# Check authentication
if not is_authenticated():
    st.warning("⚠️ Debes iniciar sesión para acceder al sistema")
    st.info("Redirigiendo a la página de login...")
    st.switch_page("app.py")
    st.stop()

# Get current user
current_user = get_current_user()

# Simple success page
st.title("🎉 ¡Autenticación Exitosa!")
st.success(f"Bienvenido, {current_user.get('name')}!")

st.markdown("---")

st.markdown(f"""
### Información del usuario:
- **Nombre:** {current_user.get('name', 'N/A')}
- **Email:** {current_user.get('email', 'N/A')}
""")

st.markdown("---")

if st.button("🚪 Cerrar Sesión", use_container_width=True):
    logout()
    st.switch_page("login.py")

st.markdown("---")
st.info("✅ La autenticación con Microsoft está funcionando correctamente!")
st.markdown("""
**Próximo paso:** Ahora que la autenticación funciona, puedes:
1. Instalar las dependencias faltantes (`groq`)
2. Reemplazar este archivo con la aplicación completa (`app_original.py`)
""")
