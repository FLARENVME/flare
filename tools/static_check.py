import re,sys
for p in sys.argv[1:]:
    L=open(p).read().split('\n'); s='\n'.join(L)
    bal={'(':0,'[':0}; bad=[]
    for i,l in enumerate(L,1):
        c=re.sub(r'"[^"]*"|\'[^\']*\'','',l.split('//')[0] if not l.strip().startswith('//') else '')
        bal['(']+=c.count('(')-c.count(')'); bal['[']+=c.count('[')-c.count(']')
        ind=len(l)-len(l.lstrip(' '))
        if l.strip() and ind%4 not in (0,1): bad.append(i)
        if '\t' in l: bad.append(i)
    plots=len(re.findall(r'^\s*(plot|plotshape|plotchar|plotarrow|plotcandle|plotbar|bgcolor|fill|barcolor)\(',s,re.M))
    print(p,'lines',len(L)-(L[-1]==''),'paren',bal,'indent_issues',bad,'plots',plots,
      'security',len(re.findall(r'request\.security\(',s)),'lookahead_on',len(re.findall('lookahead_on',s)),
      'neg_offset',len(re.findall(r'offset\s*=\s*-',s)),'isconfirmed',s.count('barstate.isconfirmed'),
      'var',len(re.findall(r'^\s*var\s',s,re.M)),'alertcondition',s.count('alertcondition('),'alert(',len(re.findall(r'\balert\(',s)),
      'TP',len(re.findall(r'\bTP\d',s)))
