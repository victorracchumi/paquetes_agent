# 📧 Agregar Búsqueda de Grupos de Distribución

Esta guía te ayudará a habilitar la búsqueda de **grupos de distribución** (listas de correo) además de usuarios individuales.

---

## ✨ Nueva Funcionalidad

Ahora el sistema puede buscar y seleccionar:
- 👤 **Usuarios individuales**: Juan Pérez, María González, etc.
- 📧 **Grupos de distribución**: Cobranzas, Tesorería, Contabilidad, etc.

Esto permite enviar notificaciones a **múltiples personas** usando una sola dirección de email.

---

## 🔐 Agregar Permiso en Azure Portal

### Paso 1: Acceder a tu App Registration

1. Ve a [Azure Portal](https://portal.azure.com)
2. Busca **"Azure Active Directory"** o **"Microsoft Entra ID"**
3. Haz clic en **"App registrations"**
4. Selecciona tu aplicación: **"Sistema Recepción Paquetes"**

### Paso 2: Agregar Permiso Group.Read.All

1. En el menú lateral, haz clic en **"API permissions"**
2. Haz clic en **"+ Add a permission"**
3. Selecciona **"Microsoft Graph"**
4. Selecciona **"Application permissions"** (NO Delegated)
5. Busca y marca el permiso:
   ```
   ✅ Group.Read.All
   ```
6. Haz clic en **"Add permissions"**

### Paso 3: Otorgar Admin Consent

⚠️ **IMPORTANTE**: Sin este paso, la búsqueda de grupos no funcionará.

1. Después de agregar el permiso, haz clic en **"Grant admin consent for [Tu Organización]"**
2. Confirma haciendo clic en **"Yes"**
3. Verifica que el permiso muestre un **check verde** ✅ en la columna "Status"

### Paso 4: Verificar Permisos Finales

Tu aplicación debe tener estos **4 permisos** con Admin Consent:

```
✅ Mail.Send              (Application)  [Granted]
✅ Mail.ReadWrite         (Application)  [Granted]
✅ User.Read.All          (Application)  [Granted]
✅ Group.Read.All         (Application)  [Granted]  ← NUEVO
```

---

## 🎯 Cómo Usar

### 1. Buscar Grupos de Distribución

1. Abre http://localhost:8501
2. Ve a **"📝 Registrar Paquete"**
3. En **"🔍 Buscar Usuario en la Organización"**, escribe:
   - `cobranzas` → Encuentra grupo "Cobranzas"
   - `tesoreria` → Encuentra grupo "Tesorería"
   - `contabilidad` → Encuentra grupo "Contabilidad"

4. Los grupos aparecerán con el ícono 📧 y la etiqueta **(Grupo)**:
   ```
   📧 Cobranzas (Grupo) (cobranzas@multiaceros.cl)
   📧 Tesorería (Grupo) (tesoreria@multiaceros.cl)
   ```

5. Selecciona el grupo y el email se autocompletará

### 2. Enviar a Múltiples Destinatarios

Cuando registras un paquete con un grupo de distribución:
- El sistema enviará **UN** email a la dirección del grupo
- Microsoft 365 distribuirá automáticamente el email a **TODOS** los miembros del grupo

**Ejemplo:**
```
Destinatario: 📧 Cobranzas (Grupo)
Email: cobranzas@multiaceros.cl

→ Todos los miembros del grupo Cobranzas recibirán el email
```

---

## 📋 Crear Grupos de Distribución (Opcional)

Si aún no tienes grupos de distribución, puedes crearlos:

### Opción 1: Microsoft 365 Admin Center

1. Ve a [admin.microsoft.com](https://admin.microsoft.com)
2. **Teams & groups** > **Active teams & groups**
3. **Distribution lists** > **Add a distribution list**
4. Completa:
   - **Name**: Cobranzas
   - **Email**: cobranzas@multiaceros.cl
   - **Members**: Agrega los usuarios del equipo
5. Haz clic en **Create**

### Opción 2: Outlook

1. Abre Outlook Web (outlook.office.com)
2. Haz clic en el ícono de **personas** (contactos)
3. **New contact list** o **New group**
4. Agrega nombre y miembros
5. Guarda

---

## 💡 Grupos Recomendados

Considera crear estos grupos de distribución:

```
📧 cobranzas@multiaceros.cl       → Equipo de Cobranzas
📧 tesoreria@multiaceros.cl       → Equipo de Tesorería
📧 contabilidad@multiaceros.cl    → Equipo de Contabilidad
📧 finanzas@multiaceros.cl        → Equipo de Finanzas
📧 logistica@multiaceros.cl       → Equipo de Logística
📧 recepcion@multiaceros.cl       → Equipo de Recepción
📧 gerencia@multiaceros.cl        → Gerencia
```

---

## 🔍 Diferencia: Usuario vs Grupo

### Usuario Individual
```
👤 Juan Pérez (jperez@multiaceros.cl)
→ Solo Juan recibe el email
```

### Grupo de Distribución
```
📧 Cobranzas (Grupo) (cobranzas@multiaceros.cl)
→ Todos los miembros del grupo reciben el email:
   - María González
   - Pedro López
   - Ana Martínez
```

---

## 🎯 Casos de Uso

### Caso 1: Cheques para Tesorería
```
Tipo de Documento: Cheque
Destinatario: 📧 Tesorería (Grupo)
Email: tesoreria@multiaceros.cl

→ Todo el equipo de Tesorería se entera del cheque
```

### Caso 2: Facturas para Contabilidad
```
Tipo de Documento: Factura
Destinatario: 📧 Contabilidad (Grupo)
Email: contabilidad@multiaceros.cl

→ Todo el equipo de Contabilidad recibe la notificación
```

### Caso 3: Paquete Personal
```
Tipo de Documento: Paquete
Destinatario: 👤 Juan Pérez
Email: jperez@multiaceros.cl

→ Solo Juan recibe el email
```

---

## 🔧 Solución de Problemas

### No aparecen grupos en la búsqueda
**Causa**: Permiso `Group.Read.All` no configurado
**Solución**: Sigue los pasos 1-3 de esta guía

### Aparece "Admin Consent Required"
**Causa**: No se otorgó Admin Consent
**Solución**: Ve a Azure Portal > API Permissions > Grant admin consent

### El grupo no tiene email
**Causa**: El grupo es de tipo "Security Group" sin email
**Solución**: Crea un "Distribution Group" o "Mail-enabled Security Group"

---

## ✅ Checklist

Antes de usar grupos de distribución:

- [ ] Permiso `Group.Read.All` agregado en Azure
- [ ] Admin Consent otorgado (check verde ✅)
- [ ] Backend reiniciado
- [ ] Frontend reiniciado
- [ ] Grupos de distribución creados en Microsoft 365
- [ ] Prueba exitosa buscando un grupo

---

## 🎉 Ventajas de Usar Grupos

### Antes ❌
- Enviar email solo a una persona
- Si esa persona está ausente, nadie más se entera
- Necesitas registrar el paquete múltiples veces para varios destinatarios

### Ahora ✅
- Enviar a todo un equipo con un clic
- Si alguien está ausente, otro miembro puede recoger
- Un solo registro notifica a múltiples personas
- Mejor visibilidad y colaboración

---

**¡Listo! Ahora puedes usar grupos de distribución para notificar a equipos completos** 🎉
