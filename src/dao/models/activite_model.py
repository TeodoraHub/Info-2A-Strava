from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# 1. Database Configuration
# Assumes SQLite for simplicity. Update the URL for PostgreSQL/MySQL if needed.
DATABASE_URL = "sqlite:///./striv.db"

# 2. Create the Database Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Define the Base class for all models
Base = declarative_base()


class ActivityModel(Base):
    __tablename__ = 'activite'

    # The actual database column is 'id_activite'
    id = Column('id_activite', Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    description = Column(String)
    sport = Column(String, nullable=False)
    date_activite = Column(Date, nullable=False)
    lieu = Column(String)
    distance = Column(Float, nullable=False)
    duree = Column(Time, nullable=True)

    # Foreign Key relation to the 'utilisateur' table's primary key 'id_user'
    id_user = Column(Integer, ForeignKey('utilisateur.id_user'), nullable=False)

    # Relationships (ensure these class names match the actual class names in other files)
    user = relationship("UtilisateurModel", back_populates="activities")
    comments = relationship("Commentaire", back_populates="activite", cascade="all, delete-orphan")
    likes = relationship("LikeModel", back_populates="activity", cascade="all, delete-orphan")