# Configuración de Autenticación con Microsoft SSO

Este documento explica cómo configurar la autenticación de Microsoft para el Sistema de Recepción de Paquetes.

## Requisitos Previos

- Una cuenta de Azure AD (Microsoft 365)
- Permisos de administrador para registrar aplicaciones en Azure AD

## Pasos de Configuración

### 1. Registrar la Aplicación en Azure AD

1. Ve a [Azure Portal](https://portal.azure.com)
2. Navega a **Azure Active Directory** > **App registrations** > **New registration**
3. Configura la aplicación:
   - **Name**: Sistema de Recepción de Paquetes
   - **Supported account types**: Accounts in this organizational directory only (Single tenant)
   - **Redirect URI**:
     - Type: **Web**
     - URL para desarrollo: `http://localhost:8501`
     - URL para producción: `https://your-app.railway.app` (reemplazar con tu URL de Railway)

### 2. Configurar Permisos de API

1. En la aplicación registrada, ve a **API permissions**
2. Click en **Add a permission**
3. Selecciona **Microsoft Graph** > **Delegated permissions**
4. Agrega los siguientes permisos:
   - `User.Read` - Para leer la información del usuario que inicia sesión
5. Click en **Grant admin consent** para aprobar los permisos

### 3. Crear Client Secret

1. Ve a **Certificates & secrets**
2. Click en **New client secret**
3. Dale un nombre descriptivo (ej: "Producción")
4. Selecciona una expiración (recomendado: 24 meses)
5. **IMPORTANTE**: Copia el valor del secret inmediatamente, no podrás verlo después

### 4. Obtener las Credenciales

En la página **Overview** de tu aplicación, encontrarás:
- **Application (client) ID**: Este es tu `CLIENT_ID`
- **Directory (tenant) ID**: Este es tu `TENANT_ID`

### 5. Configurar Variables de Entorno

Actualiza tu archivo `.env` con las credenciales:

```env
TENANT_ID=tu-tenant-id-aqui
CLIENT_ID=tu-client-id-aqui
CLIENT_SECRET=tu-client-secret-aqui
REDIRECT_URI=http://localhost:8501  # Para desarrollo
# REDIRECT_URI=https://your-app.railway.app  # Para producción
```

### 6. Configurar Redirect URIs Adicionales (Opcional)

Si quieres usar la app tanto en desarrollo como en producción:

1. Ve a **Authentication** en tu app de Azure AD
2. En **Redirect URIs**, agrega ambas URLs:
   - `http://localhost:8501`
   - `https://your-app.railway.app`

## Flujo de Autenticación

1. **Usuario accede a la app** → Redirigido a `/login.py`
2. **Click en "Iniciar sesión con Microsoft"** → Redirigido a Microsoft Login
3. **Usuario ingresa credenciales de Microsoft** → Microsoft valida
4. **Microsoft redirige de vuelta** → Con código de autorización
5. **App intercambia código por token** → Obtiene access token
6. **App obtiene info del usuario** → Desde Microsoft Graph
7. **Usuario autenticado** → Acceso a la aplicación

## Seguridad

- **Client Secret**: Nunca expongas el client secret en el código fuente
- **HTTPS en Producción**: Siempre usa HTTPS en producción
- **Tokens**: Los tokens se almacenan en `st.session_state` (solo en memoria)
- **Logout**: Al cerrar sesión, se limpian todos los datos de sesión

## Troubleshooting

### Error: "AADSTS50011: The redirect URI specified in the request does not match"
**Solución**: Verifica que el `REDIRECT_URI` en tu `.env` coincida exactamente con el configurado en Azure AD.

### Error: "Application is not configured as a multi-tenant application"
**Solución**: En Azure AD, ve a **Authentication** y verifica que "Supported account types" esté configurado correctamente.

### Error: "Invalid client secret"
**Solución**: El client secret expiró o es incorrecto. Genera uno nuevo en Azure AD.

### Usuario no puede iniciar sesión
**Solución**: Verifica que el usuario pertenezca al tenant correcto (organización de Microsoft 365).

## Testing Local

Para probar localmente:

1. Asegúrate de que las variables de entorno estén configuradas
2. Ejecuta el backend: `cd backend && uvicorn main:app --reload`
3. Ejecuta el frontend: `cd frontend && streamlit run login.py`
4. Abre `http://localhost:8501` en tu navegador
5. Intenta iniciar sesión con una cuenta de tu organización

## Deployment en Railway

1. Configura las variables de entorno en Railway:
   - `TENANT_ID`
   - `CLIENT_ID`
   - `CLIENT_SECRET`
   - `REDIRECT_URI` (con tu URL de Railway)
2. Actualiza el Redirect URI en Azure AD con la URL de Railway
3. Deploy de la aplicación

## Notas Importantes

- La autenticación es **obligatoria** para acceder a todas las páginas excepto login
- Los usuarios deben pertenecer a tu organización de Microsoft 365
- El token de acceso expira después de 1 hora (se maneja automáticamente)
- Al cerrar el navegador, la sesión se pierde (comportamiento esperado de Streamlit)
