import meraki

# Create a dashboard API instance with test key
dashboard = meraki.DashboardAPI('test', suppress_logging=True)

# Get all categories and their method counts
categories = {}
for attr in dir(dashboard):
    if not attr.startswith('_'):
        obj = getattr(dashboard, attr)
        if hasattr(obj, '__class__') and 'meraki' in str(obj.__class__):
            methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
            categories[attr] = len(methods)

# Print results
print("Official Meraki SDK Method Counts:")
print("=" * 40)
total = 0
for cat, count in sorted(categories.items()):
    print(f"{cat}: {count} methods")
    total += count
print("=" * 40)
print(f"TOTAL: {total} methods")
