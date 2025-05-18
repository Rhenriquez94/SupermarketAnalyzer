from connect import connect

try:
    engine = connect()
    with engine.connect() as conn:
        result = conn.execute("SELECT version();")
        for row in result:
            print("✅ Conectado a:", row[0])
except Exception as e:
    print("❌ Error de conexión:", e)