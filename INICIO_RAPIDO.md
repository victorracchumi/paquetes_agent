# ⚡ Inicio Rápido - Despliega en 5 Minutos

Esta guía te permite tener el sistema funcionando para la recepcionista en menos de 5 minutos.

---

## 🎯 Opción Simple: Red Local (LAN)

Si la recepcionista está en la misma oficina que tú, esta es la forma MÁS RÁPIDA:

### Paso 1: Configurar Firewall (Solo la primera vez)
1. Click derecho en `configurar_firewall.bat`
2. Selecciona **"Ejecutar como administrador"**
3. Presiona cualquier tecla cuando te lo pida
4. Espera a ver "[OK]" dos veces
5. ¡Listo! Nunca más tendrás que hacer esto

### Paso 2: Iniciar el Sistema
1. Doble click en `start_servers_lan.bat`
2. Espera 5-10 segundos a que se abran dos ventanas:
   - **Backend - FastAPI** (ventana negra con logs)
   - **Frontend - Streamlit** (ventana negra con logs)

### Paso 3: Ver tu IP Local
En la primera ventana verás algo como:
```
Tu IP local es: 192.168.1.100

COMPARTE ESTA URL CON LA RECEPCIONISTA:
http://192.168.1.100:8501
```

### Paso 4: Enviar URL a la Recepcionista
1. Copia la URL completa: `http://192.168.1.100:8501`
2. Envíasela por email, WhatsApp, o lo que uses
3. Dile que la abra en Chrome, Edge o Firefox
4. Dile que la guarde en favoritos

### Paso 5: ¡Ya Funciona!
- Ella verá la interfaz del sistema
- Puede empezar a registrar paquetes inmediatamente
- Los emails se enviarán automáticamente

---

## 💡 Consejos Importantes

### Mantén las Ventanas Abiertas
- NO cierres las dos ventanas negras (Backend y Frontend)
- Mientras estén abiertas, el sistema funciona
- Minimízalas si quieres, pero no las cierres

### Tu Computadora Debe Estar Encendida
- El sistema corre desde tu PC
- Si apagas tu PC, el sistema deja de funcionar
- Puedes usar tu PC normalmente mientras corre

### Ambos Deben Estar en la Misma Red WiFi
- Tu PC y la PC de recepción deben estar en la misma red
- Conectadas al mismo WiFi de la oficina
- Si cambian de red, la URL cambiará

---

## 🔧 Si la URL Cambia Cada Día

Tu router puede estar asignando IPs dinámicas. Para fijar tu IP:

### Windows 10/11:
1. **Inicio** > **Configuración** > **Red e Internet**
2. Click en **"Propiedades"** de tu red actual
3. Baja hasta **"Configuración de IP"**
4. Click en **"Editar"**
5. Selecciona **"Manual"**
6. Activa **IPv4**
7. Configura:
   - **Dirección IP:** 192.168.1.100 (o la que viste)
   - **Máscara de subred:** 255.255.255.0
   - **Puerta de enlace:** 192.168.1.1 (normalmente)
   - **DNS preferido:** 8.8.8.8
   - **DNS alternativo:** 8.8.4.4
8. Guarda

Ahora tu URL será siempre la misma: `http://192.168.1.100:8501`

---

## 🎨 Personalizar para la Recepcionista

### Crear Acceso Directo en su Escritorio:
1. Click derecho en su escritorio > **Nuevo** > **Acceso directo**
2. En "Ubicación" pega: `http://192.168.1.100:8501` (tu URL)
3. Nombre: "Sistema de Paquetes"
4. ¡Listo! Ahora puede hacer doble click para abrirlo

### Establecer como Página de Inicio en Chrome:
1. Abre Chrome en su PC
2. **Menú** (⋮) > **Configuración**
3. **Al iniciar** > **Abrir una página específica**
4. **Agregar nueva página:** `http://192.168.1.100:8501`
5. Ahora se abre automáticamente al iniciar Chrome

---

## 📋 Checklist de Verificación

Antes de darle acceso a la recepcionista, verifica:

- [ ] Las dos ventanas están corriendo (Backend y Frontend)
- [ ] Copiaste la URL correcta (con tu IP)
- [ ] Puedes abrir la URL en TU navegador
- [ ] Ves la interfaz del sistema (pestañas: Registrar, Asistente, Historial)
- [ ] Prueba registrar un paquete de prueba con tu email
- [ ] Recibes el email de notificación
- [ ] El paquete aparece en el historial

---

## 🚨 Solución Rápida de Problemas

### "No puedo acceder a la página"
```bash
# 1. Verifica que ambos servicios están corriendo
# Deberías ver dos ventanas abiertas

# 2. Verifica tu IP actual
ipconfig

# Busca tu IPv4, ejemplo: 192.168.1.100

# 3. Prueba acceder desde TU PC primero
http://localhost:8501
```

### "Connection refused"
```bash
# Ejecuta el firewall otra vez como Administrador
configurar_firewall.bat
```

### Ella ve la página pero no carga datos
```bash
# Verifica que el backend esté respondiendo
# Abre en tu navegador:
http://TU-IP:8000/docs

# Deberías ver la documentación de la API
```

---

## ⏱️ Timeline de Implementación

**Minuto 0-1:** Ejecutar `configurar_firewall.bat` (solo primera vez)
**Minuto 1-2:** Ejecutar `start_servers_lan.bat`
**Minuto 2-3:** Copiar URL y enviarla a recepcionista
**Minuto 3-4:** Ella abre la URL y guarda en favoritos
**Minuto 4-5:** Prueba registrando un paquete de prueba

**Total: 5 minutos** ⏱️

---

## 📞 Siguiente Paso

Una vez que funcione:

1. **Dale el manual a la recepcionista:**
   - Envíale [INSTRUCCIONES_RECEPCIONISTA.md](INSTRUCCIONES_RECEPCIONISTA.md)
   - Tiene ejemplos claros de cómo usar todo

2. **Configura IP fija (opcional):**
   - Ver sección "Si la URL Cambia Cada Día"
   - Evita tener que dar nueva URL cada día

3. **Considera opciones a largo plazo:**
   - Si funciona bien, lee [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)
   - Puedes instalar en su PC o usar nube
   - Por ahora, esta opción es perfecta para empezar

---

**¿Listo? Ejecuta `start_servers_lan.bat` y empieza** 🚀

**¿Problemas?** Revisa [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md) o contacta a soporte técnico.
