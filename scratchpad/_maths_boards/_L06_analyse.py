import re, sympy as sp

x = sp.symbols('x')

def parse_opt(s):
    # strip latex \( \)
    t = s.replace('\\(','').replace('\\)','').strip()
    # handle ^2 as **2 ; insert * between number/paren and paren, and )(
    t = t.replace('^2','**2')
    # insert explicit * : between digit and x, digit and (, ) and (, x and (
    t = re.sub(r'(\d)(x)', r'\1*\2', t)
    t = re.sub(r'(\d)\(', r'\1*(', t)
    t = re.sub(r'\)\(', r')*(', t)
    t = re.sub(r'x\(', r'x*(', t)
    return sp.expand(sp.sympify(t))

problems = {
 'bronze':[
  ('2x^2+5x+3', ['(2x+3)(x+1)','(2x+1)(x+3)','(x+3)(x+2)','2(x^2+5x+3)']),
  ('3x^2+7x+2', ['(3x+1)(x+2)','(3x+2)(x+1)','(x+7)(3x+2)','3(x^2+7x+2)']),
  ('2x^2+7x+6', ['(2x+3)(x+2)','(2x+2)(x+3)','(2x+6)(x+1)','(x+6)(2x+1)']),
  ('5x^2+11x+2',['(5x+1)(x+2)','(5x+2)(x+1)','(x+11)(5x+2)','5(x+2)(x+1)']),
  ('2x^2+3x+1', ['(2x+1)(x+1)','(x+1)(x+2)','(2x+3)(x+1)','2(x+1)^2']),
  ('3x^2+10x+3',['(3x+1)(x+3)','(3x+3)(x+1)','(x+10)(3x+3)','3(x+1)(x+3)']),
  ('4x^2+8x+3', ['(2x+1)(2x+3)','(4x+3)(x+1)','(4x+1)(x+3)','4(x+1)(x+3)']),
  ('2x^2+9x+4', ['(2x+1)(x+4)','(2x+4)(x+1)','(x+9)(2x+4)','2(x+4)(x+1)']),
 ],
 'silver':[
  ('6x^2+x-2',  ['(2x-1)(3x+2)','(6x-1)(x+2)','(3x-1)(2x+2)','(2x+1)(3x-2)']),
  ('3x^2-11x+6',['(3x-2)(x-3)','(3x-3)(x-2)','(3x-6)(x-1)','(x-6)(3x-1)']),
  ('4x^2-5x-6', ['(4x+3)(x-2)','(2x-3)(2x+2)','(4x-6)(x+1)','(x-3)(4x+2)']),
  ('6x^2-7x-3', ['(3x+1)(2x-3)','(6x+1)(x-3)','(3x-1)(2x+3)','(6x-3)(x+1)']),
  ('5x^2-13x+6',['(5x-3)(x-2)','(5x-6)(x-1)','(5x-2)(x-3)','(x-6)(5x-1)']),
  ('2x^2-x-6',  ['(2x+3)(x-2)','(2x-3)(x+2)','(x+3)(2x-2)','(2x-6)(x+1)']),
  ('8x^2+2x-3', ['(4x+3)(2x-1)','(8x+3)(x-1)','(4x-3)(2x+1)','(8x-1)(x+3)']),
 ],
 'gold':[
  ('4x^2-12x+9',['(2x-3)^2','(4x-9)(x-1)','(2x-9)(2x-1)','(4x-3)(x-3)']),
  ('9x^2-1',    ['(3x+1)(3x-1)','(9x+1)(x-1)','(3x-1)^2','9(x^2-1)']),
  ('6x^2+5x-4', ['(3x+4)(2x-1)','(6x-1)(x+4)','(3x-4)(2x+1)','(6x+4)(x-1)']),
  ('12x^2-8x-15',['(6x+5)(2x-3)','(4x-5)(3x+3)','(12x+5)(x-3)','(6x-5)(2x+3)']),
  ('25x^2-16',  ['(5x+4)(5x-4)','(25x+16)(x-1)','(5x-4)^2','5(5x^2-16)']),
 ],
}

for tier, plist in problems.items():
    print('====', tier)
    for pi,(disp, opts) in enumerate(plist):
        target = parse_opt(disp)
        exps = [parse_opt(o) for o in opts]
        correct_idx = [i for i,e in enumerate(exps) if sp.simplify(e-target)==0]
        # duplicate expansions
        dups=[]
        for i in range(len(exps)):
            for j in range(i+1,len(exps)):
                if sp.simplify(exps[i]-exps[j])==0:
                    dups.append((i,j))
        print(f'[{pi}] {disp}  correct_idx={correct_idx}  dups={dups}')
        for i,(o,e) in enumerate(zip(opts,exps)):
            tag=''
            if i in correct_idx: tag='CORRECT'
            print(f'     opt{i}: {o:18s} = {e}   {tag}')
