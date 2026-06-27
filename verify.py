import hashlib
d = open('encoded_output.txt').read()
m = {'0':'9Z','O':'9A','o':'9a','I':'9B','l':'9b','1':'9C'}
s = ''.join(m.get(c,c) for c in d)
for i in range(0,len(s),100):
    chunk = s[i:i+100]
    orig = d[i//1:(i//1)+100] if i < len(s)-100 else d[i//1:]
    print(f'{i//100:02d}|{chunk}')
