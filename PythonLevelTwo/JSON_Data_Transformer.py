import json
import operator

def transform_data(
    input_file: str,
    output_file: str,
    filters: dict = None,
    field_mapping: dict = None,
    sort_by: str = None
) -> int:

    # Load records
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Apply filtering
    if filters:
        ops = {
            "==": operator.eq,
            "!=": operator.ne,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
        }

        def record_matches(rec):
            for field, (op_symbol, value) in filters.items():
                if field not in rec:
                    return False
                if not ops[op_symbol](rec[field], value):
                    return False
            return True

        data = [rec for rec in data if record_matches(rec)]

    # Transform field names
    if field_mapping:
        transformed = []
        for rec in data:
            new_rec = {}
            for old_field, val in rec.items():
                new_field = field_mapping.get(old_field, old_field)
                new_rec[new_field] = val
            transformed.append(new_rec)
        data = transformed

    # Sort results safely
    if sort_by:
        data = sorted(data, key=lambda x: x.get(sort_by, ""))

    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return len(data)


# Example usage
transform_data(
    r"C:\Users\9901201\OneDrive - AutomatonsX\Desktop\Python_Code\PythonLevelTwo\user.json",
    "active_adults.json",
    filters={'age': ('>=', 18), 'status': ('==', 'active'),'user_name':("==",'Alice')},
    field_mapping={'user_name': 'name', 'user_email': 'email'},
    sort_by='name'
)

