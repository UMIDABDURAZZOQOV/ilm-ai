print("Importing services.db...")
try:
    from services.db import engine
    print("Engine imported:", engine)
except Exception as e:
    print("Error importing:", e)
