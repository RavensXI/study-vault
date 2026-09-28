# Simplify wording: live prompt vs proposed (28 Sep 2026)

| | Reading grade (FK) | Words per sentence | Original 3-word runs kept | Meta-replies | QA pass |
|---|---|---|---|---|---|
| Original paragraph | 12.9 | 21.1 | 100% | | |
| Live prompt (Haiku) | 9.6 | 15.4 | 51% | 0 | - |
| Proposed prompt (Haiku) | 6.6 | 9.8 | 32% | 0 | 11/28 |
| Proposed prompt (Sonnet) | 7.1 | 11.2 | 48% | 0 | 19/28 |

## Side by side

### business

**Original:** A business plan is a written document that explains a business idea and how it will work in practice. It brings together everything an entrepreneur needs to think about before launching — from the product or service they will sell, to how they will make money, to what could go wrong.

**Live prompt:** A business plan is a written document that explains a business idea and how it will work in practice. It includes everything an entrepreneur needs to think about before launching — from the product or service they will sell, to how they will make money, to what could go wrong.

**Proposed (Haiku):** A business plan is a document that explains a business idea. It shows how the business will work in real life. An entrepreneur uses it to think about everything before they start. The plan covers what product or service to sell, how to make money, and what could go wrong.

**Proposed (Sonnet):** A business plan is a written document. It explains a business idea and how the idea will work in real life. It puts together everything an entrepreneur (a person who starts a business) needs to think about before they start the business. This includes the product or service they will sell. It also covers how they will make money and what could go wrong.

QA Haiku: All the original points are kept in shorter sentences with plainer words, and the term 'entrepreneur' is still there. — QA Sonnet: All the points are kept, nothing false is added, the sentences are much shorter, and the wording is plainer, with a correct gloss for 'entrepreneur'.

### business-aqa

**Original:** Their motives vary. Many want to be their own boss and control their own hours. Others are chasing a passion — turning a hobby into a living. Some spot a gap in the market that no-one else has filled. Some are simply dissatisfied with their current job and want to earn more. Most combine several of these reasons.

**Live prompt:** Their reasons are different. Many want to be their own boss and choose their own hours. Others want to turn a hobby into money. Some see a gap in the market that nobody else has filled. Some are not happy with their job and want to earn more money. Most people have more than one reason.

**Proposed (Haiku):** Their reasons are different. Many want to be their own boss. They want to choose when they work. Some follow something they love. They turn a hobby into their job. Some see a gap in the market (something people want but nobody sells). Some are unhappy with their job. They want to earn more money. Most have more than one reason.

**Proposed (Sonnet):** People have different motives. Many want to be their own boss. They also want to choose their own hours. Others follow something they love. They turn a hobby into a way to earn money. Some see a gap in the market that no-one else has filled. Some people are unhappy in their current job and want to earn more. Most people have several of these reasons.

QA Haiku: All the original points are kept, the sentences are short and the words are plainer, and the gloss on 'gap in the market' is correct and adds no new fact. — QA Sonnet: All the points are kept, nothing new is added, sentences are shorter, and harder phrases such as 'dissatisfied', 'chasing a passion' and 'combine' are replaced with plainer ones.

### business-aqa

**Original:** A hundred years ago, manufacturing dominated the UK economy. Today, cheaper labour abroad has pulled most factory work overseas, while digital technology has created whole new tertiary businesses — Deliveroo, Monzo, Bumble. Understanding the shift matters because where a business sits affects how it competes: a primary-sector dairy farmer faces supermarket price pressure, while a tertiary tech firm competes on ideas and speed.

**Live prompt:** A hundred years ago, the UK economy was mostly manufacturing. Today, cheaper labour abroad has pulled most factory work overseas. Meanwhile, digital technology has created new tertiary businesses like Deliveroo, Monzo and Bumble. This shift matters because where a business sits affects how it competes. A primary-sector dairy farmer faces supermarket price pressure, while a tertiary tech firm competes on ideas and speed.

**Proposed (Haiku):** A hundred years ago, manufacturing was the biggest part of the UK economy. Today, things have changed. Cheaper labour abroad has pulled most factory work overseas. Digital technology has created whole new tertiary businesses like Deliveroo, Monzo, and Bumble. Understanding this change matters because the type of business affects how it competes. A primary-sector dairy farmer faces price pressure from supermarkets. A tertiary tech firm competes on ideas and speed.

**Proposed (Sonnet):** A hundred years ago, manufacturing (making goods in factories) was the biggest part of the UK economy. Today, labour is cheaper abroad, so most factory work has moved overseas. At the same time, digital technology has created many new tertiary businesses (businesses that sell services), such as Deliveroo, Monzo and Bumble.

It matters to understand this change. Where a business sits in the economy affects how it competes. A primary-sector dairy farmer is under pressure from supermarkets to keep prices low. A tertiary tech firm competes on ideas and speed.

QA Haiku: All the facts are kept, but this is a near-copy that mostly splits sentences and swaps one or two phrases, so it is not clearly easier for a weak reader. — QA Sonnet: All points, names and subject terms are kept, the added glosses are correct, and the sentences are shorter and plainer than the original.

### design-technology

**Original:** A furniture company choosing timber should look for the FSC logo, which guarantees the wood comes from responsibly managed forests. A clothing brand might use Fairtrade cotton to ensure farmers receive a fair wage. In metals, conflict minerals (such as cobalt mined in unsafe conditions) are a growing concern — responsible manufacturers audit their supply chains.

**Live prompt:** A furniture company choosing timber should look for the FSC logo. This means the timber comes from forests that are managed in the right way. A clothing brand might use Fairtrade cotton. This makes sure the farmers who grow it are paid fairly. With metals, conflict minerals are a growing worry. For example, cobalt is often mined without proper safety. Good manufacturers check their supply chains to make sure this does not happen.

**Proposed (Haiku):** A furniture company should look for the FSC logo on wood. This logo guarantees the wood came from forests that are managed carefully.

A clothing brand might use Fairtrade cotton to make sure farmers are paid fairly.

In metals, conflict minerals (like cobalt mined in unsafe conditions) are a growing problem. Responsible manufacturers check their supply chains to avoid using them.

**Proposed (Sonnet):** A furniture company that buys timber should look for the FSC logo. This logo guarantees that the wood comes from responsibly managed forests. A clothing brand might use Fairtrade cotton. This makes sure that farmers get a fair wage.

Metals can cause problems too. Conflict minerals are a growing concern. One example is cobalt that is mined in unsafe conditions. Responsible manufacturers audit their supply chains. This means they check where their materials come from.

QA Haiku: It is close to a near-copy that mainly splits sentences and swaps a few words, and it adds a claim that is not in the original. — QA Sonnet: All points and names are kept, sentences are much shorter, and the added gloss on 'audit' is a correct plain explanation.

### design-technology

**Original:** Social responsibility means ensuring a material does not cause harm during extraction, processing or disposal. Products should be safe for workers to manufacture and safe for consumers to use. Cultural sensitivity matters too — certain materials or animal-derived products may be inappropriate for some markets. Ethical sourcing, such as buying FSC timber or Fairtrade cotton, shows a designer is thinking beyond profit.

**Live prompt:** Social responsibility means making sure a material does not cause harm during extraction, processing or disposal. Products should be safe for workers to make and safe for people to use. Cultural sensitivity matters too — certain materials or animal-derived products may not be suitable for some markets. Ethical sourcing, like buying FSC timber or Fairtrade cotton, shows a designer is thinking about more than profit.

**Proposed (Haiku):** Social responsibility means making sure a material causes no harm. This matters when it is taken from the ground, processed, or thrown away. Workers must be safe when making products. Consumers must be safe when using them. Cultural sensitivity matters. Some materials or animal products may not suit some markets. Ethical sourcing means buying materials made responsibly. Examples are FSC timber and Fairtrade cotton. This shows designers care about more than profit.

**Proposed (Sonnet):** Social responsibility means making sure a material does not cause harm. This applies during extraction (taking the material from the ground or nature), processing and disposal. Products should be safe for workers to make. They should also be safe for consumers to use.

Cultural sensitivity matters too. Some materials may not be acceptable in some markets. The same is true of animal-derived products (products that come from animals).

Ethical sourcing means buying materials in a fair and responsible way. Two examples are buying FSC timber or Fairtrade cotton. This shows that a designer is thinking about more than profit.

QA Haiku: It explains 'extraction' wrongly as 'taken from the ground', although timber and cotton, both named in the paragraph, are not taken from the ground. — QA Sonnet: All points, names (FSC, Fairtrade) and terms are kept, the added explanations are correct, and the sentences are shorter with plainer words such as 'make' for 'manufacture' and 'acceptable' for 'inappropriate'.

### economics-aqa

**Original:** Think of market structures as a spectrum. At one end sit perfectly competitive markets with many sellers and almost identical products — no single firm has any meaningful power to set the price. At the other end sits a monopoly, where one firm dominates entirely. In between lie the markets most students encounter in the real world: markets with a handful of dominant firms or many smaller ones trying to stand out through branding, quality or service.

**Live prompt:** Market structures form a spectrum. At one end are perfectly competitive markets. These have many sellers and very similar products. No single firm can control the price. At the other end is a monopoly. One firm controls the whole market. In the middle are markets seen in real life. These may have a few large firms, or many smaller ones that try to stand out through branding, quality or service.

**Proposed (Haiku):** Market structures are a spectrum. At one end are perfectly competitive markets. These have many sellers. Their products are almost identical. No single firm can control the price. At the other end is a monopoly. One firm controls the whole market. Between these two are the markets you see in real life. Some have a few dominant firms. Others have many small firms. These firms try to stand out. They use branding, quality or service to attract customers.

**Proposed (Sonnet):** Think of market structures as a spectrum (a line with two ends). At one end are perfectly competitive markets. These have many sellers and almost identical products. No single firm has any real power to set the price. At the other end is a monopoly. In a monopoly, one firm controls the whole market. In between are the markets most students meet in the real world. Some of these have a few big firms. Others have many smaller firms that try to stand out through branding, quality or service.

QA Haiku: All the original points are kept in short sentences with plainer wording, and no numbers, names or quotations were lost or changed. — QA Sonnet: All points are kept with no new facts, and the sentences are much shorter with plainer words (e.g. 'handful' to 'a few', 'encounter' to 'meet', 'meaningful' to 'real').

### economics-aqa

**Original:** Competition puts constant downward pressure on prices. If one petrol station on a busy road cuts its forecourt price, drivers quickly notice and switch to it. Rivals must respond or lose customers. The result is that prices in competitive fuel markets stay close to the underlying cost of supply. Consumers win directly through lower prices and indirectly because firms are forced to keep their costs as low as possible.

**Live prompt:** Competition pushes prices down constantly. If one petrol station on a busy road cuts its forecourt price, drivers quickly notice and go to that station. Rivals must respond or lose customers. Prices in competitive fuel markets stay close to the underlying cost of supply. Consumers benefit directly through lower prices and indirectly because firms must keep their costs as low as possible.

**Proposed (Haiku):** Competition keeps pushing prices down. When one petrol station cuts its price, drivers quickly notice and switch to it. Other petrol stations must respond or they lose customers. In competitive fuel markets, prices stay close to the cost of supply. Consumers win in two ways. First, prices are lower. Second, firms must keep their costs as low as possible. They have to do this to compete.

**Proposed (Sonnet):** Competition keeps pushing prices down. Imagine one petrol station on a busy road lowers its forecourt price. Drivers soon notice and go to that station instead. The other petrol stations must lower their prices too, or they lose customers. So in competitive fuel markets, prices stay close to the underlying cost of supply (what it costs to provide the fuel). Consumers gain in two ways. They pay lower prices directly. They also gain indirectly, because firms have to keep their own costs as low as they can.

QA Haiku: It is a near-copy that mostly splits sentences and keeps the hard words, and it drops the 'busy road' detail. — QA Sonnet: All the points and terms are kept, but this is close to a near-copy that mostly splits sentences and swaps a few words, so it is not clearly easier for a weak Year 7 reader.

### engineering-eduqas

**Original:** Copper is notable in engineering for its outstanding electrical conductivity — it is the standard material for electrical wiring in buildings, appliances and vehicles precisely because it allows current to flow with very low resistance. Copper also has excellent thermal conductivity, making it useful for heat exchangers and water pipes. It is relatively soft and ductile (can be drawn into fine wire or bent into pipe without cracking). Copper corrodes slowly in air, forming a green patina (copper carbonate) that protects the surface beneath. Common uses include electrical cables, water distribution pipes, the coils of electric motors, and printed circuit board tracks.

**Live prompt:** Copper has outstanding electrical conductivity. It conducts electricity very well and allows electric current to flow with very low resistance. This is why copper is the standard material for electrical wiring in buildings, appliances and vehicles.

Copper also has excellent thermal conductivity. This means it conducts heat very well, making it useful for heat exchangers and water pipes.

Copper is soft and ductile, which means it can be drawn into fine wire or bent into pipe without cracking.

Copper corrodes slowly in air and forms a green patina (copper carbonate). This patina protects the copper beneath.

Common uses include electrical cables, water distribution pipes, the coils of electric motors, and printed circuit board tracks.

**Proposed (Haiku):** Copper has outstanding electrical conductivity. Electricity flows through it with very low resistance. This is why we use it for electrical wiring in buildings, appliances and vehicles.

Copper also has excellent thermal conductivity. It is very good at carrying heat. Engineers use it in heat exchangers and water pipes.

Copper is soft and ductile. This means you can bend it or draw it into fine wire without it cracking.

Over time, copper slowly corrodes in air. A green layer forms, called a patina (copper carbonate). This layer protects the copper underneath.

We use copper for electrical cables, water distribution pipes, motor coils, and printed circuit board tracks.

**Proposed (Sonnet):** Copper is important in engineering because it has outstanding electrical conductivity (it lets electric current flow easily). This is why it is the standard material for electrical wiring in buildings, appliances and vehicles. Current flows through copper with very low resistance.

Copper also has excellent thermal conductivity, so heat passes through it easily. This makes it useful for heat exchangers and water pipes.

Copper is relatively soft and ductile. Ductile means it can be drawn into fine wire or bent into pipe without cracking.

Copper corrodes slowly in air. It forms a green patina (copper carbonate). The patina protects the surface beneath it.

Common uses include electrical cables, water distribution pipes, the coils of electric motors, and printed circuit board tracks.

QA Haiku: All facts, terms and the uses list are kept, and the sentences are much shorter, with plain explanations added for conductivity, thermal conductivity and patina. — QA Sonnet: All the facts are kept, but this is mostly the original split into shorter sentences, with hard words like 'outstanding', 'corrodes', 'relatively', 'patina' and 'distribution' left unchanged and unexplained.

### engineering-eduqas

**Original:** Material selection requires matching the material’s properties to the engineering requirements of the product. A bicycle frame needs high tensile strength (to resist being pulled apart under load) and low density (to reduce weight) — aluminium alloy meets both. A kitchen sink needs corrosion resistance and ease of cleaning — stainless steel is the standard answer. Electrical wiring needs high conductivity and ductility — copper. Cutting tools need hardness and edge retention — tool steel. Decorative plumbing fittings need corrosion resistance and machinability — brass. Exam questions often present a product and ask you to justify a specific material choice by linking properties to requirements. Use the pattern: state the property, link it to the product requirement, name the material that provides it.

**Live prompt:** Material selection means matching a material's properties to what the product needs. A bicycle frame needs high tensile strength (so it does not break when pulled) and low density (to reduce weight) — aluminium alloy meets both. A kitchen sink needs corrosion resistance and to be easy to clean — stainless steel is the right choice. Electrical wiring needs high conductivity and ductility — copper is used. Cutting tools need hardness and edge retention — tool steel is the answer. Decorative plumbing fittings need corrosion resistance and machinability — brass is chosen. Exam questions show you a product and ask you to explain why a material was picked by connecting its properties to what the product needs. Follow this pattern: state the property, link it to what the product needs, name the material.

**Proposed (Haiku):** You choose a material by matching what it can do to what your product needs to do. A bicycle frame needs high tensile strength (to resist being pulled apart under load) and low density (to reduce weight). Aluminium alloy has both. A kitchen sink needs corrosion resistance. It must be easy to clean. Stainless steel is the answer. Electrical wiring needs high conductivity and ductility (the ability to bend without breaking). Copper has both. Cutting tools need hardness and edge retention. Tool steel has both. Decorative plumbing fittings need corrosion resistance and machinability (the ability to be shaped easily). Brass has both.

Exam questions often show you a product. They ask you to explain why a certain material was chosen. Follow this method: name the property, link it to what the product needs, and name the material that provides it.

**Proposed (Sonnet):** Choosing a material means matching its properties to what the product needs to do. A bicycle frame needs high tensile strength (it must not be pulled apart under load). It also needs low density (to reduce weight). Aluminium alloy has both. A kitchen sink needs corrosion resistance and must be easy to clean. Stainless steel is the standard choice. Electrical wiring needs high conductivity and ductility (it can be stretched into a wire). Copper is used. Cutting tools need hardness and edge retention (the sharp edge lasts). Tool steel is used. Decorative plumbing fittings need corrosion resistance and machinability (easy to cut and shape with machines). Brass is used.

Exam questions often show you a product. They then ask you to justify a choice of material. You do this by linking properties to the product's needs. Use this pattern:

1. State the property.
2. Link it to what the product needs.
3. Name the material that has it.

QA Haiku: The plain explanation of 'ductility' is inaccurate, and the rewrite is only modestly easier to read. — QA Sonnet: All materials, properties and the exam pattern are kept, the added explanations of ductility, edge retention and machinability are correct, and the sentences are much shorter and plainer.

### english-literature

**Original:** Scene Five introduces Hecate, the goddess of witchcraft, who scolds the witches for dealing with Macbeth without her permission. Many scholars believe this scene was not written by Shakespeare but added later by Thomas Middleton. Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic, equivocal language to suggest he does not believe Macbeth’s version of events. The lord reveals that Macduff has gone to England to seek Malcolm and military support from King Edward. These scenes set up Act Four’s escalation.

**Live prompt:** Scene Five introduces Hecate, the goddess of witchcraft, who scolds the witches for dealing with Macbeth without her permission. Many scholars believe this scene was not written by Shakespeare. They think Thomas Middleton added it later. Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic, equivocal language to suggest he does not believe what Macbeth says happened. The lord reveals that Macduff has gone to England. He seeks Malcolm and military support from King Edward. These scenes set up Act Four's escalation.

**Proposed (Haiku):** Scene Five brings in Hecate, the goddess of witchcraft. She scolds the witches for dealing with Macbeth without her permission. Many scholars think this scene was not written by Shakespeare. They believe Thomas Middleton added it later. Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic and unclear words. This shows he does not believe Macbeth's story. The lord tells him that Macduff has gone to England. Macduff wants to find Malcolm. He also wants military support from King Edward. These scenes set up Act Four, where things get worse.

**Proposed (Sonnet):** Scene Five brings in Hecate, the goddess of witchcraft. She tells the witches off for dealing with Macbeth without her permission. Many scholars think Shakespeare did not write this scene. They think Thomas Middleton added it later.

Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic, equivocal language (words that can mean two things). This shows he does not believe Macbeth's version of events.

The lord tells him that Macduff has gone to England. Macduff wants to find Malcolm and get military support (help from soldiers) from King Edward.

These scenes prepare for the escalation in Act Four, where events get more serious.

QA Haiku: All names, scenes and points are kept, no new facts are added, sentences are much shorter, and the hardest words (equivocal, escalation, version of events, introduces, reveals) are replaced with plainer ones. — QA Sonnet: All names and points from the original are kept, the sentences are shorter, and harder words are swapped or glossed correctly.

### english-literature

**Original:** In Scene Two, the relationship between Macbeth and Lady Macbeth shifts dramatically. Lady Macbeth reveals her own despair in a rhyming couplet: ‘Nought’s had, all’s spent, / Where our desire is got without content.’ Despite being queen, she has gained nothing of value. The word ‘spent’ suggests exhaustion — emotionally, morally, and spiritually drained. She also says ‘’Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy’ — meaning it would be better to be dead like Duncan than to live with this guilt.

**Live prompt:** In Scene Two, the relationship between Macbeth and Lady Macbeth changes dramatically. Lady Macbeth reveals her own despair in a rhyming couplet: 'Nought's had, all's spent, / Where our desire is got without content.' She is queen, but she has gained nothing of value. The word 'spent' suggests exhaustion. She is emotionally, morally, and spiritually drained. She also says ''Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy'. This means it would be better to be dead like Duncan than to live with this guilt.

**Proposed (Haiku):** In Scene Two, the relationship between Macbeth and Lady Macbeth changes a lot. Lady Macbeth shows her own despair in a rhyming couplet: 'Nought's had, all's spent, / Where our desire is got without content.' She is queen, but she has gained nothing of real value. The word 'spent' shows she is exhausted emotionally, morally, and spiritually. She also says ''Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy'. This means it would be better to be dead like Duncan than to live with this guilt.

**Proposed (Sonnet):** In Scene Two, the relationship between Macbeth and Lady Macbeth changes a lot. Lady Macbeth shows her own despair (deep hopelessness) in a rhyming couplet (two lines that rhyme): ‘Nought’s had, all’s spent, / Where our desire is got without content.’ She is queen, but she has gained nothing of value. The word ‘spent’ suggests exhaustion. She feels drained emotionally, morally and spiritually. She also says ‘’Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy’. This means it would be better to be dead like Duncan than to live with this guilt.

QA Haiku: This is a near-copy that swaps a few words (shifts dramatically to changes a lot, reveals to shows) and keeps the original sentence lengths and hard vocabulary, so a weak Year 7 reader would not find it clearly easier. — QA Sonnet: All quotations and points are kept, but it is close to a near-copy that only swaps a few words and splits sentences, so it is not clearly easier to read.

### english-literature-aqa

**Original:** By Chapter 8, the novella’s central argument is clear: power inevitably corrupts. Napoleon has become indistinguishable from the human oppressors the revolution was supposed to replace. The commandments have been rewritten, the original ideals abandoned, and the working animals are worse off than ever. Orwell suggests this is not unique to the Russian Revolution — it is a pattern that recurs whenever a small group seizes power without accountability.

**Live prompt:** By Chapter 8, the novella's central argument is clear: power inevitably corrupts. Napoleon has become the same as the human oppressors that the revolution was supposed to replace. The commandments have been rewritten. The original ideals have been abandoned. The working animals are worse off than before. Orwell suggests this does not happen only in the Russian Revolution. It is a pattern that recurs whenever a small group seizes power without accountability.

**Proposed (Haiku):** By Chapter 8, the novella shows its main idea: power always corrupts. Napoleon has become the same as the human oppressors the revolution was meant to remove. The commandments have been rewritten. The original ideals have been abandoned. The working animals are worse off than ever. Orwell shows this pattern is not special to the Russian Revolution. It happens every time a small group takes power and no one can stop them.

**Proposed (Sonnet):** By Chapter 8, the novella's main argument is clear. Power always corrupts people. Napoleon is now just like the human oppressors (cruel rulers) that the revolution was meant to get rid of. The commandments have been rewritten. The animals' original ideals have been given up. The working animals are worse off than ever.

Orwell suggests this did not only happen in the Russian Revolution. It is a pattern that happens again and again. It happens whenever a small group takes power and does not have to answer for what it does.

QA Haiku: All points, names and the Chapter 8 and Russian Revolution details are kept, sentences are much shorter, and the hardest words (inevitably, indistinguishable, seizes, accountability) are replaced with plainer ones. — QA Sonnet: All points, names and the chapter number are kept, the added gloss 'cruel rulers' for 'oppressors' is accurate, and the sentences are much shorter with plainer words.

### english-literature-aqa

**Original:** By Act 4, Scotland under Macbeth has become a place of fear and suffering. Ross tells Lady Macduff that “cruel are the times” and that people “float upon a wild and violent sea.” The motif of Scotland as a diseased or storm-tossed nation runs through the second half of the play, contrasting with Duncan’s Scotland, which was characterised by growth and natural order.

**Live prompt:** By Act 4, Scotland under Macbeth has become a place of fear and suffering. Ross tells Lady Macduff that "cruel are the times" and that people "float upon a wild and violent sea." The motif of Scotland as a diseased or storm-tossed nation appears throughout the second half of the play. This contrasts with Duncan's Scotland, which had growth and natural order.

**Proposed (Haiku):** By Act 4, Scotland under Macbeth is full of fear and suffering. Ross tells Lady Macduff that "cruel are the times" and that people "float upon a wild and violent sea."

There is a motif (an idea that repeats) throughout the second half of the play. It shows Scotland as sick or tossed about by terrible storms. This is different from Duncan's Scotland. Duncan's Scotland had growth and natural order (the natural world working as it should).

**Proposed (Sonnet):** By Act 4, Macbeth rules Scotland, and it has become a place of fear and suffering. Ross tells Lady Macduff that “cruel are the times.” He says people “float upon a wild and violent sea.” The play uses a motif (an idea that comes back again and again) that shows Scotland as a sick country, or one battered by storms. This motif runs through the second half of the play. It is very different from Duncan's Scotland. Under Duncan, the country was full of growth and natural order.

QA Haiku: All names, Act 4 and both quotations are kept exactly, every point is present, and the sentences are shorter with plainer words (sick, had, different) plus correct glosses for 'motif' and 'natural order'. — QA Sonnet: All names, Act 4 and both quotations are kept exactly, the motif point is correctly explained, and the sentences and wording are clearly simpler.

### english-literature-eduqas

**Original:** For a question on the funeral scene, zoom into Hill's word choices. Don't just say 'she looked scary' — analyse specific words: "'Wasted' connotes disease and decay, suggesting the woman is not fully alive. 'Tautly stretched' creates the image of skin pulled tight over a skull, evoking death. Hill's restraint — giving just enough physical detail — follows the M.R. James convention that suggestion generates more fear than graphic description."

**Live prompt:** I'm ready to rewrite GCSE revision text into simpler English. Please share the text you'd like me to simplify, and I'll follow the rules you've set: keep specialist terms unchanged, preserve all facts and numbers, use shorter sentences and everyday words, and output only the rewritten text.

**Proposed (Haiku):** For a question on the funeral scene, look closely at Hill's word choices. Don't just say 'she looked scary' — analyse specific words: 'Wasted' suggests disease and decay, showing the woman is not fully alive. 'Tautly stretched' creates a picture of skin pulled tight over a skull. This makes you think of death. Hill holds back on physical detail — he gives just enough. This follows what M.R. James does: suggestion creates more fear than describing things in detail.

**Proposed (Sonnet):** For a question on the funeral scene, look closely at Hill's word choices. Do not just write 'she looked scary'. Instead, analyse specific words. Here is an example:

"'Wasted' connotes disease and decay, suggesting the woman is not fully alive. 'Tautly stretched' creates the image of skin pulled tight over a skull, evoking death. Hill's restraint — giving just enough physical detail — follows the M.R. James convention that suggestion generates more fear than graphic description."

To connote means to suggest an extra idea beyond the plain meaning. Restraint means holding back. A convention is a usual way of writing in a type of story.

QA Haiku: The quoted model answer was reworded and lost its double quotation marks, and the rewrite wrongly calls Hill 'he'. — QA Sonnet: The quoted example is unchanged, no facts are lost, the added definitions of connote, restraint and convention are correct, and the surrounding instructions are shorter and clearer.

### english-literature-eduqas

**Original:** After the funeral, Arthur mentions the woman in black to Mr Jerome, expecting a simple explanation. Jerome's reaction is extreme: he goes "grey" in the face, his hands tremble, and he becomes "unable to speak." Hill uses Jerome's physical response to convey terror without explaining its cause. This is a key structural technique: the reader's fear builds not because we know what the woman is, but because we see the effect she has on people who do know. Jerome's inability to articulate the danger mirrors the town's collective silence — the curse is too terrible to name.

**Live prompt:** After the funeral, Arthur tells Mr Jerome about the woman in black. He expects a simple answer. Jerome's reaction is extreme. He goes 'grey' in the face. His hands shake. He becomes 'unable to speak'. Hill uses Jerome's physical response to show fear without saying why. This is a key structural technique. The reader becomes more afraid not because we know what the woman is, but because we see how she affects people who do know. Jerome cannot say what the danger is. The town's silence mirrors this — the curse is too terrible to name.

**Proposed (Haiku):** After the funeral, Arthur tells Mr Jerome about the woman in black. He hopes for a simple explanation. Jerome reacts very strongly. His face turns pale. His hands shake. He cannot speak.

Hill shows Jerome's fear through his body, but she does not explain why. This is a key structural technique (how Hill builds the story). We do not know what the woman is. Yet we become afraid because we see how terrified she makes the people who know her.

Jerome cannot put his fear into words. This is like the silence of the whole town. Nobody speaks about the curse because it is too terrible to name.

**Proposed (Sonnet):** After the funeral, Arthur tells Mr Jerome about the woman in black. He expects a simple answer. Jerome reacts very strongly. His face goes "grey" and his hands tremble. He becomes "unable to speak."

Hill uses Jerome's body to show terror. Hill does not explain what causes it. This is a key structural technique. The reader's fear grows because we see how the woman affects people who know the truth. It does not grow because we know what she is.

Jerome cannot say what the danger is. This matches the way everyone in the town stays silent. The curse is too terrible to name.

QA Haiku: The quoted words "grey" and "unable to speak" from the original have been replaced with 'pale' and 'cannot speak', so the quotations are not kept exactly. — QA Sonnet: All points, names and quotations are kept, nothing new is added, and the short sentences and plainer wording are clearly easier to read.

### film-studies-eduqas

**Original:** The Steadicam was developed in the mid-1970s and transformed how directors could follow actors through complex environments. Because it absorbs all camera shake, the footage has a distinctive floating, slightly uncanny quality that sits between the coldly mechanical precision of a dolly and the raw instability of handheld work. Handheld cinematography, by contrast, introduces tremor and unpredictability, placing the spectator in a position of nervous proximity to the action — commonly used in chase sequences, combat, or moments of emotional volatility.

**Live prompt:** The Steadicam was developed in the mid-1970s and changed how directors could follow actors through complex spaces. Because it removes camera shake, the footage has a floating quality that feels slightly strange. It sits between the smooth precision of a dolly and the shaky look of handheld work.

Handheld cinematography, by contrast, introduces tremor and unpredictability. This puts the viewer in a nervous, close position to the action. It is commonly used in chase sequences, combat, or moments of strong emotion.

**Proposed (Haiku):** The Steadicam was developed in the mid-1970s. It changed how directors could film actors moving through difficult spaces. The Steadicam absorbs camera shake. This makes the footage look like it is floating. It has a slightly strange quality. It sits between two other techniques. A dolly creates smooth, precise movement. Handheld cinematography is shaky and raw by contrast. Handheld work adds shake and unpredictability to footage. This makes viewers feel nervous and close to the action. Directors often use handheld cinematography in chase sequences, fights, or scenes with strong emotion.

**Proposed (Sonnet):** The Steadicam was developed in the mid-1970s. It changed how directors could follow actors through complex places. The Steadicam absorbs all camera shake. Because of this, the footage looks like it is floating, and it feels slightly strange. Its look sits between two other styles. A dolly gives cold, mechanical, exact movement. Handheld work is raw and unsteady.

Handheld cinematography, by contrast, adds shaking and unpredictability. This puts the spectator (the person watching) nervously close to the action. Filmmakers often use it in chase sequences, combat, or moments when emotions are unstable.

QA Haiku: Several details from the original are lost or changed, though the rewrite is easier to read. — QA Sonnet: All points, the date (mid-1970s) and the names are kept, the '(the person watching)' gloss for 'spectator' is correct, and the sentences and word choices are clearly simpler.

### film-studies-eduqas

**Original:** The angle from which a camera views a subject shapes the power dynamic the spectator perceives. A high angle positions the lens above the subject and tilts it downward, so the figure looks diminished and exposed. Used on a protagonist entering a hostile environment, it signals that they are at a disadvantage. The opposite, a low angle, positions the camera below the subject and tilts it upward. The subject towers over the spectator’s viewpoint, appearing dominant or threatening.

**Live prompt:** The camera angle shapes the power dynamic the spectator perceives. A high angle puts the lens above the subject and tilts it down, so the figure looks small and exposed. When a protagonist enters a hostile environment, a high angle shows they are at a disadvantage. A low angle is the opposite. It puts the camera below the subject and tilts it up. The subject towers over the spectator. It appears dominant or threatening.

**Proposed (Haiku):** How the camera views someone changes what power the viewer thinks they have. A high angle puts the camera above the subject. It looks down at them. This makes the character look small and weak. If you use a high angle on a character in danger, it shows they are in trouble. A low angle is the opposite. The camera is below the subject. It looks up at them. The character towers above the viewer. They seem powerful and threatening.

**Proposed (Sonnet):** The angle a camera uses to film a subject changes how powerful the subject looks to the spectator (the person watching). A high angle puts the lens above the subject and points it down. The figure then looks small and exposed. A high angle can be used on a protagonist who enters a hostile environment. It shows that they are at a disadvantage.

A low angle is the opposite. The camera sits below the subject and points up. The subject seems to tower over the spectator's viewpoint. They look dominant or threatening.

QA Haiku: Readability is much better, but some points from the original are dropped or changed. — QA Sonnet: All points are kept with no new facts, the 'spectator' gloss is correct, and the sentences are much shorter with plainer wording (e.g. 'diminished' became 'small', 'signals' became 'shows').

### geography

**Original:** Many people trust that scientists can predict eruptions and earthquakes in time for evacuations. They also have confidence in modern engineering — earthquake-resistant buildings, early warning systems and well-rehearsed emergency plans. This sense of security encourages people to stay, especially in wealthier countries where these measures are well-funded.

**Live prompt:** Many people believe scientists can predict eruptions and earthquakes in time for evacuations. They also trust modern engineering, including earthquake-resistant buildings, early warning systems and practiced emergency plans. This feeling of safety encourages people to stay, especially in richer countries where these measures have good funding.

**Proposed (Haiku):** Many people believe that scientists can predict when eruptions and earthquakes will happen. They also trust modern engineering. This includes earthquake-resistant buildings, early warning systems and emergency plans that people practice many times. This makes people feel safe. So they choose to stay in risky areas. This happens especially in richer countries. These countries have enough money to pay for these protections.

**Proposed (Sonnet):** Many people trust scientists to predict eruptions and earthquakes. They believe the warning will come in time for evacuations (moving people out of danger). People also trust modern engineering. This includes earthquake-resistant buildings, early warning systems and well-rehearsed emergency plans. All this makes people feel safe, so they choose to stay. This is most true in wealthier countries, where these measures get plenty of money.

QA Haiku: The rewrite drops the point that scientists can predict events 'in time for evacuations', so a point from the original is missing. — QA Sonnet: All points are kept, the added gloss for 'evacuations' is correct, and the sentences are much shorter with several plainer word choices.

### geography

**Original:** Scale of the hazard — a magnitude 9 earthquake poses far greater risk than a magnitude 1 earthquake. A Category 5 tropical storm is more destructive than a Category 1. Wealth of the country — wealthier countries can afford stronger buildings, better warning systems, trained emergency services and medical support. Poorer countries have fewer resources to prepare or respond. Population size and proximity — the more people living near a hazard, the greater the risk. As the world’s population grows and more land is inhabited, more people are exposed to natural hazards.

**Live prompt:** The scale of the hazard matters. A magnitude 9 earthquake is much more dangerous than a magnitude 1 earthquake. A Category 5 tropical storm is more destructive than a Category 1.

The wealth of a country matters. Richer countries can afford stronger buildings, better warning systems, trained emergency services and medical support. Poorer countries have fewer resources to prepare or respond.

Population size and proximity matter. The more people living near a hazard, the greater the risk. As the world's population grows and more land is used, more people face natural hazards.

**Proposed (Haiku):** Scale of the hazard — a magnitude 9 earthquake means much more risk than a magnitude 1 earthquake. A Category 5 tropical storm causes more damage than a Category 1. Wealth of the country — wealthier countries can build stronger buildings. They have better warning systems. They have trained emergency services. They have good medical support. Poorer countries do not have these resources. They cannot prepare well. They cannot respond well. Population size and proximity — more people living near a hazard means more risk. The world's population is growing. People are building homes on more land. More people are now exposed to natural hazards.

**Proposed (Sonnet):** Scale of the hazard: a magnitude 9 earthquake is far more dangerous than a magnitude 1 earthquake. A Category 5 tropical storm does more damage than a Category 1 storm.

Wealth of the country: richer countries can pay for stronger buildings and better warning systems. They can also pay for trained emergency services and medical support. Poorer countries have fewer resources to prepare for a hazard or deal with it afterwards.

Population size and proximity (how close people live to the hazard): the more people who live near a hazard, the greater the risk. The world's population is growing, and people now live on more land. This means more people are exposed to natural hazards.

QA Haiku: The rewrite is much easier to read, but it overstates the poorer-countries point and adds a small detail not in the original. — QA Sonnet: All points, numbers and terms are kept, and the rewrite uses shorter sentences and plainer wording (e.g. 'afford' became 'pay for', 'destructive' became 'does more damage'). The added gloss on 'proximity' is correct.

### geography-aqa

**Original:** In a rainforest, climate, plants, animals and soil all depend on each other. Hot, wet conditions support fast plant growth. Plants release water vapour through their leaves (transpiration), which forms clouds and falls as rain — meaning the forest creates much of its own rainfall. Animals pollinate plants and disperse their seeds. Decomposers recycle nutrients fast enough that the thin soil supports the world's tallest trees. Cut down enough trees and the cycle breaks — less transpiration means less rain, drier conditions, and the forest cannot regrow.

**Live prompt:** In a rainforest, the climate, plants, animals and soil all need each other.

Hot, wet weather helps plants grow fast. Plants release water through their leaves in a process called transpiration. This water forms clouds and falls as rain, so the forest makes much of its own rain.

Animals pollinate plants and spread their seeds. Decomposers recycle nutrients fast enough that the thin soil supports the world's tallest trees.

When we cut down enough trees, the cycle breaks. Less transpiration means less rain and drier weather. The forest cannot grow back.

**Proposed (Haiku):** In a rainforest, everything depends on everything else. The climate, plants, animals and soil are all linked. Hot and wet weather helps plants grow fast. Plants release water vapour through their leaves in a process called transpiration. This water vapour rises and forms clouds. The clouds fall as rain. In this way, the forest creates much of its own rainfall. Animals pollinate plants and disperse their seeds. Decomposers break down dead material and recycle nutrients very quickly. This helps the thin soil support the world's tallest trees. If we cut down enough trees, the cycle breaks. Fewer trees means less transpiration. Less transpiration means less rain. The weather becomes drier. The forest cannot grow back.

**Proposed (Sonnet):** In a rainforest, the climate, plants, animals and soil all depend on each other. The conditions are hot and wet. This helps plants grow fast. Plants release water vapour through their leaves. This is called transpiration. The water vapour forms clouds, and the water then falls as rain. So the forest makes much of its own rainfall.

Animals pollinate plants and spread their seeds. Decomposers (living things that break down dead material) recycle nutrients quickly. This means the thin soil can still support the world's tallest trees.

If people cut down enough trees, the cycle breaks. There is less transpiration, so there is less rain. The conditions become drier. Then the forest cannot regrow.

QA Haiku: Faithful rewrite that keeps every point and key term (transpiration, pollinate, disperse, decomposers), with much shorter sentences and plainer wording. — QA Sonnet: All points, terms and details from the original are kept, the added decomposer explanation is correct, and the sentences are clearly shorter and plainer.

### geography-aqa

**Original:** Animals are adapted to the layered environment. Howler monkeys have prehensile tails that work as a fifth limb in the canopy. Sloths move so slowly that algae grow in their fur, providing camouflage. Poison dart frogs are brightly coloured to warn predators of toxic skin. Toucans have huge bills to reach fruit on slender branches that wouldn't support their weight. Jaguars are the only big cat that hunts mainly in water.

**Live prompt:** Animals are adapted to the layered environment. Howler monkeys have prehensile tails that work as a fifth limb in the canopy. Sloths move so slowly that algae grow in their fur and provide camouflage. Poison dart frogs are brightly coloured to warn predators that their skin is toxic. Toucans have huge bills to reach fruit on thin branches that wouldn't support their weight. Jaguars are the only big cat that hunts mainly in water.

**Proposed (Haiku):** Animals are adapted to the layered environment. Howler monkeys have prehensile tails (tails that can grip). They use these like a fifth limb in the canopy. The canopy is the top layer of the forest. Sloths move very slowly. Algae grow in their fur. The algae camouflages them. Poison dart frogs are brightly coloured. This bright colour warns predators. Their skin is toxic. Toucans have huge bills. They reach fruit on thin branches. The branches cannot support their weight. Jaguars are the only big cat that hunts mainly in water.

**Proposed (Sonnet):** Animals are adapted (suited) to the layered environment.

Howler monkeys have prehensile tails (tails that can grip). In the canopy (the tops of the trees), the tail works like a fifth limb.

Sloths move so slowly that algae grow in their fur. The algae give the sloth camouflage, which helps it hide.

Poison dart frogs are brightly coloured. This warns predators that their skin is toxic (poisonous).

Toucans have huge bills. They use them to reach fruit on slender branches. These branches would not support the toucan's weight.

Jaguars are the only big cat that hunts mainly in water.

QA Haiku: All the points are kept and the sentences are shorter, but the vocabulary is barely simplified, so it reads as a sentence-split near-copy. — QA Sonnet: Content is complete and the glosses are correct, but it is a near-copy that mostly splits sentences and adds brackets, so it is not clearly easier for a weak Year 7 reader.

### history

**Original:** Monks had the knowledge, money, and discipline to create much better public health systems than towns had. Monasteries had excellent water supplies and built latrines to carry away sewage, keeping their water source separate from waste. They also had infirmaries for sick monks and herb gardens to grow plants for remedies.

**Live prompt:** Monks had the knowledge, money, and discipline to build better public health systems than towns had. Monasteries had good water supplies. They built latrines to carry away sewage and kept their water separate from waste. They also had infirmaries for sick monks and herb gardens to grow plants for remedies.

**Proposed (Haiku):** Monks had knowledge, money and discipline. This helped them build better ways to keep people healthy than towns had. Monasteries had good water supplies. They built latrines (toilets) to carry away sewage (human waste). They kept their water supply separate from their waste. Monasteries also had infirmaries (places where sick monks stayed). They grew herb gardens. Plants from these gardens were used to make remedies (medicines).

**Proposed (Sonnet):** Monks had the knowledge, the money and the discipline to build much better public health systems than towns had. Monasteries had excellent water supplies. They built latrines (toilets) that carried sewage away. This kept their water source separate from waste. Monasteries also had infirmaries (rooms for looking after sick monks). They had herb gardens too, where monks grew plants to make remedies (treatments for illness).

QA Haiku: All points are kept, the sentences are much shorter, the words are plainer, and the bracketed explanations of latrines, sewage, infirmaries and remedies are correct. — QA Sonnet: It is close to a copy of the original: the first sentence is nearly unchanged, and the rest mainly splits sentences and adds short glosses, so it is not clearly easier for a weak reader.

### history

**Original:** Run by monks, nuns, or religious orders — not trained doctors Provided food, shelter, warmth, and prayer for the sick and poor Rarely attempted to treat or cure diseases Often refused entry to patients with infectious diseases to protect other residents The focus was on spiritual care: patients were encouraged to pray and confess their sins

**Live prompt:** Monks, nuns, and religious orders ran these hospitals, not trained doctors. They provided food, shelter, warmth, and prayer to sick and poor people. They rarely tried to treat or cure diseases. They often refused entry to patients with infectious diseases to protect other residents. The main focus was on spiritual care. Patients were encouraged to pray and confess their sins.

**Proposed (Haiku):** Religious hospitals were run by monks, nuns, and religious orders. They did not have trained doctors. The hospitals gave patients food, shelter, warmth, and prayer. They rarely tried to treat or cure diseases. They often refused to let patients with infectious diseases come in. This was to keep other people in the hospital safe. The main focus was spiritual care. Patients were told to pray and confess their sins (admit their wrongs).

**Proposed (Sonnet):** Monks, nuns, or religious orders ran these places. They were not trained doctors. They gave the sick and poor food, shelter, warmth, and prayer. They rarely tried to treat or cure diseases. They often refused to let in patients with infectious diseases. This protected the other residents. The main focus was spiritual care. Patients were encouraged to pray and to confess their sins.

QA Haiku: The rewrite drops the original point that the hospitals cared for 'the sick and poor', keeping only 'patients'. — QA Sonnet: All the points are kept, but it is close to a copy: it mostly splits sentences and swaps a few words, and the harder words stay unexplained.

### history-aqa

**Original:** When Britain went to war in South Africa in 1899, recruiting officers in northern industrial cities turned away around 40% of volunteers as physically unfit. In Manchester the rejection rate exceeded 60%. The 1903 Inter-Departmental Committee on Physical Deterioration confirmed the problem and linked it to childhood undernourishment. The Boer War transformed welfare from a moral question (should we help?) into a security question (can we field an army?). National efficiency, not compassion, made reform politically irresistible.

**Live prompt:** When Britain went to war in South Africa in 1899, recruiting officers in northern industrial cities turned away around 40% of volunteers because they were physically unfit. In Manchester, the rejection rate was above 60%. The 1903 Inter-Departmental Committee on Physical Deterioration confirmed the problem and linked it to childhood undernourishment. The Boer War changed welfare from a moral question (should we help?) into a security question (can we field an army?). National efficiency, not compassion, made reform something that politicians could not avoid.

**Proposed (Haiku):** In 1899, Britain went to war in South Africa. Recruiting officers in northern industrial cities rejected many volunteers. About 40% of volunteers were turned away for being too weak or ill. In Manchester, the rate was worse - over 60% were rejected. In 1903, the Inter-Departmental Committee on Physical Deterioration investigated. They found that childhood hunger had made men weak. Before the Boer War, welfare (help for poor people) was a moral question. The question was: should we help? The Boer War changed everything. Welfare became a security question instead. The new question was: could we field enough soldiers? National efficiency (the strength of the military) mattered now, not compassion. This is what forced the government to act on welfare.

**Proposed (Sonnet):** Britain went to war in South Africa in 1899. Recruiting officers in northern industrial cities turned away around 40% of volunteers. They said these men were not physically fit. In Manchester, more than 60% were turned away. The 1903 Inter-Departmental Committee on Physical Deterioration confirmed the problem. It linked it to children not getting enough food when they were young.

The Boer War changed how people saw welfare (help for people in need). Before, it was a moral question: should we help? Now it was a security question: can we put an army in the field? National efficiency, not compassion, meant politicians could no longer ignore reform.

QA Haiku: The plain explanation of 'national efficiency' is wrong, and the 1903 Committee's confirmation of the problem is lost. — QA Sonnet: All numbers, names and points are kept, the welfare explanation is correct, and the sentences and several key words (undernourishment, transformed, irresistible) are noticeably simpler.

### history-aqa

**Original:** Nightingale was a trained mathematician. She invented the polar-area chart — later called the rose diagram — to show that more British soldiers in Crimea died from preventable disease than from enemy bullets. She presented her statistics to Lord Panmure and the 1857 Royal Commission on the Health of the Army. Statistics, not anecdotes, won the argument. Her command of data made her one of the first women elected to the Royal Statistical Society in 1858, and her methods gave hospital reform an evidence base that critics could not easily dismiss.

**Live prompt:** Nightingale was a trained mathematician. She invented the polar-area chart — later called the rose diagram — to show that more British soldiers in Crimea died from preventable disease than from enemy bullets. She showed her statistics to Lord Panmure and the 1857 Royal Commission on the Health of the Army. Statistics won the argument, not stories. Her skill with data made her one of the first women elected to the Royal Statistical Society in 1858. Her methods gave hospital reform evidence that critics could not easily dismiss.

**Proposed (Haiku):** Nightingale was trained as a mathematician. She invented the polar-area chart, which people later called the rose diagram. This chart showed something important. More British soldiers in Crimea died from preventable disease than from enemy bullets. She showed her findings to Lord Panmure and the 1857 Royal Commission on the Health of the Army. Her numbers proved the argument. Stories did not. She had great skill with numbers. In 1858, she became one of the first women elected to the Royal Statistical Society. Her work also helped hospitals reform. It gave them evidence that critics could not argue against.

**Proposed (Sonnet):** Nightingale was a trained mathematician. She invented the polar-area chart, which was later called the rose diagram. It showed that more British soldiers in Crimea died from preventable disease than from enemy bullets. She showed her statistics to Lord Panmure and to the 1857 Royal Commission on the Health of the Army. Statistics, not anecdotes (short stories about single cases), won the argument. She was very good with data. In 1858, she became one of the first women elected to the Royal Statistical Society. Her methods gave hospital reform a base of evidence. Critics could not easily dismiss it.

QA Haiku: All names, dates and points are kept, with no commentary or added facts, and the sentences and wording are clearly shorter and plainer. — QA Sonnet: All facts are kept and the anecdote gloss is correct, but this is close to a sentence-split copy: most hard words remain, so it is not clearly easier for a weak Year 7 reader.

### media-studies-eduqas

**Original:** When a question asks you to analyse media language on a set cover, avoid simply listing features you can see (“there is a masthead, there is an image, there are cover lines”). Marks for media language analysis are given for explaining the meanings those features construct and why a producer might have chosen them, not for identifying features alone. On the extended comparison question, build every paragraph around both products together — use comparative language such as “whereas” or “similarly” throughout, rather than writing one block on the set product and a separate block on the unseen resource.

**Live prompt:** I'm ready to rewrite GCSE revision text into plainer English. Please paste the text you'd like me to simplify, and I'll rewrite it following these rules:

- Keep all specialist subject terms unchanged
- Keep all numbers, dates, names, places, and quotations exactly as they are
- Use shorter sentences and everyday words
- Keep the same information and roughly the same length
- Use a neutral, factual tone with no added commentary

Just send me the text and I'll get started.

**Proposed (Haiku):** When a question asks you to analyse media language on a set cover, don't just list the features you can see. Don't write "there is a masthead, there is an image, there are cover lines".

You get marks for explaining what those features mean. You also get marks for explaining why a producer might have chosen them. You don't get marks for just naming the features.

On the comparison question, write about both products in every paragraph. Use comparative language like "whereas" or "similarly" to compare them. Don't write one block about the set product and a separate block about the unseen resource.

**Proposed (Sonnet):** Sometimes a question asks you to analyse media language on a set cover. Do not just list the features you can see, such as “there is a masthead, there is an image, there are cover lines”. You do not get marks for only naming features. You get marks for explaining two things. First, explain the meanings those features create. Second, explain why a producer might have chosen them.

The extended comparison question needs a different approach. Build every paragraph around both products together. Use comparing words such as “whereas” or “similarly” all the way through. Do not write one block on the set product and then a separate block on the unseen resource.

QA Haiku: The rewrite drops the word 'extended' from 'extended comparison question', so it no longer says which exam question the advice applies to. — QA Sonnet: All points, the quoted list, and terms like media language, masthead and cover lines are kept; sentences are much shorter and the wording is plainer, with no new facts.

### meta-case

**Original:** This is a genuinely two-part skill: you must connect a specific feature of the cover (a cover line, an image choice, a styling decision) to a specific aspect of context, rather than stating a general historical fact and a general cover description side by side without linking them.

**Live prompt:** I'm ready to rewrite GCSE revision text into plainer English. I understand the rules:

- Keep specialist subject terms unchanged
- Never change facts, numbers, dates, names, or quotations
- Same information, simpler wording only
- Shorter sentences, everyday words
- Neutral, factual tone
- Plain prose output only

However, I don't see any GCSE revision text in your message. Please paste the text you'd like me to simplify, and I'll rewrite it for you.

**Proposed (Haiku):** This is a two-part skill. You must connect one specific thing on the cover (such as a cover line, an image, or a design choice) to one specific part of the context. Do not just describe the cover in general and then state a historical fact. Link them together.

**Proposed (Sonnet):** This skill has two parts. First, pick a specific feature of the cover. This could be a cover line, an image choice or a styling decision. Then link it to a specific aspect of context. Do not just write a general historical fact and a general description of the cover next to each other. You must show how the two are connected.

QA Haiku: The rewrite keeps every point (two-part skill, link one specific cover feature to one specific part of context, avoid general description plus a historical fact side by side) in shorter sentences with plainer words. — QA Sonnet: It mostly splits the original into shorter sentences and keeps the hard vocabulary, so it is not clearly easier for a weak Year 7 reader.

### meta-case

**Original:** For AO3, always link context to Shelley’s purpose. Instead of “Galvanism was popular in the early 19th century,” write “Shelley uses Victor’s galvanic experiments to warn against the Enlightenment belief that science can overcome all limits, reflecting contemporary anxieties about rapid scientific progress.” Context should always explain WHY Shelley makes the choices she does.

**Live prompt:** I'm ready to rewrite GCSE revision text into plainer English. I understand the rules:

- Keep subject terms as they are; simplify everything around them
- No changes to facts, numbers, dates, names, places, or quotations
- Same information, simpler wording only
- Shorter sentences, everyday words, roughly the same length
- Neutral, factual tone
- Plain prose output only

Please paste the revision text you'd like me to simplify.

**Proposed (Haiku):** For AO3, always link the context to Shelley's purpose. Do not just state historical facts. For example, do not write "Galvanism was popular in the early 19th century." Instead, explain what Shelley does with this fact. Show how Shelley uses Victor's galvanic experiments. She warns against an Enlightenment belief: that science can overcome all limits. She also shows the fears of her own time about how fast science was changing. Context should always explain WHY Shelley made the choices she did.

**Proposed (Sonnet):** For AO3, always link context to Shelley’s purpose (what she wants her writing to do). Do not just state a fact about the time. Instead of “Galvanism was popular in the early 19th century,” write “Shelley uses Victor’s galvanic experiments to warn against the Enlightenment belief that science can overcome all limits, reflecting contemporary anxieties about rapid scientific progress.” Your context should always explain WHY Shelley makes the choices she does.

QA Haiku: The second quotation (the model AO3 sentence) is no longer in quotation marks and has been reworded, so quoted text is not kept exactly. — QA Sonnet: It is a near-copy of the original that adds a gloss and a sentence but does not make the wording plainer or the sentences shorter.
