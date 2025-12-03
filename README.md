# 📦 Sistema de Recepción de Paquetes

Sistema completo de gestión de paquetes con notificaciones automáticas por email y asistente virtual inteligente.

## ✨ Características

- ✅ **Registro de paquetes** con código único generado automáticamente
- ✉️ **Notificaciones automáticas** por email usando Microsoft Graph
- 🔍 **Búsqueda inteligente** de usuarios en Azure AD/Microsoft 365
- 📧 **Soporte para grupos de distribución** (enviar a equipos completos)
- 🤖 **Chatbot inteligente** con IA para consultas en lenguaje natural
- 📊 **Historial y dashboard** con estadísticas en tiempo real
- 💾 **Base de datos SQLite** para almacenamiento persistente
- 📱 **Interfaz responsive** optimizada para recepción

---

## 🏗️ Arquitectura

```
paquetes_agent/
├── backend/              # FastAPI (API REST)
│   ├── main.py          # Endpoints principales
│   ├── paquetes.db      # Base de datos SQLite
│   └── .env             # Configuración (NO subir a Git)
├── frontend/            # Streamlit (UI)
│   ├── app.py           # Interfaz principal
│   ├── chatbot_helper.py # Chatbot con reglas + IA
│   └── .streamlit/
│       └── config.toml  # Configuración UI
├── .venv/               # Entorno virtual Python
├── requirements.txt     # Dependencias
├── start_servers.bat    # Inicio local (desarrollo)
├── start_servers_lan.bat # Inicio en red local (producción)
└── configurar_firewall.bat # Configurar Windows Firewall
```

---

## 🚀 Inicio Rápido

### 1. Clonar o Descargar el Proyecto
```bash
git clone <repo-url>
cd paquetes_agent
```

### 2. Instalar Python 3.11+
Descarga desde [python.org](https://www.python.org/downloads/)

### 3. Crear Entorno Virtual e Instalar Dependencias
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Copia el archivo de ejemplo y edita con tus credenciales:
```bash
copy backend\.env.example backend\.env
```

Edita `backend/.env`:
```env
# Azure AD / Microsoft Graph
AZURE_TENANT_ID=tu-tenant-id
AZURE_CLIENT_ID=tu-client-id
AZURE_CLIENT_SECRET=tu-client-secret
SHARED_MAILBOX_EMAIL=recepcion@tuempresa.cl

# Groq API (para chatbot con IA)
GROQ_API_KEY=tu-groq-api-key
```

### 5. Configurar Azure AD (Primera vez)

Sigue las guías detalladas:
- [CONFIGURAR_AZURE.md](CONFIGURAR_AZURE.md) - Configuración inicial
- [CONFIGURAR_BUSQUEDA_USUARIOS.md](CONFIGURAR_BUSQUEDA_USUARIOS.md) - Búsqueda de usuarios
- [AGREGAR_GRUPOS_DISTRIBUCION.md](AGREGAR_GRUPOS_DISTRIBUCION.md) - Grupos de distribución

**Permisos necesarios en Azure:**
- ✅ `Mail.Send` (Application)
- ✅ `Mail.ReadWrite` (Application)
- ✅ `User.Read.All` (Application)
- ✅ `Group.Read.All` (Application)

**Todos con Admin Consent otorgado** ✅

### 6. Ejecutar la Aplicación

**Desarrollo (solo en tu PC):**
```bash
start_servers.bat
```
Abre: http://localhost:8501

**Producción (red local):**
```bash
configurar_firewall.bat  # Solo la primera vez, como Administrador
start_servers_lan.bat
```
Comparte la URL que aparece con la recepcionista

---

## 📚 Documentación Completa

- [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md) - Opciones de despliegue (LAN, nube, Azure)
- [INSTRUCCIONES_RECEPCIONISTA.md](INSTRUCCIONES_RECEPCIONISTA.md) - Manual de uso para recepción
- [CONFIGURAR_AZURE.md](CONFIGURAR_AZURE.md) - Configuración de Azure AD
- [CONFIGURAR_BUSQUEDA_USUARIOS.md](CONFIGURAR_BUSQUEDA_USUARIOS.md) - Búsqueda de usuarios
- [AGREGAR_GRUPOS_DISTRIBUCION.md](AGREGAR_GRUPOS_DISTRIBUCION.md) - Grupos de distribución

---

## 🎯 Casos de Uso

### 1. Registrar un Paquete
1. Selecciona sucursal, proveedor y tipo de documento
2. Busca al destinatario escribiendo su nombre
3. Selecciona de la lista (autocompletado)
4. Agrega observaciones opcionales
5. Registra → Email automático enviado ✉️

### 2. Consultar Paquetes (Chatbot)
```
¿Qué paquetes tiene Victor?
Cheques registrados hoy
Dame info del PK-251203-ABC
Generar dashboard
```

### 3. Enviar Recordatorios
```
Enviar recordatorio a Victor
Avisar a vracchumi@multiaceros.cl
```

### 4. Ver Historial
- Pestaña "📈 Historial de Registros del Día"
- Muestra solo paquetes de hoy
- Expandir cada registro para detalles

---

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLite** - Base de datos ligera y sin servidor
- **Microsoft Graph API** - Envío de emails y búsqueda de usuarios
- **Python 3.11+**

### Frontend
- **Streamlit** - Framework para interfaces web interactivas
- **Requests** - Cliente HTTP
- **Groq API** - IA para chatbot (modelo Llama)

### Integraciones
- **Azure AD / Microsoft Entra ID** - Autenticación y directorio
- **Microsoft Graph** - Email, usuarios y grupos
- **Groq** - Procesamiento de lenguaje natural

---

## 📊 Estructura de Base de Datos

**Tabla: `paquetes`**
```sql
- codigo_retiro (TEXT PRIMARY KEY)
- sucursal (TEXT)
- proveedor (TEXT)
- tipo_documento (TEXT)
- numero_documento (TEXT)
- destinatario_nombre (TEXT)
- destinatario_email (TEXT)
- observaciones (TEXT)
- fecha_recepcion (TIMESTAMP)
- hora_recepcion (TIME)
```

---

## 🔐 Seguridad

### Variables de Entorno
**NUNCA** subir `.env` a Git o repositorios públicos

### Client Secret
- Rotación cada 6-12 meses recomendada
- Almacenar de forma segura (1Password, Azure Key Vault)

### Permisos
- Usar **Application permissions** (no Delegated)
- Otorgar solo permisos necesarios
- Admin Consent requerido

### Red Local
- Firewall configurado correctamente
- Acceso solo desde red corporativa

---

## 🆘 Solución de Problemas

### Error: "Insufficient privileges"
**Causa:** Falta Admin Consent en Azure
**Solución:** Azure Portal > API Permissions > Grant admin consent

### Error: "Connection refused"
**Causa:** Backend no está corriendo o firewall bloqueando
**Solución:**
1. Ejecuta `start_servers_lan.bat`
2. Ejecuta `configurar_firewall.bat` como Administrador

### No aparecen usuarios al buscar
**Causa:** Permiso `User.Read.All` no configurado
**Solución:** Ver [CONFIGURAR_BUSQUEDA_USUARIOS.md](CONFIGURAR_BUSQUEDA_USUARIOS.md)

### Email no se envía
**Causa:** Credenciales incorrectas o permisos faltantes
**Solución:**
1. Verifica `.env` con credenciales correctas
2. Confirma permisos `Mail.Send` y `Mail.ReadWrite` con Admin Consent
3. Revisa logs del backend

---

## 📈 Próximas Mejoras

- [ ] Escaneo de códigos QR/barras
- [ ] Exportar reportes a Excel/PDF
- [ ] Panel de administración
- [ ] Notificaciones SMS (Twilio)
- [ ] OCR para extracción de datos de etiquetas
- [ ] Integración con SharePoint/Dataverse
- [ ] Autenticación de usuarios
- [ ] Modo offline con sincronización

---

## 👥 Soporte

**Para problemas técnicos:**
- Revisa la sección [Solución de Problemas](#-solución-de-problemas)
- Consulta la documentación en la carpeta del proyecto
- Contacta a TI/Soporte de tu empresa

**Para la recepcionista:**
- Lee [INSTRUCCIONES_RECEPCIONISTA.md](INSTRUCCIONES_RECEPCIONISTA.md)
- Usa el chatbot para consultas rápidas
- Pregunta ejemplos de comandos al asistente virtual

---

## 📝 Licencia

Proyecto interno de uso corporativo.

---

## 🎉 Créditos

Desarrollado para Multiaceros - Sistema de Recepción de Paquetes

**Stack:** Python + FastAPI + Streamlit + Microsoft Graph + Groq AI

---

**¿Listo para empezar? Ejecuta `start_servers_lan.bat` y comparte la URL con recepción** 🚀
