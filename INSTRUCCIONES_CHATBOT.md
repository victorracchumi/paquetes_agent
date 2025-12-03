# 🚀 Cómo Probar el Chatbot Inteligente

## ✅ Instalación Completada

Ya está todo instalado y configurado:
- ✅ Groq instalado
- ✅ API Key configurada
- ✅ Chatbot integrado al frontend
- ✅ Archivo .env creado

## 🎯 Pasos para Probar

### 1. Iniciar el Backend (Terminal 1)

```bash
cd "c:\Users\vracchumi\OneDrive - Multiaceros\Escritorio\paquetes_agent"
.venv\Scripts\activate
cd backend
uvicorn main:app --reload
```

### 2. Iniciar el Frontend (Terminal 2)

```bash
cd "c:\Users\vracchumi\OneDrive - Multiaceros\Escritorio\paquetes_agent"
.venv\Scripts\activate
cd frontend
streamlit run app.py
```

### 3. Usar el Chatbot

1. Abre el navegador en `http://localhost:8501`
2. Ve a la pestaña **"💬 Chatbot IA"** (la cuarta tab)
3. Prueba las preguntas sugeridas o escribe tus propias preguntas

## 🧪 Preguntas de Prueba

### Para probar SIN registros (al inicio):
```
¿Cuántos paquetes tengo?
Muéstrame el último paquete
```
**Respuesta esperada**: Mensaje indicando que no hay paquetes

### Después de registrar 1-2 paquetes:

#### Preguntas Simples (Respuesta Instantánea):
```
¿Cuántos paquetes tengo?
Muéstrame el último paquete
Listar todos los paquetes
¿Cuántos paquetes hay en Santiago?
```

#### Buscar por Código:
```
¿Dónde está PK-251128-XXXX?  (reemplaza XXXX con tu código real)
Buscar PK-251128-XXXX
```

#### Preguntas Complejas (IA de Groq):
```
¿Cuál es el proveedor más común?
Resúmeme los paquetes de hoy
Dame sugerencias para organizar mejor los paquetes
¿Qué sucursal tiene más paquetes?
```

## 📊 Qué Esperar

### Respuestas Rápidas (🎯):
- Aparecen en < 0.5 segundos
- Tienen formato estructurado
- Datos precisos del historial

### Respuestas con IA (🤖):
- Tardan 1-3 segundos
- Más conversacionales
- Pueden incluir análisis y sugerencias

## 🔧 Solución de Problemas

### Error: "Module 'groq' not found"
```bash
.venv\Scripts\activate
pip install groq
```

### Error: "Invalid API key"
Verifica en `.env` que la API key esté correcta:
```env
GROQ_API_KEY=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
```

### El chatbot no responde
1. Revisa que tengas internet
2. Verifica que Groq esté disponible en: https://console.groq.com
3. Mira los logs en la terminal de Streamlit

### Respuestas lentas
- Groq puede estar con alta demanda
- Normal: 1-3 segundos
- Si > 10 segundos, revisa tu conexión

## 🎨 Características Interactivas

1. **Botones de Sugerencias**: Haz clic en cualquier pregunta sugerida
2. **Historial de Chat**: Se muestra debajo del input
3. **Expanders**: Haz clic para ver detalles de cada conversación
4. **Limpiar Chat**: Borra el historial de conversaciones
5. **Información**: Expande "¿Cómo funciona?" para detalles

## 📸 Capturas Esperadas

### Tab Chatbot:
```
┌─────────────────────────────────────────┐
│ 💬 Asistente Virtual Inteligente       │
│ ┌─────────────────────────────────────┐ │
│ │ 🤖 Pregúntame sobre tus paquetes... │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ 💡 Preguntas sugeridas:                │
│ [¿Cuántos...] [Último...] [Buscar...] │
│                                         │
│ 🔍 Tu pregunta: [____________]         │
│        [📤 Enviar Pregunta]            │
│                                         │
│ 📝 Conversación                        │
│ 💬 ¿Cuántos paquetes tengo? - 10:30   │
│ 💬 Buscar PK-... - 10:32              │
└─────────────────────────────────────────┘
```

## ✨ Próximos Pasos

Una vez que el chatbot funcione, puedes:

1. Personalizar las preguntas sugeridas en `chatbot_helper.py`
2. Agregar más reglas rápidas
3. Modificar el prompt de la IA
4. Integrar con la base de datos Excel para consultas históricas

## 🎉 ¡Listo!

Tu chatbot está configurado y listo para usar. Es:
- ✅ 100% Gratis (Groq)
- ✅ Rápido (< 2 segundos)
- ✅ Inteligente (Llama 3.1)
- ✅ Bilingüe (Reglas + IA)

---

**¿Necesitas ayuda?** Revisa `CHATBOT_README.md` para más detalles técnicos.
