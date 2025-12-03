# 🚀 Guía de Despliegue - Sistema Recepción de Paquetes

Esta guía te ayudará a desplegar la aplicación para que la recepcionista pueda usarla.

---

## 🎯 Opción 1: Red Local (LAN) - **RECOMENDADA PARA OFICINA**

**Ideal si:** La recepcionista trabaja en la misma oficina (misma red WiFi/LAN)

**Ventajas:**
- ✅ Configuración súper simple (5 minutos)
- ✅ Completamente gratis
- ✅ Más seguro (solo accesible desde tu red)
- ✅ Rápido y sin latencia
- ✅ No requiere servidor externo

**Desventajas:**
- ❌ Tu computadora debe estar encendida
- ❌ Solo funciona dentro de la red de la oficina

### Pasos para Configurar:

#### 1. Ejecuta el archivo especial para LAN
Haz doble clic en:
```
start_servers_lan.bat
```

#### 2. Copia la URL que aparece
Verás algo como:
```
COMPARTE ESTA URL CON LA RECEPCIONISTA:
http://192.168.1.100:8501
```

#### 3. Envíale la URL a la recepcionista
- Puede abrirla en Chrome, Edge, o cualquier navegador
- Guárdala en favoritos para fácil acceso

#### 4. ¡Listo! Ya puede usar el sistema

### Configurar IP Fija (Opcional pero Recomendado)

Para que la URL no cambie cada vez:

1. Ve a **Panel de Control** > **Redes**
2. Busca tu adaptador de red
3. **Propiedades** > **IPv4** > **Usar la siguiente dirección IP**
4. Configura una IP fija (ej: 192.168.1.100)

---

## 💻 Opción 2: Instalar en la Computadora de la Recepcionista

**Ideal si:** Quieres que la recepcionista ejecute todo localmente

### Pasos:

#### 1. Copia la carpeta completa del proyecto
Copia toda la carpeta `paquetes_agent` a su computadora

#### 2. Instala Python 3.11+
Descarga desde [python.org](https://www.python.org/downloads/)

#### 3. Instala dependencias
Abre PowerShell en la carpeta del proyecto:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. Copia el archivo .env
**IMPORTANTE:** Copia tu archivo `.env` con las credenciales de Azure:
```
backend/.env
```

#### 5. Ejecuta la aplicación
Doble clic en:
```
start_servers.bat
```

#### 6. Abre el navegador
http://localhost:8501

---

## ☁️ Opción 3: Despliegue en la Nube (Acceso desde Cualquier Lugar)

**Ideal si:** Necesitan acceso desde casa o múltiples ubicaciones

### 3A. Railway.app (Recomendado - Fácil)

**Ventajas:**
- ✅ Tier gratuito generoso (500 horas/mes)
- ✅ Muy fácil de configurar
- ✅ HTTPS automático
- ✅ Acceso desde cualquier lugar

**Pasos:**

1. **Crea cuenta en Railway.app**
   - Ve a [railway.app](https://railway.app)
   - Regístrate con GitHub

2. **Sube tu proyecto**
   ```bash
   npm install -g @railway/cli
   railway login
   railway init
   railway up
   ```

3. **Configura variables de entorno**
   En Railway Dashboard:
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_TENANT_ID`
   - `SHARED_MAILBOX_EMAIL`
   - `GROQ_API_KEY`

4. **Despliega los servicios**
   - Backend: Puerto 8000
   - Frontend: Puerto 8501 (configura `BACKEND_URL` con la URL del backend)

5. **Obtén la URL pública**
   Railway te dará una URL tipo: `https://tu-app.railway.app`

### 3B. Render.com (Alternativa)

**Pasos similares a Railway:**

1. Crea cuenta en [render.com](https://render.com)
2. Crea un "Web Service" para el backend
3. Crea otro "Web Service" para el frontend
4. Configura las variables de entorno
5. Conecta ambos servicios

---

## 🏢 Opción 4: Azure (Para Integración Completa)

**Ideal si:** Tu empresa ya usa Azure para todo

### Usar Azure App Service:

1. **Crear App Service para Backend**
   ```bash
   az webapp create --name paquetes-backend --resource-group tu-grupo
   ```

2. **Crear App Service para Frontend**
   ```bash
   az webapp create --name paquetes-frontend --resource-group tu-grupo
   ```

3. **Configurar variables de entorno en Azure Portal**

4. **Desplegar con Git o VS Code**

**Costo estimado:** ~$10-20 USD/mes por ambos servicios

---

## 🔧 Configuración Adicional Según la Opción

### Para Red Local (Opción 1):

#### Permitir acceso en el Firewall de Windows:
```bash
# Ejecutar como Administrador
netsh advfirewall firewall add rule name="Streamlit" dir=in action=allow protocol=TCP localport=8501
netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
```

### Para Instalación Local (Opción 2):

#### Crear acceso directo en el escritorio:
1. Click derecho > Nuevo > Acceso directo
2. Ubicación: `C:\ruta\paquetes_agent\start_servers.bat`
3. Nombre: "Sistema Paquetes"

### Para Nube (Opción 3):

#### Configurar CORS en backend/main.py:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📋 Checklist de Seguridad

Antes de desplegar en producción:

- [ ] **NO** subir el archivo `.env` a GitHub/repositorio público
- [ ] Usar HTTPS en producción (las opciones cloud ya lo incluyen)
- [ ] Configurar CORS correctamente (solo dominios autorizados)
- [ ] Cambiar el Client Secret de Azure cada 6-12 meses
- [ ] Backup de la base de datos `paquetes.db` regularmente
- [ ] Documentar la URL y credenciales para el equipo

---

## 🎯 Mi Recomendación por Caso de Uso

### Si la recepcionista está en la oficina y tú también:
**→ Opción 1 (Red Local)** - La más simple y rápida

### Si la recepcionista trabaja desde casa a veces:
**→ Opción 3A (Railway.app)** - Acceso desde cualquier lugar

### Si quieres que sea 100% independiente:
**→ Opción 2 (Instalación local en su PC)** - No depende de tu computadora

### Si tu empresa ya paga Azure y quieren todo integrado:
**→ Opción 4 (Azure App Service)** - Máxima integración

---

## 🆘 Solución de Problemas

### Error: "No se puede acceder a la página"
- Verifica que ambas computadoras estén en la misma red WiFi
- Revisa el firewall de Windows (ver sección de configuración)
- Confirma que los servidores están corriendo

### Error: "Connection refused"
- Asegúrate de ejecutar `start_servers_lan.bat` (no `start_servers.bat`)
- Verifica que los puertos 8000 y 8501 no estén ocupados

### La recepcionista ve la página pero no carga datos:
- Verifica que el BACKEND_URL apunte a tu IP (no localhost)
- Revisa los logs del backend para errores

---

## 📞 Siguiente Paso

**Para empezar YA (5 minutos):**
1. Ejecuta `start_servers_lan.bat`
2. Copia la URL que aparece
3. Envíala a la recepcionista por email/WhatsApp
4. ¡Listo!

**¿Necesitas ayuda?** Dime qué opción prefieres y te ayudo con los detalles específicos.
