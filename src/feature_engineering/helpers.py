from itertools import groupby
from operator import itemgetter
def group_by_key(feature_data, key) -> list[dict]:
    key_func = lambda x: x["employee_id"]
    grouped_list: list[dict] = []
    for key, group in groupby(feature_data, key=itemgetter("employee_id")):
        print(key, group)
        grouped_list.append(
            {
                "employee_id": key,
                "data": list(group)
            }
        )
    return grouped_list