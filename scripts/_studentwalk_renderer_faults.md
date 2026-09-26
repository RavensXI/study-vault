# Practice walk: page faults on identical tiles

reorder compares tile positions and vocab_match ties each label to one pair, so when two tiles show the
same text a correct answer built with the other identical tile is marked wrong. Code fix, not a data fix.

- spanish-aqa — `spanish-aqa/popular-culture/3/silver/5` (reorder)
- spanish-edexcel — `spanish-edexcel/studying-and-my-future/4/silver/5` (reorder)
- spanish-edexcel — `spanish-edexcel/lifestyle-and-wellbeing/5/silver/5` (reorder)
- french-aqa — `french-aqa/people-and-lifestyle/3/bronze/1` (vocab_match)
- french-aqa — `french-aqa/communication-and-world/1/silver/5` (reorder)
- french-edexcel — `french-edexcel/my-personal-world/3/bronze/1` (vocab_match)
- spanish-unity — `spanish/popular-culture/3/silver/5` (reorder)
- french-unity — `french/communication-and-world/1/silver/5` (reorder)
