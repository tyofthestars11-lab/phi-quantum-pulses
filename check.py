import hashlib
b=open("b64_00.txt").read()
print(len(b))
print(hashlib.sha256(b.encode()).hexdigest()[:16])
for i in range(0,3100,50):
    print(f"{i//50:02d}:{b[i:i+50]}")
