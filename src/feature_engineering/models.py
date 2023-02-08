from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

db: SQLAlchemy = SQLAlchemy()


class Feature(db.Model):
    id: int = Column(Integer, primary_key=True)
    employee_id: int = Column(
        Integer,
    )
    salary_raise: str = Column(String(20), nullable=True)
    birthday: datetime.date = Column(Date, nullable=True)
    date: datetime.date = Column(Date, nullable=False)

    UniqueConstraint("employee_id", "salary_raise", "e_s_1")

    UniqueConstraint("employee_id", "birthday", "e_s_2")


class MasterKeys(db.Model):

    __tablename__ = "master_keys"

    id: int = Column(Integer, primary_key=True)
    entity_key: int = Column(Integer, unique=True)
    entity_key_mame = Column(String(30))
    dynamic_feature = relationship(
        "DynamicFeature", backref="dynamic_feature", lazy="noload"
    )


class DynamicFeature(db.Model):

    __tablename__ = "dynamic_feature"

    id: int = Column(Integer, primary_key=True)
    entry_name: str = Column(String(30), nullable=False)
    entry_value: str = Column(String(50), nullable=False)
    entity_key: int = Column(Integer, ForeignKey("master_keys.entity_key"))
    date: date = Column(Date)
