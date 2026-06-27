import base64, zlib, sys
content = sys.stdin.read()
encoded = base64.b64encode(zlib.compress(content.encode())).decode()
with open('encoded_output.txt', 'w') as f:
    f.write(encoded)
print(f'Done. Length: {len(encoded)}')
