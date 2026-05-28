# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 0.9725 | 0.0000 | 0.1000 | 0.8680 | 0.1961 |
| baseline_calibrated_logistic_orbit | 0.9725 | 0.0000 | 0.1000 | 0.8779 | 0.1827 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| semantic_swap | 20 | 0 | 20 | 0.1961 | 0.1827 | 0.0133 |
| stable | 20 | 20 | 0 | 0.8680 | 0.8779 | -0.0099 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| verifier_entropy | 0.4848 | 0.3847 | 0.1001 |
| clean_to_worst_gap | 0.0035 | 0.0994 | -0.0959 |
| min_sufficiency | 0.1887 | 0.0928 | 0.0959 |
| naive_orbit_average | 0.1905 | 0.1425 | 0.0480 |
| mean_sufficiency | 0.1905 | 0.1425 | 0.0480 |
| mean_missing | 0.7558 | 0.7815 | -0.0257 |
| sufficiency_variance | 0.0000 | 0.0032 | -0.0032 |
| max_conflict | 0.0799 | 0.0801 | -0.0002 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |
| corm_mean_clean | 0.5000 | 0.5000 | 0.0000 |
| context_sufficiency_clean | 0.1922 | 0.1922 | 0.0000 |
| clean_sufficiency | 0.1922 | 0.1922 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### hotpot_semanticswap:5a8303c255429954d2e2ec01:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8705`
- baseline_score: `0.8803`
- target_minus_baseline: `-0.0098`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Verify the original answer using only the provided evidence.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_semanticswap:5adf3e355542993a75d26440:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.8410`
- baseline_score: `0.8526`
- target_minus_baseline: `-0.0116`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Verify the original answer using only the provided evidence.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly Sweden from ...

#### hotpot_semanticswap:5adcd2435542992c1e3a241b:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.7881`
- baseline_score: `0.7601`
- target_minus_baseline: `0.0280`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Verify the original answer using only the provided evidence.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_semanticswap:5add60905542995b365fab1d:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.7445`
- baseline_score: `0.7183`
- target_minus_baseline: `0.0262`
- query: What do Victor Salva and Emilio Fernández have in common?
- candidate_answer: `director and screenwriter.`

Clean evidence:
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film director and screenwriter. He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

First perturbation evidence:
- query: What do Victor Salva and Emilio Fernández have in common? Verify the original answer using only the provided evidence.
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film Fernando Fernández (actor) He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

#### hotpot_semanticswap:5a8ba3ff55429971feec4744:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.4788`
- baseline_score: `0.3613`
- target_minus_baseline: `0.1175`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Verify the original answer using only the provided evidence.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the New Mexico Governor's Mansion. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

#### hotpot_semanticswap:5add67915542992200553af8:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0926`
- baseline_score: `0.0406`
- target_minus_baseline: `0.0521`
- query: What was the nickname of the hitman hired by an Italian American Criminal Organization?
- candidate_answer: `The Crowned Prince of the Philadelphia Mob`

Clean evidence:
- `Salvatore Testa`: Salvatore "Salvie" Testa (March 31, 1956 - September 14, 1984), nicknamed The Crowned Prince of the Philadelphia Mob, was a Philadelphia gangster who served as a hitman for the Philadelphia crime family during a period of internal gang conflict. The son of ...
- `Philadelphia crime family`: The Philadelphia crime family, (pronounced ] ) also known as the Philadelphia Mafia, the Philly Mob/Mafia, the Bruno-Scarfo family, the South Philly Mob/Mafia, or the Philadelphia-South Jersey Mob/Mafia is an Italian American criminal organization based in ...

First perturbation evidence:
- query: What was the nickname of the hitman hired by an Italian American Criminal Organization? Verify the original answer using only the provided evidence.
- `Salvatore Testa`: Salvatore "Salvie" Testa (March 31, 1956 - September 14, 1984), nicknamed National Italian American Sports Hall of Fame, was a Philadelphia gangster who served as a hitman for the Philadelphia crime family during a period of internal gang conflict. The son ...
- `Philadelphia crime family`: The Philadelphia crime family, (pronounced ] ) also known as the Philadelphia Mafia, the Philly Mob/Mafia, the Bruno-Scarfo family, the South Philly Mob/Mafia, or the Philadelphia-South Jersey Mob/Mafia is an Italian American criminal organization based in ...

#### hotpot_semanticswap:5adce88b5542992c1e3a249a:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0681`
- baseline_score: `0.0284`
- target_minus_baseline: `0.0396`
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- candidate_answer: `320 years`

Clean evidence:
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

First perturbation evidence:
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ? Verify the original answer using only the provided evidence.
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for Halebidu (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynast...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

#### hotpot_semanticswap:5ac0e0c75542997d64295a6e:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0109`
- baseline_score: `0.0037`
- target_minus_baseline: `0.0072`
- query: Reggaetón Lento is a song by the boy band formed on which date?
- candidate_answer: `December 13, 2015`

Clean evidence:
- `CNCO`: CNCO is a Latin American boy band formed on December 13, 2015, composed of Christopher Vélez, Richard Camacho, Joel Pimentel, Erick Brian Colón and Zabdiel de Jesús"." They won a 5-year recording contract with Sony Music Latin after becoming the winning com...
- `Reggaetón Lento (Bailemos)`: "Reggaetón Lento (Bailemos)" is a song by Latin American boy band CNCO. It was released on 7 October 2016 as the third single from their debut studio album, "Primera Cita" (2016). The song was written by Eric Perez, Jadan Andino, Jorge Class and Luis Angel ...

First perturbation evidence:
- query: Reggaetón Lento is a song by the boy band formed on which date? Verify the original answer using only the provided evidence.
- `CNCO`: CNCO is a Latin American boy band formed on CNCO discography, composed of Christopher Vélez, Richard Camacho, Joel Pimentel, Erick Brian Colón and Zabdiel de Jesús"." They won a 5-year recording contract with Sony Music Latin after becoming the winning comp...
- `Reggaetón Lento (Bailemos)`: "Reggaetón Lento (Bailemos)" is a song by Latin American boy band CNCO. It was released on 7 October 2016 as the third single from their debut studio album, "Primera Cita" (2016). The song was written by Eric Perez, Jadan Andino, Jorge Class and Luis Angel ...


### Low-scoring false negatives

#### hotpot_semanticswap:5a79332555429907847277e7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7894`
- baseline_score: `0.8045`
- target_minus_baseline: `-0.0151`
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- candidate_answer: `Juan Carlos Onetti`

Clean evidence:
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

First perturbation evidence:
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti? Please verify each supporting hop.
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

#### hotpot_semanticswap:5ae1fced5542997283cd230e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8156`
- baseline_score: `0.8340`
- target_minus_baseline: `-0.0184`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Please verify each supporting hop.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

#### hotpot_semanticswap:5ae6363b55429929b0807af0:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8320`
- baseline_score: `0.8368`
- target_minus_baseline: `-0.0048`
- query: When was the defending titlist of 2009–10 Biathlon World Cup – Pursuit Men born?
- candidate_answer: `27 January 1974`

Clean evidence:
- `Ole Einar Bjørndalen`: Ole Einar Bjørndalen (born 27 January 1974) is a Norwegian professional biathlete, often referred to by the nickname "The King of Biathlon". He is the most medaled Olympian in the history of the Winter Olympic Games, with 13 medals. He is also the most succ...
- `2009–10 Biathlon World Cup – Pursuit Men`: The 2009–10 Biathlon World Cup – Pursuit Men started on December 13, 2009 in Hochfilzen and finished on March 20, 2010 in Oslo. Defending titlist is Ole Einar Bjørndalen of Norway.

First perturbation evidence:
- query: When was the defending titlist of 2009–10 Biathlon World Cup – Pursuit Men born?  Please verify each supporting hop.
- `Ole Einar Bjørndalen`: Ole Einar Bjørndalen (born 27 January 1974) is a Norwegian professional biathlete, often referred to by the nickname "The King of Biathlon". He is the most medaled Olympian in the history of the Winter Olympic Games, with 13 medals. He is also the most succ...
- `2009–10 Biathlon World Cup – Pursuit Men`: The 2009–10 Biathlon World Cup – Pursuit Men started on December 13, 2009 in Hochfilzen and finished on March 20, 2010 in Oslo. Defending titlist is Ole Einar Bjørndalen of Norway.

#### hotpot_semanticswap:5add60905542995b365fab1d:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8414`
- baseline_score: `0.8535`
- target_minus_baseline: `-0.0121`
- query: What do Victor Salva and Emilio Fernández have in common?
- candidate_answer: `director and screenwriter.`

Clean evidence:
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film director and screenwriter. He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

First perturbation evidence:
- query: What do Victor Salva and Emilio Fernández have in common? Please verify each supporting hop.
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film director and screenwriter. He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

#### hotpot_semanticswap:5adf3e355542993a75d26440:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8459`
- baseline_score: `0.8588`
- target_minus_baseline: `-0.0129`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Please verify each supporting hop.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

#### hotpot_semanticswap:5ac403c45542997ea680c9b5:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8676`
- baseline_score: `0.8753`
- target_minus_baseline: `-0.0077`
- query: Where does Tiko's Spanish football club hold home games at?
- candidate_answer: `Estadio de López Cortázar`

Clean evidence:
- `Tiko (footballer)`: Roberto Martínez Rípodas (born 15 September 1976), known as Tiko, is a Spanish retired footballer who played as a central or a defensive midfielder, and the current assistant manager of CD Basconia.
- `CD Basconia`: Club Deportivo Basconia is a Spanish football club based in Basauri, Biscay, in the autonomous community of Basque Country. Founded in 1913 it currently plays in Tercera División – Group 4, holding home games at "Estadio de López Cortázar", with an 8,500-se...

First perturbation evidence:
- query: Where does Tiko's Spanish football club hold home games at? Please verify each supporting hop.
- `Tiko (footballer)`: Roberto Martínez Rípodas (born 15 September 1976), known as Tiko, is a Spanish retired footballer who played as a central or a defensive midfielder, and the current assistant manager of CD Basconia.
- `CD Basconia`: Club Deportivo Basconia is a Spanish football club based in Basauri, Biscay, in the autonomous community of Basque Country. Founded in 1913 it currently plays in Tercera División – Group 4, holding home games at "Estadio de López Cortázar", with an 8,500-se...

#### hotpot_semanticswap:5a899bf955429946c8d6e959:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8686`
- baseline_score: `0.8798`
- target_minus_baseline: `-0.0112`
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted?
- candidate_answer: `2012`

Clean evidence:
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

First perturbation evidence:
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted? Please verify each supporting hop.
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

#### hotpot_semanticswap:5a8ba3ff55429971feec4744:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8686`
- baseline_score: `0.8791`
- target_minus_baseline: `-0.0104`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Please verify each supporting hop.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...


### Target over baseline on negatives

#### hotpot_semanticswap:5a8ba3ff55429971feec4744:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.4788`
- baseline_score: `0.3613`
- target_minus_baseline: `0.1175`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Verify the original answer using only the provided evidence.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the New Mexico Governor's Mansion. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

#### hotpot_semanticswap:5add67915542992200553af8:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0926`
- baseline_score: `0.0406`
- target_minus_baseline: `0.0521`
- query: What was the nickname of the hitman hired by an Italian American Criminal Organization?
- candidate_answer: `The Crowned Prince of the Philadelphia Mob`

Clean evidence:
- `Salvatore Testa`: Salvatore "Salvie" Testa (March 31, 1956 - September 14, 1984), nicknamed The Crowned Prince of the Philadelphia Mob, was a Philadelphia gangster who served as a hitman for the Philadelphia crime family during a period of internal gang conflict. The son of ...
- `Philadelphia crime family`: The Philadelphia crime family, (pronounced ] ) also known as the Philadelphia Mafia, the Philly Mob/Mafia, the Bruno-Scarfo family, the South Philly Mob/Mafia, or the Philadelphia-South Jersey Mob/Mafia is an Italian American criminal organization based in ...

First perturbation evidence:
- query: What was the nickname of the hitman hired by an Italian American Criminal Organization? Verify the original answer using only the provided evidence.
- `Salvatore Testa`: Salvatore "Salvie" Testa (March 31, 1956 - September 14, 1984), nicknamed National Italian American Sports Hall of Fame, was a Philadelphia gangster who served as a hitman for the Philadelphia crime family during a period of internal gang conflict. The son ...
- `Philadelphia crime family`: The Philadelphia crime family, (pronounced ] ) also known as the Philadelphia Mafia, the Philly Mob/Mafia, the Bruno-Scarfo family, the South Philly Mob/Mafia, or the Philadelphia-South Jersey Mob/Mafia is an Italian American criminal organization based in ...

#### hotpot_semanticswap:5adce88b5542992c1e3a249a:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0681`
- baseline_score: `0.0284`
- target_minus_baseline: `0.0396`
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- candidate_answer: `320 years`

Clean evidence:
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

First perturbation evidence:
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ? Verify the original answer using only the provided evidence.
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for Halebidu (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynast...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

#### hotpot_semanticswap:5adcd2435542992c1e3a241b:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.7881`
- baseline_score: `0.7601`
- target_minus_baseline: `0.0280`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Verify the original answer using only the provided evidence.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_semanticswap:5add60905542995b365fab1d:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.7445`
- baseline_score: `0.7183`
- target_minus_baseline: `0.0262`
- query: What do Victor Salva and Emilio Fernández have in common?
- candidate_answer: `director and screenwriter.`

Clean evidence:
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film director and screenwriter. He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

First perturbation evidence:
- query: What do Victor Salva and Emilio Fernández have in common? Verify the original answer using only the provided evidence.
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film Fernando Fernández (actor) He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

#### hotpot_semanticswap:5ac0e0c75542997d64295a6e:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0109`
- baseline_score: `0.0037`
- target_minus_baseline: `0.0072`
- query: Reggaetón Lento is a song by the boy band formed on which date?
- candidate_answer: `December 13, 2015`

Clean evidence:
- `CNCO`: CNCO is a Latin American boy band formed on December 13, 2015, composed of Christopher Vélez, Richard Camacho, Joel Pimentel, Erick Brian Colón and Zabdiel de Jesús"." They won a 5-year recording contract with Sony Music Latin after becoming the winning com...
- `Reggaetón Lento (Bailemos)`: "Reggaetón Lento (Bailemos)" is a song by Latin American boy band CNCO. It was released on 7 October 2016 as the third single from their debut studio album, "Primera Cita" (2016). The song was written by Eric Perez, Jadan Andino, Jorge Class and Luis Angel ...

First perturbation evidence:
- query: Reggaetón Lento is a song by the boy band formed on which date? Verify the original answer using only the provided evidence.
- `CNCO`: CNCO is a Latin American boy band formed on CNCO discography, composed of Christopher Vélez, Richard Camacho, Joel Pimentel, Erick Brian Colón and Zabdiel de Jesús"." They won a 5-year recording contract with Sony Music Latin after becoming the winning comp...
- `Reggaetón Lento (Bailemos)`: "Reggaetón Lento (Bailemos)" is a song by Latin American boy band CNCO. It was released on 7 October 2016 as the third single from their debut studio album, "Primera Cita" (2016). The song was written by Eric Perez, Jadan Andino, Jorge Class and Luis Angel ...

#### hotpot_semanticswap:5ae6363b55429929b0807af0:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0084`
- baseline_score: `0.0028`
- target_minus_baseline: `0.0056`
- query: When was the defending titlist of 2009–10 Biathlon World Cup – Pursuit Men born?
- candidate_answer: `27 January 1974`

Clean evidence:
- `Ole Einar Bjørndalen`: Ole Einar Bjørndalen (born 27 January 1974) is a Norwegian professional biathlete, often referred to by the nickname "The King of Biathlon". He is the most medaled Olympian in the history of the Winter Olympic Games, with 13 medals. He is also the most succ...
- `2009–10 Biathlon World Cup – Pursuit Men`: The 2009–10 Biathlon World Cup – Pursuit Men started on December 13, 2009 in Hochfilzen and finished on March 20, 2010 in Oslo. Defending titlist is Ole Einar Bjørndalen of Norway.

First perturbation evidence:
- query: When was the defending titlist of 2009–10 Biathlon World Cup – Pursuit Men born?  Verify the original answer using only the provided evidence.
- `Ole Einar Bjørndalen`: Ole Einar Bjørndalen (born Ole Einar Bjørndalen) is a Norwegian professional biathlete, often referred to by the nickname "The King of Biathlon". He is the most medaled Olympian in the history of the Winter Olympic Games, with 13 medals. He is also the most...
- `2009–10 Biathlon World Cup – Pursuit Men`: The 2009–10 Biathlon World Cup – Pursuit Men started on December 13, 2009 in Hochfilzen and finished on March 20, 2010 in Oslo. Defending titlist is Ole Einar Bjørndalen of Norway.

#### hotpot_semanticswap:5a79332555429907847277e7:semantic_swap

- label_answerable: `False`
- construction_type: `semantic_swap`
- target_score: `0.0065`
- baseline_score: `0.0023`
- target_minus_baseline: `0.0043`
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- candidate_answer: `Juan Carlos Onetti`

Clean evidence:
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

First perturbation evidence:
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti? Verify the original answer using only the provided evidence.
- `Juan Carlos Onetti`: Felipe VI of Spain Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".


### Baseline over target on positives

#### hotpot_semanticswap:5ae1fced5542997283cd230e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8156`
- baseline_score: `0.8340`
- target_minus_baseline: `-0.0184`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Please verify each supporting hop.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

#### hotpot_semanticswap:5a79332555429907847277e7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7894`
- baseline_score: `0.8045`
- target_minus_baseline: `-0.0151`
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- candidate_answer: `Juan Carlos Onetti`

Clean evidence:
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

First perturbation evidence:
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti? Please verify each supporting hop.
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

#### hotpot_semanticswap:5adf3e355542993a75d26440:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8459`
- baseline_score: `0.8588`
- target_minus_baseline: `-0.0129`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Please verify each supporting hop.
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

#### hotpot_semanticswap:5add60905542995b365fab1d:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8414`
- baseline_score: `0.8535`
- target_minus_baseline: `-0.0121`
- query: What do Victor Salva and Emilio Fernández have in common?
- candidate_answer: `director and screenwriter.`

Clean evidence:
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film director and screenwriter. He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

First perturbation evidence:
- query: What do Victor Salva and Emilio Fernández have in common? Please verify each supporting hop.
- `Victor Salva`: Victor Ronald Salva (born March 29, 1958) is an American film director and screenwriter. He directed the films "Powder" (1995) and "Jeepers Creepers" (2001). The latter of these has been expanded into a franchise with two sequels that he has also directed.
- `Emilio Fernández`: Emilio "El Indio" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter. He was one of the most prolific film directors of the Golden Age of Mexican cinema in the 1940s and 1950s. He ...

#### hotpot_semanticswap:5a899bf955429946c8d6e959:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8686`
- baseline_score: `0.8798`
- target_minus_baseline: `-0.0112`
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted?
- candidate_answer: `2012`

Clean evidence:
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

First perturbation evidence:
- query: When was the New Orleans Pelicans player featured on the NBA 2K16 cover first drafted? Please verify each supporting hop.
- `Anthony Davis (basketball)`: Anthony Marshon Davis Jr. (born March 11, 1993) is an American professional basketball player for the New Orleans Pelicans of the National Basketball Association (NBA). He plays the power forward and center positions. Davis was selected first overall in the...
- `NBA 2K16`: NBA 2K16 is a basketball simulation video game developed by Visual Concepts and published by 2K Sports. It is the 17th installment in the "NBA 2K" franchise and the successor to "NBA 2K15". It was released on September 29, 2015 for Microsoft Windows, Xbox O...

#### hotpot_semanticswap:5a8303c255429954d2e2ec01:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8731`
- baseline_score: `0.8836`
- target_minus_baseline: `-0.0105`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Please verify each supporting hop.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_semanticswap:5a8ba3ff55429971feec4744:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8686`
- baseline_score: `0.8791`
- target_minus_baseline: `-0.0104`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Please verify each supporting hop.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

#### hotpot_semanticswap:5adcd2435542992c1e3a241b:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8854`
- baseline_score: `0.8953`
- target_minus_baseline: `-0.0098`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Please verify each supporting hop.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...
