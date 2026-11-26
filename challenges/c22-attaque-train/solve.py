"""c22 - Attaque du train : Morse (telegraphe.png) -> Vigenere cle RENO."""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = Path(__file__).parent
MORSE = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H',
 '..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q',
 '.-.':'R','...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z'}


def read_morse():
    a = np.asarray(Image.open(HERE / 'data' / 'telegraphe.png').convert('L')).astype(int)
    reg = a[550:720, 15:1015] < 90
    lab, _ = ndimage.label(reg)
    comps = []
    for i, s in enumerate(ndimage.find_objects(lab)):
        if (lab[s] == i + 1).sum() < 3:
            continue
        comps.append(((s[0].start + s[0].stop) / 2, s[1].start, s[1].stop, s[1].stop - s[1].start))
    comps.sort()
    lines = []
    for c in comps:
        if lines and abs(c[0] - lines[-1][-1][0]) < 10:
            lines[-1].append(c)
        else:
            lines.append([c])
    words = []
    for L in lines:
        L.sort(key=lambda c: c[1])
        cur = [['']]
        prev = None
        for c in L:
            if prev is not None:
                g = c[1] - prev
                if g >= 28:
                    cur.append([''])      # espace entre mots
                elif g >= 10:
                    cur[-1].append('')    # espace entre lettres
            cur[-1][-1] += '-' if c[3] >= 6 else '.'
            prev = c[2]
        words += cur
    return words


def vig_dec(t, key):
    return ''.join(chr((ord(ch) - ord(key[k % len(key)])) % 26 + 65) for k, ch in enumerate(t))


if __name__ == '__main__':
    words = read_morse()
    print(' / '.join(' '.join(w) for w in words))
    ct = [''.join(MORSE[s] for s in w) for w in words]
    print('CT :', ' '.join(ct))
    key = 'RENO'
    flat = vig_dec(''.join(ct), key)   # cle continue, espaces ignores
    pt, i = [], 0
    for w in ct:
        pt.append(flat[i:i + len(w)])
        i += len(w)
    print('PT :', ' '.join(pt))
    (HERE / 'answer.txt').write_text(' '.join(pt) + '\n')
