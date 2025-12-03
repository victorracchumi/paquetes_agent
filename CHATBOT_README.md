# 🤖 Chatbot Inteligente - Guía de Uso

## 📋 Descripción

El sistema ahora incluye un **Asistente Virtual Inteligente** que utiliza IA para responder preguntas sobre tus paquetes en lenguaje natural.

## ✨ Características

### 🎯 Sistema Híbrido de Dos Niveles

1. **Respuestas Rápidas (Reglas)**
   - Búsqueda instantánea por código de paquete
   - Conteo de paquetes
   - Filtrado por sucursal
   - Últimos registros
   - Búsqueda por destinatario

2. **IA Conversacional (Groq - Llama 3.1)**
   - Entiende lenguaje natural
   - Respuestas contextuales
   - Completamente GRATIS
   - 14,400 consultas por día

## 🚀 Instalación

### 1. Instalar dependencias
```bash
pip install groq
```

O desde requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

Tu API key ya está configurada en el archivo `.env`:
```env
GROQ_API_KEY=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
```

## 💬 Ejemplos de Uso

### Preguntas Básicas (Respuestas Instantáneas)

```
Usuario: ¿Cuántos paquetes tengo?
Bot: 📦 Hay 5 paquetes registrados en esta sesión.

Usuario: Muéstrame el último paquete
Bot: 📦 Último paquete registrado:
- Código: PK-251128-ABCD
- Destinatario: Juan Pérez
- Sucursal: SANTIAGO
- Fecha: 2025-11-28 10:30:00

Usuario: ¿Dónde está PK-251128-ABCD?
Bot: ✅ Paquete encontrado:
- Código: PK-251128-ABCD
- Destinatario: Juan Pérez
...
```

### Preguntas Complejas (IA de Groq)

```
Usuario: Resúmeme los paquetes de esta semana
Bot: 🤖 Esta semana has recibido 5 paquetes...

Usuario: ¿Qué proveedor es más común?
Bot: 🤖 Según los datos, el proveedor más frecuente es...

Usuario: Dame recomendaciones para organizar mejor los paquetes
Bot: 🤖 Te sugiero las siguientes mejoras...
```

## 📊 Ventajas del Sistema

| Característica | Valor |
|----------------|-------|
| **Costo** | $0 (100% gratis) |
| **Límite diario** | 14,400 consultas |
| **Velocidad** | < 1 segundo |
| **Calidad IA** | Llama 3.1 (70B) |
| **Precisión** | Alta |

## 🔧 Arquitectura

```
┌─────────────────┐
│  Usuario hace   │
│    pregunta     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  chatbot_       │
│  inteligente()  │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌───────┐  ┌───────┐
│Reglas │  │ Groq  │
│Rápidas│  │  IA   │
└───────┘  └───────┘
```

## 🎓 Preguntas Frecuentes

### ¿Es realmente gratis?
Sí, Groq ofrece 14,400 consultas diarias completamente gratis. Para tu volumen estimado de < 500 consultas/día, será gratis para siempre.

### ¿Qué tan rápido es?
- Reglas: < 0.1 segundos (instantáneo)
- IA Groq: 0.5-2 segundos (muy rápido)

### ¿Qué modelo de IA usa?
Llama 3.1 de 70B parámetros, uno de los modelos más potentes disponibles gratuitamente.

### ¿Puedo cambiar de modelo?
Sí, en `chatbot_helper.py` línea 137, puedes cambiar el modelo:
```python
model="llama-3.1-70b-versatile"  # Actual
# Otras opciones:
# model="llama-3.3-70b-versatile"
# model="mixtral-8x7b-32768"
```

### ¿Los datos son privados?
Los datos se envían a Groq para procesamiento. Si necesitas privacidad total, considera usar Ollama (modelo local).

## 🛠️ Personalización

### Agregar nuevas reglas rápidas

Edita `frontend/chatbot_helper.py`:

```python
def chatbot_reglas(pregunta: str, historial: List[Dict]) -> Optional[str]:
    # Agregar tu nueva regla aquí
    if "mi condición" in pregunta.lower():
        return "Tu respuesta personalizada"
```

### Cambiar el prompt de la IA

Edita `chatbot_groq()` en `chatbot_helper.py`:

```python
system_prompt = f"""Tu prompt personalizado aquí"""
```

## 📝 Notas Importantes

1. La API key está hardcoded en `chatbot_helper.py` como fallback
2. El historial solo incluye la sesión actual (no persistente)
3. Para consultas sobre datos históricos del Excel, necesitarás integrar la lectura del archivo

## 🔮 Mejoras Futuras

- [ ] Integrar con base de datos para consultas históricas
- [ ] Agregar reconocimiento de voz
- [ ] Exportar conversaciones
- [ ] Multi-idioma
- [ ] Sugerencias proactivas

## 📞 Soporte

Si tienes problemas:
1. Verifica que la API key esté correcta
2. Revisa que el paquete `groq` esté instalado
3. Confirma conexión a internet

---

**¡Disfruta de tu nuevo asistente virtual inteligente! 🎉**
