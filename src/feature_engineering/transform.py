import pandas as pd
from settings import DATABASE_URL
from datetime import datetime, timedelta


class BaseTransform:
    def process():
        pass


class PandasTransform(BaseTransform):
    def __get_age(self, value):
        try:
            birthdate = datetime.strptime(value, "%Y-%m-%d")
            today = datetime.now()
            delta = (today - birthdate) / timedelta(days=365)
            return int(delta)
        except:
            return None

    def __convert_num(self, value):
        try:
            return int(value)
        except:
            return value

    def process(self):
        try:
            df = pd.read_sql_table("dynamic_feature", DATABASE_URL)
            df["entry_value"] = df["entry_value"].apply(self.__convert_num)

            # grouped = df.groupby(["entity_key", "entry_name"], as_index=False).agg(
            #     entry_value=("entry_value", "sum"),
            #     entry_value_count=("entry_value", "count"),
            #     date=("date", "first"),
            # )

            pivotdf = df.pivot_table(
                index=["entity_key"],
                columns=["entry_name"],
                values=["entry_value"],
                aggfunc=["count", "sum"],
            )

            pivotdf.columns = [
                f"{col[0]}-{col[len(col) -1]}"
                if col[0] == "count"
                else col[len(col) - 1]
                for col in pivotdf.columns
            ]
            pivotdf["age"] = pivotdf["birthday"].apply(self.__get_age)
            return pivotdf.to_dict("records")

        except Exception as e:
            print(e)
            raise Exception("transformation error")
