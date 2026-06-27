import os
lines = open(r'C:\VesuviusChallenge\phi_output.txt', 'r', encoding='utf-16').readlines()
print(f'Total lines: {len(lines)}')
os.makedirs(r'C:\VesuviusChallenge\chunks2', exist_ok=True)
for i in range(0, len(lines), 48):
    chunk = lines[i:i+48]
    fn = rf'C:\VesuviusChallenge\chunks2\c{i:03d}.txt'
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(''.join(chunk))
    print(f'c{i:03d}.txt: {len(chunk)} lines')
print('Done')
