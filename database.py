from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import conf.properties as props

#cambiar segun DB
SQLALCHEMY_DATABASE_URL = props.SQLALCHEMY_DATABASE_URL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

#check same thread es solo para SQL Lite,ver clase
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Cada Instancia de esta clase= una sesion 
#contra la base
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, 
                            bind=engine)

#La clase madre del ORM
#cada instancia de la clase 
# sera una objeto-tabla 
Base = declarative_base()