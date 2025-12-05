"""
Database module for PostgreSQL storage
"""
import os
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
Base = declarative_base()

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_recepcion = Column(String, nullable=False)
    hora_recepcion = Column(String, nullable=False)
    sucursal = Column(String, nullable=False)
    recepcionista = Column(String, nullable=False)
    proveedor = Column(String, nullable=False)
    tipo_documento = Column(String, nullable=False)
    numero_documento = Column(String, nullable=False)
    destinatario_nombre = Column(String, nullable=False)
    destinatario_email = Column(String, nullable=False)
    medio_notificacion = Column(String, nullable=False)
    codigo_retiro = Column(String, nullable=False, unique=True)
    estado = Column(String, nullable=False, default="Pendiente")
    fecha_notificacion = Column(String, nullable=True)
    destinatario_confirmo = Column(String, nullable=True)
    fecha_retiro = Column(String, nullable=True)
    entregado_a = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    adjunto_url = Column(String, nullable=True)
    monto_cheque = Column(String, nullable=True)
    fecha_vencimiento_cheque = Column(String, nullable=True)

# Initialize database connection
def get_engine():
    if not DATABASE_URL:
        # Fallback to SQLite for local development
        db_url = "sqlite:///./paquetes.db"
    else:
        # Fix Railway's postgres:// to postgresql://
        db_url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    return create_engine(db_url)

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
