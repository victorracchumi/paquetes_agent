import os
import requests
import streamlit as st
from datetime import datetime, timedelta
import random
import string
from chatbot_helper import chatbot_inteligente
import locale

# Configurar locale para español
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')
        except:
            pass  # Si falla, usar el locale por defecto

# Función para obtener la hora de Chile
def get_chile_time():
    """
    Retorna la hora actual de Chile (UTC-3 o UTC-4 dependiendo de horario de verano)
    Chile usa horario de verano desde el primer domingo de septiembre hasta el primer domingo de abril
    """
    from datetime import timezone
    utc_now = datetime.now(timezone.utc)

    # Determinar si estamos en horario de verano (CLT) o normal (CLST)
    # Aproximación simple: Sep-Marzo = UTC-3, Abr-Ago = UTC-4
    month = utc_now.month
    if month >= 9 or month <= 3:  # Septiembre a Marzo
        offset = timedelta(hours=-3)  # Horario de verano (CLST)
    else:  # Abril a Agosto
        offset = timedelta(hours=-4)  # Horario normal (CLT)

    chile_time = utc_now + offset
    return chile_time.replace(tzinfo=None)  # Remover timezone info para compatibilidad

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Función para cargar paquetes del backend
def cargar_paquetes_desde_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/packages", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('packages', [])
    except:
        pass
    return []

# Inicializar session_state
if 'historial' not in st.session_state:
    # Cargar datos del Excel al iniciar
    st.session_state['historial'] = cargar_paquetes_desde_backend()
if 'ultimo_registro' not in st.session_state:
    st.session_state['ultimo_registro'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'datos_cargados' not in st.session_state:
    st.session_state['datos_cargados'] = True

st.set_page_config(page_title="Recepción de Paquetes", page_icon="📦", layout="wide")

# CSS Personalizado Profesional - Tema Oscuro Mejorado
st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Variables CSS */
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

    /* Fondo oscuro elegante */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Contenedor principal mejorado */
    .main .block-container {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        border: 1px solid var(--border-color);
        margin-top: 1rem;
        max-width: 1400px;
        backdrop-filter: blur(10px);
    }

    /* Títulos mejorados */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
        letter-spacing: -0.5px;
    }

    h2 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3, h4 {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
    }

    /* Labels y textos mejorados */
    label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stMarkdown p {
        color: var(--text-secondary) !important;
        line-height: 1.6;
    }

    /* Tabs modernos */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        color: var(--text-muted) !important;
        border: none !important;
        transition: all 0.3s ease;
        position: relative;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        color: var(--text-secondary) !important;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.15) !important;
        color: var(--primary-color) !important;
        box-shadow: none !important;
    }

    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-color);
        border-radius: 3px 3px 0 0;
    }

    /* Botones modernos sin bordes */
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
        text-transform: none !important;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Inputs modernos y limpios */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1.5px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        padding: 0.85rem 1rem !important;
        transition: all 0.3s ease;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.6;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        background: rgba(15, 23, 42, 0.7) !important;
        outline: none !important;
    }

    /* Eliminar todos los bordes blancos */
    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"],
    .stDateInput > div > div,
    input, select, textarea {
        border: none !important;
        outline: none !important;
    }

    /* Selectbox específico */
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1.5px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
    }

    .stSelectbox [data-baseweb="select"] > div:hover,
    .stSelectbox [data-baseweb="select"] > div:focus {
        border-color: var(--primary-color) !important;
    }

    /* Alerts sin bordes blancos */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        border-left: 4px solid !important;
        padding: 1rem 1.25rem !important;
        backdrop-filter: blur(10px);
    }

    /* Info boxes */
    .stInfo {
        background: rgba(99, 102, 241, 0.15) !important;
        border-left-color: var(--primary-color) !important;
        color: var(--text-secondary) !important;
    }

    .stInfo > div {
        border: none !important;
    }

    /* Success boxes */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border-left-color: #22c55e !important;
        color: var(--text-secondary) !important;
    }

    .stSuccess > div {
        border: none !important;
    }

    /* Error boxes */
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border-left-color: #ef4444 !important;
        color: var(--text-secondary) !important;
    }

    .stError > div {
        border: none !important;
    }

    /* Warning boxes */
    .stWarning {
        background: rgba(251, 191, 36, 0.15) !important;
        border-left-color: #fbbf24 !important;
        color: var(--text-secondary) !important;
    }

    .stWarning > div {
        border: none !important;
    }

    /* Alertas y cajas de éxito dentro del sidebar - fondo oscuro */
    [data-testid="stSidebar"] .stAlert,
    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stWarning,
    [data-testid="stSidebar"] .stError,
    [data-testid="stSidebar"] .stInfo {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }

    /* Sidebar moderno */
    [data-testid="stSidebar"] {
        background: var(--bg-dark);
        border-right: 1px solid var(--border-color);
        padding: 1.5rem 1rem;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
    }

    /* Métricas mejoradas */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--primary-color) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Divisores elegantes */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 2rem 0;
    }

    /* Expander moderno */
    .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.05) !important;
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 10px !important;
        font-weight: 600;
        color: var(--text-secondary) !important;
        padding: 1rem !important;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        border-color: rgba(99, 102, 241, 0.3);
    }

    /* Contenido del expander con fondo oscuro */
    .streamlit-expanderContent,
    [data-testid="stExpander"] > div:last-child,
    [data-testid="stExpanderDetails"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-top: none;
        border-radius: 0 0 10px 10px !important;
        padding: 1.5rem !important;
        color: var(--text-secondary) !important;
    }

    /* Asegurar que todo el contenido dentro del expander sea oscuro */
    .streamlit-expanderContent > div,
    [data-testid="stExpander"] > div:last-child > div,
    [data-testid="stExpanderDetails"] > div {
        background: transparent !important;
    }

    /* Forzar fondo oscuro en todos los elementos del expander */
    [data-testid="stExpander"] {
        background: transparent !important;
    }

    /* Columnas dentro de expanders también deben ser oscuras */
    [data-testid="stExpander"] [data-testid="column"],
    [data-testid="stExpander"] [data-testid="stVerticalBlock"],
    [data-testid="stExpander"] [data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }

    /* Éxito/Info boxes dentro de expanders */
    [data-testid="stExpander"] .stAlert {
        background: rgba(99, 102, 241, 0.1) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
    }

    /* Animación de carga */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent !important;
    }

    /* Chat messages modernos */
    .stChatMessage {
        background: rgba(99, 102, 241, 0.05);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        background: rgba(99, 102, 241, 0.08);
        border-color: rgba(99, 102, 241, 0.2);
    }

    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Header mejorado con logo
st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='font-size: 3rem; margin: 0;'>📦 Sistema de Recepción de Paquetes</h1>
        <p style='color: #4299e1; font-size: 1.2rem; font-weight: 500;'>Multiaceros S.A. - Gestión Inteligente</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar con información y estadísticas
with st.sidebar:
    st.header("📊 Panel de Control")

    st.markdown("---")

    # Filtrar paquetes del día actual
    from collections import Counter
    hoy = get_chile_time().strftime("%Y-%m-%d")
    paquetes_hoy = [
        p for p in st.session_state['historial']
        if (p.get('FechaRecepcion') or p.get('fechaRecepcion', '')).startswith(hoy)
    ]

    # Métricas principales
    pendientes_hoy = [p for p in paquetes_hoy if (p.get('Estado') or p.get('estado', 'Pendiente')) != "Retirado"]
    retirados_hoy = [p for p in paquetes_hoy if (p.get('Estado') or p.get('estado', 'Pendiente')) == "Retirado"]

    col_met1, col_met2, col_met3 = st.columns(3)
    with col_met1:
        st.metric("📦 Total Hoy", len(paquetes_hoy))
    with col_met2:
        st.metric("⏳ Pendientes", len(pendientes_hoy), delta=None, delta_color="off")
    with col_met3:
        st.metric("✅ Retirados", len(retirados_hoy), delta=None, delta_color="normal")

    # Búsqueda rápida global
    st.markdown("---")
    st.markdown("### 🔍 Búsqueda Rápida")
    busqueda_global = st.text_input(
        "Buscar paquete",
        placeholder="Código, destinatario o documento...",
        key="busqueda_global_sidebar",
        label_visibility="collapsed"
    )

    if busqueda_global and len(busqueda_global) >= 2:
        busqueda_lower = busqueda_global.lower()
        resultados = []

        for p in st.session_state['historial']:
            codigo = (p.get('CodigoRetiro') or p.get('codigoRetiro', '')).lower()
            destinatario = (p.get('DestinatarioNombre') or p.get('destinatarioNombre', '')).lower()
            numero_doc = (p.get('NumeroDocumento') or p.get('numeroDocumento', '')).lower()

            if (busqueda_lower in codigo or
                busqueda_lower in destinatario or
                busqueda_lower in numero_doc):
                resultados.append(p)

        if resultados:
            st.success(f"✅ {len(resultados)} resultado(s)")
            for r in resultados[:3]:  # Mostrar máximo 3
                codigo = r.get('CodigoRetiro') or r.get('codigoRetiro', 'N/A')
                dest = r.get('DestinatarioNombre') or r.get('destinatarioNombre', 'N/A')
                estado = r.get('Estado') or r.get('estado', 'Pendiente')
                emoji = "✅" if estado == "Retirado" else "📦"
                st.caption(f"{emoji} **{codigo}**\n{dest[:25]}...")
            if len(resultados) > 3:
                st.caption(f"_+{len(resultados)-3} más_")
        else:
            st.warning("No se encontraron resultados")

    # Alertas automáticas
    st.markdown("---")
    st.markdown("### ⚠️ Alertas")

    # Calcular paquetes urgentes (más de 3 días sin retirar)
    from datetime import datetime, timedelta
    hoy_dt = get_chile_time()
    hace_3_dias = (hoy_dt - timedelta(days=3)).strftime("%Y-%m-%d")

    paquetes_urgentes = []
    paquetes_ayer = []

    for p in st.session_state['historial']:
        estado = p.get('Estado') or p.get('estado', 'Pendiente')
        fecha_rec = p.get('FechaRecepcion') or p.get('fechaRecepcion', '')

        if estado != "Retirado":
            if fecha_rec < hace_3_dias:
                paquetes_urgentes.append(p)
            elif fecha_rec.startswith((hoy_dt - timedelta(days=1)).strftime("%Y-%m-%d")):
                paquetes_ayer.append(p)

    # Mostrar alertas
    if paquetes_urgentes:
        st.error(f"🚨 **{len(paquetes_urgentes)}** paquete(s) urgente(s)")
        st.caption("Sin retirar hace más de 3 días")
        for p in paquetes_urgentes[:2]:
            dest = (p.get('DestinatarioNombre') or p.get('destinatarioNombre', 'N/A'))[:20]
            st.caption(f"• {dest}...")

    if paquetes_ayer:
        st.warning(f"⏰ **{len(paquetes_ayer)}** de ayer sin retirar")

    if not paquetes_urgentes and not paquetes_ayer and pendientes_hoy == 0:
        st.success("✅ Sin alertas")
    elif not paquetes_urgentes and not paquetes_ayer:
        st.info("📋 Todo al día")

    if paquetes_hoy:
        st.markdown("---")

        # Estadísticas por tipo de documento
        st.markdown("**📄 Por Tipo:**")
        tipos = [p.get('TipoDocumento') or p.get('tipoDocumento', 'Otro') for p in paquetes_hoy]
        tipo_contador = Counter(tipos)

        for tipo, count in tipo_contador.most_common(3):  # Top 3 tipos
            porcentaje = (count / len(paquetes_hoy)) * 100
            st.markdown(f"• **{tipo}**: {count} ({porcentaje:.0f}%)")

        st.markdown("---")

        # Estadísticas por sucursal
        st.markdown("**📍 Por Sucursal:**")
        sucursales = [p.get('Sucursal') or p.get('sucursal', 'N/A') for p in paquetes_hoy]
        sucursal_contador = Counter(sucursales)

        for sucursal, count in sucursal_contador.most_common(3):  # Top 3 sucursales
            porcentaje = (count / len(paquetes_hoy)) * 100
            st.markdown(f"• **{sucursal}**: {count} ({porcentaje:.0f}%)")

        st.markdown("---")

        # Última recepción
        ultimo = paquetes_hoy[-1]
        hora_ultima = ultimo.get('HoraRecepcion') or ultimo.get('horaRecepcion', 'N/A')
        dest_ultimo = ultimo.get('DestinatarioNombre') or ultimo.get('destinatarioNombre', 'N/A')

        # Calcular tiempo desde última recepción
        try:
            from datetime import datetime, timedelta
            hora_actual = get_chile_time()
            hora_recepcion = datetime.strptime(f"{hoy} {hora_ultima}", "%Y-%m-%d %H:%M:%S")
            diferencia = hora_actual - hora_recepcion
            minutos = int(diferencia.total_seconds() / 60)

            if minutos < 60:
                tiempo_texto = f"Hace {minutos} min"
            else:
                horas = minutos // 60
                tiempo_texto = f"Hace {horas}h {minutos % 60}min"
        except:
            tiempo_texto = hora_ultima

        st.markdown(f"**⏰ Última recepción:**")
        st.markdown(f"{tiempo_texto}")
        st.caption(f"👤 {dest_ultimo[:20]}{'...' if len(dest_ultimo) > 20 else ''}")

    else:
        st.markdown("---")
        st.caption("📭 No hay paquetes registrados hoy")
        st.caption("Registra el primer paquete del día en la pestaña **📝 Nuevo Registro**")

# Tabs para mejor organización
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Nuevo Registro", "🔍 Consultar", "📈 Historial", "📊 Reportes", "💬 Chatbot IA"])

with tab1:
    # Buscador de usuarios FUERA del formulario
    st.markdown("### 🔍 Buscar Destinatario")

    col_search, col_clear = st.columns([4, 1])
    with col_search:
        busqueda_usuario = st.text_input(
            "Buscar por nombre o email",
            placeholder="Ej: Victor, Cobranzas, varriagada@multiaceros.cl",
            key="busqueda_usuario_pre",
            help="Busca usuarios y grupos en tu organización de Microsoft 365",
            label_visibility="collapsed"
        )

    # Si hay texto de búsqueda, realizar la consulta
    if busqueda_usuario and len(busqueda_usuario) >= 2:
        # Detectar si el texto de búsqueda cambió → limpiar autocompletado anterior y buscar
        if st.session_state.get('busqueda_anterior') != busqueda_usuario:
            st.session_state['nombre_autocompletado'] = ""
            st.session_state['email_autocompletado'] = ""
            st.session_state['busqueda_anterior'] = busqueda_usuario
            st.session_state['necesita_buscar'] = True  # Marcar que necesita buscar

        # Solo buscar si es necesario (no después de seleccionar usuario)
        if st.session_state.get('necesita_buscar', True):
            with st.spinner("🔍 Buscando..."):
                try:
                    response = requests.get(
                        f"{BACKEND_URL}/search-users",
                        params={"query": busqueda_usuario},
                        timeout=4  # Balance entre velocidad y confiabilidad
                    )
                    if response.status_code == 200:
                        data = response.json()
                        usuarios_encontrados = data.get("users", [])

                        # Guardar en session_state para que esté disponible en callback
                        st.session_state['usuarios_busqueda'] = usuarios_encontrados

                        if not usuarios_encontrados:
                            st.session_state['usuarios_busqueda'] = []
                    else:
                        st.error(f"❌ Error al buscar usuarios: {response.status_code}")
                        st.session_state['usuarios_busqueda'] = []
                except Exception as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
                    st.session_state['usuarios_busqueda'] = []

            # Marcar que ya se buscó
            st.session_state['necesita_buscar'] = False
    else:
        # Si no hay búsqueda, limpiar resultados
        st.session_state['usuarios_busqueda'] = []
        st.session_state['busqueda_anterior'] = ""
        st.session_state['necesita_buscar'] = True

    # Mostrar resultados y permitir selección
    usuarios_encontrados = st.session_state.get('usuarios_busqueda', [])
    if usuarios_encontrados:
        # Crear opciones para el selectbox
        opciones_display = ["-- Seleccionar usuario --"] + [f"{u['displayName']} ({u['email']})" for u in usuarios_encontrados]

        # Callback para autocompletar
        def autocompletar_campos():
            sel_idx = st.session_state.get('user_select_dropdown_idx', 0)
            usuarios = st.session_state.get('usuarios_busqueda', [])
            if sel_idx > 0 and usuarios:
                selected = usuarios[sel_idx - 1]
                st.session_state['nombre_autocompletado'] = selected['displayName']
                st.session_state['email_autocompletado'] = selected['email']

        # Selectbox con índices
        seleccion_idx = st.selectbox(
            "Selecciona un usuario para autocompletar",
            range(len(opciones_display)),
            format_func=lambda x: opciones_display[x],
            key="user_select_dropdown_idx",
            on_change=autocompletar_campos
        )

    st.divider()

    # ACTUALIZAR valores de autocompletado ANTES del formulario
    # Esto asegura que los campos se llenen cuando se selecciona un usuario
    if st.session_state.get('nombre_autocompletado'):
        st.session_state['destinatario_nombre_input'] = st.session_state['nombre_autocompletado']
    if st.session_state.get('email_autocompletado'):
        st.session_state['destinatario_email_input'] = st.session_state['email_autocompletado']

    with st.form("form_paquete", clear_on_submit=False):
        # Sección de Información General
        st.markdown("### 🏢 Información General")
        col1, col2, col3 = st.columns(3)
        with col1:
            sucursal = st.selectbox("Sucursal", ["Santiago"], index=0)
        with col2:
            recepcionista = st.text_input("Recepcionista", value="Recepción", placeholder="Nombre del recepcionista")
        with col3:
            proveedor = st.text_input("Proveedor", value="Transporte X", placeholder="Nombre del proveedor")

        st.divider()

        # Sección de Documento
        st.markdown("### 📄 Información del Documento")
        col1, col2 = st.columns(2)
        with col1:
            tipoDocumento = st.selectbox("Tipo de documento", ["Guía", "Factura", "Cheque", "OT", "Otro"], index=0)
        with col2:
            numeroDocumento = st.text_input("Número de documento/seguimiento", placeholder="Ej: GU-123456")

        # Campos adicionales para Cheque (siempre visibles)
        st.markdown("#### 💰 Información del Cheque (solo si es cheque)")
        col1, col2 = st.columns(2)
        with col1:
            montoCheque = st.text_input("Monto del Cheque (opcional)", placeholder="Ej: $500.000", key="monto_cheque", help="Solo completar si el tipo de documento es Cheque")
        with col2:
            fechaVencimientoCheque = st.date_input("Fecha de Vencimiento (opcional)", key="fecha_venc_cheque", help="Solo completar si el tipo de documento es Cheque")
            fechaVencimientoCheque = fechaVencimientoCheque.strftime("%Y-%m-%d") if fechaVencimientoCheque else ""

        st.divider()

        # Sección de Destinatario
        st.markdown("### 👤 Información del Destinatario")

        col1, col2 = st.columns(2)
        with col1:
            destinatarioNombre = st.text_input(
                "Nombre del Destinatario",
                placeholder="Nombre completo o grupo",
                key="destinatario_nombre_input"
            )
            destinatarioEmail = st.text_input(
                "Email del Destinatario",
                placeholder="usuario@ejemplo.com",
                key="destinatario_email_input"
            )
        with col2:
            medioNotificacion = st.selectbox("Medio de notificación", ["Correo", "Teams", "Ambos"], index=0)

        st.divider()

        # Sección de Detalles Adicionales
        st.markdown("### 📝 Detalles Adicionales")
        col1, col2 = st.columns([2, 1])
        with col1:
            observaciones = st.text_area("Observaciones (opcional)", placeholder="Ingrese cualquier información adicional...", height=100)
        with col2:
            adjuntoUrl = st.text_input("URL del adjunto (opcional)", placeholder="https://...")
            st.caption("🔗 Link a foto o documento")

        st.divider()

        # Botón de envío principal
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("✅ Registrar y Notificar", use_container_width=True, type="primary")

if submitted:
    required = [sucursal, recepcionista, proveedor, tipoDocumento, numeroDocumento, destinatarioNombre, destinatarioEmail]
    if any(not x for x in required):
        st.error("⚠️ Complete todos los campos obligatorios.")
        st.stop()

    # Generar código de retiro automáticamente
    now = get_chile_time()
    y = str(now.year)[-2:]
    m = f"{now.month:02d}"
    d = f"{now.day:02d}"
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    codigoRetiro = f"PK-{y}{m}{d}-{rand}"

    payload = {
        "sucursal": sucursal,
        "recepcionista": recepcionista,
        "proveedor": proveedor,
        "tipoDocumento": tipoDocumento,
        "numeroDocumento": numeroDocumento,
        "destinatarioNombre": destinatarioNombre,
        "destinatarioEmail": destinatarioEmail,
        "medioNotificacion": medioNotificacion,
        "observaciones": observaciones,
        "adjuntoUrl": adjuntoUrl,
        "codigoRetiro": codigoRetiro,
        "fechaRecepcion": get_chile_time().strftime("%Y-%m-%d"),
        "horaRecepcion": get_chile_time().strftime("%H:%M:%S"),
        "montoCheque": montoCheque,
        "fechaVencimientoCheque": fechaVencimientoCheque,
    }

    with st.spinner('⏳ Procesando registro...'):
        try:
            r = requests.post(f"{BACKEND_URL}/register", json=payload, timeout=30)
            if r.status_code == 200:
                data = r.json()

                # Recargar paquetes desde el backend
                st.session_state['historial'] = cargar_paquetes_desde_backend()
                st.session_state['ultimo_registro'] = data

                # Mostrar mensaje de éxito
                st.success(f"✅ Paquete registrado exitosamente con código: **{codigoRetiro}**")

                # Mostrar resumen del paquete registrado
                st.markdown("---")
                st.markdown("### 📦 Paquete Registrado")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🎫 Código:** `{codigoRetiro}`")
                    st.markdown(f"**👤 Destinatario:** {destinatarioNombre}")
                    st.markdown(f"**📧 Email:** {destinatarioEmail}")
                    st.markdown(f"**📍 Sucursal:** {sucursal}")
                with col2:
                    st.markdown(f"**📄 Tipo Doc:** {tipoDocumento}")
                    st.markdown(f"**🔢 Nº Doc:** {numeroDocumento}")
                    st.markdown(f"**🔔 Notificación:** {medioNotificacion}")
                    st.markdown(f"**⏰ Registrado:** {get_chile_time().strftime('%H:%M:%S')}")

                st.info("💡 Ve a la pestaña **📈 Historial** para ver todos los paquetes del día y marcar como retirado cuando corresponda.")
            else:
                st.error(f"❌ Error del backend: {r.status_code} — {r.text}")
        except Exception as e:
            st.error(f"❌ No se pudo conectar al backend: {e}")

with tab2:
    st.subheader("🔍 Consultar Paquete")

    buscar_codigo = st.text_input("Ingrese el código de retiro", placeholder="PK-251128-XXXX")

    if st.button("🔎 Buscar", type="primary"):
        if buscar_codigo:
            # Buscar en el historial local primero
            codigo_normalizado = buscar_codigo.strip().upper()
            paquete_encontrado = None

            for pkg in st.session_state['historial']:
                codigo_pkg = pkg.get('CodigoRetiro') or pkg.get('codigoRetiro', '')
                if codigo_pkg.upper() == codigo_normalizado:
                    paquete_encontrado = pkg
                    break

            if paquete_encontrado:
                # Mostrar información del paquete en tarjeta
                st.markdown("### ✅ Paquete Encontrado")
                st.markdown("---")

                # Información principal
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📦 Información del Paquete")
                    st.markdown(f"**🔖 Código:** {paquete_encontrado.get('CodigoRetiro') or paquete_encontrado.get('codigoRetiro', 'N/A')}")
                    st.markdown(f"**📅 Fecha Recepción:** {paquete_encontrado.get('FechaRecepcion') or paquete_encontrado.get('fechaRecepcion', 'N/A')}")
                    st.markdown(f"**🕐 Hora:** {paquete_encontrado.get('HoraRecepcion') or paquete_encontrado.get('horaRecepcion', 'N/A')}")
                    st.markdown(f"**📍 Sucursal:** {paquete_encontrado.get('Sucursal') or paquete_encontrado.get('sucursal', 'N/A')}")
                    st.markdown(f"**👤 Recepcionista:** {paquete_encontrado.get('Recepcionista') or paquete_encontrado.get('recepcionista', 'N/A')}")

                with col2:
                    st.markdown("### 👥 Información del Destinatario")
                    nombre_dest = paquete_encontrado.get('DestinatarioNombre') or paquete_encontrado.get('destinatarioNombre', 'N/A')
                    email_dest = paquete_encontrado.get('DestinatarioEmail') or paquete_encontrado.get('destinatarioEmail', 'N/A')
                    st.markdown(f"**👤 Nombre:** {nombre_dest}")
                    st.markdown(f"**📧 Email:** {email_dest}")
                    st.markdown(f"**🔔 Notificación:** {paquete_encontrado.get('MedioNotificacion') or paquete_encontrado.get('medioNotificacion', 'N/A')}")

                st.markdown("---")

                # Información del documento
                st.markdown("### 📄 Información del Documento")
                col3, col4 = st.columns(2)

                with col3:
                    st.markdown(f"**📋 Tipo:** {paquete_encontrado.get('TipoDocumento') or paquete_encontrado.get('tipoDocumento', 'N/A')}")
                    st.markdown(f"**🔢 Número:** {paquete_encontrado.get('NumeroDocumento') or paquete_encontrado.get('numeroDocumento', 'N/A')}")
                    st.markdown(f"**🚚 Proveedor:** {paquete_encontrado.get('Proveedor') or paquete_encontrado.get('proveedor', 'N/A')}")

                with col4:
                    # Información específica de cheques
                    tipo_doc = paquete_encontrado.get('TipoDocumento') or paquete_encontrado.get('tipoDocumento', '')
                    if tipo_doc.lower() == 'cheque':
                        monto = paquete_encontrado.get('MontoCheque') or paquete_encontrado.get('montoCheque', '')
                        fecha_venc = paquete_encontrado.get('FechaVencimientoCheque') or paquete_encontrado.get('fechaVencimientoCheque', '')
                        if monto:
                            st.markdown(f"**💵 Monto:** {monto}")
                        if fecha_venc:
                            st.markdown(f"**📆 Vencimiento:** {fecha_venc}")

                # Observaciones
                obs = paquete_encontrado.get('Observaciones') or paquete_encontrado.get('observaciones', '')
                if obs:
                    st.markdown("### 📝 Observaciones")
                    st.markdown(f"> {obs}")

                st.markdown("---")

                # Acciones disponibles
                st.markdown("### ⚡ Acciones")
                col5, col6, col7 = st.columns(3)

                with col5:
                    if st.button("📧 Enviar Recordatorio", use_container_width=True):
                        try:
                            r = requests.post(
                                f"{BACKEND_URL}/send-reminder",
                                json={"email": email_dest, "nombre": nombre_dest},
                                timeout=30
                            )
                            if r.status_code == 200:
                                data = r.json()
                                if data.get("success"):
                                    st.markdown(f"✅ **Recordatorio enviado a {email_dest}**")
                                else:
                                    st.error(f"❌ {data.get('message', 'Error desconocido')}")
                            else:
                                st.error(f"❌ Error: {r.status_code}")
                        except Exception as e:
                            st.error(f"❌ Error al enviar: {e}")

                with col6:
                    # Copiar código al portapapeles (simulado con texto seleccionable)
                    if st.button("📋 Copiar Código", use_container_width=True):
                        st.code(codigo_normalizado, language=None)
                        st.caption("💡 Selecciona el código y copia con Ctrl+C")

                with col7:
                    # Ver imagen adjunta (si existe)
                    imagen_path = paquete_encontrado.get('ImagenPath') or paquete_encontrado.get('imagenPath', '')
                    if imagen_path:
                        if st.button("🖼️ Ver Imagen", use_container_width=True):
                            try:
                                from PIL import Image
                                img = Image.open(imagen_path)
                                st.image(img, caption="Imagen del paquete", use_container_width=True)
                            except Exception as e:
                                st.error(f"❌ No se pudo cargar la imagen: {e}")
                    else:
                        st.button("🖼️ Sin Imagen", use_container_width=True, disabled=True)

            else:
                st.error(f"❌ No se encontró el paquete con código: **{codigo_normalizado}**")
                st.caption("💡 Verifica el código (formato: PK-YYMMDD-XXXX) o consulta el historial")
        else:
            st.error("⚠️ Ingrese un código de retiro")

with tab3:
    st.subheader("📈 Historial de Registros")

    # Buscador de paquetes
    col_buscar, col_filtro = st.columns([3, 1])
    with col_buscar:
        busqueda_historial = st.text_input(
            "🔍 Buscar paquete",
            placeholder="Código, destinatario, documento...",
            key="busqueda_historial",
            help="Busca en todo el historial, no solo del día"
        )
    with col_filtro:
        filtro_dia = st.selectbox(
            "Mostrar",
            ["Solo hoy", "Últimos 7 días", "Últimos 30 días", "Todos"],
            key="filtro_historial"
        )

    # Aplicar filtros
    from datetime import datetime, timedelta
    hoy = get_chile_time().strftime("%Y-%m-%d")

    # Filtrar por fecha según selección
    if filtro_dia == "Solo hoy":
        registros_filtrados = [
            r for r in st.session_state['historial']
            if (r.get('FechaRecepcion') or r.get('fechaRecepcion', '')).startswith(hoy)
        ]
    elif filtro_dia == "Últimos 7 días":
        hace_7_dias = (get_chile_time() - timedelta(days=7)).strftime("%Y-%m-%d")
        registros_filtrados = [
            r for r in st.session_state['historial']
            if (r.get('FechaRecepcion') or r.get('fechaRecepcion', '')) >= hace_7_dias
        ]
    elif filtro_dia == "Últimos 30 días":
        hace_30_dias = (get_chile_time() - timedelta(days=30)).strftime("%Y-%m-%d")
        registros_filtrados = [
            r for r in st.session_state['historial']
            if (r.get('FechaRecepcion') or r.get('fechaRecepcion', '')) >= hace_30_dias
        ]
    else:  # Todos
        registros_filtrados = st.session_state['historial']

    # Aplicar búsqueda si hay texto
    if busqueda_historial and len(busqueda_historial) >= 2:
        busqueda_lower = busqueda_historial.lower()
        registros_hoy = []
        for r in registros_filtrados:
            codigo = (r.get('CodigoRetiro') or r.get('codigoRetiro', '')).lower()
            destinatario = (r.get('DestinatarioNombre') or r.get('destinatarioNombre', '')).lower()
            numero_doc = (r.get('NumeroDocumento') or r.get('numeroDocumento', '')).lower()

            if (busqueda_lower in codigo or
                busqueda_lower in destinatario or
                busqueda_lower in numero_doc):
                registros_hoy.append(r)
    else:
        registros_hoy = registros_filtrados

    if registros_hoy:
        # Mensaje dinámico según filtros
        if busqueda_historial:
            st.metric("📦 Resultados de búsqueda", len(registros_hoy))
        elif filtro_dia == "Solo hoy":
            st.metric("📦 Registros de Hoy", len(registros_hoy))
        else:
            st.metric(f"📦 Registros ({filtro_dia})", len(registros_hoy))

        for i, registro in enumerate(reversed(registros_hoy), 1):
            # Obtener valores con compatibilidad de nombres (Excel vs Frontend)
            codigo = registro.get('CodigoRetiro') or registro.get('codigoRetiro', 'N/A')
            destinatario = registro.get('DestinatarioNombre') or registro.get('destinatarioNombre', 'N/A')
            sucursal = registro.get('Sucursal') or registro.get('sucursal', 'N/A')
            email = registro.get('DestinatarioEmail') or registro.get('destinatarioEmail', 'N/A')
            tipo_doc = registro.get('TipoDocumento') or registro.get('tipoDocumento', 'N/A')
            numero_doc = registro.get('NumeroDocumento') or registro.get('numeroDocumento', 'N/A')
            proveedor = registro.get('Proveedor') or registro.get('proveedor', 'N/A')
            fecha = registro.get('FechaRecepcion') or registro.get('fechaRecepcion', 'N/A')
            hora = registro.get('HoraRecepcion') or registro.get('horaRecepcion', 'N/A')
            notif = registro.get('MedioNotificacion') or registro.get('medioNotificacion', 'N/A')
            obs = registro.get('Observaciones') or registro.get('observaciones', '')

            # Obtener estado del paquete
            estado = registro.get('Estado') or registro.get('estado', 'Pendiente')
            fecha_retiro = registro.get('FechaRetiro') or registro.get('fechaRetiro', '')
            entregado_a = registro.get('EntregadoA') or registro.get('entregadoA', '')

            # Color del expander según estado
            estado_emoji = "✅" if estado == "Retirado" else "📦"
            titulo_expander = f"{estado_emoji} #{len(registros_hoy) - i + 1} - {codigo} | {destinatario}"
            if estado == "Retirado":
                titulo_expander += f" (RETIRADO)"

            with st.expander(titulo_expander, expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**📍 Sucursal:** {sucursal}")
                    st.markdown(f"**👤 Destinatario:** {destinatario}")
                    st.markdown(f"**📧 Email:** {email}")
                with col2:
                    st.markdown(f"**📄 Tipo Doc:** {tipo_doc}")
                    st.markdown(f"**🔢 Nº Doc:** {numero_doc}")
                    st.markdown(f"**🚚 Proveedor:** {proveedor}")
                with col3:
                    st.markdown(f"**📅 Fecha:** {fecha}")
                    st.markdown(f"**🕐 Hora:** {hora}")
                    st.markdown(f"**🔔 Notif:** {notif}")

                if obs:
                    st.markdown(f"**📝 Observaciones:** {obs}")

                # Sección de retiro
                st.markdown("---")
                if estado == "Retirado":
                    st.success(f"✅ **Paquete Retirado**")
                    st.markdown(f"**📅 Fecha de Retiro:** {fecha_retiro}")
                    st.markdown(f"**👤 Retirado por:** {entregado_a}")
                else:
                    st.info("📦 **Paquete Pendiente de Retiro**")

                    # Formulario para marcar como retirado
                    with st.form(key=f"form_retiro_{codigo}"):
                        nombre_retira = st.text_input(
                            "Nombre de quien retira",
                            placeholder="Ej: Juan Pérez",
                            key=f"nombre_retira_{codigo}"
                        )

                        col_btn1, col_btn2 = st.columns([1, 1])
                        with col_btn1:
                            submit_retiro = st.form_submit_button(
                                "✅ Marcar como Retirado",
                                type="primary",
                                use_container_width=True
                            )

                        if submit_retiro:
                            if nombre_retira and len(nombre_retira.strip()) > 0:
                                try:
                                    # Llamar al endpoint de retiro
                                    response = requests.post(
                                        f"{BACKEND_URL}/withdraw",
                                        json={
                                            "codigo_retiro": codigo,
                                            "entregado_a": nombre_retira.strip()
                                        },
                                        timeout=5
                                    )

                                    if response.status_code == 200:
                                        result = response.json()
                                        if result.get('success'):
                                            st.success(f"✅ {result.get('message')}")
                                            # Recargar datos
                                            st.session_state['historial'] = cargar_paquetes_desde_backend()
                                            st.rerun()
                                        else:
                                            st.warning(f"⚠️ {result.get('message')}")
                                    else:
                                        st.error(f"❌ Error: {response.status_code}")
                                except Exception as e:
                                    st.error(f"❌ Error al marcar como retirado: {e}")
                            else:
                                st.error("⚠️ Ingrese el nombre de quien retira el paquete")

    else:
        st.markdown("📭 No hay registros del día de hoy")
        if st.session_state['historial']:
            st.caption(f"💡 Hay {len(st.session_state['historial'])} registros de días anteriores")

with tab4:
    st.subheader("📊 Dashboard de Reportes y Estadísticas")

    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime, timedelta
    from collections import Counter
    from io import BytesIO

    # Crear DataFrame de todos los paquetes
    if st.session_state['historial']:
        df = pd.DataFrame(st.session_state['historial'])

        # Normalizar nombres de columnas (compatibilidad frontend/backend)
        if 'FechaRecepcion' in df.columns and 'fechaRecepcion' not in df.columns:
            df['fechaRecepcion'] = df['FechaRecepcion']
        if 'fechaRecepcion' in df.columns and 'FechaRecepcion' not in df.columns:
            df['FechaRecepcion'] = df['fechaRecepcion']

        # Convertir fechas
        df['fecha'] = pd.to_datetime(df['fechaRecepcion'] if 'fechaRecepcion' in df.columns else df['FechaRecepcion'], errors='coerce')
        df['estado'] = df.get('Estado', df.get('estado', 'Pendiente'))
        df['sucursal'] = df.get('Sucursal', df.get('sucursal', 'N/A'))
        df['tipoDoc'] = df.get('TipoDocumento', df.get('tipoDocumento', 'N/A'))

        # Filtros
        st.markdown("### 🔍 Filtros")
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            fecha_desde = st.date_input("Desde", value=datetime.now() - timedelta(days=30))
        with col_f2:
            fecha_hasta = st.date_input("Hasta", value=datetime.now())
        with col_f3:
            sucursal_filtro = st.multiselect("Sucursal", options=df['sucursal'].unique().tolist(), default=df['sucursal'].unique().tolist())

        # Aplicar filtros
        df_filtrado = df[
            (df['fecha'] >= pd.Timestamp(fecha_desde)) &
            (df['fecha'] <= pd.Timestamp(fecha_hasta)) &
            (df['sucursal'].isin(sucursal_filtro))
        ]

        st.markdown("---")

        # Métricas principales
        st.markdown("### 📈 Métricas Clave")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        total_paquetes = len(df_filtrado)
        pendientes = len(df_filtrado[df_filtrado['estado'] != 'Retirado'])
        retirados = len(df_filtrado[df_filtrado['estado'] == 'Retirado'])
        tasa_retiro = (retirados / total_paquetes * 100) if total_paquetes > 0 else 0

        with col_m1:
            st.metric("📦 Total Paquetes", total_paquetes)
        with col_m2:
            st.metric("⏳ Pendientes", pendientes)
        with col_m3:
            st.metric("✅ Retirados", retirados)
        with col_m4:
            st.metric("📊 Tasa de Retiro", f"{tasa_retiro:.1f}%")

        st.markdown("---")

        # Gráficos
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("#### 📅 Paquetes por Día")
            # Agrupar por fecha
            paquetes_por_dia = df_filtrado.groupby(df_filtrado['fecha'].dt.date).size().reset_index()
            paquetes_por_dia.columns = ['Fecha', 'Cantidad']

            fig_linea = px.line(paquetes_por_dia, x='Fecha', y='Cantidad',
                               markers=True,
                               title="")
            fig_linea.update_traces(line_color='#6366f1', marker=dict(size=8))
            fig_linea.update_layout(
                plot_bgcolor='rgba(15, 23, 42, 0.8)',
                paper_bgcolor='rgba(15, 23, 42, 0.8)',
                font_color='#cbd5e1',
                xaxis=dict(gridcolor='rgba(99, 102, 241, 0.1)'),
                yaxis=dict(gridcolor='rgba(99, 102, 241, 0.1)')
            )
            st.plotly_chart(fig_linea, use_container_width=True)

        with col_g2:
            st.markdown("#### 📍 Por Sucursal")
            sucursal_counts = df_filtrado['sucursal'].value_counts().reset_index()
            sucursal_counts.columns = ['Sucursal', 'Cantidad']

            fig_pie = px.pie(sucursal_counts, values='Cantidad', names='Sucursal',
                            title="",
                            color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_pie.update_layout(
                plot_bgcolor='rgba(15, 23, 42, 0.8)',
                paper_bgcolor='rgba(15, 23, 42, 0.8)',
                font_color='#cbd5e1'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Segunda fila de gráficos
        col_g3, col_g4 = st.columns(2)

        with col_g3:
            st.markdown("#### 📄 Por Tipo de Documento")
            tipo_counts = df_filtrado['tipoDoc'].value_counts().reset_index()
            tipo_counts.columns = ['Tipo', 'Cantidad']

            fig_bar = px.bar(tipo_counts, x='Tipo', y='Cantidad',
                           title="",
                           color='Cantidad',
                           color_continuous_scale='Blues')
            fig_bar.update_layout(
                plot_bgcolor='rgba(15, 23, 42, 0.8)',
                paper_bgcolor='rgba(15, 23, 42, 0.8)',
                font_color='#cbd5e1',
                xaxis=dict(gridcolor='rgba(99, 102, 241, 0.1)'),
                yaxis=dict(gridcolor='rgba(99, 102, 241, 0.1)'),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_g4:
            st.markdown("#### 📊 Estado de Paquetes")
            estado_counts = df_filtrado['estado'].value_counts().reset_index()
            estado_counts.columns = ['Estado', 'Cantidad']

            fig_donut = px.pie(estado_counts, values='Cantidad', names='Estado',
                              title="",
                              hole=0.4,
                              color_discrete_map={'Pendiente': '#fbbf24', 'Notificado': '#60a5fa', 'Retirado': '#34d399'})
            fig_donut.update_layout(
                plot_bgcolor='rgba(15, 23, 42, 0.8)',
                paper_bgcolor='rgba(15, 23, 42, 0.8)',
                font_color='#cbd5e1'
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown("---")

        # Top 5s
        col_t1, col_t2 = st.columns(2)

        with col_t1:
            st.markdown("#### 🏆 Top 5 Destinatarios")
            destinatarios = df_filtrado.get('DestinatarioNombre', df_filtrado.get('destinatarioNombre', pd.Series(dtype=str)))
            if not destinatarios.empty:
                top_dest = destinatarios.value_counts().head(5)
                for i, (nombre, count) in enumerate(top_dest.items(), 1):
                    st.markdown(f"{i}. **{nombre}**: {count} paquetes")

        with col_t2:
            st.markdown("#### 📦 Top 5 Proveedores")
            proveedores = df_filtrado.get('Proveedor', df_filtrado.get('proveedor', pd.Series(dtype=str)))
            if not proveedores.empty:
                top_prov = proveedores.value_counts().head(5)
                for i, (nombre, count) in enumerate(top_prov.items(), 1):
                    st.markdown(f"{i}. **{nombre}**: {count} paquetes")

        st.markdown("---")

        # Exportar a Excel
        st.markdown("### 📥 Exportar Datos")

        col_e1, col_e2 = st.columns([3, 1])
        with col_e1:
            st.markdown("Descarga todos los paquetes filtrados en formato Excel")
        with col_e2:
            # Preparar datos para exportar
            df_export = df_filtrado[[c for c in df_filtrado.columns if c not in ['fecha', 'estado', 'sucursal', 'tipoDoc']]].copy()

            # Crear Excel en memoria
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_export.to_excel(writer, index=False, sheet_name='Paquetes')
            output.seek(0)

            st.download_button(
                label="📥 Descargar Excel",
                data=output.getvalue(),
                file_name=f"paquetes_{fecha_desde}_{fecha_hasta}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    else:
        st.info("📭 No hay datos para mostrar. Registra algunos paquetes primero.")

with tab5:
    st.subheader("💬 Asistente Virtual Inteligente")

    # Generar preguntas sugeridas dinámicas basadas en los datos del día
    def generar_preguntas_dinamicas(historial):
        """Genera preguntas sugeridas basadas en los datos actuales del sistema"""
        from datetime import datetime
        from collections import Counter

        preguntas = []
        hoy = get_chile_time().strftime("%Y-%m-%d")

        # Filtrar paquetes de hoy
        paquetes_hoy = [p for p in historial if (p.get('FechaRecepcion') or p.get('fechaRecepcion', '')).startswith(hoy)]

        if not historial:
            return [
                "¿Cómo funciona el sistema?",
                "¿Qué puedo hacer aquí?",
                "Ayuda con el chatbot",
                "¿Cómo registro un paquete?",
                "¿Cómo consulto paquetes?",
                "Generar dashboard"
            ]

        # 1. Pregunta sobre paquetes de hoy
        if paquetes_hoy:
            dia_actual = get_chile_time().day
            mes_actual = get_chile_time().strftime("%B").lower()
            meses_es = {
                'january': 'enero', 'february': 'febrero', 'march': 'marzo',
                'april': 'abril', 'may': 'mayo', 'june': 'junio',
                'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
                'october': 'octubre', 'november': 'noviembre', 'december': 'diciembre'
            }
            mes_es = meses_es.get(mes_actual, mes_actual)
            preguntas.append(f"¿Qué se registró hoy {dia_actual} de {mes_es}?")
        else:
            preguntas.append("¿Cuántos paquetes hay registrados?")

        # 2. Tipo de documento más común de hoy
        if paquetes_hoy:
            tipos = [p.get('TipoDocumento') or p.get('tipoDocumento', '') for p in paquetes_hoy]
            tipo_mas_comun = Counter(tipos).most_common(1)[0][0] if tipos else None
            if tipo_mas_comun and tipo_mas_comun.lower() != 'paquete':
                preguntas.append(f"¿Cuántos {tipo_mas_comun.lower()}s hay hoy?")
            else:
                preguntas.append("¿Cuántos cheques hay registrados?")
        else:
            preguntas.append("¿Hay cheques registrados?")

        # 3. Sucursal con más actividad de hoy
        if paquetes_hoy:
            sucursales = [p.get('Sucursal') or p.get('sucursal', '') for p in paquetes_hoy]
            sucursal_top = Counter(sucursales).most_common(1)[0][0] if sucursales else None
            if sucursal_top:
                preguntas.append(f"Paquetes en {sucursal_top}")
            else:
                preguntas.append("Listar paquetes por sucursal")
        else:
            preguntas.append("Listar paquetes por sucursal")

        # 4. Destinatario más frecuente de hoy (si hay al menos 2 del mismo)
        if paquetes_hoy:
            destinatarios = [p.get('DestinatarioNombre') or p.get('destinatarioNombre', '') for p in paquetes_hoy]
            dest_contador = Counter(destinatarios)
            dest_top = dest_contador.most_common(1)[0] if dest_contador else (None, 0)
            if dest_top[1] >= 2:  # Si tiene 2 o más paquetes
                nombre_corto = dest_top[0].split()[0] if dest_top[0] else ""
                preguntas.append(f"Paquetes de {nombre_corto}")
            else:
                preguntas.append("Generar dashboard")
        else:
            preguntas.append("Generar dashboard")

        # 5. Última consulta útil
        if len(historial) > 5:
            preguntas.append("Últimos 5 paquetes registrados")
        else:
            preguntas.append("Mostrar todos los paquetes")

        # 6. Siempre útil - enviar recordatorio al último destinatario
        if paquetes_hoy:
            ultimo_dest = paquetes_hoy[-1].get('DestinatarioNombre') or paquetes_hoy[-1].get('destinatarioNombre', '')
            if ultimo_dest:
                nombre_corto = ultimo_dest.split()[0]
                preguntas.append(f"Enviar recordatorio a {nombre_corto}")
            else:
                preguntas.append("Listar destinatarios")
        else:
            preguntas.append("Ver historial completo")

        # Limitar a 6 preguntas
        return preguntas[:6]

    preguntas_dinamicas = generar_preguntas_dinamicas(st.session_state['historial'])

    # Sección de preguntas sugeridas dinámicas
    st.markdown("### 💡 Preguntas sugeridas:")
    cols = st.columns(3)

    pregunta_desde_boton = None
    for i, pregunta_sugerida in enumerate(preguntas_dinamicas):
        with cols[i % 3]:
            if st.button(pregunta_sugerida, key=f"sugerencia_{i}", use_container_width=True):
                pregunta_desde_boton = pregunta_sugerida

    st.divider()

    # Input del usuario
    pregunta_input = st.text_input(
        "🔍 Tu pregunta:",
        placeholder="Ej: ¿Cuántos paquetes tengo? ¿Dónde está PK-251128-ABCD?",
        key="chat_input"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        enviar = st.button("📤 Enviar Pregunta", type="primary", use_container_width=True)

    # Procesar pregunta desde botón o input
    pregunta_a_procesar = pregunta_desde_boton or (pregunta_input if enviar else None)

    if pregunta_a_procesar:
        with st.spinner("🤔 Pensando..."):
            try:
                # Usar chatbot inteligente
                respuesta, tipo = chatbot_inteligente(pregunta_a_procesar, st.session_state['historial'])

                # Guardar en historial de chat
                st.session_state['chat_history'].append({
                    'timestamp': get_chile_time().strftime("%H:%M:%S"),
                    'pregunta': pregunta_a_procesar,
                    'respuesta': respuesta,
                    'tipo': tipo
                })

                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Mostrar historial de conversación
    if st.session_state['chat_history']:
        st.divider()
        st.markdown("### 📝 Conversación")

        # Botón para limpiar chat
        if st.button("🗑️ Limpiar conversación"):
            st.session_state['chat_history'] = []
            st.rerun()

        # Mostrar las conversaciones más recientes primero
        for i, chat in enumerate(reversed(st.session_state['chat_history'][-10:])):
            with st.expander(f"💬 {chat['pregunta'][:60]}{'...' if len(chat['pregunta']) > 60 else ''} — {chat['timestamp']}",
                           expanded=(i == 0)):

                # Pregunta del usuario
                st.markdown(f"**👤 Tu pregunta:**")
                st.markdown(f"> {chat['pregunta']}")

                # Respuesta del bot
                st.markdown(f"**🤖 Respuesta:** {chat['tipo']}")
                st.markdown(chat['respuesta'])

        if len(st.session_state['chat_history']) > 10:
            st.caption(f"_(Mostrando las últimas 10 de {len(st.session_state['chat_history'])} conversaciones)_")

    # Información adicional
    st.divider()
    with st.expander("ℹ️ ¿Cómo funciona el chatbot?"):
        st.markdown("""
        Este asistente virtual usa **dos niveles de inteligencia**:

        1. **🎯 Reglas rápidas**: Para consultas simples como buscar códigos o contar paquetes
           - Respuesta instantánea
           - 100% precisa

        2. **🤖 IA de Groq**: Para preguntas complejas o conversacionales
           - Usa el modelo Llama 3.1 (70B parámetros)
           - Completamente gratis
           - Entiende lenguaje natural

        **Ejemplos de preguntas:**
        - "¿Cuántos paquetes hay en Santiago?"
        - "Muéstrame el paquete más reciente"
        - "Busca el código PK-251128-ABCD"
        - "¿Hay paquetes para María?"
        - "Listar todos los registros"
        """)

# Footer
st.divider()
st.caption("💡 Sistema de Recepción de Paquetes - VictoIA")
