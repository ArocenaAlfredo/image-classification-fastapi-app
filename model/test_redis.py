import redis

try:
    db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    response = db.ping()
    print("✅ Redis is accessible:", response)
except Exception as e:
    print("❌ Could not connect to Redis:", str(e))

