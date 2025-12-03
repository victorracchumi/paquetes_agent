# 📧 Configuración de Correo Corporativo con Microsoft Graph

Esta guía te ayudará a configurar el envío de correos corporativos usando Microsoft Graph API para que los destinatarios reciban notificaciones cuando lleguen sus paquetes.

---

## 📋 Prerrequisitos

- Cuenta de Microsoft 365 / Azure AD corporativa
- Permisos de administrador en Azure Portal
- Correo corporativo desde donde se enviarán las notificaciones (ej: `recepcion@tuempresa.com`)

---

## 🔧 Paso 1: Crear una App Registration en Azure

### 1.1 Acceder a Azure Portal

1. Ve a [Azure Portal](https://portal.azure.com)
2. Inicia sesión con tu cuenta corporativa

### 1.2 Crear el App Registration

1. En el menú lateral, busca **"Azure Active Directory"** o **"Microsoft Entra ID"**
2. En el menú izquierdo, haz clic en **"App registrations"** (Registros de aplicaciones)
3. Haz clic en **"+ New registration"** (Nuevo registro)
4. Completa el formulario:
   ```
   Name: Sistema Recepción Paquetes
   Supported account types: Accounts in this organizational directory only
   Redirect URI: (déjalo vacío por ahora)
   ```
5. Haz clic en **"Register"**

### 1.3 Guardar el Application (client) ID

1. En la página de **Overview** de tu aplicación, copia el **Application (client) ID**
2. También copia el **Directory (tenant) ID**
3. Guárdalos temporalmente

---

## 🔑 Paso 2: Crear un Client Secret

### 2.1 Generar Secret

1. En el menú lateral de tu aplicación, haz clic en **"Certificates & secrets"**
2. En la pestaña **"Client secrets"**, haz clic en **"+ New client secret"**
3. Agrega una descripción: `Sistema Paquetes Secret`
4. Selecciona la expiración (recomendado: 24 months)
5. Haz clic en **"Add"**
6. **⚠️ IMPORTANTE**: Copia el **Value** del secret INMEDIATAMENTE (solo se muestra una vez)

---

## 🔐 Paso 3: Configurar Permisos (API Permissions)

### 3.1 Agregar Permisos de Microsoft Graph

1. En el menú lateral, haz clic en **"API permissions"**
2. Haz clic en **"+ Add a permission"**
3. Selecciona **"Microsoft Graph"**
4. Selecciona **"Application permissions"** (NO Delegated)
5. Busca y agrega los siguientes permisos:
   ```
   ✅ Mail.Send
   ✅ Mail.ReadWrite
   ```
6. Haz clic en **"Add permissions"**

### 3.2 Grant Admin Consent

1. Después de agregar los permisos, haz clic en el botón **"Grant admin consent for [Tu Organización]"**
2. Confirma haciendo clic en **"Yes"**
3. Verifica que los permisos muestren un check verde ✅

---

## 📮 Paso 4: Configurar la Cuenta de Envío

### 4.1 Crear Buzón Compartido (Recomendado)

Opción 1: Buzón compartido (gratis, recomendado)
1. Ve a [Microsoft 365 Admin Center](https://admin.microsoft.com)
2. Ve a **Teams & groups** > **Shared mailboxes**
3. Haz clic en **"+ Add a shared mailbox"**
4. Nombre: `Recepción de Paquetes`
5. Email: `recepcion@tuempresa.com`
6. Asigna permisos a los usuarios que necesiten acceso

Opción 2: Usar cuenta de usuario existente
- Simplemente usa el email de un usuario existente

### 4.2 Obtener el UPN (User Principal Name)

El UPN es el email de la cuenta que enviará los correos:
```
recepcion@tuempresa.com
```

---

## ⚙️ Paso 5: Configurar el Backend

### 5.1 Actualizar el archivo .env

Edita el archivo `.env` en la raíz del proyecto:

```env
# ==== Microsoft Graph (Application permissions) ====
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_SECRET=tu_secret_value_aqui

# The mailbox that will send the notifications
GRAPH_SENDER_UPN=recepcion@tuempresa.com

# ==== Excel & Storage ====
EXCEL_PATH=./data/recepcion_paquetes.xlsx

# ==== Backend URL ====
BACKEND_URL=http://localhost:8000
```

Reemplaza:
- `TENANT_ID`: con tu Directory (tenant) ID
- `CLIENT_ID`: con tu Application (client) ID
- `CLIENT_SECRET`: con el valor del secret que copiaste
- `GRAPH_SENDER_UPN`: con el email desde donde se enviarán notificaciones

### 5.2 Verificar que el Backend esté configurado

El archivo `backend/main.py` ya tiene el código configurado para usar Microsoft Graph.

---

## 🧪 Paso 6: Probar el Envío de Correos

### 6.1 Reiniciar los Servicios

```bash
# Terminal 1 - Backend
cd backend
.venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
.venv\Scripts\activate
streamlit run app.py
```

### 6.2 Registrar un Paquete de Prueba

1. Abre http://localhost:8501
2. Genera un código de retiro
3. Completa el formulario con:
   - Tu email corporativo real en "Email del Destinatario"
   - Selecciona "Correo" en Medio de notificación
4. Haz clic en "Registrar y Notificar"

### 6.3 Verificar

1. Revisa tu bandeja de entrada corporativa
2. Deberías recibir un email de `recepcion@tuempresa.com`
3. Si no llega, revisa:
   - Carpeta de Spam/Junk
   - Logs del backend en la terminal
   - Que los permisos tengan Admin Consent

---

## 🔍 Solución de Problemas

### Error: "Insufficient privileges"
**Causa**: No se otorgó Admin Consent
**Solución**: Ve a Azure Portal > API Permissions > Grant admin consent

### Error: "The specified object was not found"
**Causa**: El UPN (email) es incorrecto
**Solución**: Verifica que `GRAPH_SENDER_UPN` sea exactamente el email correcto

### Error: "AADSTS7000215: Invalid client secret"
**Causa**: El secret expiró o está mal copiado
**Solución**: Crea un nuevo secret en Azure Portal

### No llega el correo
**Posibles causas**:
1. Verifica que el email esté en la misma organización
2. Revisa la carpeta de spam
3. Verifica los logs del backend
4. Asegúrate que el buzón compartido exista

### Logs del Backend

Revisa la terminal donde corre el backend para ver errores:
```
INFO:     127.0.0.1:xxxxx - "POST /register HTTP/1.1" 200 OK
```

Si ves un error 500, revisa los detalles en la terminal.

---

## 📊 Configuración Opcional: Teams

Si quieres notificar también por Teams:

### 1. Crear Webhook en Teams

1. Ve al canal de Teams donde quieres las notificaciones
2. Haz clic en **"..."** > **Connectors** > **Incoming Webhook**
3. Dale un nombre: "Notificaciones Paquetes"
4. Copia la URL del webhook

### 2. Agregar a .env

```env
TEAMS_WEBHOOK_URL=https://tu-organizacion.webhook.office.com/webhookb2/...
```

---

## ✅ Checklist Final

Antes de ir a producción, verifica:

- [ ] App Registration creada en Azure
- [ ] Client Secret generado y guardado
- [ ] Permisos Mail.Send y Mail.ReadWrite agregados
- [ ] Admin Consent otorgado (check verde ✅)
- [ ] Buzón compartido creado o cuenta de usuario lista
- [ ] Archivo .env configurado con todos los valores
- [ ] Prueba exitosa enviando correo a ti mismo
- [ ] Backend y Frontend corriendo sin errores

---

## 🔒 Seguridad

### Mejores Prácticas

1. **Nunca** subas el archivo `.env` a Git
2. El `.env` ya está en `.gitignore`
3. Rota el Client Secret cada 6-12 meses
4. Usa un buzón compartido en lugar de cuenta personal
5. Monitorea los envíos para detectar uso inusual

### Archivo .env.example

Ya existe un archivo `.env.example` con placeholders. Los demás desarrolladores deben:
1. Copiar `.env.example` a `.env`
2. Solicitar los valores reales al administrador
3. Nunca compartir los valores reales públicamente

---

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs del backend
2. Verifica que todos los valores en `.env` sean correctos
3. Confirma que el Admin Consent esté otorgado
4. Prueba con un email dentro de tu organización primero

---

**¡Listo! Tu sistema ahora puede enviar correos corporativos automáticamente cuando lleguen paquetes** 🎉
