import base64
import zlib

flag = 'ctfcup{bUnd1eD_pyTh0n-ReV-fr0m-0peN5ourCe}'

correct = str([e for e in base64.b64encode(zlib.compress(flag.encode()))])
tmpl = open('./checker.tmpl').read()
tmpl = tmpl.replace('{{ CORRECT }}', correct)
with open('./checker/__init__.py', 'w') as fout:
    fout.write(tmpl)
