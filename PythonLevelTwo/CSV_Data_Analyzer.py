import csv
from statistics import mean, median

def analyze_csv(file_path: str) -> dict:
    """
    Returns a summary report:
    {
        "numeric_stats": {
            "age": {"min": 18, "max": 45, "mean": 27.5, "median": 26}
        },
        "categorical_unique": {
            "city": ["NY", "LA", "TX"]
        },
        "missing_values": {
            "name": 2,
            "age": 0
        },
        "total_rows": 100
    }
    """

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total_rows = len(rows)
    if total_rows == 0:
        return {"error": "CSV file is empty"}

    # Determine column types & initialize containers
    numeric_columns = {}
    categorical_columns = {}
    missing_counts = {}

    # First pass: find missing values & separate types
    for col in reader.fieldnames:
        missing_counts[col] = 0
        numeric_columns[col] = []
        categorical_columns[col] = set()

    for row in rows:
        for col, val in row.items():
            if val == "" or val is None:
                missing_counts[col] += 1
                continue

            # Try converting to a number
            try:
                numeric_columns[col].append(float(val))
            except ValueError:
                categorical_columns[col].add(val)

    # Build summary stats
    numeric_stats = {}

    for col, values in numeric_columns.items():
        if len(values) > 0:
            numeric_stats[col] = {
                "min": min(values),
                "max": max(values),
                "mean": round(mean(values), 2),
                "median": round(median(values), 2)
            }
        else:
            numeric_columns[col] = None  # mark non-numeric

    categorical_unique = {
        col: list(vals)
        for col, vals in categorical_columns.items()
        if len(vals) > 0
    }

    return {
        "numeric_stats": numeric_stats,
        "categorical_unique": categorical_unique,
        "missing_values": missing_counts,
        "total_rows": total_rows
    }
result = analyze_csv(r"C:\Users\9901201\OneDrive - AutomatonsX\Desktop\Python_Code\PythonLevelTwo\sample.csv")

print("\n📊 CSV Summary Report\n")
print("Total Rows:", result["total_rows"])

print("\nNumeric Stats:")
for col, stats in result["numeric_stats"].items():
    print(f" {col}: {stats}")

print("\nUnique Values (Categorical):")
for col, vals in result["categorical_unique"].items():
    print(f" {col}: {vals}")

print("\nMissing Values:")
for col, count in result["missing_values"].items():
    print(f" {col}: {count}")
