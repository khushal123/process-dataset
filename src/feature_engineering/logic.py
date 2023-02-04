from datetime import datetime
from sqlalchemy import func, text
from abc import ABC, abstractmethod
import pandas as pd
import logging
from .models import db, Feature, DynamicFeature, MasterKeys
from settings import DATABASE_URL
from .helpers import group_by_key
import pdb

logger = logging.getLogger("logic.py")


class BaseFeatureLogic(ABC):
    @abstractmethod
    def save_fl(self) -> bool | str:
        pass

    @abstractmethod
    def get_fl(self, feature_data):
        pass


class DynamicFeatureLogic(BaseFeatureLogic):
    def __init__(self):
        self.melt_id_vars = ["employee_id", "salary_raise", "date", "birthday"]

        self.master_keys = ["employee_id"]
        self.entity_keys = ["entity"]

    def save_fl(self, feature_data) -> bool | str:
        try:
            logger.debug("grouping")
            grouped_feature_data = group_by_key(
                feature_data=feature_data, key="employee_id"
            )
            # logger.debug(grouped_feature_data)
            db.session.bulk_insert_mappings(MasterKeys, grouped_feature_data.get("parents"))
            db.session.bulk_insert_mappings(DynamicFeature, grouped_feature_data.get("children"))
            db.session.commit()
            return grouped_feature_data

        except Exception as e:
            raise e

    def get_fl(self):
        """ """
        df = pd.read_sql_table("dynamic_feature", DATABASE_URL)
        print(df)
        # df_unmelt = df.pivot(index='id', columns=["entry_name"])
        # print(df_unmelt)

        return "done"


class FeatureLogic(BaseFeatureLogic):
    def save_fl(self, feature_data: list) -> bool | str:
        try:
            models = []
            for item in feature_data:
                salary_raise = (
                    item.get("value") if item.get("entity") == "salary_raise" else -1
                )
                # 2020-01-01
                feature = Feature(
                    employee_id=item["employee_id"],
                    salary_raise=salary_raise,
                    date=datetime.strptime(item.get("date"), "%Y-%m-%d"),
                )
                if item.get("entity") == "birthday":
                    birthday = datetime.strptime(item.get("value"), "%Y-%m-%d")
                    feature.birthday = birthday
                models.append(feature)

        except:
            return "Unknown column"
        return True

    def get_fl(self):
        """
        query=SELECT employee_id, (SELECT DATE_FORMAT(FROM_DAYS(DATEDIFF(now(),birthday)), '%Y')+0 AS age FROM features f2
                WHERE birthday IS NOT NULL
                AND
                f2.employee_id=f1.employee_id
                GROUP BY age) AS age,
                COUNT(salary_raise), SUM(salary_raise) FROM features f1
                WHERE salary_raise <> -1
                GROUP BY employee_id, age;

        """

        try:
            subquery = (
                db.session.query(
                    Feature.employee_id,
                    (
                        func.DATE_FORMAT(
                            func.FROM_DAYS(
                                func.DATEDIFF(text("now()"), Feature.birthday)
                            ),
                            "%Y",
                        )
                        + 0
                    ).label("age_alias"),
                )
                .filter(
                    Feature.birthday.isnot(None),
                    Feature.employee_id == Feature.employee_id,
                )
                .subquery()
            )

            records = (
                db.session.query(
                    Feature.employee_id,
                    subquery.c.age_alias,
                    func.count(Feature.salary_raise).label("count_salary_raise"),
                    func.sum(Feature.salary_raise).label("total_salary_raise"),
                )
                .filter(Feature.salary_raise != -1)
                .join(subquery, Feature.employee_id == subquery.c.employee_id)
                .group_by(Feature.employee_id, subquery.c.age_alias)
                .all()
            )

            response = []
            for row in records:
                response.append(dict(row))
            return response

        except:
            return False


class LogicFactory:
    def __init__(self, dbtype="feature"):
        self.__logic = {
            "feature": FeatureLogic(),
            "dynamic_feature": DynamicFeatureLogic(),
        }

    def get_logic(self, dbtype) -> FeatureLogic | DynamicFeatureLogic:
        print(self.__logic.get(dbtype))
        return self.__logic.get(dbtype, FeatureLogic())
