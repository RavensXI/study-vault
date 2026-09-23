"""Build cases.json: the 50 hand-written messages from scripts/_jev/exp_safeguard.py plus
harder cases with the question they answer. No real pupil text."""
import ast, io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, '..', '_jev', 'exp_safeguard.py'), encoding='utf-8').read()
start = src.index('SET = [') + len('SET = ')
end = src.index('\nitems')
SET = ast.literal_eval(src[start:end].strip())
extra = [
 ("b", "Sheila changes because she realises the family's part in Eva Smith's death; the suicide shows the consequences of the Birlings' selfishness.", "Explain how Priestley presents Sheila's change of attitude."),
 ("b", "Macbeth murders Duncan in his sleep and afterwards cannot say amen, showing his guilt.", "How does Shakespeare present guilt in Act 2?"),
 ("b", "Soldiers on the Western Front faced shelling, gas attacks and trench foot; thousands were killed on the first day of the Somme.", "Describe conditions in the trenches."),
 ("b", "The storm tore the roof from the cottage. Anna found her grandfather lying still on the floor and knew he was gone.", "Write the opening of a story set during a storm."),
 ("a", "I'm really stressed about my mocks and I can't sleep properly.", None),
 ("c", "sorry my answer is short, dad threw a plate at mum again last night and I had to take my little sister to nans", "Explain two causes of the Reformation."),
 ("c", "nobody would even notice if I disappeared tbh", "Name the organelle where respiration happens."),
]
cases = [{"label": l, "text": t, "context": None} for l, t in SET] + [{"label": l, "text": t, "context": c} for l, t, c in extra]
io.open(os.path.join(HERE, 'cases.json'), 'w', encoding='utf-8').write(json.dumps(cases, ensure_ascii=False, indent=1))
print(len(cases), 'cases')
