# ☁️ Despliegue en la Nube - Guía Completa

Sistema 100% independiente que funciona sin tu computadora encendida.

---

## 🎯 Opción Recomendada: Railway (Backend) + Streamlit Cloud (Frontend)

**Por qué esta combinación:**
- ✅ **Completamente gratis** (tier gratuito de ambos)
- ✅ **Súper fácil** de configurar (15-20 minutos)
- ✅ **HTTPS automático** incluido
- ✅ **Acceso desde cualquier lugar** (casa, oficina, celular)
- ✅ **100% independiente** de tu PC
- ✅ **Actualización automática** cuando modificas el código

---

## 📦 Preparación Inicial (5 minutos)

### 1. Crear Cuenta en GitHub
Si no tienes, crea una cuenta gratuita en [github.com](https://github.com)

### 2. Subir tu Proyecto a GitHub

**Importante:** NUNCA subir el archivo `.env` con tus credenciales.

#### Crear .gitignore (protege tus credenciales):
```bash
# Ejecuta en la carpeta del proyecto
echo .env > .gitignore
echo .venv/ >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo .DS_Store >> .gitignore
echo backend/paquetes.db >> .gitignore
```

#### Subir a GitHub:
```bash
# Inicializar Git (si no lo has hecho)
git init
git add .
git commit -m "Sistema de recepción de paquetes"

# Crear repositorio en GitHub (hazlo desde github.com)
# Luego conecta tu repositorio local:
git remote add origin https://github.com/TU-USUARIO/paquetes_agent.git
git branch -M main
git push -u origin main
```

---

## 🚂 PARTE 1: Desplegar Backend en Railway (10 minutos)

### Paso 1: Crear Cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Click en **"Login"** > **"Login with GitHub"**
3. Autoriza Railway a acceder a tu GitHub

### Paso 2: Crear Nuevo Proyecto
1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Selecciona tu repositorio `paquetes_agent`
4. Railway detectará automáticamente que es Python

### Paso 3: Configurar el Backend
1. En el dashboard de Railway, haz click en tu servicio
2. Ve a **"Settings"**
3. En **"Root Directory"**, pon: `backend`
4. En **"Start Command"**, pon: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Paso 4: Configurar Variables de Entorno
1. Ve a la pestaña **"Variables"**
2. Agrega cada una de estas variables con tus valores reales:

```
TENANT_ID=tu-tenant-id
CLIENT_ID=tu-client-id
CLIENT_SECRET=tu-client-secret
GRAPH_SENDER_UPN=recepcion@tuempresa.cl
GROQ_API_KEY=tu-groq-api-key
```

**Dónde encontrar estos valores:**
- Copialos de tu archivo local `backend/.env`
- O usa los valores del Azure Portal (Tenant ID, Client ID, Client Secret)

### Paso 5: Generar Dominio Público
1. Ve a **"Settings"** > **"Networking"**
2. Click en **"Generate Domain"**
3. Te dará una URL como: `https://paquetes-backend-production.up.railway.app`
4. **GUARDA ESTA URL** - la necesitarás para el frontend

### Paso 6: Verificar que Funciona
1. Abre tu URL del backend en el navegador
2. Agrega `/docs` al final: `https://tu-backend.railway.app/docs`
3. Deberías ver la documentación de la API (Swagger UI)
4. ✅ Si ves la documentación, el backend funciona correctamente

---

## 🎨 PARTE 2: Desplegar Frontend en Streamlit Cloud (10 minutos)

### Paso 1: Crear Cuenta en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Click en **"Sign up"** > **"Continue with GitHub"**
3. Autoriza Streamlit Cloud

### Paso 2: Desplegar la App
1. Click en **"New app"**
2. Selecciona tu repositorio `paquetes_agent`
3. En **"Main file path"**, pon: `frontend/app.py`
4. En **"Advanced settings"** > **"Python version"**, selecciona `3.11`

### Paso 3: Configurar Variables de Entorno
1. En **"Advanced settings"** > **"Secrets"**
2. Agrega esta variable (con la URL de Railway del Paso 1):

```toml
BACKEND_URL = "https://tu-backend.railway.app"
```

Ejemplo real:
```toml
BACKEND_URL = "https://paquetes-backend-production.up.railway.app"
```

### Paso 4: Deploy
1. Click en **"Deploy!"**
2. Espera 2-3 minutos mientras se despliega
3. Te dará una URL como: `https://paquetes-frontend.streamlit.app`
4. **ESTA ES LA URL QUE DARÁS A LA RECEPCIONISTA** ✅

### Paso 5: Verificar que Funciona
1. Abre la URL del frontend
2. Intenta registrar un paquete de prueba
3. Verifica que llegue el email
4. ✅ Si todo funciona, ya está listo para producción

---

## 🔐 Actualizar CORS en el Backend

Para mayor seguridad, después de desplegar, actualiza el CORS:

### En tu archivo local `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-frontend.streamlit.app",  # Producción
        "http://localhost:8501",              # Desarrollo local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Luego:
```bash
git add backend/main.py
git commit -m "Actualizar CORS para producción"
git push
```

Railway se actualizará automáticamente.

---

## 🎉 ¡Ya Está Listo!

### URLs Finales:
- **Backend (API):** `https://tu-backend.railway.app`
- **Frontend (App):** `https://tu-frontend.streamlit.app`

### Envía a la Recepcionista:
1. **URL de la app:** `https://tu-frontend.streamlit.app`
2. **Manual de uso:** [INSTRUCCIONES_RECEPCIONISTA.md](INSTRUCCIONES_RECEPCIONISTA.md)

---

## 📊 Características del Despliegue en Nube

### ✅ Ventajas:
- **Disponibilidad 24/7** - Funciona siempre
- **Acceso desde cualquier lugar** - Casa, oficina, celular
- **HTTPS seguro** - Certificado SSL automático
- **Auto-actualizaciones** - Push a GitHub y se actualiza solo
- **No requiere tu PC** - Completamente independiente
- **Gratis** (dentro de los límites del tier gratuito)

### 📈 Límites del Tier Gratuito:

**Railway:**
- 500 horas/mes (suficiente para uso 24/7)
- $5 USD de crédito mensual
- Inactividad después de 30 días sin deployments

**Streamlit Cloud:**
- 1 app privada gratis
- Recursos compartidos (suficiente para recepción)
- No hay límite de tiempo

### 💰 Si Superas el Tier Gratuito:

**Railway:**
- ~$5-10 USD/mes para backend
- Pago por uso

**Streamlit Cloud:**
- $20 USD/mes para apps adicionales o más recursos

---

## 🔄 Actualizar la Aplicación

Cuando hagas cambios al código:

```bash
# En tu PC local
git add .
git commit -m "Descripción del cambio"
git push

# Railway y Streamlit se actualizan automáticamente
```

---

## 🆘 Solución de Problemas

### Backend no despliega en Railway
**Error:** "Build failed"
**Solución:**
1. Ve a **Settings** > **Root Directory** y asegúrate que dice `backend`
2. Ve a **Variables** y confirma que todas las variables están configuradas
3. Revisa los logs en la pestaña **"Deployments"**

### Frontend no conecta con Backend
**Error:** "Connection refused" o "CORS error"
**Solución:**
1. Verifica que `BACKEND_URL` en Streamlit Secrets sea correcto
2. Confirma que el backend esté corriendo (abre `/docs`)
3. Actualiza CORS en `backend/main.py` con la URL de Streamlit

### Base de datos se resetea
**Causa:** SQLite se resetea en cada deploy
**Solución:** Usar Railway PostgreSQL (ver sección avanzada abajo)

### Aplicación muy lenta
**Causa:** Tier gratuito con recursos limitados
**Solución:**
1. Optimizar consultas a la BD
2. Agregar caché
3. O actualizar a plan pagado ($5-10/mes)

---

## 🚀 Configuración Avanzada (Opcional)

### Usar PostgreSQL en Lugar de SQLite

Railway ofrece PostgreSQL gratis:

1. En Railway, click en **"New"** > **"Database"** > **"PostgreSQL"**
2. Railway te dará las credenciales
3. Instala psycopg2 en `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
4. Modifica `backend/main.py` para usar PostgreSQL en lugar de SQLite

### Dominio Personalizado

Si quieres usar tu propio dominio (ej: `paquetes.tuempresa.cl`):

**Railway (Backend):**
1. Settings > Networking > Custom Domain
2. Agrega `api.tuempresa.cl`
3. Configura DNS en tu proveedor de dominios

**Streamlit Cloud (Frontend):**
1. Settings > Custom domain
2. Agrega `paquetes.tuempresa.cl`
3. Configura DNS

---

## 📋 Checklist de Despliegue

Antes de dar acceso a producción:

### Preparación:
- [ ] Proyecto subido a GitHub
- [ ] Archivo `.gitignore` configurado (NO subir `.env`)
- [ ] Variables de entorno anotadas en lugar seguro

### Backend (Railway):
- [ ] Cuenta creada en Railway
- [ ] Proyecto desplegado desde GitHub
- [ ] Root directory: `backend`
- [ ] Variables de entorno configuradas
- [ ] Dominio público generado
- [ ] `/docs` funciona correctamente

### Frontend (Streamlit Cloud):
- [ ] Cuenta creada en Streamlit Cloud
- [ ] App desplegada desde GitHub
- [ ] Main file: `frontend/app.py`
- [ ] `BACKEND_URL` configurado en Secrets
- [ ] App carga correctamente

### Pruebas:
- [ ] Registrar paquete de prueba
- [ ] Email llega correctamente
- [ ] Chatbot responde
- [ ] Historial muestra registros
- [ ] Búsqueda de usuarios funciona

---

## 🎯 Alternativas a Railway + Streamlit Cloud

### Opción 2: Todo en Railway (Dos Servicios)
**Pro:** Todo en un solo lugar
**Con:** Requiere dos servicios (pero gratis)

### Opción 3: Render.com (Backend + Frontend)
**Pro:** Similar a Railway, interfaz amigable
**Con:** Tier gratuito más limitado (750 horas/mes)

### Opción 4: Azure App Service
**Pro:** Integrado con tus servicios de Azure
**Con:** Más caro (~$13-55 USD/mes), más complejo de configurar

---

## 💡 Recomendación Final

**Para empezar:** Railway (Backend) + Streamlit Cloud (Frontend)
- Gratis
- Fácil
- Rápido

**Si crece el uso:** Migrar a Azure App Service o Render Pro
- Más recursos
- SLA garantizado
- Soporte profesional

---

## 📞 Próximos Pasos

1. **Sigue esta guía paso a paso** (15-20 minutos total)
2. **Prueba todo antes de dar acceso** a la recepcionista
3. **Guarda las URLs** en un lugar seguro
4. **Envía el manual** [INSTRUCCIONES_RECEPCIONISTA.md](INSTRUCCIONES_RECEPCIONISTA.md)

**¿Listo para empezar? Crea tu cuenta en Railway y Streamlit Cloud** 🚀

**¿Necesitas ayuda?** Revisa la sección de Solución de Problemas o contacta a soporte técnico.
