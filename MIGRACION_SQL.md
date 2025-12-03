# 🗄️ Migración a Base de Datos SQL

Esta guía te ayudará a migrar del sistema actual (Excel) a una base de datos SQL más robusta y escalable.

---

## 🎯 Beneficios de Usar SQL

| Característica | Excel | SQL Database |
|----------------|-------|--------------|
| **Concurrencia** | ❌ Problemas con múltiples usuarios | ✅ Miles de usuarios simultáneos |
| **Velocidad** | ❌ Lento con >10,000 registros | ✅ Rápido con millones de registros |
| **Búsquedas** | ❌ Limitadas | ✅ Consultas complejas y rápidas |
| **Integridad** | ❌ Puede corromperse | ✅ Transacciones ACID |
| **Backup** | ❌ Manual | ✅ Automático |
| **Relaciones** | ❌ Difícil | ✅ Relaciones nativas |
| **APIs** | ❌ No nativo | ✅ Integración fácil |

---

## 📦 Opción 1: SQL Server (Recomendado para Corporativo)

### Ventajas
- ✅ Integración nativa con Microsoft 365
- ✅ Soporte empresarial
- ✅ Azure SQL Database disponible
- ✅ Herramientas visuales (SSMS)

### Instalación Local

#### 1. Descargar SQL Server Express (Gratis)
```
https://www.microsoft.com/es-es/sql-server/sql-server-downloads
```

#### 2. Instalar SQL Server Management Studio (SSMS)
```
https://aka.ms/ssmsfullsetup
```

#### 3. Crear la Base de Datos

```sql
CREATE DATABASE PaquetesDB;
GO

USE PaquetesDB;
GO

CREATE TABLE Paquetes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fechaRecepcion DATE NOT NULL,
    horaRecepcion TIME NOT NULL,
    sucursal NVARCHAR(50) NOT NULL,
    recepcionista NVARCHAR(100) NOT NULL,
    proveedor NVARCHAR(100) NOT NULL,
    tipoDocumento NVARCHAR(50) NOT NULL,
    numeroDocumento NVARCHAR(100) NOT NULL,
    destinatarioNombre NVARCHAR(200) NOT NULL,
    destinatarioEmail NVARCHAR(200) NOT NULL,
    medioNotificacion NVARCHAR(50) NOT NULL,
    codigoRetiro NVARCHAR(50) UNIQUE NOT NULL,
    estado NVARCHAR(50) DEFAULT 'Pendiente',
    fechaNotificacion DATETIME,
    destinatarioConfirmo BIT DEFAULT 0,
    fechaRetiro DATETIME,
    entregadoA NVARCHAR(200),
    observaciones NVARCHAR(MAX),
    adjuntoUrl NVARCHAR(500),
    creadoEn DATETIME DEFAULT GETDATE()
);
GO

-- Índices para búsquedas rápidas
CREATE INDEX IX_Paquetes_CodigoRetiro ON Paquetes(codigoRetiro);
CREATE INDEX IX_Paquetes_Email ON Paquetes(destinatarioEmail);
CREATE INDEX IX_Paquetes_Fecha ON Paquetes(fechaRecepcion);
CREATE INDEX IX_Paquetes_Estado ON Paquetes(estado);
GO
```

#### 4. Instalar Dependencias Python

```bash
pip install pyodbc sqlalchemy
```

#### 5. String de Conexión

```env
# En .env
SQL_SERVER_CONNECTION=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=PaquetesDB;Trusted_Connection=yes;
```

---

## 🐘 Opción 2: PostgreSQL (Recomendado para Open Source)

### Ventajas
- ✅ Completamente gratis
- ✅ Muy robusto
- ✅ Excelente para JSON
- ✅ Multi-plataforma

### Instalación

#### 1. Descargar PostgreSQL
```
https://www.postgresql.org/download/
```

#### 2. Instalar pgAdmin (Interfaz Visual)
Viene incluido con PostgreSQL

#### 3. Crear la Base de Datos

```sql
CREATE DATABASE paquetesdb;

\c paquetesdb;

CREATE TABLE paquetes (
    id SERIAL PRIMARY KEY,
    fecha_recepcion DATE NOT NULL,
    hora_recepcion TIME NOT NULL,
    sucursal VARCHAR(50) NOT NULL,
    recepcionista VARCHAR(100) NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(50) NOT NULL,
    numero_documento VARCHAR(100) NOT NULL,
    destinatario_nombre VARCHAR(200) NOT NULL,
    destinatario_email VARCHAR(200) NOT NULL,
    medio_notificacion VARCHAR(50) NOT NULL,
    codigo_retiro VARCHAR(50) UNIQUE NOT NULL,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    fecha_notificacion TIMESTAMP,
    destinatario_confirmo BOOLEAN DEFAULT FALSE,
    fecha_retiro TIMESTAMP,
    entregado_a VARCHAR(200),
    observaciones TEXT,
    adjunto_url VARCHAR(500),
    creado_en TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_codigo_retiro ON paquetes(codigo_retiro);
CREATE INDEX idx_email ON paquetes(destinatario_email);
CREATE INDEX idx_fecha ON paquetes(fecha_recepcion);
CREATE INDEX idx_estado ON paquetes(estado);
```

#### 4. Instalar Dependencias

```bash
pip install psycopg2-binary sqlalchemy
```

#### 5. String de Conexión

```env
# En .env
POSTGRES_CONNECTION=postgresql://postgres:tu_password@localhost:5432/paquetesdb
```

---

## 🪶 Opción 3: SQLite (Más Sencillo, Para Empezar)

### Ventajas
- ✅ No requiere instalación de servidor
- ✅ Archivo único portátil
- ✅ Perfecto para desarrollo/pequeñas empresas
- ✅ Viene con Python

### Configuración

#### 1. Crear script de migración

Crea `backend/init_sqlite.py`:

```python
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "paquetes.db"
DB_PATH.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS paquetes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_recepcion TEXT NOT NULL,
    hora_recepcion TEXT NOT NULL,
    sucursal TEXT NOT NULL,
    recepcionista TEXT NOT NULL,
    proveedor TEXT NOT NULL,
    tipo_documento TEXT NOT NULL,
    numero_documento TEXT NOT NULL,
    destinatario_nombre TEXT NOT NULL,
    destinatario_email TEXT NOT NULL,
    medio_notificacion TEXT NOT NULL,
    codigo_retiro TEXT UNIQUE NOT NULL,
    estado TEXT DEFAULT 'Pendiente',
    fecha_notificacion TEXT,
    destinatario_confirmo INTEGER DEFAULT 0,
    fecha_retiro TEXT,
    entregado_a TEXT,
    observaciones TEXT,
    adjunto_url TEXT,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Índices
cursor.execute("CREATE INDEX IF NOT EXISTS idx_codigo_retiro ON paquetes(codigo_retiro)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON paquetes(destinatario_email)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_fecha ON paquetes(fecha_recepcion)")

conn.commit()
conn.close()

print(f"✅ Base de datos creada en: {DB_PATH}")
```

#### 2. Ejecutar

```bash
cd backend
python init_sqlite.py
```

#### 3. String de Conexión

```env
# En .env
SQLITE_DB_PATH=./data/paquetes.db
```

---

## 🔄 Código Backend Actualizado

Crea `backend/database.py`:

```python
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Elegir base de datos según .env
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite, postgres, sqlserver

if DB_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{os.getenv('SQLITE_DB_PATH', './data/paquetes.db')}"
elif DB_TYPE == "postgres":
    DATABASE_URL = os.getenv("POSTGRES_CONNECTION")
elif DB_TYPE == "sqlserver":
    DATABASE_URL = os.getenv("SQL_SERVER_CONNECTION")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Paquete(Base):
    __tablename__ = "paquetes"

    id = Column(Integer, primary_key=True, index=True)
    fecha_recepcion = Column(String, nullable=False)
    hora_recepcion = Column(String, nullable=False)
    sucursal = Column(String(50), nullable=False)
    recepcionista = Column(String(100), nullable=False)
    proveedor = Column(String(100), nullable=False)
    tipo_documento = Column(String(50), nullable=False)
    numero_documento = Column(String(100), nullable=False)
    destinatario_nombre = Column(String(200), nullable=False)
    destinatario_email = Column(String(200), nullable=False)
    medio_notificacion = Column(String(50), nullable=False)
    codigo_retiro = Column(String(50), unique=True, nullable=False, index=True)
    estado = Column(String(50), default="Pendiente")
    fecha_notificacion = Column(DateTime)
    destinatario_confirmo = Column(Boolean, default=False)
    fecha_retiro = Column(DateTime)
    entregado_a = Column(String(200))
    observaciones = Column(Text)
    adjunto_url = Column(String(500))
    creado_en = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
```

Actualiza `backend/main.py`:

```python
from database import SessionLocal, Paquete
from sqlalchemy.exc import IntegrityError

# ... (mantener imports anteriores)

@app.post("/register", response_model=PackageOut)
def register_package(pkg: PackageIn):
    db = SessionLocal()

    try:
        # Crear registro en base de datos
        db_paquete = Paquete(
            fecha_recepcion=pkg.fechaRecepcion,
            hora_recepcion=pkg.horaRecepcion,
            sucursal=pkg.sucursal,
            recepcionista=pkg.recepcionista,
            proveedor=pkg.proveedor,
            tipo_documento=pkg.tipoDocumento,
            numero_documento=pkg.numeroDocumento,
            destinatario_nombre=pkg.destinatarioNombre,
            destinatario_email=pkg.destinatarioEmail,
            medio_notificacion=pkg.medioNotificacion,
            codigo_retiro=pkg.codigoRetiro,
            observaciones=pkg.observaciones,
            adjunto_url=pkg.adjuntoUrl
        )

        db.add(db_paquete)
        db.commit()
        db.refresh(db_paquete)

        # Enviar notificaciones (código existente)
        notified = False
        if pkg.medioNotificacion in ("Correo", "Ambos"):
            ok_mail = send_email_graph(...)
            notified = notified or ok_mail

        if notified:
            db_paquete.estado = "Notificado"
            db_paquete.fecha_notificacion = datetime.now()
            db.commit()

        return {
            "id": str(db_paquete.id),
            "estado": db_paquete.estado
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Código de retiro duplicado")
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error: {str(e)}")
    finally:
        db.close()

@app.get("/consultar/{codigo}")
def consultar_paquete(codigo: str):
    db = SessionLocal()
    try:
        paquete = db.query(Paquete).filter(
            Paquete.codigo_retiro == codigo
        ).first()

        if not paquete:
            raise HTTPException(404, "Paquete no encontrado")

        return paquete
    finally:
        db.close()
```

---

## 📊 Comparación de Opciones

| Característica | SQLite | PostgreSQL | SQL Server |
|----------------|---------|-----------|------------|
| **Instalación** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Rendimiento** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Escalabilidad** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Costo** | Gratis | Gratis | Express gratis |
| **Soporte** | Comunidad | Excelente | Microsoft |
| **Herramientas** | Básicas | pgAdmin | SSMS |

---

## 🚀 Migración de Datos Excel → SQL

Script para migrar datos existentes:

```python
# backend/migrate_excel_to_sql.py
import pandas as pd
from database import SessionLocal, Paquete

# Leer Excel
df = pd.read_excel("./data/recepcion_paquetes.xlsx", sheet_name="RecepcionLog")

db = SessionLocal()

for _, row in df.iterrows():
    paquete = Paquete(
        fecha_recepcion=row['FechaRecepcion'],
        hora_recepcion=row['HoraRecepcion'],
        sucursal=row['Sucursal'],
        # ... mapear todas las columnas
    )
    db.add(paquete)

db.commit()
print(f"✅ Migrados {len(df)} registros")
```

---

## ✅ Recomendación Final

**Para tu caso corporativo, recomiendo:**

1. **Comenzar con SQLite** (si < 100 paquetes/día)
   - Fácil de configurar
   - Cero mantenimiento
   - Migración simple

2. **Migrar a PostgreSQL** (cuando > 100 paquetes/día o múltiples usuarios)
   - Gratis
   - Muy robusto
   - Fácil de escalar

3. **Considerar SQL Server** (si ya usan Microsoft Stack)
   - Integración nativa con Azure
   - Soporte empresarial
   - Herramientas Microsoft

---

¿Quieres que implemente la opción SQLite para empezar? Es la más simple y puedes migrar después sin cambiar código.
