# Simple sample file to exercise completions and verify syntax
def generate_report(data):
    """Generate a simple report from a list of dicts with 'value' keys."""
    total = 0
    for item in data:
        total += item.get('value', 0)
    avg = total / len(data) if data else 0
    return {"total": total, "average": avg}


if __name__ == "__main__":
    sample = [{"value": 10}, {"value": 20}, {"value": 5}]
    print(generate_report(sample))
