import sqlite3, os

path = os.path.join(os.path.dirname(__file__), "crm.db")
size = os.path.getsize(path)
print(f"Archivo: crm.db ({size} bytes)")
print(f"Ubicacion: {path}")

conn = sqlite3.connect(path)
tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()

print(f"\nTablas encontradas: {len(tables)}\n")
for t in tables:
    count = conn.execute(f"SELECT COUNT(*) FROM [{t[0]}]").fetchone()[0]
    print(f"  - {t[0]}: {count} registros")

print("\n--- Esquema detallado ---")
for t in tables:
    print(f"\n  > {t[0]}")
    cols = conn.execute(f"PRAGMA table_info([{t[0]}])").fetchall()
    for c in cols:
        pk = "PK" if c[5] else ""
        nn = "NOT NULL" if c[3] else ""
        extras = " | ".join(filter(None, [pk, nn]))
        print(f"    - {c[1]} ({c[2]}) {extras}")

conn.close()
print("\n--- Conexion cerrada ---")
