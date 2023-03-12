import sys


ss_debug = {
    0: 'a',
    1: 'b',
    2: 'c',
    4: 'd',
    8: 'e'
}
ss = {
    0: '\u0020',
    1: '\u00A0',
    2: '\u202F',
    4: '\u2007',
    8: '\u2060'
}
ssi = { v: k for k, v in ss.items() }

def char_encode(c: str) -> str:
    ord_c = ord(c) & 0xFF
    ct = []
    for m_shift in range(8):
        masked = (2 ** m_shift) & ord_c
        ct.append(ss[1] if masked else ss[0])
    return ''.join(ct)

def char_encode_wide(c: str) -> str:
    ord_c = ord(c)
    ct = [''] * 4
    for u_char in range(4):
        for m_shift in range(4):
            masked = (2 ** m_shift) & ord_c
            ct[u_char] += ss[masked]
        ord_c = ord_c >> 4
    return ''.join(ct)

def char_decode(c: str) -> str:
    acc = 0
    for m_shift in range(8):
        acc += (2 ** m_shift) * ssi[c[m_shift]]
    return chr(acc)

def char_decode_wide(s: str) -> str:
    acc = [0] * 4
    for u_char in range(4):
        for code_point in range(4):
            sp = s[u_char*4 + code_point]
            acc[u_char] += ssi[sp]
        acc[u_char] *= (16**u_char)
    return chr(sum(acc))

def bwt(s: str) -> str:
    s = '\u0002' + s + '\u0003'
    r = [s[i:] + s[:i] for i in range(len(s))]
    s = sorted(r, key=str.lower)
    return ''.join([a[-1] for a in s])

def ibwt(r: str) -> str:
    table = [''] * len(r)
    for i in range(len(r)):
        table = sorted(r[i] + table[i] for i in range(len(r)))
    s = [row for row in table if row.endswith('\u0003')][0]
    return s.rstrip('\u0003').strip('\u0002')

def sp_enc(s: str) -> str:
    return ''.join([char_encode(c) for c in s])

def sp_dec(s: str) -> str:
    acc = []
    for slide in range(0, len(s), 8):
        acc += char_decode(s[slide:slide+8])
    return ''.join(acc)

def help():
    print('python3 sp.py enc|dec [str] # or stdin')

if __name__ == '__main__':
    verb = sys.argv[1]
    if len(sys.argv) < 2:
        help()
    data = sys.stdin.read() if len(sys.argv) == 2 else sys.argv[2]
    if  verb == 'dec':
        print(sp_dec(data), end='')
    elif verb == 'enc':
        print(sp_enc(data), end='')
    else:
        help()
