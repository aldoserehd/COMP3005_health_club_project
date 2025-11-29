from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Numeric
)
from sqlalchemy.orm import relationship
from .base import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    phone = Column(String(30), nullable=True)

    fitness_goal = Column(String(255), nullable=True)
    target_weight = Column(Float, nullable=True)

    health_metrics = relationship("HealthMetric", back_populates="member")
    pt_sessions = relationship("PTSession", back_populates="member")
    invoices = relationship("Invoice", back_populates="member")


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    specialty = Column(String(100), nullable=True)

    pt_sessions = relationship("PTSession", back_populates="trainer")
    class_sessions = relationship("ClassSession", back_populates="trainer")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)

    pt_sessions = relationship("PTSession", back_populates="room")
    class_sessions = relationship("ClassSession", back_populates="room")


class ClassSession(Base):
    __tablename__ = "class_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)

    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)

    room = relationship("Room", back_populates="class_sessions")
    trainer = relationship("Trainer", back_populates="class_sessions")


class PTSession(Base):
    __tablename__ = "pt_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="scheduled")

    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    member = relationship("Member", back_populates="pt_sessions")
    trainer = relationship("Trainer", back_populates="pt_sessions")
    room = relationship("Room", back_populates="pt_sessions")


class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    recorded_at = Column(DateTime, nullable=False)
    weight = Column(Float, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)

    member = relationship("Member", back_populates="health_metrics")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="unpaid")
    description = Column(String(255), nullable=True)

    member = relationship("Member", back_populates="invoices")
