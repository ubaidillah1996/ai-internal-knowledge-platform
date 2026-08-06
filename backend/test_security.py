from app.core.security import hash_password


password = "hello123"

hashed = hash_password(password)


print(hashed)