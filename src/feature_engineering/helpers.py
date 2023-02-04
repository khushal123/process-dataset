from itertools import groupby
from operator import itemgetter
from datetime import datetime
import pdb


def group_by_key(feature_data, key) -> dict:
    grouped_dict: dict = {"parents": [], "children": []}
    for key, group in groupby(feature_data, key=itemgetter("employee_id")):
        grouped_dict["parents"].append(
            {"entity_key": key, "entity_name": "employee_id"}
        )
        for item in list(group):
            grouped_dict["children"].append(
                {
                    "entry_name": item.get("entity"),
                    "entry_value": str(item.get('value')),
                    "entity_key": item.get("employee_id"),
                    "date": item.get("date") 
                }
            )
    return grouped_dict
