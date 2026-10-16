# Extra checks: shorttitle length (<=10) and global use-before-declare.
import re,sys
KW=set('if else for while to by in and or not true false na var varip int float bool string color line label box table array matrix map series simple const import export method type switch break continue'.split())
for p in sys.argv[1:]:
    L=open(p).read().split('\n'); issues=[]
    m=re.search(r"^(?:indicator|strategy)\(\s*'[^']*'\s*,\s*'([^']*)'",'\n'.join(L),re.M)
    st=m.group(1) if m else None
    decl={}
    for i,l in enumerate(L,1):
        if l.startswith((' ','/')) or not l.strip(): continue
        mm=re.match(r"(?:var\s+|varip\s+)?(?:[\w<>\.\[\]]+\s+)?([A-Za-z_]\w*)\s*(?:=|:=)(?!=)",l)
        if mm and not l.lstrip().startswith(('if ','for ','while ')) and ':=' not in l.split('=')[0]+'=' :
            decl.setdefault(mm.group(1),i)
        tm=re.match(r"\[([\w\s,]+)\]\s*=",l)
        if tm:
            for n in tm.group(1).split(','): decl.setdefault(n.strip(),i)
        fm=re.match(r"([A-Za-z_]\w*)\s*\(.*\)\s*=>",l)
        if fm: decl.setdefault(fm.group(1),i)
    for i,l in enumerate(L,1):
        code=re.sub(r'"[^"]*"|\'[^\']*\'','',l.split('//')[0])
        for w in set(re.findall(r'(?<![\.\w])([A-Za-z_]\w*)',code)):
            d=decl.get(w)
            if d and i<d and w not in KW: issues.append((w,i,d))
    print(p,'| shorttitle',repr(st),len(st or ''),'OK' if st and len(st)<=10 else 'TOO LONG','| use-before-declare:',issues or 'none')
