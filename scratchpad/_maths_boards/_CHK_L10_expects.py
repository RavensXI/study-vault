import json
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
bank=pd['problem_bank']
errs=[]
# For factor_sign_flip on a monic quadratic, sign-flipping brackets negates both roots.
# For G0 the quadratic is 5x^2+4x-9 = (5x+9)(x-1); flip -> (5x-9)(x+1) -> x=9/5=1.8, x=-1.
special={('gold',0):[-1,1.8]}
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        sols=p['solutions']
        for mc in p.get('misconceptions',[]):
            pat=mc['pattern']; exp=mc['expect']
            if pat=='factor_sign_flip':
                if (tier,i) in special:
                    want=special[(tier,i)]
                else:
                    want=[-s for s in sols]
                if exp is None or sorted(exp)!=sorted(want):
                    errs.append(f"{tier}[{i}] factor_sign_flip expect {exp} != derived {want} (sols {sols})")
            else:
                # divide_by_x, square_bracket_error, one_root_only -> expect must be null
                if exp is not None:
                    errs.append(f"{tier}[{i}] {pat} expect should be null, got {exp}")
print("EXPECT errors:", len(errs))
for e in errs: print("  ",e)

# Now recompute every guided_steps numeric box: I trust hand-check but verify the FINAL two roots boxes == solutions
# Find boxes labelled 'root' and verify.
berr=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        roots=[]
        for st in p['guided_steps']:
            pre=st.get('pre','')
            if 'root' in pre.lower() and 'answer' in st:
                roots.append(st['answer'])
        # roots collected should match solutions (order-insensitive) for 2-root problems
        if len(roots)>=2:
            if sorted(roots[:2] if len(roots)==2 else roots)!=sorted(p['solutions']):
                berr.append(f"{tier}[{i}] guided root boxes {roots} != solutions {p['solutions']}")
print("GUIDED ROOT-BOX vs solutions errors:", len(berr))
for e in berr: print("  ",e)
