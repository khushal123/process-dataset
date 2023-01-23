from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint

db:SQLAlchemy = SQLAlchemy()

class Features(db.Model):
    id:int = Column(Integer, primary_key=True)
    employee_id:int = Column(Integer, )
    salary_raise:str = Column(String(20), nullable=True)
    birthday:datetime.date = Column(Date, nullable=True)
    date: datetime.date = Column(Date, nullable=False)

    UniqueConstraint(
        'employee_id', 
        'salary_raise',
        'e_s_1'
    )

    UniqueConstraint(
        'employee_id', 
        'birthday',
        'e_s_2'
    )