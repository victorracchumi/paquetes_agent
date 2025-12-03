"""
Módulo de chatbot inteligente para el sistema de recepción de paquetes
Usa Groq API (gratis) con modelo Llama 3.1
"""

import os
import requests
import re
from typing import List, Dict, Optional, Tuple
from groq import Groq

# Configurar cliente Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_field(pkg: Dict, field_name: str, default='') -> str:
    """
    Obtiene un campo del paquete con compatibilidad entre formato Excel y Frontend.
    Excel usa PascalCase (CodigoRetiro), Frontend usa camelCase (codigoRetiro).
    """
    # Mapeo de campos camelCase a PascalCase
    field_map = {
        'codigoRetiro': 'CodigoRetiro',
        'destinatarioNombre': 'DestinatarioNombre',
        'destinatarioEmail': 'DestinatarioEmail',
        'sucursal': 'Sucursal',
        'proveedor': 'Proveedor',
        'tipoDocumento': 'TipoDocumento',
        'numeroDocumento': 'NumeroDocumento',
        'fechaRecepcion': 'FechaRecepcion',
        'horaRecepcion': 'HoraRecepcion',
        'medioNotificacion': 'MedioNotificacion',
        'recepcionista': 'Recepcionista',
        'observaciones': 'Observaciones'
    }

    # Intentar primero con PascalCase (Excel)
    pascal_case = field_map.get(field_name, field_name)
    value = pkg.get(pascal_case)

    # Si no existe, intentar con camelCase (Frontend)
    if value is None:
        value = pkg.get(field_name)

    return value if value is not None else default


def enviar_recordatorio(email: str, nombre: str) -> Tuple[bool, str]:
    """
    Envía un correo de recordatorio a un usuario.
    Returns: (éxito, mensaje)
    """
    try:
        r = requests.post(
            f"{BACKEND_URL}/send-reminder",
            json={"email": email, "nombre": nombre},
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("success"):
                return True, f"✅ Recordatorio enviado exitosamente a {email}"
            else:
                return False, f"❌ No se pudo enviar el recordatorio: {data.get('message', 'Error desconocido')}"
        else:
            return False, f"❌ Error del servidor: {r.status_code}"
    except Exception as e:
        return False, f"❌ Error al enviar recordatorio: {str(e)}"


def generar_dashboard(historial: List[Dict]) -> str:
    """
    Genera un dashboard con estadísticas de los paquetes.
    """
    if not historial:
        return "📭 No hay datos para generar el dashboard."

    from collections import Counter
    from datetime import datetime

    # Estadísticas generales
    total = len(historial)

    # Contar por tipo de documento
    tipos = Counter(get_field(pkg, 'tipoDocumento') for pkg in historial)

    # Contar por sucursal
    sucursales = Counter(get_field(pkg, 'sucursal') for pkg in historial)

    # Contar por destinatario (top 5)
    destinatarios = Counter(get_field(pkg, 'destinatarioNombre') for pkg in historial)
    top_destinatarios = destinatarios.most_common(5)

    # Contar por proveedor (top 5)
    proveedores = Counter(get_field(pkg, 'proveedor') for pkg in historial)
    top_proveedores = proveedores.most_common(5)

    # Generar dashboard
    dashboard = f"""📊 **DASHBOARD DE PAQUETES**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 **Total de paquetes:** {total}

**📄 Por Tipo de Documento:**
"""
    for tipo, count in tipos.most_common():
        barra = "█" * min(count, 20)
        dashboard += f"  {tipo}: {barra} ({count})\n"

    dashboard += f"\n**📍 Por Sucursal:**\n"
    for sucursal, count in sucursales.most_common():
        barra = "█" * min(count, 20)
        dashboard += f"  {sucursal}: {barra} ({count})\n"

    dashboard += f"\n**👥 Top 5 Destinatarios:**\n"
    for i, (nombre, count) in enumerate(top_destinatarios, 1):
        dashboard += f"  {i}. {nombre}: {count} paquete(s)\n"

    dashboard += f"\n**🚚 Top 5 Proveedores:**\n"
    for i, (proveedor, count) in enumerate(top_proveedores, 1):
        dashboard += f"  {i}. {proveedor}: {count} paquete(s)\n"

    return dashboard


def enviar_alertas_masivas(historial: List[Dict]) -> str:
    """
    Envía recordatorios a todos los usuarios con paquetes pendientes.
    """
    if not historial:
        return "📭 No hay paquetes para enviar alertas."

    # Agrupar por email
    emails_unicos = {}
    for pkg in historial:
        email = get_field(pkg, 'destinatarioEmail')
        nombre = get_field(pkg, 'destinatarioNombre')
        if email and email not in emails_unicos:
            emails_unicos[email] = nombre

    # Enviar recordatorios
    exitosos = 0
    fallidos = 0

    resultado = f"📧 **Enviando alertas a {len(emails_unicos)} destinatario(s)...**\n\n"

    for email, nombre in emails_unicos.items():
        exito, _ = enviar_recordatorio(email, nombre)
        if exito:
            exitosos += 1
            resultado += f"✅ {nombre} ({email})\n"
        else:
            fallidos += 1
            resultado += f"❌ {nombre} ({email})\n"

    resultado += f"\n**Resumen:**\n"
    resultado += f"✅ Exitosos: {exitosos}\n"
    resultado += f"❌ Fallidos: {fallidos}\n"

    return resultado


def chatbot_reglas(pregunta: str, historial: List[Dict]) -> Optional[str]:
    """
    Chatbot basado en reglas para consultas simples y rápidas.
    Retorna None si no puede responder con reglas.
    """
    pregunta_lower = pregunta.lower()

    # Búsqueda por fecha específica
    if any(palabra in pregunta_lower for palabra in ["día", "dia", "fecha", "registrado el", "registro el"]):
        # Intentar extraer fecha de la pregunta
        import re
        from datetime import datetime

        # Buscar patrones de fecha
        # "1 de diciembre" o "1 diciembre" o "diciembre 1"
        meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }

        fecha_encontrada = None
        for mes_nombre, mes_num in meses.items():
            if mes_nombre in pregunta_lower:
                # Buscar día (número antes o después del mes)
                match = re.search(r'(\d{1,2})\s+(?:de\s+)?' + mes_nombre, pregunta_lower)
                if not match:
                    match = re.search(mes_nombre + r'\s+(\d{1,2})', pregunta_lower)

                if match:
                    dia = match.group(1).zfill(2)
                    # Buscar año (si no está, usar 2025)
                    year_match = re.search(r'20\d{2}', pregunta_lower)
                    anio = year_match.group(0) if year_match else '2025'
                    fecha_encontrada = f"{anio}-{mes_num}-{dia}"
                    break

        if fecha_encontrada:
            # Buscar paquetes de esa fecha
            paquetes_fecha = [
                p for p in historial
                if (get_field(p, 'fechaRecepcion') or '').startswith(fecha_encontrada)
            ]

            if paquetes_fecha:
                resultado = f"📦 **Paquetes registrados el {fecha_encontrada}:**\n\n"
                for i, pkg in enumerate(paquetes_fecha, 1):
                    codigo = get_field(pkg, 'codigoRetiro')
                    destinatario = get_field(pkg, 'destinatarioNombre')
                    tipo = get_field(pkg, 'tipoDocumento')
                    hora = get_field(pkg, 'horaRecepcion')
                    resultado += f"{i}. **{codigo}**\n"
                    resultado += f"   - Destinatario: {destinatario}\n"
                    resultado += f"   - Tipo: {tipo}\n"
                    resultado += f"   - Hora: {hora}\n\n"
                resultado += f"**Total: {len(paquetes_fecha)} paquete(s)**"
                return resultado
            else:
                return f"📭 No hay paquetes registrados el {fecha_encontrada}"

    # Búsqueda por sucursal
    if any(palabra in pregunta_lower for palabra in ["sucursal", "sucursales", "oficina", "local"]):
        # Extraer posible nombre de sucursal de la pregunta
        sucursales_posibles = ["santiago", "viña", "viña del mar", "valparaíso", "valparaiso", "concepción", "concepcion",
                               "temuco", "antofagasta", "la serena", "iquique", "puerto montt"]

        sucursal_buscada = None
        for suc in sucursales_posibles:
            if suc in pregunta_lower:
                sucursal_buscada = suc
                break

        if sucursal_buscada:
            # Buscar paquetes de esa sucursal
            paquetes_sucursal = [
                p for p in historial
                if sucursal_buscada in get_field(p, 'sucursal').lower()
            ]

            if paquetes_sucursal:
                resultado = f"📍 **Paquetes en sucursal '{sucursal_buscada.title()}':** {len(paquetes_sucursal)}\n\n"
                for i, pkg in enumerate(paquetes_sucursal[-10:], 1):  # Últimos 10
                    codigo = get_field(pkg, 'codigoRetiro')
                    destinatario = get_field(pkg, 'destinatarioNombre')
                    tipo = get_field(pkg, 'tipoDocumento')
                    fecha = get_field(pkg, 'fechaRecepcion')
                    resultado += f"{i}. **{codigo}** - {destinatario}\n"
                    resultado += f"   Tipo: {tipo} | Fecha: {fecha}\n\n"

                if len(paquetes_sucursal) > 10:
                    resultado += f"_(Mostrando últimos 10 de {len(paquetes_sucursal)} total)_"
                return resultado
            else:
                return f"📭 No hay paquetes registrados en sucursal '{sucursal_buscada.title()}'"
        else:
            # Listar todas las sucursales
            sucursales = {}
            for pkg in historial:
                suc = get_field(pkg, 'sucursal')
                sucursales[suc] = sucursales.get(suc, 0) + 1

            if sucursales:
                resultado = "📍 **Paquetes por sucursal:**\n\n"
                for suc, count in sorted(sucursales.items(), key=lambda x: x[1], reverse=True):
                    resultado += f"• **{suc}**: {count} paquete(s)\n"
                resultado += f"\n💡 Ejemplo: '¿Cuántos paquetes hay en Santiago?'"
                return resultado
            else:
                return "📭 No hay paquetes registrados"

    # Búsqueda por tipo de documento
    if any(palabra in pregunta_lower for palabra in ["tipo de documento", "tipo documento", "cheque", "cheques", "factura", "facturas",
                                                       "carta", "cartas", "paquete", "paquetes", "sobre", "sobres"]):
        # Detectar tipo específico
        tipo_mapa = {
            "cheque": "Cheque",
            "cheques": "Cheque",
            "factura": "Factura",
            "facturas": "Factura",
            "carta": "Carta",
            "cartas": "Carta",
            "paquete": "Paquete",
            "paquetes": "Paquete",
            "sobre": "Sobre",
            "sobres": "Sobre"
        }

        tipo_buscado = None
        for palabra, tipo_formal in tipo_mapa.items():
            if palabra in pregunta_lower:
                tipo_buscado = tipo_formal
                break

        if tipo_buscado:
            # Buscar paquetes de ese tipo
            paquetes_tipo = [
                p for p in historial
                if get_field(p, 'tipoDocumento').lower() == tipo_buscado.lower()
            ]

            if paquetes_tipo:
                resultado = f"📄 **{tipo_buscado}s registrados:** {len(paquetes_tipo)}\n\n"
                for i, pkg in enumerate(paquetes_tipo[-10:], 1):  # Últimos 10
                    codigo = get_field(pkg, 'codigoRetiro')
                    destinatario = get_field(pkg, 'destinatarioNombre')
                    sucursal = get_field(pkg, 'sucursal')
                    fecha = get_field(pkg, 'fechaRecepcion')
                    resultado += f"{i}. **{codigo}** - {destinatario}\n"
                    resultado += f"   Sucursal: {sucursal} | Fecha: {fecha}\n\n"

                if len(paquetes_tipo) > 10:
                    resultado += f"_(Mostrando últimos 10 de {len(paquetes_tipo)} total)_"
                return resultado
            else:
                return f"📭 No hay {tipo_buscado.lower()}s registrados"
        else:
            # Listar todos los tipos
            tipos = {}
            for pkg in historial:
                tipo = get_field(pkg, 'tipoDocumento')
                tipos[tipo] = tipos.get(tipo, 0) + 1

            if tipos:
                resultado = "📄 **Paquetes por tipo de documento:**\n\n"
                for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
                    resultado += f"• **{tipo}**: {count} paquete(s)\n"
                resultado += f"\n💡 Ejemplo: '¿Cuántos cheques hay?'"
                return resultado
            else:
                return "📭 No hay paquetes registrados"

    # Búsqueda por destinatario (nombre)
    if any(palabra in pregunta_lower for palabra in ["destinatario", "para quien", "para quién", "destinado a", "paquete de", "paquetes de"]):
        # Extraer palabras relevantes (ignorar palabras clave)
        palabras_ignorar = ["que", "hay", "un", "el", "la", "los", "las", "para", "quien", "quién", "es", "son",
                           "paquete", "paquetes", "destinatario", "destinatarios", "de", "del", "a", "tiene"]
        palabras = [p.strip("¿?.,;:") for p in pregunta_lower.split() if p.strip("¿?.,;:") not in palabras_ignorar]

        if palabras:
            # Buscar destinatarios que coincidan
            destinatarios_encontrados = []
            for palabra in palabras:
                if len(palabra) >= 3:  # Mínimo 3 caracteres
                    for pkg in historial:
                        nombre = get_field(pkg, 'destinatarioNombre').lower()
                        if palabra in nombre:
                            destinatarios_encontrados.append(pkg)

            if destinatarios_encontrados:
                # Agrupar por destinatario único
                dest_unicos = {}
                for pkg in destinatarios_encontrados:
                    nombre = get_field(pkg, 'destinatarioNombre')
                    if nombre not in dest_unicos:
                        dest_unicos[nombre] = []
                    dest_unicos[nombre].append(pkg)

                resultado = f"👤 **Destinatarios encontrados:** {len(dest_unicos)}\n\n"
                for nombre, paquetes in list(dest_unicos.items())[:5]:  # Máximo 5 destinatarios
                    resultado += f"**{nombre}** ({len(paquetes)} paquete(s))\n"
                    for i, pkg in enumerate(paquetes[:3], 1):  # Máximo 3 paquetes por destinatario
                        codigo = get_field(pkg, 'codigoRetiro')
                        tipo = get_field(pkg, 'tipoDocumento')
                        fecha = get_field(pkg, 'fechaRecepcion')
                        resultado += f"  {i}. {codigo} - {tipo} ({fecha})\n"
                    if len(paquetes) > 3:
                        resultado += f"  _(y {len(paquetes) - 3} más)_\n"
                    resultado += "\n"

                if len(dest_unicos) > 5:
                    resultado += f"_(Mostrando 5 de {len(dest_unicos)} destinatarios)_"
                return resultado

    # Generar dashboard
    if any(palabra in pregunta_lower for palabra in ["dashboard", "estadísticas", "estadisticas", "resumen general", "análisis", "analisis", "métricas", "metricas"]):
        return generar_dashboard(historial)

    # Enviar alertas masivas
    if any(palabra in pregunta_lower for palabra in ["enviar alertas", "alertar a todos", "notificar a todos", "recordar a todos", "avisar a todos"]):
        return enviar_alertas_masivas(historial)

    # Detectar solicitud de recordatorio
    palabras_recordatorio = ["recordatorio", "recordar", "avisar", "notificar", "enviar correo", "enviar email", "enviar recordatorio", "enviales"]
    if any(palabra in pregunta_lower for palabra in palabras_recordatorio):
        # Primero intentar buscar email en la pregunta (formato: usuario@dominio.com)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, pregunta)

        if emails:
            email = emails[0]
            # Intentar extraer el nombre del historial
            nombre = "Usuario"
            for pkg in historial:
                if get_field(pkg, 'destinatarioEmail').lower() == email.lower():
                    nombre = get_field(pkg, 'destinatarioNombre')
                    break

            # Enviar recordatorio
            exito, mensaje = enviar_recordatorio(email, nombre)
            return mensaje
        else:
            # Si no hay email, buscar por nombre en el historial
            # Extraer palabras relevantes (ignorar palabras clave)
            palabras_ignorar = ["que", "hay", "un", "paquete", "aun", "para", "a", "de", "el", "la", "los", "las",
                              "recordatorio", "recordar", "avisar", "notificar", "enviar", "correo", "email", "le", "enviales"]
            palabras = [p.strip("¿?.,;:") for p in pregunta_lower.split() if p.strip("¿?.,;:") not in palabras_ignorar]

            # Buscar coincidencias en el historial
            destinatarios_encontrados = []
            for pkg in historial:
                nombre_pkg = get_field(pkg, 'destinatarioNombre').lower()
                email_pkg = get_field(pkg, 'destinatarioEmail')

                # Buscar si alguna palabra de la pregunta está en el nombre del destinatario
                for palabra in palabras:
                    if palabra and len(palabra) >= 3 and palabra in nombre_pkg:
                        # Evitar duplicados
                        if email_pkg not in [d['email'] for d in destinatarios_encontrados]:
                            destinatarios_encontrados.append({
                                'nombre': get_field(pkg, 'destinatarioNombre'),
                                'email': email_pkg,
                                'codigo': get_field(pkg, 'codigoRetiro'),
                                'sucursal': get_field(pkg, 'sucursal')
                            })
                        break

            if len(destinatarios_encontrados) == 1:
                # Único destinatario encontrado, enviar automáticamente
                dest = destinatarios_encontrados[0]
                exito, mensaje = enviar_recordatorio(dest['email'], dest['nombre'])

                resultado = f"🔍 **Destinatario encontrado:**\n"
                resultado += f"- **Nombre:** {dest['nombre']}\n"
                resultado += f"- **Email:** {dest['email']}\n"
                resultado += f"- **Código:** {dest['codigo']}\n"
                resultado += f"- **Sucursal:** {dest['sucursal']}\n\n"
                resultado += mensaje

                return resultado

            elif len(destinatarios_encontrados) > 1:
                # Múltiples destinatarios encontrados, mostrar lista
                resultado = f"🔍 **Encontré {len(destinatarios_encontrados)} destinatarios:**\n\n"
                for i, dest in enumerate(destinatarios_encontrados, 1):
                    resultado += f"{i}. **{dest['nombre']}** ({dest['email']})\n"
                    resultado += f"   - Código: {dest['codigo']}\n"
                    resultado += f"   - Sucursal: {dest['sucursal']}\n\n"

                resultado += "💡 **Enviar recordatorio a uno específico:**\n"
                resultado += f"Escribe: 'enviar recordatorio a {destinatarios_encontrados[0]['email']}'"

                return resultado

            else:
                # No se encontró ningún destinatario
                return f"❌ No encontré ningún destinatario con ese nombre.\n\n💡 **Opciones:**\n1. Intenta con otro nombre\n2. Usa el email directo: 'enviar recordatorio a email@multiaceros.cl'\n3. Consulta la lista de destinatarios con: 'listar paquetes'"

    # Búsqueda por código específico (SOLO si NO es un recordatorio)
    if "pk-" in pregunta_lower and not any(palabra in pregunta_lower for palabra in palabras_recordatorio):
        # Extraer código de la pregunta
        partes = pregunta_lower.split("pk-")
        if len(partes) > 1:
            codigo_parte = partes[1].split()[0] if partes[1].split() else partes[1][:10]
            codigo = f"PK-{codigo_parte.upper()}"

            # Buscar en historial
            for pkg in historial:
                if get_field(pkg, 'codigoRetiro').upper() == codigo.upper():
                    return f"""✅ **Paquete encontrado:**
- **Código:** {get_field(pkg, 'codigoRetiro')}
- **Destinatario:** {get_field(pkg, 'destinatarioNombre')}
- **Email:** {get_field(pkg, 'destinatarioEmail')}
- **Sucursal:** {get_field(pkg, 'sucursal')}
- **Proveedor:** {get_field(pkg, 'proveedor')}
- **Documento:** {get_field(pkg, 'tipoDocumento')} - {get_field(pkg, 'numeroDocumento')}
- **Fecha:** {get_field(pkg, 'fechaRecepcion')} {get_field(pkg, 'horaRecepcion')}
"""
            return f"❌ No encontré el código {codigo} en el historial actual."

    # Contar paquetes
    if any(palabra in pregunta_lower for palabra in ["cuántos", "cuantos", "cantidad", "total"]):
        if "paquete" in pregunta_lower or "registro" in pregunta_lower:
            total = len(historial)
            if total == 0:
                return "📭 No hay paquetes registrados en esta sesión."
            elif total == 1:
                return "📦 Hay **1 paquete** registrado."
            else:
                return f"📦 Hay **{total} paquetes** registrados en esta sesión."

    # Último paquete
    if any(palabra in pregunta_lower for palabra in ["último", "ultimo", "reciente", "más nuevo"]):
        if historial:
            ultimo = historial[-1]
            return f"""📦 **Último paquete registrado:**
- **Código:** {get_field(ultimo, 'codigoRetiro')}
- **Destinatario:** {get_field(ultimo, 'destinatarioNombre')}
- **Sucursal:** {get_field(ultimo, 'sucursal')}
- **Fecha:** {get_field(ultimo, 'fechaRecepcion')} {get_field(ultimo, 'horaRecepcion')}
"""
        return "📭 No hay paquetes registrados todavía."

    # Listar todos los paquetes
    if "listar" in pregunta_lower or "mostrar todos" in pregunta_lower or "ver todos" in pregunta_lower:
        if not historial:
            return "📭 No hay paquetes registrados en esta sesión."

        resultado = f"📋 **Lista de {len(historial)} paquete(s):**\n\n"
        for i, pkg in enumerate(historial[-10:], 1):  # Últimos 10
            resultado += f"{i}. {get_field(pkg, 'codigoRetiro')} - {get_field(pkg, 'destinatarioNombre')} ({get_field(pkg, 'sucursal')})\n"

        if len(historial) > 10:
            resultado += f"\n_(Mostrando los últimos 10 de {len(historial)} total)_"

        return resultado

    # Buscar por nombre de destinatario
    if "destinatario" in pregunta_lower or "nombre" in pregunta_lower:
        # Intentar extraer un nombre
        palabras = pregunta.split()
        for i, palabra in enumerate(palabras):
            if palabra.lower() in ["destinatario", "nombre", "para", "de"] and i + 1 < len(palabras):
                nombre_buscar = palabras[i + 1].lower()
                encontrados = [pkg for pkg in historial if nombre_buscar in get_field(pkg, 'destinatarioNombre').lower()]

                if encontrados:
                    resultado = f"🔍 Encontré **{len(encontrados)} paquete(s)** con '{nombre_buscar}':\n\n"
                    for pkg in encontrados:
                        resultado += f"- {get_field(pkg, 'codigoRetiro')}: {get_field(pkg, 'destinatarioNombre')} ({get_field(pkg, 'sucursal')})\n"
                    return resultado

    # Buscar por sucursal
    sucursales = ["SANTIAGO", "VIÑA DEL MAR", "CONCEPCIÓN", "LA SERENA"]
    for sucursal in sucursales:
        if sucursal.lower() in pregunta_lower or sucursal.replace(" ", "").lower() in pregunta_lower:
            encontrados = [pkg for pkg in historial if get_field(pkg, 'sucursal').upper() == sucursal.upper()]
            if encontrados:
                return f"📍 Hay **{len(encontrados)} paquete(s)** en {sucursal}."
            return f"📍 No hay paquetes registrados en {sucursal}."

    # Buscar por tipo de documento (Cheque, Factura, Guía, etc.)
    tipos_doc = {
        "cheque": ["cheque", "cheques"],
        "factura": ["factura", "facturas"],
        "guía": ["guia", "guía", "guias", "guías"],
        "ot": ["ot", "orden de trabajo", "orden trabajo"],
        "otro": ["otro", "otros"]
    }

    for tipo, variantes in tipos_doc.items():
        if any(var in pregunta_lower for var in variantes):
            encontrados = [pkg for pkg in historial if get_field(pkg, 'tipoDocumento').lower() == tipo.lower()]

            if encontrados:
                resultado = f"💰 Encontré **{len(encontrados)} paquete(s)** con tipo de documento '{tipo.upper()}':\n\n"
                for pkg in encontrados:
                    resultado += f"- **{get_field(pkg, 'codigoRetiro')}**: {get_field(pkg, 'destinatarioNombre')}\n"
                    resultado += f"  📄 Documento: {get_field(pkg, 'numeroDocumento')}\n"
                    resultado += f"  🚚 Proveedor: {get_field(pkg, 'proveedor')}\n"

                    # Si es cheque, mostrar monto y fecha de vencimiento si existen
                    if tipo.lower() == "cheque":
                        monto = get_field(pkg, 'montoCheque')
                        fecha_venc = get_field(pkg, 'fechaVencimientoCheque')
                        if monto:
                            resultado += f"  💵 Monto: {monto}\n"
                        if fecha_venc:
                            resultado += f"  📆 Vencimiento: {fecha_venc}\n"

                    resultado += "\n"

                return resultado
            else:
                return f"📭 No hay paquetes con tipo de documento '{tipo.upper()}' registrados."

    # No pudo responder con reglas
    return None


def chatbot_groq(pregunta: str, historial: List[Dict]) -> str:
    """
    Chatbot con IA usando Groq (gratis y rápido).
    Se usa cuando las reglas no pueden responder.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)

        # Preparar contexto con información relevante - ENVIAR TODO EL HISTORIAL
        contexto = f"Tienes acceso a {len(historial)} paquetes registrados en total.\n"

        if historial:
            # Incluir TODOS los registros como contexto (máximo 50 para no saturar)
            limite = min(len(historial), 50)
            contexto += f"\nTODOS los registros (mostrando {limite} más recientes):\n"
            for i, pkg in enumerate(historial[-limite:], 1):
                contexto += f"{i}. Código: {get_field(pkg, 'codigoRetiro')}, "
                contexto += f"Destinatario: {get_field(pkg, 'destinatarioNombre')}, "
                contexto += f"Sucursal: {get_field(pkg, 'sucursal')}, "
                contexto += f"Tipo: {get_field(pkg, 'tipoDocumento')}, "
                contexto += f"Fecha: {get_field(pkg, 'fechaRecepcion')} {get_field(pkg, 'horaRecepcion')}\n"

            if len(historial) > 50:
                contexto += f"\n(Hay {len(historial) - 50} paquetes más antiguos no mostrados aquí)\n"
        else:
            contexto += "\nNo hay paquetes registrados aún."

        # Crear prompt para el modelo
        system_prompt = f"""Eres un asistente virtual para un sistema de recepción de paquetes.
Tu trabajo es ayudar a los usuarios con consultas sobre paquetes registrados.

Contexto actual:
{contexto}

Instrucciones:
- Sé amable, conciso y profesional
- Usa emojis para hacer las respuestas más visuales
- Si no tienes información suficiente, sugiere usar la pestaña de Historial
- Responde en español
- Si el usuario pregunta por un código o datos específicos que no tienes, indícalo claramente
"""

        # Llamar a Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pregunta}
            ],
            model="llama-3.3-70b-versatile",  # Modelo actualizado y gratis
            temperature=0.7,
            max_tokens=500,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error al procesar con IA: {str(e)}\n\nPuedes intentar reformular tu pregunta o usar las pestañas de Consultar e Historial."


def chatbot_inteligente(pregunta: str, historial: List[Dict]) -> Tuple[str, str]:
    """
    Función principal del chatbot híbrido.
    Intenta primero con reglas (rápido) y luego con IA (más inteligente).

    Returns:
        Tuple[str, str]: (respuesta, tipo_de_respuesta)
    """
    # Primero intenta con reglas (instantáneo y gratis)
    respuesta_reglas = chatbot_reglas(pregunta, historial)

    if respuesta_reglas:
        return respuesta_reglas, "🎯 Respuesta directa"

    # Si las reglas no funcionaron, usa IA de Groq
    respuesta_ia = chatbot_groq(pregunta, historial)
    return respuesta_ia, "🤖 Respuesta con IA"


# Ejemplos de preguntas sugeridas - ACTUALIZADO con nuevas capacidades
PREGUNTAS_SUGERIDAS = [
    "¿Qué se registró el 1 de diciembre?",
    "¿Cuántos cheques hay registrados?",
    "Muéstrame los paquetes de Santiago",
    "¿Qué paquetes tiene Victor?",
    "Generar dashboard",
    "Listar paquetes por sucursal",
    "¿Cuántas facturas hay?",
    "Enviar recordatorio a Victor",
]
