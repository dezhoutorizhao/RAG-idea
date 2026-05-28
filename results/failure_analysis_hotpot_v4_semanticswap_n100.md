# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 0.9500 | 0.0000 | 0.1500 | 0.8863 | 0.2405 |
| baseline_calibrated_logistic_orbit | 0.9525 | 0.0000 | 0.1500 | 0.8947 | 0.2356 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| semantic_swap | 20 | 0 | 20 | 0.2405 | 0.2356 | 0.0049 |
| stable | 20 | 20 | 0 | 0.8863 | 0.8947 | -0.0085 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| verifier_entropy | 0.4993 | 0.4003 | 0.0990 |
| min_sufficiency | 0.1988 | 0.1000 | 0.0988 |
| clean_to_worst_gap | 0.0048 | 0.1035 | -0.0988 |
| naive_orbit_average | 0.2012 | 0.1518 | 0.0494 |
| mean_sufficiency | 0.2012 | 0.1518 | 0.0494 |
| mean_missing | 0.7452 | 0.7754 | -0.0302 |
| sufficiency_variance | 0.0000 | 0.0038 | -0.0037 |
| max_conflict | 0.0792 | 0.0793 | -0.0001 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |
| corm_mean_clean | 0.5000 | 0.5000 | 0.0000 |
| context_sufficiency_clean | 0.2035 | 0.2035 | 0.0000 |
| clean_sufficiency | 0.2035 | 0.2035 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### hotpot_semanticswap:5a8303c255429954d2e2ec01:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8872`
- baseline_score: `0.8974`
- target_minus_baseline: `-0.0102`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Verify the original answer using only the provided evidence.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_semanticswap:5ae55b8255429908b63265ef:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8859`
- baseline_score: `0.8877`
- target_minus_baseline: `-0.0018`
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada?
- candidate_answer: `Masayoshi "Masa" Takayama`

Clean evidence:
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...

First perturbation evidence:
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada? Verify the original answer using only the provided evidence.
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Roxy Hotel (New York City) (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two l...

#### hotpot_semanticswap:5adf3e355542993a75d26440:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8660`
- baseline_score: `0.8757`
- target_minus_baseline: `-0.0097`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Verify the original answer using only the provided evidence.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly Sweden from ...

#### hotpot_semanticswap:5ac31602554299741d48a1bf:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8172`
- baseline_score: `0.8036`
- target_minus_baseline: `0.0136`
- query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"?
- candidate_answer: `Jennifer Taylor`

Clean evidence:
- `Jennifer Taylor (actress)`: Jennifer Taylor (née Bini, and sometimes credited as Jennifer Bini Taylor; born April 19, 1972) is an American actress, best known for her role as Chelsea Melini on CBS sitcom "Two and a Half Men", and earlier, for three other female roles on the show. She ...
- `Zombie Night (2013 film)`: Zombie Night is a 2013 American zombie horror film directed by John Gulager, written by Keith Allan and Delondra Williams from a story by Richard Schenkman, and starring Anthony Michael Hall, Daryl Hannah, Jennifer Taylor, Alan Ruck, and Shirley Jones.

First perturbation evidence:
- query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"? Verify the original answer using only the provided evidence.
- `Jennifer Taylor (actress)`: Wild Things 2 (née Bini, and sometimes credited as Jennifer Bini Taylor; born April 19, 1972) is an American actress, best known for her role as Chelsea Melini on CBS sitcom "Two and a Half Men", and earlier, for three other female roles on the show. She ap...
- `Zombie Night (2013 film)`: Zombie Night is a 2013 American zombie horror film directed by John Gulager, written by Keith Allan and Delondra Williams from a story by Richard Schenkman, and starring Anthony Michael Hall, Daryl Hannah, Wild Things 2, Alan Ruck, and Shirley Jones.

#### hotpot_semanticswap:5adcd2435542992c1e3a241b:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8131`
- baseline_score: `0.8006`
- target_minus_baseline: `0.0125`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Verify the original answer using only the provided evidence.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_semanticswap:5a8ba3ff55429971feec4744:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.4979`
- baseline_score: `0.4224`
- target_minus_baseline: `0.0756`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Verify the original answer using only the provided evidence.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the New Mexico Governor's Mansion. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

#### hotpot_semanticswap:5a80522b5542996402f6a4c1:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0183`
- baseline_score: `0.0105`
- target_minus_baseline: `0.0078`
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres?
- candidate_answer: `fifth-largest`

Clean evidence:
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

First perturbation evidence:
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres? Verify the original answer using only the provided evidence.
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

#### hotpot_semanticswap:5adf8ade5542993344016ce8:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0121`
- baseline_score: `0.0064`
- target_minus_baseline: `0.0057`
- query: Dutch-born American businessman, Harry Koch, fathered a son born in 1900 that founded which oil refinery firm?
- candidate_answer: `Koch Industries`

Clean evidence:
- `Fred C. Koch`: Fred Chase Koch ( ; September 23, 1900 – November 17, 1967) was an American chemical engineer and entrepreneur who founded the oil refinery firm that later became Koch Industries, a privately held company which, under the principal ownership and leadership ...
- `Harry Koch (businessman)`: Hotze "Harry" Koch ( ; 22 October 1867 – 21 June 1942) was a Dutch-born American businessman who founded the "Quanah Tribune-Chief" newspaper. He was the father of Fred C. Koch (1900–1967), founder of Koch Industries.

First perturbation evidence:
- query: Dutch-born American businessman, Harry Koch, fathered a son born in 1900 that founded which oil refinery firm? Verify the original answer using only the provided evidence.
- `Fred C. Koch`: Fred Chase Koch ( ; September 23, 1900 – November 17, 1967) was an American chemical engineer and entrepreneur who founded the oil refinery firm that later became Nghi Sơn Refinery, a privately held company which, under the principal ownership and leadershi...
- `Harry Koch (businessman)`: Hotze "Harry" Koch ( ; 22 October 1867 – 21 June 1942) was a Dutch-born American businessman who founded the "Quanah Tribune-Chief" newspaper. He was the father of Fred C. Koch (1900–1967), founder of Nghi Sơn Refinery.


### Low-scoring false negatives

#### hotpot_semanticswap:5adf3e835542993a75d26442:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7704`
- baseline_score: `0.7914`
- target_minus_baseline: `-0.0210`
- query: Which comic series involves characters such as Nick Fury and Baron von Strucker?
- candidate_answer: `Marvel`

Clean evidence:
- `Nick Fury: Agent of S.H.I.E.L.D. (film)`: Nick Fury: Agent of S.H.I.E.L.D. is an American television film based on the Marvel Comics character Nick Fury. It was first broadcast on May 26, 1998 on Fox. Directed by Rod Hardy, the film stars David Hasselhoff as Fury, a retired super spy who is approac...
- `Fenris (comics)`: Andrea von Strucker and Andreas von Strucker are two fictional characters appearing in American comic books published by Marvel Comics. They are the German twin children of supervillain Baron von Strucker of HYDRA and the half-siblings of Werner von Strucker.

First perturbation evidence:
- query: Which comic series involves characters such as Nick Fury and Baron von Strucker? Please verify each supporting hop.
- `Nick Fury: Agent of S.H.I.E.L.D. (film)`: Nick Fury: Agent of S.H.I.E.L.D. is an American television film based on the Marvel Comics character Nick Fury. It was first broadcast on May 26, 1998 on Fox. Directed by Rod Hardy, the film stars David Hasselhoff as Fury, a retired super spy who is approac...
- `Fenris (comics)`: Andrea von Strucker and Andreas von Strucker are two fictional characters appearing in American comic books published by Marvel Comics. They are the German twin children of supervillain Baron von Strucker of HYDRA and the half-siblings of Werner von Strucker.

#### hotpot_semanticswap:5ae1fced5542997283cd230e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7845`
- baseline_score: `0.8012`
- target_minus_baseline: `-0.0167`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Please verify each supporting hop.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

#### hotpot_semanticswap:5a8078d85542995d8a8ddf78:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8362`
- baseline_score: `0.8286`
- target_minus_baseline: `0.0077`
- query: Which of the following rock bands is from Chicago: Kill Hannah or Louis XIV?
- candidate_answer: `Kill Hannah`

Clean evidence:
- `Louis XIV (band)`: Louis XIV is an American rock band from San Diego, California. The band has released four EPs between 2003 and 2007, and three albums between 2003 and 2008, the latter two of which were distributed by Atlantic Records. The band broke up in 2009, but in 2013...
- `Kill Hannah`: Kill Hannah was an American rock band formed in 1993 in Chicago, Illinois. The band released six studio albums, seven EPs, and two compilation albums as well as three DVDs.

First perturbation evidence:
- query: Which of the following rock bands is from Chicago: Kill Hannah or Louis XIV? Please verify each supporting hop.
- `Louis XIV (band)`: Louis XIV is an American rock band from San Diego, California. The band has released four EPs between 2003 and 2007, and three albums between 2003 and 2008, the latter two of which were distributed by Atlantic Records. The band broke up in 2009, but in 2013...
- `Kill Hannah`: Kill Hannah was an American rock band formed in 1993 in Chicago, Illinois. The band released six studio albums, seven EPs, and two compilation albums as well as three DVDs.

#### hotpot_semanticswap:5adf8ade5542993344016ce8:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8659`
- baseline_score: `0.8749`
- target_minus_baseline: `-0.0089`
- query: Dutch-born American businessman, Harry Koch, fathered a son born in 1900 that founded which oil refinery firm?
- candidate_answer: `Koch Industries`

Clean evidence:
- `Fred C. Koch`: Fred Chase Koch ( ; September 23, 1900 – November 17, 1967) was an American chemical engineer and entrepreneur who founded the oil refinery firm that later became Koch Industries, a privately held company which, under the principal ownership and leadership ...
- `Harry Koch (businessman)`: Hotze "Harry" Koch ( ; 22 October 1867 – 21 June 1942) was a Dutch-born American businessman who founded the "Quanah Tribune-Chief" newspaper. He was the father of Fred C. Koch (1900–1967), founder of Koch Industries.

First perturbation evidence:
- query: Dutch-born American businessman, Harry Koch, fathered a son born in 1900 that founded which oil refinery firm? Please verify each supporting hop.
- `Fred C. Koch`: Fred Chase Koch ( ; September 23, 1900 – November 17, 1967) was an American chemical engineer and entrepreneur who founded the oil refinery firm that later became Koch Industries, a privately held company which, under the principal ownership and leadership ...
- `Harry Koch (businessman)`: Hotze "Harry" Koch ( ; 22 October 1867 – 21 June 1942) was a Dutch-born American businessman who founded the "Quanah Tribune-Chief" newspaper. He was the father of Fred C. Koch (1900–1967), founder of Koch Industries.

#### hotpot_semanticswap:5adf3e355542993a75d26440:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8708`
- baseline_score: `0.8812`
- target_minus_baseline: `-0.0104`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Please verify each supporting hop.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

#### hotpot_semanticswap:5a79c1095542996c55b2dc62:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8719`
- baseline_score: `0.8812`
- target_minus_baseline: `-0.0093`
- query: Who died first, Chester Erskine or Sam Taylor?
- candidate_answer: `Sam Taylor`

Clean evidence:
- `Sam Taylor (director)`: Sam Taylor (August 13, 1895, New York City – March 6, 1958, Santa Monica) was a film director, screenwriter, and producer, most active in the silent film era. Taylor is best known for his comedic directorial work with Harold Lloyd and Mary Pickford, and als...
- `Chester Erskine`: Chester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.

First perturbation evidence:
- query: Who died first, Chester Erskine or Sam Taylor? Please verify each supporting hop.
- `Sam Taylor (director)`: Sam Taylor (August 13, 1895, New York City – March 6, 1958, Santa Monica) was a film director, screenwriter, and producer, most active in the silent film era. Taylor is best known for his comedic directorial work with Harold Lloyd and Mary Pickford, and als...
- `Chester Erskine`: Chester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.

#### hotpot_semanticswap:5a8303c255429954d2e2ec01:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8898`
- baseline_score: `0.9004`
- target_minus_baseline: `-0.0106`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Please verify each supporting hop.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_semanticswap:5ac31602554299741d48a1bf:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8953`
- baseline_score: `0.9028`
- target_minus_baseline: `-0.0075`
- query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"?
- candidate_answer: `Jennifer Taylor`

Clean evidence:
- `Jennifer Taylor (actress)`: Jennifer Taylor (née Bini, and sometimes credited as Jennifer Bini Taylor; born April 19, 1972) is an American actress, best known for her role as Chelsea Melini on CBS sitcom "Two and a Half Men", and earlier, for three other female roles on the show. She ...
- `Zombie Night (2013 film)`: Zombie Night is a 2013 American zombie horror film directed by John Gulager, written by Keith Allan and Delondra Williams from a story by Richard Schenkman, and starring Anthony Michael Hall, Daryl Hannah, Jennifer Taylor, Alan Ruck, and Shirley Jones.

First perturbation evidence:
- query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"? Please verify each supporting hop.
- `Jennifer Taylor (actress)`: Jennifer Taylor (née Bini, and sometimes credited as Jennifer Bini Taylor; born April 19, 1972) is an American actress, best known for her role as Chelsea Melini on CBS sitcom "Two and a Half Men", and earlier, for three other female roles on the show. She ...
- `Zombie Night (2013 film)`: Zombie Night is a 2013 American zombie horror film directed by John Gulager, written by Keith Allan and Delondra Williams from a story by Richard Schenkman, and starring Anthony Michael Hall, Daryl Hannah, Jennifer Taylor, Alan Ruck, and Shirley Jones.


### Target over baseline on negatives

#### hotpot_semanticswap:5a8ba3ff55429971feec4744:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.4979`
- baseline_score: `0.4224`
- target_minus_baseline: `0.0756`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Verify the original answer using only the provided evidence.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the New Mexico Governor's Mansion. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

#### hotpot_semanticswap:5ac31602554299741d48a1bf:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8172`
- baseline_score: `0.8036`
- target_minus_baseline: `0.0136`
- query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"?
- candidate_answer: `Jennifer Taylor`

Clean evidence:
- `Jennifer Taylor (actress)`: Jennifer Taylor (née Bini, and sometimes credited as Jennifer Bini Taylor; born April 19, 1972) is an American actress, best known for her role as Chelsea Melini on CBS sitcom "Two and a Half Men", and earlier, for three other female roles on the show. She ...
- `Zombie Night (2013 film)`: Zombie Night is a 2013 American zombie horror film directed by John Gulager, written by Keith Allan and Delondra Williams from a story by Richard Schenkman, and starring Anthony Michael Hall, Daryl Hannah, Jennifer Taylor, Alan Ruck, and Shirley Jones.

First perturbation evidence:
- query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"? Verify the original answer using only the provided evidence.
- `Jennifer Taylor (actress)`: Wild Things 2 (née Bini, and sometimes credited as Jennifer Bini Taylor; born April 19, 1972) is an American actress, best known for her role as Chelsea Melini on CBS sitcom "Two and a Half Men", and earlier, for three other female roles on the show. She ap...
- `Zombie Night (2013 film)`: Zombie Night is a 2013 American zombie horror film directed by John Gulager, written by Keith Allan and Delondra Williams from a story by Richard Schenkman, and starring Anthony Michael Hall, Daryl Hannah, Wild Things 2, Alan Ruck, and Shirley Jones.

#### hotpot_semanticswap:5adcd2435542992c1e3a241b:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8131`
- baseline_score: `0.8006`
- target_minus_baseline: `0.0125`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Verify the original answer using only the provided evidence.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_semanticswap:5a80522b5542996402f6a4c1:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0183`
- baseline_score: `0.0105`
- target_minus_baseline: `0.0078`
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres?
- candidate_answer: `fifth-largest`

Clean evidence:
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

First perturbation evidence:
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres? Verify the original answer using only the provided evidence.
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

#### hotpot_semanticswap:5adf8ade5542993344016ce8:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0121`
- baseline_score: `0.0064`
- target_minus_baseline: `0.0057`
- query: Dutch-born American businessman, Harry Koch, fathered a son born in 1900 that founded which oil refinery firm?
- candidate_answer: `Koch Industries`

Clean evidence:
- `Fred C. Koch`: Fred Chase Koch ( ; September 23, 1900 – November 17, 1967) was an American chemical engineer and entrepreneur who founded the oil refinery firm that later became Koch Industries, a privately held company which, under the principal ownership and leadership ...
- `Harry Koch (businessman)`: Hotze "Harry" Koch ( ; 22 October 1867 – 21 June 1942) was a Dutch-born American businessman who founded the "Quanah Tribune-Chief" newspaper. He was the father of Fred C. Koch (1900–1967), founder of Koch Industries.

First perturbation evidence:
- query: Dutch-born American businessman, Harry Koch, fathered a son born in 1900 that founded which oil refinery firm? Verify the original answer using only the provided evidence.
- `Fred C. Koch`: Fred Chase Koch ( ; September 23, 1900 – November 17, 1967) was an American chemical engineer and entrepreneur who founded the oil refinery firm that later became Nghi Sơn Refinery, a privately held company which, under the principal ownership and leadershi...
- `Harry Koch (businessman)`: Hotze "Harry" Koch ( ; 22 October 1867 – 21 June 1942) was a Dutch-born American businessman who founded the "Quanah Tribune-Chief" newspaper. He was the father of Fred C. Koch (1900–1967), founder of Nghi Sơn Refinery.

#### hotpot_semanticswap:5a79c1095542996c55b2dc62:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0062`
- baseline_score: `0.0036`
- target_minus_baseline: `0.0026`
- query: Who died first, Chester Erskine or Sam Taylor?
- candidate_answer: `Sam Taylor`

Clean evidence:
- `Sam Taylor (director)`: Sam Taylor (August 13, 1895, New York City – March 6, 1958, Santa Monica) was a film director, screenwriter, and producer, most active in the silent film era. Taylor is best known for his comedic directorial work with Harold Lloyd and Mary Pickford, and als...
- `Chester Erskine`: Chester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.

First perturbation evidence:
- query: Who died first, Chester Erskine or Sam Taylor? Verify the original answer using only the provided evidence.
- `Sam Taylor (director)`: Lord Cardross (August 13, 1895, New York City – March 6, 1958, Santa Monica) was a film director, screenwriter, and producer, most active in the silent film era. Taylor is best known for his comedic directorial work with Harold Lloyd and Mary Pickford, and ...
- `Chester Erskine`: Chester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.

#### hotpot_semanticswap:5a764c0b55429976ec32bd89:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0019`
- baseline_score: `0.0012`
- target_minus_baseline: `0.0007`
- query: What criteria subjectively qualifies the Houston Astrodome to be called the Eighth Wonder of the World?
- candidate_answer: `comparable to the seven Wonders of the World`

Clean evidence:
- `Astrodome`: The NRG Astrodome, also known as the Houston Astrodome or simply The Astrodome, is the world's first multi-purpose, domed sports stadium, located in Houston, Texas. Construction on the stadium began in 1962, and it officially opened in 1965. It served as ho...
- `Eighth Wonder of the World`: Eighth Wonder of the World is an unofficial title sometimes given to new buildings, structures, projects, or even designs that are deemed to be comparable to the seven Wonders of the World.

First perturbation evidence:
- query: What criteria subjectively qualifies the Houston Astrodome to be called the Eighth Wonder of the World? Verify the original answer using only the provided evidence.
- `Astrodome`: The NRG Astrodome, also known as the Houston Astrodome or simply The Astrodome, is the world's first multi-purpose, domed sports stadium, located in Houston, Texas. Construction on the stadium began in 1962, and it officially opened in 1965. It served as ho...
- `Eighth Wonder of the World`: Eighth Wonder of the World is an unofficial title sometimes given to new buildings, structures, projects, or even designs that are deemed to be For the Last Time: Live from the Astrodome.

#### hotpot_semanticswap:5a881cbb55429938390d3ee7:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0014`
- baseline_score: `0.0009`
- target_minus_baseline: `0.0005`
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style?
- candidate_answer: `Hellenism`

Clean evidence:
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

First perturbation evidence:
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style? Verify the original answer using only the provided evidence.
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Greek Revival architecture, it may be looked upon as the last phase in the development of Neoclas...


### Baseline over target on positives

#### hotpot_semanticswap:5adf3e835542993a75d26442:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7704`
- baseline_score: `0.7914`
- target_minus_baseline: `-0.0210`
- query: Which comic series involves characters such as Nick Fury and Baron von Strucker?
- candidate_answer: `Marvel`

Clean evidence:
- `Nick Fury: Agent of S.H.I.E.L.D. (film)`: Nick Fury: Agent of S.H.I.E.L.D. is an American television film based on the Marvel Comics character Nick Fury. It was first broadcast on May 26, 1998 on Fox. Directed by Rod Hardy, the film stars David Hasselhoff as Fury, a retired super spy who is approac...
- `Fenris (comics)`: Andrea von Strucker and Andreas von Strucker are two fictional characters appearing in American comic books published by Marvel Comics. They are the German twin children of supervillain Baron von Strucker of HYDRA and the half-siblings of Werner von Strucker.

First perturbation evidence:
- query: Which comic series involves characters such as Nick Fury and Baron von Strucker? Please verify each supporting hop.
- `Nick Fury: Agent of S.H.I.E.L.D. (film)`: Nick Fury: Agent of S.H.I.E.L.D. is an American television film based on the Marvel Comics character Nick Fury. It was first broadcast on May 26, 1998 on Fox. Directed by Rod Hardy, the film stars David Hasselhoff as Fury, a retired super spy who is approac...
- `Fenris (comics)`: Andrea von Strucker and Andreas von Strucker are two fictional characters appearing in American comic books published by Marvel Comics. They are the German twin children of supervillain Baron von Strucker of HYDRA and the half-siblings of Werner von Strucker.

#### hotpot_semanticswap:5ae1fced5542997283cd230e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7845`
- baseline_score: `0.8012`
- target_minus_baseline: `-0.0167`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Please verify each supporting hop.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

#### hotpot_semanticswap:5a8f155e554299458435d54c:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9202`
- baseline_score: `0.9310`
- target_minus_baseline: `-0.0107`
- query: The Kellock-Taschereau Commission was appointed by a prime minister who served how long in office?
- candidate_answer: `21 years and 154 days`

Clean evidence:
- `Kellock–Taschereau Commission`: The Kellock–Taschereau Commission (officially the Royal Commission to Investigate the Facts Relating to and the Circumstances Surrounding the Communication, by Public Officials and Other Persons in Positions of Trust of Secret and Confidential Information t...
- `William Lyon Mackenzie King`: William Lyon Mackenzie King (December 17, 1874 – July 22, 1950), also commonly known as Mackenzie King, was the dominant Canadian political leader, as the Prime Minister of Canada, from the 1920s through the 1940s. He served as the tenth Prime Minister of C...

First perturbation evidence:
- query: The Kellock-Taschereau Commission was appointed by a prime minister who served how long in office? Please verify each supporting hop.
- `Kellock–Taschereau Commission`: The Kellock–Taschereau Commission (officially the Royal Commission to Investigate the Facts Relating to and the Circumstances Surrounding the Communication, by Public Officials and Other Persons in Positions of Trust of Secret and Confidential Information t...
- `William Lyon Mackenzie King`: William Lyon Mackenzie King (December 17, 1874 – July 22, 1950), also commonly known as Mackenzie King, was the dominant Canadian political leader, as the Prime Minister of Canada, from the 1920s through the 1940s. He served as the tenth Prime Minister of C...

#### hotpot_semanticswap:5a8303c255429954d2e2ec01:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8898`
- baseline_score: `0.9004`
- target_minus_baseline: `-0.0106`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Please verify each supporting hop.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_semanticswap:5adf3e355542993a75d26440:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8708`
- baseline_score: `0.8812`
- target_minus_baseline: `-0.0104`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Please verify each supporting hop.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

#### hotpot_semanticswap:5ac26ac15542992f1f2b38bc:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9211`
- baseline_score: `0.9311`
- target_minus_baseline: `-0.0099`
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to?
- candidate_answer: `Sam Phillips`

Clean evidence:
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

First perturbation evidence:
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to? Please verify each supporting hop.
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

#### hotpot_semanticswap:5a79c1095542996c55b2dc62:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8719`
- baseline_score: `0.8812`
- target_minus_baseline: `-0.0093`
- query: Who died first, Chester Erskine or Sam Taylor?
- candidate_answer: `Sam Taylor`

Clean evidence:
- `Sam Taylor (director)`: Sam Taylor (August 13, 1895, New York City – March 6, 1958, Santa Monica) was a film director, screenwriter, and producer, most active in the silent film era. Taylor is best known for his comedic directorial work with Harold Lloyd and Mary Pickford, and als...
- `Chester Erskine`: Chester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.

First perturbation evidence:
- query: Who died first, Chester Erskine or Sam Taylor? Please verify each supporting hop.
- `Sam Taylor (director)`: Sam Taylor (August 13, 1895, New York City – March 6, 1958, Santa Monica) was a film director, screenwriter, and producer, most active in the silent film era. Taylor is best known for his comedic directorial work with Harold Lloyd and Mary Pickford, and als...
- `Chester Erskine`: Chester Erskine (November 29, 1905 – April 7, 1986) was a Hollywood and Broadway director, writer, and producer.

#### hotpot_semanticswap:5ac458f8554299204fd21f2a:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9053`
- baseline_score: `0.9146`
- target_minus_baseline: `-0.0093`
- query: What is the relationship of Yeshahework Yilma's mother to the man who was Ethiopia's emperor from 1930 to 1974?
- candidate_answer: `niece`

Clean evidence:
- `Yeshashework Yilma`: Princess Yeshashework Yilma (died 1982) was the daughter of Dejazmatch Yilma Makonnen, governor of Harar and niece of Emperor Haile Selassie of Ethiopia. Her mother Woizero Aselefech Wolde Hanna was the niece of Empress Taitu Bitul, consort of Emperor Menel...
- `Haile Selassie`: Haile Selassie I (Ge'ez: , "qädamawi haylä səllasé" ; ] ; 23 July 1892 – 27 August 1975) , born Tafari Makonnen Woldemikael, was Ethiopia's regent from 1916 to 1930 and emperor from 1930 to 1974. He also served as Chairperson of the Organisation of African ...

First perturbation evidence:
- query: What is the relationship of Yeshahework Yilma's mother to the man who was Ethiopia's emperor from 1930 to 1974?  Please verify each supporting hop.
- `Yeshashework Yilma`: Princess Yeshashework Yilma (died 1982) was the daughter of Dejazmatch Yilma Makonnen, governor of Harar and niece of Emperor Haile Selassie of Ethiopia. Her mother Woizero Aselefech Wolde Hanna was the niece of Empress Taitu Bitul, consort of Emperor Menel...
- `Haile Selassie`: Haile Selassie I (Ge'ez: , "qädamawi haylä səllasé" ; ] ; 23 July 1892 – 27 August 1975) , born Tafari Makonnen Woldemikael, was Ethiopia's regent from 1916 to 1930 and emperor from 1930 to 1974. He also served as Chairperson of the Organisation of African ...
