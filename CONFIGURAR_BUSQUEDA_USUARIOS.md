# 🔍 Configurar Búsqueda de Usuarios con Microsoft Graph

Esta guía te ayudará a habilitar la búsqueda de usuarios en tu organización para el autocompletado del campo "Destinatario".

---

## ✨ Nueva Funcionalidad

El sistema ahora incluye un **buscador inteligente** que te permite:
- 🔎 Buscar usuarios escribiendo su nombre o email
- 📋 Ver sugerencias en tiempo real desde Azure AD / Microsoft 365
- ✅ Seleccionar usuarios y autocompletar nombre + email automáticamente
- ⚡ No más errores de tipeo en emails

---

## 🔐 Paso 1: Agregar Permiso en Azure Portal

### 1.1 Acceder a tu App Registration

1. Ve a [Azure Portal](https://portal.azure.com)
2. Busca **"Azure Active Directory"** o **"Microsoft Entra ID"**
3. Haz clic en **"App registrations"**
4. Selecciona tu aplicación: **"Sistema Recepción Paquetes"**

### 1.2 Agregar Permiso User.Read.All

1. En el menú lateral, haz clic en **"API permissions"**
2. Haz clic en **"+ Add a permission"**
3. Selecciona **"Microsoft Graph"**
4. Selecciona **"Application permissions"** (NO Delegated)
5. Busca y marca el permiso:
   ```
   ✅ User.Read.All
   ```
6. Haz clic en **"Add permissions"**

### 1.3 Otorgar Admin Consent

⚠️ **IMPORTANTE**: Sin este paso, la búsqueda no funcionará.

1. Después de agregar el permiso, haz clic en **"Grant admin consent for [Tu Organización]"**
2. Confirma haciendo clic en **"Yes"**
3. Verifica que el permiso muestre un **check verde** ✅ en la columna "Status"

### 1.4 Verificar Permisos Finales

Tu aplicación debe tener estos 3 permisos con Admin Consent:

```
✅ Mail.Send              (Application)  [Granted]
✅ Mail.ReadWrite         (Application)  [Granted]
✅ User.Read.All          (Application)  [Granted]
```

---

## 🧪 Paso 2: Probar la Búsqueda

### 2.1 Reiniciar el Backend

El backend se recargará automáticamente si está en modo `--reload`:

```bash
# Si no está corriendo, reinicia:
cd backend
.venv\Scripts\activate
uvicorn main:app --reload
```

### 2.2 Probar en el Frontend

1. Abre http://localhost:8501
2. Ve a la pestaña **"📝 Registrar Paquete"**
3. Baja hasta **"👤 Información del Destinatario"**
4. En el campo **"🔍 Buscar Usuario en la Organización"**:
   - Escribe algunas letras de tu nombre o apellido
   - Ejemplo: `vic` → debería mostrar "Victor Racchumi"
5. Selecciona el usuario de la lista desplegable
6. Los campos **Nombre** y **Email** se llenarán automáticamente ✨

---

## 🔍 Cómo Funciona

### Backend (FastAPI)
- Nuevo endpoint: `GET /search-users?query=texto`
- Usa Microsoft Graph API: `https://graph.microsoft.com/v1.0/users`
- Busca por `displayName`, `givenName`, `surname`, o `mail`
- Retorna hasta 10 usuarios ordenados alfabéticamente

### Frontend (Streamlit)
- Campo de búsqueda con mínimo 2 caracteres
- Realiza búsqueda automática al escribir
- Muestra resultados en un selectbox
- Autocompleta los campos nombre + email al seleccionar

---

## 🔧 Solución de Problemas

### Error: "Insufficient privileges"
**Causa**: No se otorgó Admin Consent para `User.Read.All`
**Solución**: Ve a Azure Portal > API Permissions > Grant admin consent

### No muestra usuarios al buscar
**Posibles causas**:
1. Verifica que el permiso `User.Read.All` tenga Admin Consent ✅
2. Asegúrate de escribir al menos 2 caracteres
3. Revisa los logs del backend en la terminal
4. Verifica que existan usuarios en tu Azure AD

### Error: "The specified object was not found"
**Causa**: Los usuarios no existen en tu organización
**Solución**: Busca con un nombre/email que exista en Microsoft 365

### Búsqueda muy lenta
**Causa**: Muchos usuarios en la organización
**Solución**: Escribe más caracteres para afinar la búsqueda (ej: "vic" en vez de "v")

---

## 📊 Ejemplo de Uso

### Caso 1: Buscar por nombre
```
1. Escribe: "Victor"
2. Aparece: ✅ Encontrados 1 usuario(s)
3. Selecciona: "Victor Racchumi (vracchumi@multiaceros.cl)"
4. Campos autocompletados:
   - Nombre: Victor Racchumi
   - Email: vracchumi@multiaceros.cl
```

### Caso 2: Buscar por apellido
```
1. Escribe: "Racc"
2. Aparece: ✅ Encontrados 1 usuario(s)
3. Selecciona el usuario
4. Listo ✨
```

### Caso 3: Buscar por email
```
1. Escribe: "vracch"
2. Aparece: ✅ Encontrados 1 usuario(s)
3. Selecciona el usuario
4. Autocompletado ✨
```

---

## 🔒 Seguridad y Privacidad

### ¿Qué información puede ver la app?
Con el permiso `User.Read.All`, la aplicación puede:
- ✅ Leer nombres de usuarios (displayName)
- ✅ Leer direcciones de email corporativas
- ❌ **NO puede** leer contraseñas
- ❌ **NO puede** leer correos del buzón
- ❌ **NO puede** modificar usuarios

### Mejores Prácticas
1. Solo otorga permisos de Application (no Delegated)
2. No compartas el Client Secret públicamente
3. Monitorea el uso de la aplicación en Azure Portal
4. Rota el Client Secret cada 6-12 meses

---

## ✅ Checklist

Antes de usar la búsqueda de usuarios:

- [ ] Permiso `User.Read.All` agregado en Azure
- [ ] Admin Consent otorgado (check verde ✅)
- [ ] Backend reiniciado
- [ ] Frontend reiniciado
- [ ] Prueba exitosa buscando tu propio nombre

---

## 🎯 Ventajas de Esta Funcionalidad

### Antes ❌
- Escribir nombre completo manualmente
- Copiar/pegar emails desde Outlook
- Riesgo de errores de tipeo
- Emails incorrectos = notificaciones perdidas

### Ahora ✅
- Buscar con 2-3 letras
- Seleccionar de una lista
- Autocompletado instantáneo
- Cero errores en emails corporativos

---

**¡Listo! Ahora puedes buscar usuarios de tu organización al registrar paquetes** 🎉
