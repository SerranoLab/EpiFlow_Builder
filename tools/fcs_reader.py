"""Minimal FCS 3.0/3.1 reader (float/int, little or big endian). Returns (keywords, ndarray events x params, param names)."""
import numpy as np, re
def read_fcs(path):
    with open(path,'rb') as fh: raw=fh.read()
    ver=raw[:6].decode(); 
    tb,te=int(raw[10:18]),int(raw[18:26]); db,de=int(raw[26:34]),int(raw[34:42])
    text=raw[tb:te+1].decode('latin-1'); delim=text[0]
    parts=text[1:].split(delim); kw={}
    for i in range(0,len(parts)-1,2): kw[parts[i].strip()]=parts[i+1].strip()
    if db==0 or de==0: db,de=int(kw['$BEGINDATA']),int(kw['$ENDDATA'])
    npar=int(kw['$PAR']); tot=int(kw['$TOT']); dtype=kw['$DATATYPE']; bo=kw.get('$BYTEORD','1,2,3,4')
    endian='<' if bo.startswith('1') else '>'
    bits={int(kw[f'$P{i}B']) for i in range(1,npar+1)}
    assert len(bits)==1, bits
    b=bits.pop()
    if dtype=='F': dt=np.dtype(endian+'f4')
    elif dtype=='D': dt=np.dtype(endian+'f8')
    elif dtype=='I': dt=np.dtype(endian+('u2' if b==16 else 'u4'))
    else: raise ValueError(dtype)
    arr=np.frombuffer(raw[db:de+1],dtype=dt,count=npar*tot).reshape(tot,npar).astype(np.float64)
    names=[kw[f'$P{i}N'] for i in range(1,npar+1)]
    return kw,arr,names
