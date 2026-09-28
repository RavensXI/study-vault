# Simplify wording: live prompt vs proposed (28 Sep 2026)

| | Reading grade (FK) | Words per sentence | Original 3-word runs kept | Meta-replies | QA pass |
|---|---|---|---|---|---|
| Original paragraph | 12.9 | 21.1 | 100% | | |
| Live prompt (Haiku) | 9.9 | 16.1 | 49% | 0 | - |
| Proposed prompt (Haiku) | 7.3 | 11.9 | 32% | 0 | 13/28 |
| Proposed prompt (Sonnet) | 6.8 | 10.9 | 45% | 0 | 25/28 |

## Side by side

### business

**Original:** A business plan is a written document that explains a business idea and how it will work in practice. It brings together everything an entrepreneur needs to think about before launching — from the product or service they will sell, to how they will make money, to what could go wrong.

**Live prompt:** A business plan is a written document that explains a business idea and how it will work. It includes everything an entrepreneur needs to think about before starting a business. It covers what product or service they will sell, how they will make money, and what could go wrong.

**Proposed (Haiku):** A business plan is a document. It explains a business idea. It shows how the idea will actually work.

A business plan includes everything an entrepreneur (a person who starts a business) needs to think about before they start. This includes the product or service they will sell. This includes how they will make money. This includes what could go wrong.

**Proposed (Sonnet):** A business plan is a written document. It explains a business idea and how the idea will work in real life. Before an entrepreneur (a person who starts a business) begins, they need to think about many things. The business plan brings all of these things together. It covers the product or service they will sell. It covers how they will make money. It also covers what could go wrong.

QA Haiku: All the points are kept, the plain gloss of 'entrepreneur' is correct, and the short sentences and simpler words make it clearly easier to read. — QA Sonnet: All points are kept, in short plain sentences, and the added explanation of 'entrepreneur' is correct.

### business-aqa

**Original:** Their motives vary. Many want to be their own boss and control their own hours. Others are chasing a passion — turning a hobby into a living. Some spot a gap in the market that no-one else has filled. Some are simply dissatisfied with their current job and want to earn more. Most combine several of these reasons.

**Live prompt:** People have different reasons. Many want to work for themselves and choose when they work. Some follow something they love, turning it into a job. Some see something that people want to buy but no-one is selling. Some are unhappy with their current job and want to earn more money. Most have more than one reason.

**Proposed (Haiku):** People start businesses for different reasons. Many want to be their own boss and choose when they work. Others have a hobby they love and want to turn it into their job. Some see something people need but no-one is selling yet. Some are not happy with their job now and want to earn more money. Most people have more than one reason.

**Proposed (Sonnet):** Their reasons are different. Many want to be their own boss. They want to choose their own working hours.

Others are chasing a passion. This means they want to turn a hobby into a way of earning money.

Some spot a gap in the market that no-one else has filled. This is something customers want that no business sells yet.

Some are unhappy with their current job and want to earn more.

Most have more than one of these reasons.

QA Haiku: All the points are kept, but the sentences are no shorter than the original and several are longer, so this is mostly a word swap rather than a clearly easier rewrite. — QA Sonnet: All points are kept, sentences are shorter, and harder words like 'motives', 'dissatisfied' and 'combine' are replaced with plainer ones. The added explanations of 'chasing a passion' and 'gap in the market' are correct.

### business-aqa

**Original:** A hundred years ago, manufacturing dominated the UK economy. Today, cheaper labour abroad has pulled most factory work overseas, while digital technology has created whole new tertiary businesses — Deliveroo, Monzo, Bumble. Understanding the shift matters because where a business sits affects how it competes: a primary-sector dairy farmer faces supermarket price pressure, while a tertiary tech firm competes on ideas and speed.

**Live prompt:** A hundred years ago, manufacturing dominated the UK economy. Today, most factory jobs have moved to other countries because workers there cost less. Digital technology has also created whole new tertiary businesses — Deliveroo, Monzo, Bumble. It matters to understand this shift because which sector a business is in affects how it competes. A primary-sector dairy farmer faces pressure from supermarkets to lower prices. A tertiary tech firm competes by having better ideas and moving faster.

**Proposed (Haiku):** About a hundred years ago, making things was the biggest part of the UK economy. Today, workers in other countries work for much less money. So most factory work has moved abroad. Computers and the internet have created whole new types of businesses. These are called tertiary businesses (businesses that provide services, not things). Deliveroo, Monzo, and Bumble are examples.

Understanding this change matters. What type of business you have affects how it competes. A primary-sector dairy farmer (who produces farm goods like milk) faces supermarkets pushing prices down. But a tertiary tech firm (a service business) competes by having good ideas and working quickly.

**Proposed (Sonnet):** A hundred years ago, manufacturing was the biggest part of the UK economy. Today, most factory work has moved to other countries, because workers there cost less to pay. At the same time, digital technology has created whole new tertiary businesses (businesses that sell services). Deliveroo, Monzo and Bumble are examples.

It matters to understand this change. The sector a business is in affects how it competes. A primary-sector dairy farmer faces pressure from supermarkets to lower prices. A tertiary tech firm competes by having better ideas and by being faster.

QA Haiku: All points, names (UK, Deliveroo, Monzo, Bumble) and terms (tertiary, primary-sector) are kept, the added explanations are correct, and the sentences are much shorter and plainer. — QA Sonnet: All names, the time reference and every point are kept, the tertiary explanation is correct, and the sentences and words are clearly simpler.

### design-technology

**Original:** A furniture company choosing timber should look for the FSC logo, which guarantees the wood comes from responsibly managed forests. A clothing brand might use Fairtrade cotton to ensure farmers receive a fair wage. In metals, conflict minerals (such as cobalt mined in unsafe conditions) are a growing concern — responsible manufacturers audit their supply chains.

**Live prompt:** A furniture company should look for the FSC logo when choosing timber. This guarantees that the wood comes from responsibly managed forests. A clothing brand might use Fairtrade cotton to ensure farmers get a fair wage. Conflict minerals are a growing concern in metals. Cobalt is often mined in unsafe conditions. Responsible manufacturers check their supply chains.

**Proposed (Haiku):** A furniture company choosing timber should look for the FSC logo. The FSC logo means the wood comes from forests that are looked after properly. A clothing brand might use Fairtrade cotton. Fairtrade means farmers get paid fairly for their work. In metals, conflict minerals are a growing problem. Cobalt is one example. Conflict minerals are mined in dangerous conditions. Responsible manufacturers check their supply chains.

**Proposed (Sonnet):** A furniture company choosing timber should look for the FSC logo. This logo guarantees that the wood comes from responsibly managed forests. That means the forests are looked after with care.

A clothing brand might use Fairtrade cotton. This makes sure farmers get a fair wage, which means fair pay for their work.

Metals have a different problem. Conflict minerals are a growing concern, which means more and more people worry about them. One example is cobalt mined in unsafe conditions. Manufacturers who act responsibly audit their supply chains. This means they check every step and every company that supplies their materials.

QA Haiku: All points, names and the cobalt example are kept, with no new facts. Sentences are much shorter and the wording is plainer, with FSC, Fairtrade and 'responsible' explained simply. — QA Sonnet: All points, terms and examples (FSC, Fairtrade, cobalt, conflict minerals, audit, supply chains) are kept, the sentences are shorter, and the added explanations are correct and only clarify words already in the original.

### design-technology

**Original:** Social responsibility means ensuring a material does not cause harm during extraction, processing or disposal. Products should be safe for workers to manufacture and safe for consumers to use. Cultural sensitivity matters too — certain materials or animal-derived products may be inappropriate for some markets. Ethical sourcing, such as buying FSC timber or Fairtrade cotton, shows a designer is thinking beyond profit.

**Live prompt:** Social responsibility means making sure a material does not cause harm when it is taken from the ground, changed into a product, or thrown away. Products must be safe for the workers who make them and safe for the people who use them. Cultural sensitivity is important too. Some materials or products made from animals may not be right for some communities. Ethical sourcing, such as buying FSC timber or Fairtrade cotton, shows a designer cares about more than just making money.

**Proposed (Haiku):** Social responsibility means making sure a material does not harm people during three stages. The first stage is extraction - taking the material from the ground. The second is processing - treating and shaping it. The third is disposal - throwing it away. Products must be safe for workers to make. They must be safe for the people who buy and use them. Different cultures have different beliefs. A designer should respect what matters to different groups. Some materials or animal-derived products might not be right for some places or people. Ethical sourcing means buying materials in a fair way. FSC timber is wood from forests that are looked after well. Fairtrade cotton is cotton from places where workers earn fair pay. This shows a designer cares about more than profit.

**Proposed (Sonnet):** Social responsibility means making sure a material does not cause harm. This applies when the material is taken from its source (extraction), when it is made into something useful (processing), and when it is thrown away (disposal). Products should be safe for workers to make. They should also be safe for consumers to use.

Cultural sensitivity matters too. Some materials may not be suitable for some markets, which are the groups of customers in different places. The same is true of animal-derived products, which are products made from animals.

Ethical sourcing shows that a designer thinks about more than making money. Examples are buying FSC timber or Fairtrade cotton.

QA Haiku: The plain explanation of 'extraction' is too narrow to be correct, and the rewrite limits the harm to people when the original does not. — QA Sonnet: All points, terms (extraction, processing, disposal, FSC, Fairtrade) and examples are kept, the added explanations are correct, and the sentences are shorter and use plainer words.

### economics-aqa

**Original:** Think of market structures as a spectrum. At one end sit perfectly competitive markets with many sellers and almost identical products — no single firm has any meaningful power to set the price. At the other end sits a monopoly, where one firm dominates entirely. In between lie the markets most students encounter in the real world: markets with a handful of dominant firms or many smaller ones trying to stand out through branding, quality or service.

**Live prompt:** Market structures form a spectrum. At one end sit perfectly competitive markets with many sellers and almost identical products — no single firm can set the price. At the other end sits a monopoly, where one firm dominates entirely. Between these lie the markets most students see in real life: either a handful of dominant firms or many smaller ones trying to stand out through branding, quality, or service.

**Proposed (Haiku):** Think of market structures as a range. At one end are perfectly competitive markets. Many sellers offer products that are almost identical. No single firm can set the price on its own. At the other end sits a monopoly. One firm controls the market entirely. In between are the markets you see in real life. Some have a few big firms. Others have many small firms trying to be different. They do this through branding (making a product look special), quality or service.

**Proposed (Sonnet):** Think of market structures as a spectrum. A spectrum is a line with two ends and many types in between.

At one end are perfectly competitive markets. These have many sellers. Their products are almost identical. No single firm has any real power to set the price.

At the other end is a monopoly. In a monopoly, one firm controls the whole market.

In between are the markets most students meet in real life. Some have a handful of dominant firms. A handful means a small number, and dominant firms are the biggest and most powerful ones. Other markets have many smaller firms that try to stand out through branding, quality or service.

QA Haiku: All points are kept, the sentences are much shorter with plainer words, and the plain explanation of 'branding' is correct and allowed. — QA Sonnet: All the original points are kept, the added explanations of 'spectrum', 'handful' and 'dominant' are correct, and the short sentences and plainer wording make it clearly easier to read.

### economics-aqa

**Original:** Competition puts constant downward pressure on prices. If one petrol station on a busy road cuts its forecourt price, drivers quickly notice and switch to it. Rivals must respond or lose customers. The result is that prices in competitive fuel markets stay close to the underlying cost of supply. Consumers win directly through lower prices and indirectly because firms are forced to keep their costs as low as possible.

**Live prompt:** Competition keeps prices down. If one petrol station on a busy road cuts its forecourt price, drivers quickly notice and go there. Rivals must do the same or they lose customers. So prices in competitive fuel markets stay close to the underlying cost of supply. Consumers benefit in two ways. They pay less directly. They also benefit because firms are forced to keep their costs as low as possible.

**Proposed (Haiku):** Competition makes prices go down all the time. When one petrol station on a busy road cuts its price, drivers notice quickly. They switch to that station. Other stations have to lower their prices too, or they will lose customers. In competitive markets, prices stay close to what it actually costs to supply petrol. Consumers gain in two ways. First, they pay less. Second, companies must keep their costs as low as possible. This helps consumers.

**Proposed (Sonnet):** Competition keeps pushing prices down all the time. Imagine one petrol station on a busy road cuts its forecourt price. The forecourt is the area where drivers fill up their cars. Drivers quickly notice the lower price. They switch to that petrol station. The rival petrol stations must respond, or they will lose customers.

So in competitive fuel markets, prices stay close to the underlying cost of supply. This is the cost of getting the fuel to sell. Consumers win in two ways. They win directly, because prices are lower. They win indirectly, because firms are forced to keep their costs as low as possible.

QA Haiku: The first sentence changes the meaning: 'constant downward pressure' becomes 'prices go down all the time', which is wrong and clashes with prices staying close to cost. — QA Sonnet: All the points are kept, but it is mostly a near-copy of the original with split sentences and two added explanations, and the hard words are still there.

### engineering-eduqas

**Original:** Copper is notable in engineering for its outstanding electrical conductivity — it is the standard material for electrical wiring in buildings, appliances and vehicles precisely because it allows current to flow with very low resistance. Copper also has excellent thermal conductivity, making it useful for heat exchangers and water pipes. It is relatively soft and ductile (can be drawn into fine wire or bent into pipe without cracking). Copper corrodes slowly in air, forming a green patina (copper carbonate) that protects the surface beneath. Common uses include electrical cables, water distribution pipes, the coils of electric motors, and printed circuit board tracks.

**Live prompt:** Copper is important in engineering for its outstanding electrical conductivity. It is the standard material for electrical wiring in buildings, appliances and vehicles because it allows current to flow with very low resistance. Copper also has excellent thermal conductivity, making it useful for heat exchangers and water pipes. It is relatively soft and ductile, which means it can be drawn into fine wire or bent into pipe without cracking. Copper corrodes slowly in air, forming a green patina (copper carbonate) that protects the surface below. Common uses include electrical cables, water distribution pipes, the coils of electric motors, and printed circuit board tracks.

**Proposed (Haiku):** Copper is important in engineering because it is an excellent electrical conductor. This means electricity flows through it very easily. It has very low resistance (almost nothing stops the electricity). Engineers use copper for electrical wiring in buildings, appliances and vehicles for this reason.

Copper also has excellent thermal conductivity — this means heat passes through it very easily. People use it for heat exchangers (special equipment that moves heat from one place to another) and for water pipes.

Copper is relatively soft and ductile. You can stretch it into very fine wire or bend it into pipe shape without it cracking.

Copper corrodes slowly in air. This means it rusts very slowly and forms a green layer called a patina (copper carbonate). This green layer actually protects the copper underneath.

Common uses for copper are electrical cables, water distribution pipes, the coils inside electric motors, and printed circuit board tracks (the tiny metal paths on circuit boards that carry electricity).

**Proposed (Sonnet):** Copper is well known in engineering because it has outstanding electrical conductivity. Electric current flows through it very easily, with very low resistance. This is why copper is the usual material for electrical wiring in buildings, appliances and vehicles.

Copper also has excellent thermal conductivity. Heat passes through it easily. This makes it useful for heat exchangers and water pipes.

Copper is relatively soft and ductile. This means it can be drawn into fine wire or bent into pipe without cracking.

Copper corrodes slowly in air. A green layer forms on it, called a patina. The patina is copper carbonate. It protects the surface underneath.

Common uses include electrical cables, water distribution pipes, the coils of electric motors, and printed circuit board tracks.

QA Haiku: It explains 'corrodes' as 'rusts', which is wrong because rust is specific to iron and copper forms a green patina instead. — QA Sonnet: Every point, term and name from the original is kept with no new facts. The sentences are much shorter and the wording is plainer, with a correct explanation of ductile and thermal conductivity.

### engineering-eduqas

**Original:** Material selection requires matching the material’s properties to the engineering requirements of the product. A bicycle frame needs high tensile strength (to resist being pulled apart under load) and low density (to reduce weight) — aluminium alloy meets both. A kitchen sink needs corrosion resistance and ease of cleaning — stainless steel is the standard answer. Electrical wiring needs high conductivity and ductility — copper. Cutting tools need hardness and edge retention — tool steel. Decorative plumbing fittings need corrosion resistance and machinability — brass. Exam questions often present a product and ask you to justify a specific material choice by linking properties to requirements. Use the pattern: state the property, link it to the product requirement, name the material that provides it.

**Live prompt:** Choosing a material means matching its properties to what the product needs. A bicycle frame needs high tensile strength (so it does not snap under load) and low density (to keep weight down). Aluminium alloy meets both. A kitchen sink needs corrosion resistance (so it does not rust) and ease of cleaning. Stainless steel is the answer. Electrical wiring needs high conductivity (to carry electricity) and ductility (so it can bend without breaking). Copper works. Cutting tools need hardness (so they do not blunt easily) and edge retention (to stay sharp). Tool steel is the answer. Decorative plumbing fittings need corrosion resistance (so they do not rust) and machinability (they can be shaped easily). Brass works. Exam questions show a product and ask you to explain why a certain material is used. You do this by linking its properties to what the product needs. Follow this pattern: state what property it needs, explain why the product needs it, then name the material.

**Proposed (Haiku):** When you choose a material, you match its properties to what the product needs. A bicycle frame needs high tensile strength (to resist being pulled apart under load) and low density (to reduce weight) — aluminium alloy provides both. A kitchen sink needs corrosion resistance (so it does not rust) and to be easy to clean — stainless steel is the answer. Electrical wiring needs high conductivity (which means electricity passes through it easily) and ductility (which means it can be bent without breaking) — copper. Cutting tools need hardness and the ability to keep a sharp edge — tool steel. Decorative plumbing fittings need corrosion resistance and machinability (which means they can be shaped during manufacture) — brass. In exams, you are given a product and asked to explain a material choice. You show how its properties match what the product needs. Follow this pattern: name the property, link it to what the product needs, then name the material.

**Proposed (Sonnet):** Choosing a material means matching its properties to what the product needs to do. A bicycle frame needs high tensile strength. This means it can resist being pulled apart under load. It also needs low density, so the frame weighs less. Aluminium alloy has both.

A kitchen sink needs corrosion resistance. It also needs to be easy to clean. Stainless steel is the usual choice.

Electrical wiring needs high conductivity and ductility. Copper has both.

Cutting tools need hardness and edge retention. Tool steel has both.

Decorative plumbing fittings need corrosion resistance and machinability. Brass has both.

Exam questions often show you a product. They then ask you to give reasons for a choice of material. You do this by linking properties to requirements. Use this pattern:

1. State the property.
2. Link it to what the product needs.
3. Name the material that has that property.

QA Haiku: The plain explanation of 'ductility' as 'can be bent without breaking' is inaccurate, and the rewrite is only modestly easier to read. — QA Sonnet: All materials, properties, examples and the three-step exam pattern are kept, with shorter sentences and plainer wording such as 'give reasons' instead of 'justify'.

### english-literature

**Original:** Scene Five introduces Hecate, the goddess of witchcraft, who scolds the witches for dealing with Macbeth without her permission. Many scholars believe this scene was not written by Shakespeare but added later by Thomas Middleton. Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic, equivocal language to suggest he does not believe Macbeth’s version of events. The lord reveals that Macduff has gone to England to seek Malcolm and military support from King Edward. These scenes set up Act Four’s escalation.

**Live prompt:** Scene Five introduces Hecate, the goddess of witchcraft, who scolds the witches for dealing with Macbeth without her permission. Many scholars believe this scene was not written by Shakespeare but was added later by Thomas Middleton. Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic, equivocal language to show he does not believe Macbeth's story of events. The lord says that Macduff has gone to England to find Malcolm and ask King Edward for military support. These scenes set up Act Four's escalation.

**Proposed (Haiku):** Scene Five introduces Hecate, the goddess of witchcraft. She tells off the witches for dealing with Macbeth without her permission. Many scholars believe Thomas Middleton wrote this scene later, not Shakespeare.

Scene Six shows Lennox talking to another lord. Lennox uses sarcastic words (saying the opposite of what he really thinks). He also uses unclear words (words that could mean different things). This shows that Lennox does not believe Macbeth's story of what happened.

The lord tells them that Macduff has gone to England. He wanted to find Malcolm and get military help from King Edward.

These two scenes lead into Act Four, where things become much more serious and dangerous.

**Proposed (Sonnet):** Scene Five introduces Hecate, the goddess of witchcraft. She scolds the witches because they dealt with Macbeth without her permission. Many scholars (experts who study the play) believe Shakespeare did not write this scene. They think Thomas Middleton added it later.

Scene Six is a conversation between Lennox and another lord. Lennox uses sarcastic, equivocal language. Sarcastic words mock what they seem to say. Equivocal words can be understood in two ways. This suggests Lennox does not believe Macbeth's version of events, which is the story Macbeth tells about what happened.

The lord reveals that Macduff has gone to England. Macduff has gone to seek Malcolm and military support from King Edward. These scenes set up Act Four, where the tension and danger rise.

QA Haiku: All points, names and details are kept, sarcastic and equivocal are explained correctly, and the sentences and words are clearly simpler than the original. — QA Sonnet: Mostly a near-copy that splits sentences and adds glosses, with hard words left in and one loose explanation.

### english-literature

**Original:** In Scene Two, the relationship between Macbeth and Lady Macbeth shifts dramatically. Lady Macbeth reveals her own despair in a rhyming couplet: ‘Nought’s had, all’s spent, / Where our desire is got without content.’ Despite being queen, she has gained nothing of value. The word ‘spent’ suggests exhaustion — emotionally, morally, and spiritually drained. She also says ‘’Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy’ — meaning it would be better to be dead like Duncan than to live with this guilt.

**Live prompt:** In Scene Two, the relationship between Macbeth and Lady Macbeth shifts greatly. Lady Macbeth shows her despair in a rhyming couplet: 'Nought's had, all's spent, / Where our desire is got without content.' Even though she is now queen, she has got nothing of real value. The word 'spent' suggests exhaustion — she is worn out emotionally, morally, and spiritually. She also says ''Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy' — it would be better to be dead like Duncan than to live with this guilt.

**Proposed (Haiku):** In Scene Two, the relationship between Macbeth and Lady Macbeth changes a lot. Lady Macbeth shows her own sadness and hopelessness in a rhyming couplet (two lines of poetry that rhyme): 'Nought's had, all's spent, / Where our desire is got without content.' Although she is queen, she has nothing worth having. The word 'spent' shows she is exhausted in three ways: in her feelings, in her sense of right and wrong, and in her inner spirit. She also says ''Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy' — meaning it would be better to be dead like Duncan than to live with this guilt.

**Proposed (Sonnet):** In Scene Two, the relationship between Macbeth and Lady Macbeth changes a lot. Lady Macbeth shows her own despair (a deep feeling of having no hope). She does this in a rhyming couplet, which is two lines next to each other that rhyme: ‘Nought’s had, all’s spent, / Where our desire is got without content.’ She is queen, but she has gained nothing of value. The word ‘spent’ suggests she is worn out. She feels drained in her emotions, in her sense of right and wrong, and in her spirit.

She also says ‘’Tis safer to be that which we destroy / Than by destruction dwell in doubtful joy’. This means it would be better to be dead like Duncan than to live with this guilt.

QA Haiku: All the facts and quotations are kept, but it is a near-copy with a few word swaps and no shorter sentences, so it is not clearly easier for a weak Year 7 reader. — QA Sonnet: All quotes, names and points are kept exactly, the two added explanations (despair, rhyming couplet) are correct, and the sentences and word choices are noticeably plainer.

### english-literature-aqa

**Original:** By Chapter 8, the novella’s central argument is clear: power inevitably corrupts. Napoleon has become indistinguishable from the human oppressors the revolution was supposed to replace. The commandments have been rewritten, the original ideals abandoned, and the working animals are worse off than ever. Orwell suggests this is not unique to the Russian Revolution — it is a pattern that recurs whenever a small group seizes power without accountability.

**Live prompt:** By Chapter 8, the novella's central argument is clear: power inevitably corrupts. Napoleon has become no different from the human oppressors the revolution was meant to replace. The commandments have been rewritten, the original ideals abandoned, and the working animals are worse off than ever. Orwell suggests this is not unique to the Russian Revolution. It is a pattern that happens whenever a small group seizes power without anyone to answer to.

**Proposed (Haiku):** By Chapter 8, the novella's main idea is clear: power always makes people behave badly.

Napoleon now looks and acts like the cruel humans the animals fought to get rid of. The commandments have been changed. The animals' first dreams have been forgotten. The working animals now suffer more than before.

Orwell shows that this does not happen only in the Russian Revolution. It is something that happens again and again: whenever a small group takes power and no one checks what they do, they become corrupt.

**Proposed (Sonnet):** By Chapter 8, the main argument of the novella (a short novel) is clear. Power will always corrupt. It makes people selfish and dishonest. Napoleon is now just like the human oppressors, the cruel rulers who treated the animals unfairly. The revolution was supposed to get rid of those humans.

The commandments have been rewritten. The animals' first ideals have been given up. The working animals have harder lives than ever.

Orwell suggests this does not only happen in the Russian Revolution. It happens again and again. A small group takes power, and nobody can make them answer for what they do.

QA Haiku: All points, names and the chapter number are kept, and the sentences are shorter and use plainer words. — QA Sonnet: The rewrite adds a claim that is not in the original: that power 'makes people selfish and dishonest'.

### english-literature-aqa

**Original:** By Act 4, Scotland under Macbeth has become a place of fear and suffering. Ross tells Lady Macduff that “cruel are the times” and that people “float upon a wild and violent sea.” The motif of Scotland as a diseased or storm-tossed nation runs through the second half of the play, contrasting with Duncan’s Scotland, which was characterised by growth and natural order.

**Live prompt:** By Act 4, Scotland under Macbeth has become a place of fear and suffering. Ross tells Lady Macduff that "cruel are the times" and that people "float upon a wild and violent sea." The motif of Scotland as a sick or storm-tossed place runs through the second half of the play. It contrasts with Duncan's Scotland, which had growth and natural order.

**Proposed (Haiku):** By Act 4, Scotland under Macbeth is a place of fear and suffering. Ross tells Lady Macduff that "cruel are the times." He also says people "float upon a wild and violent sea." This means everyone is now in danger and chaos. The motif (an idea that repeats) of Scotland as diseased or storm-tossed runs throughout the second half of the play. Scotland is shown as sick and battered by storms. This is very different from Duncan's Scotland. Under Duncan, Scotland had growth and natural order. Everything was healthy and in its right place.

**Proposed (Sonnet):** By Act 4, Scotland under Macbeth has become a place of fear and suffering. Ross tells Lady Macduff that “cruel are the times” and that people “float upon a wild and violent sea.” This compares life in Scotland to being tossed about on a rough sea.

A motif (an idea that keeps coming back) runs through the second half of the play. It shows Scotland as a nation that is ill, or thrown about like a ship in a storm. Duncan's Scotland was different. It was marked by growth and natural order (things as they should be).

QA Haiku: The rewrite adds interpretive claims that are not in the original, and much of the harder wording is still there. — QA Sonnet: All names, quotes and points are kept, 'motif' is retained with a correct gloss, and the sentences are shorter and plainer with no new facts.

### english-literature-eduqas

**Original:** For a question on the funeral scene, zoom into Hill's word choices. Don't just say 'she looked scary' — analyse specific words: "'Wasted' connotes disease and decay, suggesting the woman is not fully alive. 'Tautly stretched' creates the image of skin pulled tight over a skull, evoking death. Hill's restraint — giving just enough physical detail — follows the M.R. James convention that suggestion generates more fear than graphic description."

**Live prompt:** I'm ready to rewrite GCSE revision text into plainer English. Please share the text you'd like me to simplify, and I'll apply the rules: keeping specialist terms unchanged, simplifying sentences around them, preserving all facts and numbers, and using everyday language with shorter sentences.

**Proposed (Haiku):** For a question on the funeral scene, look closely at Hill's word choices. Do not just say 'she looked scary'. Analyse specific words instead.

Take 'Wasted'. This connotes disease and decay. It suggests the woman is not fully alive. Take 'Tautly stretched'. This creates an image of skin pulled tight over a skull. This makes us think of death.

Hill shows restraint. She gives just enough detail about the woman's appearance. This follows the M.R. James convention. Suggestion (hinting at things) creates more fear than graphic (very detailed) description.

**Proposed (Sonnet):** For a question on the funeral scene, look closely at Hill's word choices. Do not just write 'she looked scary'. Instead, analyse specific words, like this:

"'Wasted' connotes disease and decay, suggesting the woman is not fully alive. 'Tautly stretched' creates the image of skin pulled tight over a skull, evoking death. Hill's restraint — giving just enough physical detail — follows the M.R. James convention that suggestion generates more fear than graphic description."

In plain words, "wasted" makes the reader think of illness and rotting. This suggests the woman is not fully alive. "Tautly stretched" means pulled tight. It makes the reader picture skin tight over a skull, and that brings death to mind. Hill holds back and gives only a little physical detail. This follows the M.R. James convention (the usual way of writing in his stories). The idea is that hinting at something frightens readers more than describing every horrible detail.

QA Haiku: The original's long double-quoted example passage was reworded and its quotation marks removed, so the quoted text is no longer unchanged. — QA Sonnet: The rewrite keeps every name, word and the quoted example exactly, then explains it in short sentences with plainer words, adding no new facts.

### english-literature-eduqas

**Original:** After the funeral, Arthur mentions the woman in black to Mr Jerome, expecting a simple explanation. Jerome's reaction is extreme: he goes "grey" in the face, his hands tremble, and he becomes "unable to speak." Hill uses Jerome's physical response to convey terror without explaining its cause. This is a key structural technique: the reader's fear builds not because we know what the woman is, but because we see the effect she has on people who do know. Jerome's inability to articulate the danger mirrors the town's collective silence — the curse is too terrible to name.

**Live prompt:** After the funeral, Arthur tells Mr Jerome about the woman in black. He expects a simple answer. Jerome's reaction is extreme: his face turns grey, his hands shake, and he cannot speak. Hill uses Jerome's physical reaction to show fear without explaining why. This is a key structural technique: readers become scared not because we know what the woman is, but because we see the effect she has on people who do know. Jerome cannot put the danger into words. This mirrors the town's silence. The curse is too terrible to say.

**Proposed (Haiku):** After the funeral, Arthur tells Mr Jerome about the woman in black. He expects a simple explanation. But Jerome reacts very strongly and suddenly. His face becomes 'grey' in the face. His hands shake. He is 'unable to speak.'

Hill shows Jerome's fear through his body. She does not explain why he is afraid. This is a key structural technique. The reader becomes afraid. But the reader does not become afraid because we know what the woman is. The reader becomes afraid because we see how the people who know about her are afraid.

Jerome cannot say what the danger is. This is like how the whole town stays silent. No one will speak about the curse. The curse is so terrible that no one will name it.

**Proposed (Sonnet):** After the funeral, Arthur talks to Mr Jerome about the woman in black. He expects a simple explanation. Jerome reacts very strongly. His face goes "grey". His hands tremble (shake). He becomes "unable to speak."

Hill uses Jerome's physical response to show terror. Hill does not explain what causes it. This is a key structural technique. The reader's fear grows, but not because we know what the woman is. It grows because we see how she affects people who do know.

Jerome cannot put the danger into words. This mirrors the town's collective silence, which means the whole town stays quiet about it together. The curse is too terrible to name.

QA Haiku: It is easier to read and keeps the quotations and points, but it adds a detail the original does not state: that Jerome reacts 'suddenly'. — QA Sonnet: Every point and both quotations are kept, the explanation of 'collective silence' is correct, and the sentences are short and the wording plainer.

### film-studies-eduqas

**Original:** The Steadicam was developed in the mid-1970s and transformed how directors could follow actors through complex environments. Because it absorbs all camera shake, the footage has a distinctive floating, slightly uncanny quality that sits between the coldly mechanical precision of a dolly and the raw instability of handheld work. Handheld cinematography, by contrast, introduces tremor and unpredictability, placing the spectator in a position of nervous proximity to the action — commonly used in chase sequences, combat, or moments of emotional volatility.

**Live prompt:** The Steadicam was developed in the mid-1970s and changed how directors could follow actors through complicated settings. Because it removes camera shake, the footage has a distinctive floating look that feels slightly strange. It sits somewhere between the mechanical precision of a dolly and the shaky, unpredictable quality of handheld work. Handheld cinematography, by contrast, adds shaking and unpredictability, placing the viewer close to the action and making them feel tense. It is commonly used in chase sequences, combat, or moments of intense emotion.

**Proposed (Haiku):** The Steadicam was developed in the mid-1970s. It changed how directors filmed. A Steadicam removes camera shake (movement that happens by accident). This creates a floating look that feels slightly strange or odd. This quality sits somewhere between a dolly (a camera on wheels that moves smoothly) and handheld work (a camera that shakes).

By contrast, handheld cinematography works differently. The camera shakes and moves unpredictably. This makes the viewer feel nervous and close to the action. Filmmakers use it in chase sequences, fights, and emotional moments—when characters have strong feelings.

**Proposed (Sonnet):** The Steadicam was developed in the mid-1970s. It changed how directors could follow actors through complicated places. It soaks up all the camera shake. This gives the footage a floating look that feels slightly strange and eerie. That look sits between two other styles. A dolly gives cold, mechanical, very exact shots. Handheld work is raw and shaky.

Handheld cinematography is different. It adds tremor (shaking) and is unpredictable. This puts the spectator, the person watching, close to the action. It makes them feel nervous. Directors often use it in chase sequences, in combat, or in moments of emotional volatility, when feelings can suddenly change or explode.

QA Haiku: The rewrite drops the point that the Steadicam let directors follow actors through complex environments, and loses other details from the original. — QA Sonnet: All points, the date and the terms are kept, sentences are much shorter with plainer words, and the added glosses (tremor, spectator, emotional volatility) are correct.

### film-studies-eduqas

**Original:** The angle from which a camera views a subject shapes the power dynamic the spectator perceives. A high angle positions the lens above the subject and tilts it downward, so the figure looks diminished and exposed. Used on a protagonist entering a hostile environment, it signals that they are at a disadvantage. The opposite, a low angle, positions the camera below the subject and tilts it upward. The subject towers over the spectator’s viewpoint, appearing dominant or threatening.

**Live prompt:** Camera angle affects how strong or weak someone appears to the viewer. A high angle puts the camera above the subject, looking downward. The person looks small and exposed. When a high angle is used on a protagonist entering a dangerous place, it shows they are at a disadvantage. A low angle is the opposite. The camera is below the subject, looking upward. The person towers over the viewer. They appear dominant or threatening.

**Proposed (Haiku):** The camera angle shapes how powerful the viewer thinks a character is.

A high angle positions the lens above the subject and tilts it downward. The figure looks smaller and unprotected. When used on a protagonist (main character) entering a dangerous place, it shows they are in trouble.

The opposite is a low angle. It positions the camera below the subject and tilts it upward. The subject now seems much bigger and more powerful than the viewer. They appear dominant (in control) or threatening (dangerous).

**Proposed (Sonnet):** The camera angle changes how powerful a subject seems to the spectator (the person watching). A high angle puts the lens above the subject. The camera tilts downward. The figure looks smaller, less important and unprotected.

Sometimes a high angle is used on a protagonist (the main character) who enters a hostile environment, which is an unfriendly or dangerous place. This signals that the protagonist is at a disadvantage, or in a weaker position.

A low angle is the opposite. It puts the camera below the subject and tilts it upward. The subject seems to tower over the spectator's viewpoint, which means it looks very tall and looms above them. The subject then looks dominant (in control) or threatening.

QA Haiku: Most content is kept and the explanations are correct, but the two key sentences on high and low angles are largely copied from the original, so the rewrite is not clearly easier for a weak reader. — QA Sonnet: All the original points are kept with no wrong or new facts, the sentences are shorter, and the hard words are explained correctly in plain language.

### geography

**Original:** Many people trust that scientists can predict eruptions and earthquakes in time for evacuations. They also have confidence in modern engineering — earthquake-resistant buildings, early warning systems and well-rehearsed emergency plans. This sense of security encourages people to stay, especially in wealthier countries where these measures are well-funded.

**Live prompt:** Many people believe that scientists can predict eruptions and earthquakes in time for evacuations. They also trust modern engineering, such as earthquake-resistant buildings, early warning systems and well-rehearsed emergency plans. This feeling of safety encourages people to stay, especially in wealthier countries where these measures get better funding.

**Proposed (Haiku):** Many people believe scientists can predict eruptions and earthquakes in time for them to escape. They also trust modern engineering to keep them safe. Earthquake-resistant buildings, early warning systems (systems that warn people quickly), and emergency plans all help with this. This feeling of safety makes people want to stay. It is strongest in richer countries that can afford these measures.

**Proposed (Sonnet):** Many people trust scientists. They believe scientists can predict eruptions and earthquakes early enough for evacuations, when people leave a dangerous area. Many people also trust modern engineering. This includes buildings made to resist earthquakes, early warning systems and emergency plans that people have practised well. These things make people feel safe, so they choose to stay where they live. This is especially true in wealthier countries, where plenty of money is spent on these measures.

QA Haiku: The rewrite drops the detail that the emergency plans are "well-rehearsed" and is only a mild simplification of the original. — QA Sonnet: All points are kept with no new facts, the 'evacuations' gloss is correct, and the shorter sentences and plainer phrasing (feel safe, practised well, money is spent) make it easier to read.

### geography

**Original:** Scale of the hazard — a magnitude 9 earthquake poses far greater risk than a magnitude 1 earthquake. A Category 5 tropical storm is more destructive than a Category 1. Wealth of the country — wealthier countries can afford stronger buildings, better warning systems, trained emergency services and medical support. Poorer countries have fewer resources to prepare or respond. Population size and proximity — the more people living near a hazard, the greater the risk. As the world’s population grows and more land is inhabited, more people are exposed to natural hazards.

**Live prompt:** The size of the hazard — a magnitude 9 earthquake causes far more danger than a magnitude 1 earthquake. A Category 5 tropical storm is more damaging than a Category 1. How rich a country is — richer countries can afford to build stronger buildings, have better warning systems, trained emergency services and medical support. Poorer countries have less money to prepare for or respond to hazards. How many people live near the hazard — the more people living near a hazard, the higher the risk. As the world's population grows and more land is built on, more people are exposed to natural hazards.

**Proposed (Haiku):** How big the hazard is affects the risk. A magnitude 9 earthquake poses far greater risk than a magnitude 1 earthquake. A Category 5 tropical storm causes far more damage than a Category 1. Richer countries can afford strong buildings, better warning systems, trained emergency workers, and medical help. Poorer countries do not have enough money or supplies to prepare or respond. The more people living near a hazard, the greater the risk. As the world's population grows and people spread to more land, more people face natural hazards.

**Proposed (Sonnet):** Scale of the hazard: this is how big or strong the hazard is. A magnitude 9 earthquake is much more risky than a magnitude 1 earthquake. A Category 5 tropical storm does more damage than a Category 1 tropical storm.

Wealth of the country: wealthier countries have more money to spend on protection. They can afford stronger buildings and better warning systems. They can also pay for trained emergency services and medical support. Poorer countries have fewer resources (less money and equipment) to prepare for a hazard or to respond to it.

Population size and proximity: proximity means how close people live to something. The more people who live near a hazard, the greater the risk. The world's population is growing. People now live on more land than before. This means more people are exposed to natural hazards, so they are more likely to be affected by them.

QA Haiku: All points, numbers and terms are kept, no new facts are added, and the sentences are shorter with plainer wording (e.g. 'proximity' became 'near', 'exposed' became 'face'). — QA Sonnet: A faithful rewrite that keeps every number and point, adds only correct explanations of scale, proximity and resources, and uses shorter sentences and plainer words.

### geography-aqa

**Original:** In a rainforest, climate, plants, animals and soil all depend on each other. Hot, wet conditions support fast plant growth. Plants release water vapour through their leaves (transpiration), which forms clouds and falls as rain — meaning the forest creates much of its own rainfall. Animals pollinate plants and disperse their seeds. Decomposers recycle nutrients fast enough that the thin soil supports the world's tallest trees. Cut down enough trees and the cycle breaks — less transpiration means less rain, drier conditions, and the forest cannot regrow.

**Live prompt:** In a rainforest, climate, plants, animals and soil all depend on each other. Hot, wet conditions help plants grow fast. Plants release water vapour through their leaves (transpiration). This forms clouds and falls as rain. So the forest makes much of its own rainfall. Animals pollinate plants and disperse their seeds. Decomposers recycle nutrients fast, so the thin soil supports the world's tallest trees. Cut down enough trees and the cycle breaks. Less transpiration means less rain, drier conditions, and the forest cannot regrow.

**Proposed (Haiku):** In a rainforest, climate, plants, animals and soil all depend on each other. The hot, wet weather helps plants grow quickly. Plants release water vapour through their leaves (transpiration). This forms clouds. Then rain falls. The forest creates much of its own rainfall. Animals pollinate plants, which helps them make seeds. Animals also disperse their seeds to new places. Decomposers recycle nutrients (plant food) fast enough that even thin soil supports the world's tallest trees. If you cut down enough trees, the cycle breaks. Less transpiration means less rain. Conditions get drier. The forest cannot regrow.

**Proposed (Sonnet):** In a rainforest, the climate, plants, animals and soil all depend on each other. The conditions are hot and wet. This helps plants grow fast.

Plants release water vapour (water as a gas) through their leaves. This is called transpiration. The water vapour forms clouds, and the water falls as rain. So the forest makes much of its own rainfall.

Animals pollinate plants (they move pollen from one plant to another). Animals also disperse the plants' seeds, which means they spread the seeds to new places.

Decomposers recycle nutrients very fast. Nutrients are the goodness that plants take from the soil. Because of this, the thin soil can still support the world's tallest trees.

If people cut down enough trees, the cycle breaks. There is less transpiration, so there is less rain. The conditions become drier. Then the forest cannot regrow.

QA Haiku: All points are kept, the subject terms are kept with short correct glosses (plant food, help make seeds, new places), and the sentences are much shorter and easier to follow. — QA Sonnet: All points and terms are kept, the added explanations are correct, and the short sentences with plain wording make it easier for a weak reader.

### geography-aqa

**Original:** Animals are adapted to the layered environment. Howler monkeys have prehensile tails that work as a fifth limb in the canopy. Sloths move so slowly that algae grow in their fur, providing camouflage. Poison dart frogs are brightly coloured to warn predators of toxic skin. Toucans have huge bills to reach fruit on slender branches that wouldn't support their weight. Jaguars are the only big cat that hunts mainly in water.

**Live prompt:** Animals are adapted to the layered environment. Howler monkeys have prehensile tails. These work as a fifth limb in the canopy. Sloths move very slowly. Algae grow in their fur and give them camouflage. Poison dart frogs are brightly coloured. They warn predators that their skin is toxic. Toucans have huge bills. This helps them reach fruit on slender branches. The branches would not hold the bird's full weight. Jaguars are the only big cat that hunts mainly in water.

**Proposed (Haiku):** The rainforest has different layers. Different animals are suited to each layer.

Howler monkeys live high in the canopy (the top layer). They have prehensile tails that can grip. A prehensile tail works like a fifth arm.

Sloths move very slowly. Algae grows in their fur because they move so slowly. This algae is camouflage, hiding the sloth from predators.

Poison dart frogs have very bright colours. The bright colours warn predators that the frog's skin is toxic (poisonous).

Toucans have huge bills (beaks). They use the bills to grab fruit on thin branches. The branches are too weak to hold a toucan's weight.

Jaguars are big cats. They are the only big cat that hunts mainly in water.

**Proposed (Sonnet):** Animals are adapted to the layered environment. This means their bodies have features that help them live there.

Howler monkeys have prehensile tails, which can grip things. The tail works like a fifth limb in the canopy (the top layer of the trees).

Sloths move very slowly. Algae grow in their fur. The algae give the sloths camouflage, so they are hard to see.

Poison dart frogs are brightly coloured. The colours warn predators that their skin is toxic (poisonous).

Toucans have huge bills. The bills help them reach fruit on slender (thin) branches. These branches would not hold the weight of a toucan's body.

Jaguars are the only big cat that hunts mainly in water.

QA Haiku: It adds a fact and gives a wrong explanation: the original never says 'rainforest', and it calls the canopy 'the top layer' when the emergent layer sits above it. — QA Sonnet: All the original points are kept with no new facts, the added explanations are correct, and the shorter sentences and glossed hard words make it clearly easier.

### history

**Original:** Monks had the knowledge, money, and discipline to create much better public health systems than towns had. Monasteries had excellent water supplies and built latrines to carry away sewage, keeping their water source separate from waste. They also had infirmaries for sick monks and herb gardens to grow plants for remedies.

**Live prompt:** Monks had the knowledge, money, and discipline to build much better public health systems than towns had. Monasteries had clean water supplies and built latrines to carry away sewage. They kept their water separate from waste. They also had infirmaries for sick monks and herb gardens to grow plants for medicine.

**Proposed (Haiku):** Monks had knowledge, money, and strong organization. They built much better ways of keeping places clean and healthy than towns. Monasteries had very good water supplies. They built latrines (toilets) to carry sewage away. They made sure their water stayed separate from waste, so it stayed clean. They also had infirmaries (rooms for sick monks) and herb gardens. They grew plants in these gardens to use as medicines.

**Proposed (Sonnet):** Monks had the knowledge, the money and the discipline to build much better public health systems than towns had. Discipline means they kept strictly to rules and routines.

Monasteries were the places where monks lived and worked. They had excellent water supplies. They also built latrines (toilets). The latrines carried sewage (waste from toilets) away. The monks kept their water source separate from this waste.

Monasteries also had infirmaries, which were places to look after sick monks. They had herb gardens too. In these, monks grew plants to make remedies (medicines).

QA Haiku: The rewrite changes 'discipline' to 'strong organization', which is a different idea, and it adds a small claim that was not in the original. — QA Sonnet: All points are kept with no new facts. The glosses (discipline, latrines, sewage, infirmaries, remedies, monasteries) are correct, and the sentences are shorter and plainer, apart from the first sentence, which stays close to the original.

### history

**Original:** Run by monks, nuns, or religious orders — not trained doctors Provided food, shelter, warmth, and prayer for the sick and poor Rarely attempted to treat or cure diseases Often refused entry to patients with infectious diseases to protect other residents The focus was on spiritual care: patients were encouraged to pray and confess their sins

**Live prompt:** Monks, nuns, and religious orders ran these places, though they were not trained doctors. They gave food, shelter, warmth, and prayer to sick and poor people. They rarely tried to treat or cure diseases. They often refused entry to patients with infectious diseases to protect other residents. The focus was on spiritual care: patients were encouraged to pray and confess their sins.

**Proposed (Haiku):** These places were run by monks, nuns, and religious orders (communities of people who followed strict religious rules) - not trained doctors. They gave food, shelter, warmth, and prayer to sick and poor people. They rarely tried to treat diseases or make people better. They often turned away patients who had infectious diseases (illnesses that pass from one person to another). They did this to protect other people living there. They mainly gave spiritual care (helping people's souls and faith, not treating their bodies). They asked patients to pray and confess their sins (admit the wrong things they had done).

**Proposed (Sonnet):** These places were run by monks, nuns, or religious orders (groups of religious people who live by shared rules). Trained doctors did not run them. They gave food, shelter (a safe place to stay), warmth, and prayer to the sick and poor. They rarely tried to treat or cure diseases. They often refused to let in patients with infectious diseases (diseases that spread from person to person). This protected the other residents, the people already living there. The focus was on spiritual care, which means care for the soul, not the body. Patients were encouraged to pray and to confess their sins, which means to admit the wrong things they had done.

QA Haiku: All five points are kept, the sentences are shorter, the wording is plainer, and the added explanations of religious orders, infectious diseases, spiritual care and confess are correct. — QA Sonnet: All points are kept, the added explanations are correct, and the sentences are shorter and use plainer words than the original.

### history-aqa

**Original:** When Britain went to war in South Africa in 1899, recruiting officers in northern industrial cities turned away around 40% of volunteers as physically unfit. In Manchester the rejection rate exceeded 60%. The 1903 Inter-Departmental Committee on Physical Deterioration confirmed the problem and linked it to childhood undernourishment. The Boer War transformed welfare from a moral question (should we help?) into a security question (can we field an army?). National efficiency, not compassion, made reform politically irresistible.

**Live prompt:** In 1899, Britain went to war in South Africa. Recruiting officers in northern industrial cities turned away around 40% of volunteers as physically unfit. In Manchester the rejection rate exceeded 60%. The 1903 Inter-Departmental Committee on Physical Deterioration confirmed the problem and linked it to children not eating enough. The Boer War changed welfare from a moral question (should we help?) into a security question (can we field an army?). National efficiency, not compassion, made reform necessary.

**Proposed (Haiku):** In 1899, Britain went to war in South Africa. Recruiting officers in northern industrial cities turned away about 40% of volunteers. These men were too weak to be soldiers. In Manchester, more than 60% were turned away.

The 1903 Inter-Departmental Committee on Physical Deterioration confirmed the problem. They found the link to childhood undernourishment: many children had not eaten enough food as they grew up, and this made them weak as adults.

The Boer War changed how people thought about welfare (help given to poor people). Before, it was a moral question: "should we help?" Now it was a security question: "can we field an army?" Welfare became less about kindness and more about national strength.

National efficiency (making Britain powerful), not compassion (kindness), made welfare reform unavoidable. Politicians had to make changes.

**Proposed (Sonnet):** Britain went to war in South Africa in 1899. Recruiting officers were signing up men for the army. In northern industrial cities, they turned away around 40% of volunteers. They said these men were physically unfit, which means not healthy or strong enough. In Manchester, they rejected more than 60%.

In 1903, the Inter-Departmental Committee on Physical Deterioration studied the problem and confirmed it was real. It linked the problem to undernourishment in childhood. This means children had not had enough food to grow strong.

The Boer War changed how people thought about welfare, which is help for people in need. Before, welfare was a moral question: should we help? After the war, it became a security question: can we field an army? This means: can we find enough fit men to fight?

National efficiency, not compassion (caring about others), was the reason for reform. Politicians could not ignore it.

QA Haiku: All numbers, names and quoted questions are kept, every point is present, the added explanations are correct, and the sentences and vocabulary are clearly plainer than the original. — QA Sonnet: All numbers, dates, names and places are kept, every point is covered, the added explanations are correct, and the sentences are shorter and plainer.

### history-aqa

**Original:** Nightingale was a trained mathematician. She invented the polar-area chart — later called the rose diagram — to show that more British soldiers in Crimea died from preventable disease than from enemy bullets. She presented her statistics to Lord Panmure and the 1857 Royal Commission on the Health of the Army. Statistics, not anecdotes, won the argument. Her command of data made her one of the first women elected to the Royal Statistical Society in 1858, and her methods gave hospital reform an evidence base that critics could not easily dismiss.

**Live prompt:** Nightingale was a trained mathematician. She invented the polar-area chart — later called the rose diagram — to show that more British soldiers in Crimea died from preventable disease than from enemy bullets. She presented her statistics to Lord Panmure and the 1857 Royal Commission on the Health of the Army. Statistics won the argument, not anecdotes. Her knowledge of data made her one of the first women elected to the Royal Statistical Society in 1858. Her methods gave hospital reform an evidence base that was difficult to dismiss.

**Proposed (Haiku):** Nightingale was trained in mathematics. She invented the polar-area chart — also called the rose diagram. She used it to show that more British soldiers in Crimea died from disease that could have been prevented than from enemy bullets. She presented her numbers to Lord Panmure and the 1857 Royal Commission on the Health of the Army. What won the argument was statistics — real numbers — not just stories. Her skill with data was so strong that she became one of the first women elected to the Royal Statistical Society in 1858. Her methods gave hospital reform evidence that critics could not easily dismiss.

**Proposed (Sonnet):** Nightingale had trained as a mathematician. She invented the polar-area chart. It was later called the rose diagram. She wanted to show something about British soldiers in Crimea. More of them died from preventable disease (disease that could have been stopped) than from enemy bullets.

She showed her statistics to Lord Panmure. She also showed them to the 1857 Royal Commission on the Health of the Army. Statistics won the argument. Stories about single events did not.

She was very skilled with data. In 1858, she became one of the first women elected to the Royal Statistical Society. Her methods gave hospital reform strong proof to rely on. People who disagreed with her could not easily ignore it.

QA Haiku: It is close to a copy of the original, with only a few word swaps and one split sentence, and several sentences are still long and hard for a weak Year 7 reader. — QA Sonnet: All names, dates and points are kept, the added explanation of 'preventable disease' is correct, and the text uses shorter sentences and plainer words.

### media-studies-eduqas

**Original:** When a question asks you to analyse media language on a set cover, avoid simply listing features you can see (“there is a masthead, there is an image, there are cover lines”). Marks for media language analysis are given for explaining the meanings those features construct and why a producer might have chosen them, not for identifying features alone. On the extended comparison question, build every paragraph around both products together — use comparative language such as “whereas” or “similarly” throughout, rather than writing one block on the set product and a separate block on the unseen resource.

**Live prompt:** I'm ready to help simplify GCSE revision text. I understand the rules:

- Keep specialist terms unchanged, simplify around them
- Never alter facts, numbers, dates, names, places, or quotations
- Keep the same information, just plainer language
- Use shorter sentences and everyday words
- Keep a neutral, factual tone with no added commentary

Please paste the revision text you'd like me to rewrite, and I'll make it clearer for students with a lower reading age or learning English as an additional language.

**Proposed (Haiku):** When a question asks you to analyse media language on a set cover, do not just list the features you see. For example, do not write "there is a masthead, there is an image, there are cover lines". You get marks for explaining what those features mean. You also get marks for saying why a producer might have chosen them. You do not get marks just for spotting them. On the extended comparison question, write about both products in every paragraph. Use comparative language such as "whereas" or "similarly" all the way through. Do not write all about the set product first, then all about the unseen resource second.

**Proposed (Sonnet):** When a question asks you to analyse media language on a set cover, do not just list the features you can see. For example, do not write “there is a masthead, there is an image, there are cover lines”. Naming features on their own does not earn marks. You get marks for explaining two things. First, explain the meanings that the features create. Second, explain why a producer might have chosen them.

The extended comparison question works differently. Build every paragraph around both products together. Use comparative language, such as “whereas” or “similarly”, all the way through your answer. Do not write one block about the set product and then a separate block about the unseen resource.

QA Haiku: All points, quotations and terms are kept, and the rewrite uses much shorter sentences and plainer words (e.g. 'spotting' for 'identifying', 'mean' for 'construct') without adding any facts. — QA Sonnet: All points, both quotations and the media terms are kept exactly, no new facts are added, and the sentences are much shorter with plainer wording.

### meta-case

**Original:** This is a genuinely two-part skill: you must connect a specific feature of the cover (a cover line, an image choice, a styling decision) to a specific aspect of context, rather than stating a general historical fact and a general cover description side by side without linking them.

**Live prompt:** I'm ready to rewrite GCSE revision text into plainer English following your rules. However, I don't see the text you'd like me to simplify in your message.

Please paste the GCSE revision passage you need rewritten, and I'll apply the rules you've set out:

- Keep specialist terms unchanged
- Keep numbers, dates, names, places, quotations exactly as they are
- Use shorter sentences and everyday words
- Keep roughly the same length and information
- Maintain a neutral, factual tone
- Output only the rewritten text as plain prose

What text would you like me to work on?

**Proposed (Haiku):** This is a real skill with two parts. You must link something specific from the cover to something specific about the context – what was happening at the time.

A thing on the cover could be a cover line (words printed on the front), the picture chosen, or the way it was designed.

Do not write a general historical fact and then a general cover description without linking them. Instead, show how the cover was made because of what was happening at that time.

**Proposed (Sonnet):** This skill has two parts. First, pick one specific feature of the cover. This could be a cover line, an image choice, or a styling decision (a choice about how the cover looks). Second, link that feature to one specific part of context. Do not just state a general historical fact and then give a general description of the cover next to it. That does not link the two together.

QA Haiku: All points are kept (two-part skill, link a specific cover feature to specific context, avoid unlinked general statements), the sentences are shorter and the words plainer, and the glosses for 'cover line' and 'context' are correct. — QA Sonnet: All points are kept, with no new facts. The sentences are shorter and the words plainer, and the added gloss on 'styling decision' is correct.

### meta-case

**Original:** For AO3, always link context to Shelley’s purpose. Instead of “Galvanism was popular in the early 19th century,” write “Shelley uses Victor’s galvanic experiments to warn against the Enlightenment belief that science can overcome all limits, reflecting contemporary anxieties about rapid scientific progress.” Context should always explain WHY Shelley makes the choices she does.

**Live prompt:** I'm ready to rewrite GCSE revision text into plainer English. Please provide the text you'd like me to simplify, and I'll follow the rules:

- Keep subject terms unchanged, simplify around them
- Preserve all facts, numbers, dates, names, quotations
- Keep the same information, shorter sentences, everyday words
- Neutral tone, no added points or commentary

For literary analysis like Frankenstein, I'll connect context to authorial purpose — explaining why Shelley makes her choices, not just what was happening historically.

Send the text and I'll rewrite it.

**Proposed (Haiku):** For AO3, always link context to Shelley's purpose. Do not just say, 'Galvanism was popular in the early 19th century.' Instead, write, 'Shelley uses Victor's galvanic experiments to warn against the Enlightenment belief that science can overcome all limits, reflecting contemporary anxieties about rapid scientific progress.' This shows how Shelley uses galvanism. It explains what she is trying to tell readers: that science has limits. It shows the fears people had at the time. They were worried about how fast science was changing. Context should always explain WHY Shelley makes the choices she does.

**Proposed (Sonnet):** For AO3, always link context to Shelley’s purpose. In other words, connect the background facts to what Shelley wanted to achieve.

Do not write “Galvanism was popular in the early 19th century,” because that only gives a fact. Instead, write “Shelley uses Victor’s galvanic experiments to warn against the Enlightenment belief that science can overcome all limits, reflecting contemporary anxieties about rapid scientific progress.” This sentence gives a reason. In it, “contemporary anxieties” means the worries people had at that time. “Rapid” means fast.

Context should always explain WHY Shelley makes the choices she does.

QA Haiku: All points, terms and quoted text are kept, and the added short plain sentences accurately explain the hard quoted wording (Enlightenment belief, contemporary anxieties) without adding new facts. — QA Sonnet: All points, names, the AO3 term and both quotations are kept exactly, the new glosses for 'contemporary anxieties' and 'rapid' are correct, and the surrounding sentences are shorter and plainer.
