# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 1.0000 | 0.0000 | 0.0000 | 0.9884 | 0.0113 |
| baseline_calibrated_logistic_orbit | 1.0000 | 0.0000 | 0.0000 | 0.9738 | 0.0277 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| stable | 20 | 20 | 0 | 0.9884 | 0.9738 | 0.0146 |
| wrong_answer | 20 | 0 | 20 | 0.0113 | 0.0277 | -0.0165 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| answer_consistency | 1.0000 | 0.0000 | 1.0000 |
| support_signature_consistency | 1.0000 | 0.0000 | 1.0000 |
| orbit_answer_flip_rate | 0.0000 | 1.0000 | -1.0000 |
| clean_to_worst_gap | 0.0047 | 0.0662 | -0.0615 |
| min_sufficiency | 0.1970 | 0.1354 | 0.0615 |
| verifier_entropy | 0.4964 | 0.4391 | 0.0573 |
| naive_orbit_average | 0.1993 | 0.1721 | 0.0272 |
| mean_sufficiency | 0.1993 | 0.1721 | 0.0272 |
| mean_missing | 0.7459 | 0.7551 | -0.0093 |
| sufficiency_variance | 0.0000 | 0.0026 | -0.0026 |
| max_conflict | 0.0802 | 0.0804 | -0.0002 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### hotpot_supportpreserve:5a764c0b55429976ec32bd89:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0179`
- baseline_score: `0.0533`
- target_minus_baseline: `-0.0354`
- query: What criteria subjectively qualifies the Houston Astrodome to be called the Eighth Wonder of the World?
- candidate_answer: `comparable to the seven Wonders of the World`

Clean evidence:
- `Astrodome`: The NRG Astrodome, also known as the Houston Astrodome or simply The Astrodome, is the world's first multi-purpose, domed sports stadium, located in Houston, Texas. Construction on the stadium began in 1962, and it officially opened in 1965. It served as ho...
- `Eighth Wonder of the World`: Eighth Wonder of the World is an unofficial title sometimes given to new buildings, structures, projects, or even designs that are deemed to be comparable to the seven Wonders of the World.

First perturbation evidence:
- query: What criteria subjectively qualifies the Houston Astrodome to be called the Eighth Wonder of the World? Verify whether the answer is For the Last Time: Live from the Astrodome using the same evidence.
- `Astrodome`: The NRG Astrodome, also known as the Houston Astrodome or simply The Astrodome, is the world's first multi-purpose, domed sports stadium, located in Houston, Texas. Construction on the stadium began in 1962, and it officially opened in 1965. It served as ho...
- `Eighth Wonder of the World`: Eighth Wonder of the World is an unofficial title sometimes given to new buildings, structures, projects, or even designs that are deemed to be comparable to the seven Wonders of the World.

#### hotpot_supportpreserve:5a80522b5542996402f6a4c1:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0178`
- baseline_score: `0.0636`
- target_minus_baseline: `-0.0457`
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres?
- candidate_answer: `fifth-largest`

Clean evidence:
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

First perturbation evidence:
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres? Verify whether the answer is Lawton, Oklahoma using the same evidence.
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

#### hotpot_supportpreserve:5ae25d2b554299495565da46:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0174`
- baseline_score: `0.0643`
- target_minus_baseline: `-0.0469`
- query: Who has more singles titles, Brian Gottfried or Peter Fleming?
- candidate_answer: `21`

Clean evidence:
- `Peter Fleming (tennis)`: Peter Blair Fleming (born January 21, 1955 in Chatham Borough, New Jersey) is a former professional tennis player from the United States. In his doubles partnership with John McEnroe, he won 52 titles, of which seven were at Grand Slams (four at Wimbledon, ...
- `Brian Gottfried`: Brian Edward Gottfried (born January 27, 1952) is a retired tennis player from the United States who won 25 singles titles and 54 doubles titles during his professional career. The right-hander was the runner-up at the 1977 French Open and achieved a career...

First perturbation evidence:
- query: Who has more singles titles, Brian Gottfried or Peter Fleming? Verify whether the answer is Scheer (band) using the same evidence.
- `Peter Fleming (tennis)`: Peter Blair Fleming (born January 21, 1955 in Chatham Borough, New Jersey) is a former professional tennis player from the United States. In his doubles partnership with John McEnroe, he won 52 titles, of which seven were at Grand Slams (four at Wimbledon, ...
- `Brian Gottfried`: Brian Edward Gottfried (born January 27, 1952) is a retired tennis player from the United States who won 25 singles titles and 54 doubles titles during his professional career. The right-hander was the runner-up at the 1977 French Open and achieved a career...

#### hotpot_supportpreserve:5ac213805542992f1f2b37e7:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0173`
- baseline_score: `0.0474`
- target_minus_baseline: `-0.0301`
- query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"?
- candidate_answer: `November`

Clean evidence:
- `Kenn Scott`: Kenn Scott is a Toronto-based screenwriter noted for his work in children's programming and animation. Included amongst the many shows he has written for are "Ned's Newt", "Iggy Arbuckle", "Captain Flamingo", "Rescue Heroes", "Seven Little Monsters", "Pelsw...
- `Pelswick`: Pelswick is an animated television series co-produced by Nelvana Limited and Suzhou Hong Ying Animation Corporation Limited in association with The Canadian Broadcasting Corporation and Nickelodeon. The series is about a teenage boy who uses a wheelchair, e...

First perturbation evidence:
- query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"? Verify whether the answer is Pelswick using the same evidence.
- `Kenn Scott`: Kenn Scott is a Toronto-based screenwriter noted for his work in children's programming and animation. Included amongst the many shows he has written for are "Ned's Newt", "Iggy Arbuckle", "Captain Flamingo", "Rescue Heroes", "Seven Little Monsters", "Pelsw...
- `Pelswick`: Pelswick is an animated television series co-produced by Nelvana Limited and Suzhou Hong Ying Animation Corporation Limited in association with The Canadian Broadcasting Corporation and Nickelodeon. The series is about a teenage boy who uses a wheelchair, e...

#### hotpot_supportpreserve:5a8303c255429954d2e2ec01:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0173`
- baseline_score: `0.0572`
- target_minus_baseline: `-0.0400`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Verify whether the answer is Chrysler F platform using the same evidence.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_supportpreserve:5adf3e355542993a75d26440:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0171`
- baseline_score: `0.0379`
- target_minus_baseline: `-0.0208`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Verify whether the answer is Sweden using the same evidence.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

#### hotpot_supportpreserve:5a899bf955429946c8d6e959:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0167`
- baseline_score: `0.0577`
- target_minus_baseline: `-0.0410`
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted?
- candidate_answer: `2012`

Clean evidence:
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

First perturbation evidence:
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted? Verify whether the answer is NBA 2K15 using the same evidence.
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

#### hotpot_supportpreserve:5a881cbb55429938390d3ee7:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0166`
- baseline_score: `0.0306`
- target_minus_baseline: `-0.0140`
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style?
- candidate_answer: `Hellenism`

Clean evidence:
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

First perturbation evidence:
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style? Verify whether the answer is Greek Revival architecture using the same evidence.
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...


### Low-scoring false negatives

#### hotpot_supportpreserve:5ae1fced5542997283cd230e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9878`
- baseline_score: `0.9718`
- target_minus_baseline: `0.0160`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Please verify each supporting hop.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

#### hotpot_supportpreserve:5ae25d2b554299495565da46:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9880`
- baseline_score: `0.9726`
- target_minus_baseline: `0.0154`
- query: Who has more singles titles, Brian Gottfried or Peter Fleming?
- candidate_answer: `21`

Clean evidence:
- `Peter Fleming (tennis)`: Peter Blair Fleming (born January 21, 1955 in Chatham Borough, New Jersey) is a former professional tennis player from the United States. In his doubles partnership with John McEnroe, he won 52 titles, of which seven were at Grand Slams (four at Wimbledon, ...
- `Brian Gottfried`: Brian Edward Gottfried (born January 27, 1952) is a retired tennis player from the United States who won 25 singles titles and 54 doubles titles during his professional career. The right-hander was the runner-up at the 1977 French Open and achieved a career...

First perturbation evidence:
- query: Who has more singles titles, Brian Gottfried or Peter Fleming? Please verify each supporting hop.
- `Peter Fleming (tennis)`: Peter Blair Fleming (born January 21, 1955 in Chatham Borough, New Jersey) is a former professional tennis player from the United States. In his doubles partnership with John McEnroe, he won 52 titles, of which seven were at Grand Slams (four at Wimbledon, ...
- `Brian Gottfried`: Brian Edward Gottfried (born January 27, 1952) is a retired tennis player from the United States who won 25 singles titles and 54 doubles titles during his professional career. The right-hander was the runner-up at the 1977 French Open and achieved a career...

#### hotpot_supportpreserve:5a8303c255429954d2e2ec01:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9881`
- baseline_score: `0.9734`
- target_minus_baseline: `0.0147`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Please verify each supporting hop.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_supportpreserve:5a899bf955429946c8d6e959:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9881`
- baseline_score: `0.9732`
- target_minus_baseline: `0.0149`
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted?
- candidate_answer: `2012`

Clean evidence:
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

First perturbation evidence:
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted? Please verify each supporting hop.
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

#### hotpot_supportpreserve:5ac26ac15542992f1f2b38bc:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9881`
- baseline_score: `0.9736`
- target_minus_baseline: `0.0145`
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to?
- candidate_answer: `Sam Phillips`

Clean evidence:
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

First perturbation evidence:
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to? Please verify each supporting hop.
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

#### hotpot_supportpreserve:5a80522b5542996402f6a4c1:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9882`
- baseline_score: `0.9725`
- target_minus_baseline: `0.0157`
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres?
- candidate_answer: `fifth-largest`

Clean evidence:
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

First perturbation evidence:
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres? Please verify each supporting hop.
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

#### hotpot_supportpreserve:5adcd2435542992c1e3a241b:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9883`
- baseline_score: `0.9739`
- target_minus_baseline: `0.0144`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Please verify each supporting hop.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_supportpreserve:5ae5dae2554299546bf82fa4:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9883`
- baseline_score: `0.9740`
- target_minus_baseline: `0.0143`
- query: Faruk Halibegovic was born in what city that is the capital and largest city of Bosnia and Herzegovina with a population of 275,524?
- candidate_answer: `Sarajevo`

Clean evidence:
- `Faruk Halilbegović`: Faruk Halilbegović (born 7 September 1987 in Sarajevo, Bosnia and Herzegovina) is a handball left back who plays for Polish club Zagłębie Lubin. He started his career in Bosna Visoko and later played for Borac Banja Luka, Bosna Sarajevo and Sloga Doboj. Wit...
- `Sarajevo`: Sarajevo (Cyrillic: Сарајево , ] , ) is the capital and largest city of Bosnia and Herzegovina, with a population of 275,524 in its current administrative limits. The Sarajevo metropolitan area, including Sarajevo Canton and East Sarajevo is home to 643,016...

First perturbation evidence:
- query: Faruk Halibegovic was born in what city that is the capital and largest city of Bosnia and Herzegovina with a population of 275,524? Please verify each supporting hop.
- `Faruk Halilbegović`: Faruk Halilbegović (born 7 September 1987 in Sarajevo, Bosnia and Herzegovina) is a handball left back who plays for Polish club Zagłębie Lubin. He started his career in Bosna Visoko and later played for Borac Banja Luka, Bosna Sarajevo and Sloga Doboj. Wit...
- `Sarajevo`: Sarajevo (Cyrillic: Сарајево , ] , ) is the capital and largest city of Bosnia and Herzegovina, with a population of 275,524 in its current administrative limits. The Sarajevo metropolitan area, including Sarajevo Canton and East Sarajevo is home to 643,016...


### Target over baseline on negatives

#### hotpot_supportpreserve:5ab90fdd55429916710eb0fc:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0041`
- baseline_score: `0.0020`
- target_minus_baseline: `0.0021`
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from?
- candidate_answer: `London, England`

Clean evidence:
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

First perturbation evidence:
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from? Verify whether the answer is Roscoe Channing using the same evidence.
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

#### hotpot_supportpreserve:5ac26ac15542992f1f2b38bc:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0032`
- baseline_score: `0.0013`
- target_minus_baseline: `0.0019`
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to?
- candidate_answer: `Sam Phillips`

Clean evidence:
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

First perturbation evidence:
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to? Verify whether the answer is Zack Norman using the same evidence.
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

#### hotpot_supportpreserve:5a79332555429907847277e7:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0025`
- baseline_score: `0.0009`
- target_minus_baseline: `0.0017`
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- candidate_answer: `Juan Carlos Onetti`

Clean evidence:
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

First perturbation evidence:
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti? Verify whether the answer is Felipe VI of Spain using the same evidence.
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

#### hotpot_supportpreserve:5adcd2435542992c1e3a241b:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0024`
- baseline_score: `0.0008`
- target_minus_baseline: `0.0016`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Verify whether the answer is Lindsay Crouse using the same evidence.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_supportpreserve:5abd1b6e55429933744ab729:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0024`
- baseline_score: `0.0008`
- target_minus_baseline: `0.0016`
- query: Which of the following cities is a county-level city, Jingzhou or Zixing?
- candidate_answer: `Zixing`

Clean evidence:
- `Jingzhou`: Jingzhou () is a prefecture-level city in southern Hubei, China, located on the banks of the Yangtze River. As of the 2010 census, its total population was 5,691,707, 1,154,086 of whom resided in the built-up ("or metro") area comprising the two urban distr...
- `Zixing`: Zixing () is a county-level city in Hunan Province, China, it is under the administration of Chenzhou prefecture-level City.

First perturbation evidence:
- query: Which of the following cities is a county-level city, Jingzhou or Zixing? Verify whether the answer is KWN31 using the same evidence.
- `Jingzhou`: Jingzhou () is a prefecture-level city in southern Hubei, China, located on the banks of the Yangtze River. As of the 2010 census, its total population was 5,691,707, 1,154,086 of whom resided in the built-up ("or metro") area comprising the two urban distr...
- `Zixing`: Zixing () is a county-level city in Hunan Province, China, it is under the administration of Chenzhou prefecture-level City.

#### hotpot_supportpreserve:5a792ad055429907847277d1:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0024`
- baseline_score: `0.0008`
- target_minus_baseline: `0.0016`
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?
- candidate_answer: `Mickey's PhilharMagic`

Clean evidence:
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

First perturbation evidence:
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?  Verify whether the answer is Stitch's Great Escape! using the same evidence.
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

#### hotpot_supportpreserve:5ae1fced5542997283cd230e:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0012`
- baseline_score: `0.0003`
- target_minus_baseline: `0.0009`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Verify whether the answer is Salah Abu Seif using the same evidence.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

#### hotpot_supportpreserve:5a8ba3ff55429971feec4744:wrong_answer

- label_answerable: `False`
- construction_type: `wrong_answer`
- target_score: `0.0099`
- baseline_score: `0.0125`
- target_minus_baseline: `-0.0026`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Verify whether the answer is New Mexico Governor's Mansion using the same evidence.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...


### Baseline over target on positives

#### hotpot_supportpreserve:5adce88b5542992c1e3a249a:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9884`
- baseline_score: `0.9762`
- target_minus_baseline: `0.0122`
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- candidate_answer: `320 years`

Clean evidence:
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

First perturbation evidence:
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ? Please verify each supporting hop.
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

#### hotpot_supportpreserve:5a792ad055429907847277d1:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9888`
- baseline_score: `0.9763`
- target_minus_baseline: `0.0125`
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?
- candidate_answer: `Mickey's PhilharMagic`

Clean evidence:
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

First perturbation evidence:
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?  Please verify each supporting hop.
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

#### hotpot_supportpreserve:5a881cbb55429938390d3ee7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9885`
- baseline_score: `0.9759`
- target_minus_baseline: `0.0126`
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style?
- candidate_answer: `Hellenism`

Clean evidence:
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

First perturbation evidence:
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style? Please verify each supporting hop.
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

#### hotpot_supportpreserve:5a8ba3ff55429971feec4744:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9886`
- baseline_score: `0.9758`
- target_minus_baseline: `0.0128`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Please verify each supporting hop.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

#### hotpot_supportpreserve:5abd8c295542992ac4f382ab:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9888`
- baseline_score: `0.9755`
- target_minus_baseline: `0.0134`
- query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year?
- candidate_answer: `1874`

Clean evidence:
- `Minnesota State High School Mathematics League`: The Minnesota State High School Mathematics League is the premier high school mathematics league in the state of Minnesota. It was founded in 1980 by Macalester College professor Wayne Roberts. The league holds five statewide tournaments per year from Novem...
- `Macalester College`: Macalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US. It was founded in 1874 as a Presbyterian-affiliated but nonsectarian college. Its first class entered September 15, 1885. Macalester is exclusively...

First perturbation evidence:
- query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year?  Please verify each supporting hop.
- `Minnesota State High School Mathematics League`: The Minnesota State High School Mathematics League is the premier high school mathematics league in the state of Minnesota. It was founded in 1980 by Macalester College professor Wayne Roberts. The league holds five statewide tournaments per year from Novem...
- `Macalester College`: Macalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US. It was founded in 1874 as a Presbyterian-affiliated but nonsectarian college. Its first class entered September 15, 1885. Macalester is exclusively...

#### hotpot_supportpreserve:5adf3e355542993a75d26440:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9885`
- baseline_score: `0.9750`
- target_minus_baseline: `0.0135`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Please verify each supporting hop.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

#### hotpot_supportpreserve:5ab90fdd55429916710eb0fc:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9886`
- baseline_score: `0.9747`
- target_minus_baseline: `0.0139`
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from?
- candidate_answer: `London, England`

Clean evidence:
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

First perturbation evidence:
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from? Please verify each supporting hop.
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

#### hotpot_supportpreserve:5ae55b8255429908b63265ef:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9891`
- baseline_score: `0.9751`
- target_minus_baseline: `0.0141`
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada?
- candidate_answer: `Masayoshi "Masa" Takayama`

Clean evidence:
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...

First perturbation evidence:
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada? Please verify each supporting hop.
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...
