encoded = open('encoded_output.txt').read()
cmd = 'python -c "import base64,zlib;open(r' + "'" + r'C:\VesuviusChallenge\phi_scroll_decode.py' + "'" + ",'w',newline=" + "'" + r'\n' + "'" + ").write(zlib.decompress(base64.b64decode(b'" + encoded + "')).decode())" + '"'
open('decode_command.txt','w').write(cmd)
print('Command file written, length:', len(cmd))
