from feature_engineering.models import Features, db
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import aliased

import json

class FeatureLogic():

    @classmethod
    def _save(cls, feature_data:list):
        try:
            models = []
            for item in feature_data:
                salary_raise = item.get("value") if item.get("entity") == "salary_raise" else -1
                # 2020-01-01
                feature = Features(
                    employee_id=item['employee_id'],
                    salary_raise = salary_raise,
                    date = datetime.strptime(item.get("date"), '%Y-%m-%d')
                )
                if(item.get("entity") == "birthday"):
                    birthday = datetime.strptime(item.get("value"), '%Y-%m-%d')
                    feature.birthday = birthday
                models.append(feature)
            
            db.session.add_all(models)
            db.session.commit()
        except:
            return "Unknown column" 
        return True

    
    @classmethod
    def _get(cls):
        """
        query=SELECT employee_id,  (SELECT DATE_FORMAT(FROM_DAYS(DATEDIFF(now(),birthday)), '%Y')+0 AS age FROM features f2 
                WHERE birthday IS NOT NULL
                AND
                f2.employee_id=f1.employee_id
                GROUP BY age) AS age,
                COUNT(salary_raise), SUM(salary_raise) FROM features f1
                WHERE salary_raise <> -1
                GROUP BY employee_id, age;

        response = {
                "calculated": [
                    {
                        "employee_id": 0,
                        "count": 9,
                        "sum": 327.0
                    },
                    {
                        "employee_id": 1,
                        "count": 9,
                        "sum": 207.0
                    }
                ]
            }
            
        """

        ft1 = aliased(Features, name="ft1")
        ft2 = aliased(Features, name="ft2")

        subquery = db.session.query(
            func.date_format(
                func.from_days(
                    func.datediff(func.now(), ft1.birthday)
                )
            ).label("age")
        ).filter(ft1.employee_id==ft2.employee_id).group_by("age")

        records = db.session.execute(db.select(aliased(subquery, "age"), Features.employee_id, func.count(Features.salary_raise), func.sum(Features.salary_raise)).group_by(Features.employee_id).filter(Features.salary_raise!=None)).all()
        response = []
        for record in records:
            r = {
                "employee_id": record[0],
                "count": record[1],
                "sum": record[1]
            }
            response.append(dict(record))
        return response
         