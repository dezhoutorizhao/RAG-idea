# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 1.0000 | 0.0000 | 0.0000 | 0.9555 | 0.0469 |
| baseline_calibrated_logistic_orbit | 1.0000 | 0.0000 | 0.0000 | 0.9559 | 0.0464 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| hard_missing_hop | 20 | 0 | 20 | 0.0469 | 0.0464 | 0.0005 |
| stable | 20 | 20 | 0 | 0.9555 | 0.9559 | -0.0004 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| retrieval_overlap | 1.0000 | 0.6226 | 0.3774 |
| max_conflict | 0.0361 | 0.0800 | -0.0439 |
| min_sufficiency | 0.2075 | 0.1974 | 0.0101 |
| clean_to_worst_gap | 0.0049 | 0.0150 | -0.0101 |
| mean_missing | 0.7334 | 0.7420 | -0.0086 |
| verifier_entropy | 0.5109 | 0.5053 | 0.0055 |
| naive_orbit_average | 0.2100 | 0.2059 | 0.0041 |
| mean_sufficiency | 0.2100 | 0.2059 | 0.0041 |
| sufficiency_variance | 0.0000 | 0.0001 | -0.0001 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |
| corm_mean_clean | 0.5000 | 0.5000 | 0.0000 |
| context_sufficiency_clean | 0.2125 | 0.2125 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### hotpot_hardneg:5adce88b5542992c1e3a249a:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.1345`
- baseline_score: `0.1473`
- target_minus_baseline: `-0.0128`
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- candidate_answer: `320 years`

Clean evidence:
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

First perturbation evidence:
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ? Use the retrieved evidence only; one reasoning hop may be absent.
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Founding of modern Singapore`: A significant port and settlement, known as Temasek, later renamed Singapura, existed on the island of Singapore in the 14th century. Vietnamese records indicate possible diplomatic relationship between Temasek and Vietnam in the 13th century, and Chinese d...

#### hotpot_hardneg:5a881cbb55429938390d3ee7:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.1327`
- baseline_score: `0.1557`
- target_minus_baseline: `-0.0230`
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style?
- candidate_answer: `Hellenism`

Clean evidence:
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

First perturbation evidence:
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style? Use the retrieved evidence only; one reasoning hop may be absent.
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...
- `St. Augustine's Episcopal Church Complex`: St. Augustine's Episcopal Church Complex is a historic Episcopal church complex at 6 Old Post Road north of Croton-on-Hudson, Westchester County, New York. The complex consists of the church and rectory The church consists of the original building and a lat...

#### hotpot_hardneg:5ae5dae2554299546bf82fa4:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.1206`
- baseline_score: `0.1157`
- target_minus_baseline: `0.0049`
- query: Faruk Halibegovic was born in what city that is the capital and largest city of Bosnia and Herzegovina with a population of 275,524?
- candidate_answer: `Sarajevo`

Clean evidence:
- `Faruk Halilbegović`: Faruk Halilbegović (born 7 September 1987 in Sarajevo, Bosnia and Herzegovina) is a handball left back who plays for Polish club Zagłębie Lubin. He started his career in Bosna Visoko and later played for Borac Banja Luka, Bosna Sarajevo and Sloga Doboj. Wit...
- `Sarajevo`: Sarajevo (Cyrillic: Сарајево , ] , ) is the capital and largest city of Bosnia and Herzegovina, with a population of 275,524 in its current administrative limits. The Sarajevo metropolitan area, including Sarajevo Canton and East Sarajevo is home to 643,016...

First perturbation evidence:
- query: Faruk Halibegovic was born in what city that is the capital and largest city of Bosnia and Herzegovina with a population of 275,524? Use the retrieved evidence only; one reasoning hop may be absent.
- `Sarajevo`: Sarajevo (Cyrillic: Сарајево , ] , ) is the capital and largest city of Bosnia and Herzegovina, with a population of 275,524 in its current administrative limits. The Sarajevo metropolitan area, including Sarajevo Canton and East Sarajevo is home to 643,016...
- `Tuzla`: Tuzla is a city in Bosnia and Herzegovina. It is the seat of the Tuzla Canton and is the economic, scientific, cultural, educational, health and tourist centre of northeast Bosnia. After Sarajevo and Banja Luka, Tuzla is the third largest city in Bosnia and...

#### hotpot_hardneg:5adf3e355542993a75d26440:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.1085`
- baseline_score: `0.1071`
- target_minus_baseline: `0.0014`
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden?
- candidate_answer: `8 km`

Clean evidence:
- `Øresund Region`: The Øresund or Öresund Region (Danish: "Øresundsregionen" ; Swedish: "Öresundsregionen" ] ) is a transnational metropolitan area in northern Europe, centred around the Øresund strait and the two cities which lie on either side, Copenhagen, Denmark and Malmö...
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...

First perturbation evidence:
- query: How long is the bridge in the Öresund Region that connect Copenhagen, Denmark and Malmo, Sweden? Use the retrieved evidence only; one reasoning hop may be absent.
- `Øresund Bridge`: The Øresund/Öresund/Oresund Bridge (Danish: "Øresundsbroen" , ] ; Swedish: "Öresundsbron" , ] ; hybrid name: "Øresundsbron ") is a combined railway and motorway bridge across the Øresund strait between Sweden and Denmark. The bridge runs nearly 8 km from th...
- `Øresund`: Øresund or Öresund (Danish: "Øresund" , ] ; Swedish: "Öresund" , ] ), commonly known in English as the Sound, is a strait which forms the Danish–Swedish border, separating Sjælland (Denmark) from Skåne (Sweden). The strait has a length of 118 km and the wid...

#### hotpot_hardneg:5ae55b8255429908b63265ef:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0875`
- baseline_score: `0.0831`
- target_minus_baseline: `0.0045`
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada?
- candidate_answer: `Masayoshi "Masa" Takayama`

Clean evidence:
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...

First perturbation evidence:
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada? Use the retrieved evidence only; one reasoning hop may be absent.
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...
- `Dinner Rush`: Dinner Rush is a 2000 American independent feature film, written by Brian S. Kalata and Rick Shaughnessy, and directed by Bob Giraldi. It stars Danny Aiello as a restaurateur-bookmaker in New York City's Tribeca neighborhood and Edoardo Ballerini as his son...

#### hotpot_hardneg:5ab90fdd55429916710eb0fc:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0816`
- baseline_score: `0.0783`
- target_minus_baseline: `0.0034`
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from?
- candidate_answer: `London, England`

Clean evidence:
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

First perturbation evidence:
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from? Use the retrieved evidence only; one reasoning hop may be absent.
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Harry Payne Whitney`: Harry Payne Whitney (April 29, 1872 – October 26, 1930) was an American businessman, thoroughbred horse breeder, and member of the prominent Whitney family.

#### hotpot_hardneg:5abd8c295542992ac4f382ab:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0664`
- baseline_score: `0.0607`
- target_minus_baseline: `0.0057`
- query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year?
- candidate_answer: `1874`

Clean evidence:
- `Minnesota State High School Mathematics League`: The Minnesota State High School Mathematics League is the premier high school mathematics league in the state of Minnesota. It was founded in 1980 by Macalester College professor Wayne Roberts. The league holds five statewide tournaments per year from Novem...
- `Macalester College`: Macalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US. It was founded in 1874 as a Presbyterian-affiliated but nonsectarian college. Its first class entered September 15, 1885. Macalester is exclusively...

First perturbation evidence:
- query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year?  Use the retrieved evidence only; one reasoning hop may be absent.
- `Macalester College`: Macalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US. It was founded in 1874 as a Presbyterian-affiliated but nonsectarian college. Its first class entered September 15, 1885. Macalester is exclusively...
- `Oberlin College`: Oberlin College is a private liberal arts college in Oberlin, Ohio. The college was founded as the Oberlin Collegiate Institute in 1833 by John Jay Shipherd and Philo Stewart. It is the oldest coeducational liberal arts college in the United States and the ...

#### hotpot_hardneg:5a792ad055429907847277d1:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0576`
- baseline_score: `0.0518`
- target_minus_baseline: `0.0057`
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?
- candidate_answer: `Mickey's PhilharMagic`

Clean evidence:
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

First perturbation evidence:
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?  Use the retrieved evidence only; one reasoning hop may be absent.
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Guardians of the Galaxy (Epcot Attraction)`: Guardians of the Galaxy is an upcoming attraction to be built at Epcot within the Walt Disney World Resort. It will be the third attraction based on a Marvel Comics property at Walt Disney Parks and Resorts after the Iron Man Experience at Hong Kong Disneyl...


### Low-scoring false negatives

#### hotpot_hardneg:5abd1b6e55429933744ab729:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.8964`
- baseline_score: `0.8797`
- target_minus_baseline: `0.0166`
- query: Which of the following cities is a county-level city, Jingzhou or Zixing?
- candidate_answer: `Zixing`

Clean evidence:
- `Jingzhou`: Jingzhou () is a prefecture-level city in southern Hubei, China, located on the banks of the Yangtze River. As of the 2010 census, its total population was 5,691,707, 1,154,086 of whom resided in the built-up ("or metro") area comprising the two urban distr...
- `Zixing`: Zixing () is a county-level city in Hunan Province, China, it is under the administration of Chenzhou prefecture-level City.

First perturbation evidence:
- query: Which of the following cities is a county-level city, Jingzhou or Zixing? Please verify each supporting hop.
- `Jingzhou`: Jingzhou () is a prefecture-level city in southern Hubei, China, located on the banks of the Yangtze River. As of the 2010 census, its total population was 5,691,707, 1,154,086 of whom resided in the built-up ("or metro") area comprising the two urban distr...
- `Zixing`: Zixing () is a county-level city in Hunan Province, China, it is under the administration of Chenzhou prefecture-level City.

#### hotpot_hardneg:5a79332555429907847277e7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9440`
- baseline_score: `0.9365`
- target_minus_baseline: `0.0075`
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- candidate_answer: `Juan Carlos Onetti`

Clean evidence:
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

First perturbation evidence:
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti? Please verify each supporting hop.
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

#### hotpot_hardneg:5a80522b5542996402f6a4c1:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9524`
- baseline_score: `0.9541`
- target_minus_baseline: `-0.0018`
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres?
- candidate_answer: `fifth-largest`

Clean evidence:
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

First perturbation evidence:
- query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres? Please verify each supporting hop.
- `Lawton, Oklahoma`: The city of Lawton is the county seat of Comanche County, in the State of Oklahoma. Located in southwestern Oklahoma, about 87 mi southwest of Oklahoma City, it is the principal city of the Lawton, Oklahoma Metropolitan Statistical Area. According to the 20...
- `Charon Gardens Wilderness Area`: The Charon's Garden Wilderness Area is part of the Wichita Mountains Wildlife Refuge in southwestern Oklahoma and is managed by the US Fish & Wildlife Service. It is located to the west of Medicine Park, Oklahoma and north of Lawton, Oklahoma. The wildernes...

#### hotpot_hardneg:5ac26ac15542992f1f2b38bc:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9529`
- baseline_score: `0.9576`
- target_minus_baseline: `-0.0047`
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to?
- candidate_answer: `Sam Phillips`

Clean evidence:
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

First perturbation evidence:
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to? Please verify each supporting hop.
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

#### hotpot_hardneg:5ac213805542992f1f2b37e7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9532`
- baseline_score: `0.9582`
- target_minus_baseline: `-0.0050`
- query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"?
- candidate_answer: `November`

Clean evidence:
- `Kenn Scott`: Kenn Scott is a Toronto-based screenwriter noted for his work in children's programming and animation. Included amongst the many shows he has written for are "Ned's Newt", "Iggy Arbuckle", "Captain Flamingo", "Rescue Heroes", "Seven Little Monsters", "Pelsw...
- `Pelswick`: Pelswick is an animated television series co-produced by Nelvana Limited and Suzhou Hong Ying Animation Corporation Limited in association with The Canadian Broadcasting Corporation and Nickelodeon. The series is about a teenage boy who uses a wheelchair, e...

First perturbation evidence:
- query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"? Please verify each supporting hop.
- `Kenn Scott`: Kenn Scott is a Toronto-based screenwriter noted for his work in children's programming and animation. Included amongst the many shows he has written for are "Ned's Newt", "Iggy Arbuckle", "Captain Flamingo", "Rescue Heroes", "Seven Little Monsters", "Pelsw...
- `Pelswick`: Pelswick is an animated television series co-produced by Nelvana Limited and Suzhou Hong Ying Animation Corporation Limited in association with The Canadian Broadcasting Corporation and Nickelodeon. The series is about a teenage boy who uses a wheelchair, e...

#### hotpot_hardneg:5ae55b8255429908b63265ef:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9535`
- baseline_score: `0.9513`
- target_minus_baseline: `0.0022`
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada?
- candidate_answer: `Masayoshi "Masa" Takayama`

Clean evidence:
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...

First perturbation evidence:
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada? Please verify each supporting hop.
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...

#### hotpot_hardneg:5ab90fdd55429916710eb0fc:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9542`
- baseline_score: `0.9545`
- target_minus_baseline: `-0.0003`
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from?
- candidate_answer: `London, England`

Clean evidence:
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

First perturbation evidence:
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from? Please verify each supporting hop.
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

#### hotpot_hardneg:5ae25d2b554299495565da46:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9556`
- baseline_score: `0.9567`
- target_minus_baseline: `-0.0011`
- query: Who has more singles titles, Brian Gottfried or Peter Fleming?
- candidate_answer: `21`

Clean evidence:
- `Peter Fleming (tennis)`: Peter Blair Fleming (born January 21, 1955 in Chatham Borough, New Jersey) is a former professional tennis player from the United States. In his doubles partnership with John McEnroe, he won 52 titles, of which seven were at Grand Slams (four at Wimbledon, ...
- `Brian Gottfried`: Brian Edward Gottfried (born January 27, 1952) is a retired tennis player from the United States who won 25 singles titles and 54 doubles titles during his professional career. The right-hander was the runner-up at the 1977 French Open and achieved a career...

First perturbation evidence:
- query: Who has more singles titles, Brian Gottfried or Peter Fleming? Please verify each supporting hop.
- `Peter Fleming (tennis)`: Peter Blair Fleming (born January 21, 1955 in Chatham Borough, New Jersey) is a former professional tennis player from the United States. In his doubles partnership with John McEnroe, he won 52 titles, of which seven were at Grand Slams (four at Wimbledon, ...
- `Brian Gottfried`: Brian Edward Gottfried (born January 27, 1952) is a retired tennis player from the United States who won 25 singles titles and 54 doubles titles during his professional career. The right-hander was the runner-up at the 1977 French Open and achieved a career...


### Target over baseline on negatives

#### hotpot_hardneg:5a79332555429907847277e7:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0571`
- baseline_score: `0.0507`
- target_minus_baseline: `0.0064`
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- candidate_answer: `Juan Carlos Onetti`

Clean evidence:
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Bryce Courtenay`: Bryce Courtenay, AM (14 August 193322 November 2012) was a South African/Australian advertising director and novelist. He is one of Australia's best-selling authors, notable for his book "The Power of One".

First perturbation evidence:
- query: Who died first, Bryce Courtenay or Juan Carlos Onetti? Use the retrieved evidence only; one reasoning hop may be absent.
- `Juan Carlos Onetti`: Juan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.
- `Concurso Literario Juan Carlos Onetti`: The Juan Carlos Onetti Literary Contest (Spanish: Concurso Literario Juan Carlos Onetti ) is an important literary award in Uruguay.

#### hotpot_hardneg:5abd8c295542992ac4f382ab:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0664`
- baseline_score: `0.0607`
- target_minus_baseline: `0.0057`
- query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year?
- candidate_answer: `1874`

Clean evidence:
- `Minnesota State High School Mathematics League`: The Minnesota State High School Mathematics League is the premier high school mathematics league in the state of Minnesota. It was founded in 1980 by Macalester College professor Wayne Roberts. The league holds five statewide tournaments per year from Novem...
- `Macalester College`: Macalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US. It was founded in 1874 as a Presbyterian-affiliated but nonsectarian college. Its first class entered September 15, 1885. Macalester is exclusively...

First perturbation evidence:
- query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year?  Use the retrieved evidence only; one reasoning hop may be absent.
- `Macalester College`: Macalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US. It was founded in 1874 as a Presbyterian-affiliated but nonsectarian college. Its first class entered September 15, 1885. Macalester is exclusively...
- `Oberlin College`: Oberlin College is a private liberal arts college in Oberlin, Ohio. The college was founded as the Oberlin Collegiate Institute in 1833 by John Jay Shipherd and Philo Stewart. It is the oldest coeducational liberal arts college in the United States and the ...

#### hotpot_hardneg:5a792ad055429907847277d1:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0576`
- baseline_score: `0.0518`
- target_minus_baseline: `0.0057`
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?
- candidate_answer: `Mickey's PhilharMagic`

Clean evidence:
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

First perturbation evidence:
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?  Use the retrieved evidence only; one reasoning hop may be absent.
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Guardians of the Galaxy (Epcot Attraction)`: Guardians of the Galaxy is an upcoming attraction to be built at Epcot within the Walt Disney World Resort. It will be the third attraction based on a Marvel Comics property at Walt Disney Parks and Resorts after the Iron Man Experience at Hong Kong Disneyl...

#### hotpot_hardneg:5a8ba3ff55429971feec4744:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0516`
- baseline_score: `0.0460`
- target_minus_baseline: `0.0055`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Use the retrieved evidence only; one reasoning hop may be absent.
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...
- `New Mexico Governor's Mansion`: The New Mexico Governor's Residence is the official residence of the Governor of New Mexico and his or her family. The current structure, located at 1 Mansion Drive in Santa Fe, New Mexico, has served as the Governor's official residence since 1954. It is t...

#### hotpot_hardneg:5ae1fced5542997283cd230e:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0119`
- baseline_score: `0.0065`
- target_minus_baseline: `0.0054`
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- candidate_answer: `Naguib Mahfouz`

Clean evidence:
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Naguib Mahfouz`: Naguib Mahfouz (Arabic: نجيب محفوظ‎ ‎ "Nagīb Maḥfūẓ ", ] ; December 11, 1911 – August 30, 2006) was an Egyptian writer who won the 1988 Nobel Prize for Literature. He is regarded as one of the first contemporary writers of Arabic literature, along with Tawf...

First perturbation evidence:
- query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz? Use the retrieved evidence only; one reasoning hop may be absent.
- `William H. Gass`: William Howard Gass (born July 30, 1924) is an American novelist, short-story writer, essayist, critic, and former philosophy professor. He has written three novels, three collections of short stories, a collection of novellas, and seven volumes of essays, ...
- `Cairo Trilogy`: The Cairo Trilogy (Arabic: الثلاثية‎ ‎ ("The Trilogy") or ثلاثية القاهرة ("The Cairo Trilogy")) is a trilogy of novels written by the Egyptian novelist and Nobel Prize winner Naguib Mahfouz, and one of the prime works of his literary career.

#### hotpot_hardneg:5ae5dae2554299546bf82fa4:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.1206`
- baseline_score: `0.1157`
- target_minus_baseline: `0.0049`
- query: Faruk Halibegovic was born in what city that is the capital and largest city of Bosnia and Herzegovina with a population of 275,524?
- candidate_answer: `Sarajevo`

Clean evidence:
- `Faruk Halilbegović`: Faruk Halilbegović (born 7 September 1987 in Sarajevo, Bosnia and Herzegovina) is a handball left back who plays for Polish club Zagłębie Lubin. He started his career in Bosna Visoko and later played for Borac Banja Luka, Bosna Sarajevo and Sloga Doboj. Wit...
- `Sarajevo`: Sarajevo (Cyrillic: Сарајево , ] , ) is the capital and largest city of Bosnia and Herzegovina, with a population of 275,524 in its current administrative limits. The Sarajevo metropolitan area, including Sarajevo Canton and East Sarajevo is home to 643,016...

First perturbation evidence:
- query: Faruk Halibegovic was born in what city that is the capital and largest city of Bosnia and Herzegovina with a population of 275,524? Use the retrieved evidence only; one reasoning hop may be absent.
- `Sarajevo`: Sarajevo (Cyrillic: Сарајево , ] , ) is the capital and largest city of Bosnia and Herzegovina, with a population of 275,524 in its current administrative limits. The Sarajevo metropolitan area, including Sarajevo Canton and East Sarajevo is home to 643,016...
- `Tuzla`: Tuzla is a city in Bosnia and Herzegovina. It is the seat of the Tuzla Canton and is the economic, scientific, cultural, educational, health and tourist centre of northeast Bosnia. After Sarajevo and Banja Luka, Tuzla is the third largest city in Bosnia and...

#### hotpot_hardneg:5ae55b8255429908b63265ef:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0875`
- baseline_score: `0.0831`
- target_minus_baseline: `0.0045`
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada?
- candidate_answer: `Masayoshi "Masa" Takayama`

Clean evidence:
- `Tetsu (restaurant)`: Tetsu is a modern Japanese restaurant located in the Tribeca neighborhood of New York City. Conceived by Michelin-starred chef Masa Takayama, Tetsu serves a Yakitori-based menu with an emphasis upon grilled fare. Similar to Takayama’s other restaurant ventu...
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...

First perturbation evidence:
- query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada? Use the retrieved evidence only; one reasoning hop may be absent.
- `Masa Takayama`: Masayoshi "Masa" Takayama (高山 雅氏 , Takayama Masayoshi ) (born 1 May 1954 in Kuroiso, Tochigi, Japan) is the chef and owner of Masa, a three-Michelin-starred Japanese and sushi restaurant in Manhattan, New York City. He is also owner of Bar Masa, with two lo...
- `Dinner Rush`: Dinner Rush is a 2000 American independent feature film, written by Brian S. Kalata and Rick Shaughnessy, and directed by Bob Giraldi. It stars Danny Aiello as a restaurateur-bookmaker in New York City's Tribeca neighborhood and Edoardo Ballerini as his son...

#### hotpot_hardneg:5ab90fdd55429916710eb0fc:hard_missing_hop

- label_answerable: `False`
- construction_type: `hard_missing_hop`
- target_score: `0.0816`
- baseline_score: `0.0783`
- target_minus_baseline: `0.0034`
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from?
- candidate_answer: `London, England`

Clean evidence:
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Wheelock Whitney`: Wheelock Whitney may refer to one of three members of the Whitney family:

First perturbation evidence:
- query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from? Use the retrieved evidence only; one reasoning hop may be absent.
- `Whitney family`: The Whitney family is an American family notable for their social prominence, wealth, business enterprises and philanthropy, founded by John Whitney (1592–1673) who came from London, England to Watertown, Massachusetts in 1635. The historic family mansion i...
- `Harry Payne Whitney`: Harry Payne Whitney (April 29, 1872 – October 26, 1930) was an American businessman, thoroughbred horse breeder, and member of the prominent Whitney family.


### Baseline over target on positives

#### hotpot_hardneg:5ac213805542992f1f2b37e7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9532`
- baseline_score: `0.9582`
- target_minus_baseline: `-0.0050`
- query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"?
- candidate_answer: `November`

Clean evidence:
- `Kenn Scott`: Kenn Scott is a Toronto-based screenwriter noted for his work in children's programming and animation. Included amongst the many shows he has written for are "Ned's Newt", "Iggy Arbuckle", "Captain Flamingo", "Rescue Heroes", "Seven Little Monsters", "Pelsw...
- `Pelswick`: Pelswick is an animated television series co-produced by Nelvana Limited and Suzhou Hong Ying Animation Corporation Limited in association with The Canadian Broadcasting Corporation and Nickelodeon. The series is about a teenage boy who uses a wheelchair, e...

First perturbation evidence:
- query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"? Please verify each supporting hop.
- `Kenn Scott`: Kenn Scott is a Toronto-based screenwriter noted for his work in children's programming and animation. Included amongst the many shows he has written for are "Ned's Newt", "Iggy Arbuckle", "Captain Flamingo", "Rescue Heroes", "Seven Little Monsters", "Pelsw...
- `Pelswick`: Pelswick is an animated television series co-produced by Nelvana Limited and Suzhou Hong Ying Animation Corporation Limited in association with The Canadian Broadcasting Corporation and Nickelodeon. The series is about a teenage boy who uses a wheelchair, e...

#### hotpot_hardneg:5adce88b5542992c1e3a249a:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9633`
- baseline_score: `0.9681`
- target_minus_baseline: `-0.0048`
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- candidate_answer: `320 years`

Clean evidence:
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

First perturbation evidence:
- query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ? Please verify each supporting hop.
- `Delhi Sultanate`: The Delhi Sultanate was a Muslim sultanate based mostly in Delhi that stretched over large parts of the Indian subcontinent for 320 years (1206–1526). Five dynasties ruled over the Delhi Sultanate sequentially: the Mamluk dynasty (1206–90), the Khalji dynas...
- `Halebidu`: Halebeedu (literally "old capital") is a town located in Hassan District, Karnataka, India. Halebidu (which used to be called Dorasamudra or Dwarasamudra) was the regal capital of the Hoysala Empire in the 12th century. It is home to some of the best exampl...

#### hotpot_hardneg:5ac26ac15542992f1f2b38bc:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9529`
- baseline_score: `0.9576`
- target_minus_baseline: `-0.0047`
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to?
- candidate_answer: `Sam Phillips`

Clean evidence:
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

First perturbation evidence:
- query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to? Please verify each supporting hop.
- `Beneath (2007 film)`: Beneath is a straight-to-DVD thriller-horror film co-produced in a first time partnership between Paramount Classics (a Viacom subsidiary) and MTV Films (although both co-purchased the rights to "Hustle & Flow" in 2005). The film is directed by the newcomer...
- `Hustle &amp; Flow`: Hustle & Flow is a 2005 American independent drama film written and directed by Craig Brewer and produced by John Singleton and Stephanie Allain. It was released on July 22, 2005. Terrence Howard stars as a Memphis hustler and pimp who faces his aspiration ...

#### hotpot_hardneg:5a8303c255429954d2e2ec01:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9614`
- baseline_score: `0.9656`
- target_minus_baseline: `-0.0042`
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- candidate_answer: `Chrysler K platform`

Clean evidence:
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

First perturbation evidence:
- query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications? Please verify each supporting hop.
- `Chrysler F platform`: Chrysler's rear wheel drive F platform was used from 1976 to 1980. It was replaced by the nearly identical Chrysler M platform. There were two wheelbases: 108.7 in for 2-door models, and 112.7 in for four-doors. As the market evolved, these would be markete...
- `Plymouth Fury`: The Plymouth Fury is a model of automobile which was produced by Plymouth from 1955 to 1989. It was introduced for the 1956 model year as a sub-series of the Plymouth Belvedere, becoming a separate series one level above the contemporary Belvedere for 1959....

#### hotpot_hardneg:5a881cbb55429938390d3ee7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9605`
- baseline_score: `0.9639`
- target_minus_baseline: `-0.0034`
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style?
- candidate_answer: `Hellenism`

Clean evidence:
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

First perturbation evidence:
- query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style? Please verify each supporting hop.
- `St. John of the Cross Episcopal Church`: St. John of the Cross Episcopal Church, Rectory and Cemetery is a historic Episcopal church complex located at Bristol, Elkhart County, Indiana. The church was built between 1843 and 1847, and is a one-story, Gothic Revival style frame building. It has a pr...
- `Greek Revival architecture`: The Greek Revival was an architectural movement of the late 18th and early 19th centuries, predominantly in Northern Europe and the United States. A product of Hellenism, it may be looked upon as the last phase in the development of Neoclassical architectur...

#### hotpot_hardneg:5adcd2435542992c1e3a241b:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9645`
- baseline_score: `0.9676`
- target_minus_baseline: `-0.0031`
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"?
- candidate_answer: `Geraldine Page`

Clean evidence:
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

First perturbation evidence:
- query: Which eight-time Academy Award nominee was Tennessee Williams's choice to play a leading role in his play "Clothes for a Summer Hotel"? Please verify each supporting hop.
- `Clothes for a Summer Hotel`: Clothes for a Summer Hotel is a 1980 play by Tennessee Williams about the relationship between novelist F. Scott Fitzgerald and his wife Zelda. A critical and commercial failure, it was Williams' last play to debut on Broadway during his lifetime. The play ...
- `Geraldine Page`: Geraldine Sue Page (November 22, 1924 – June 13, 1987) was an American film, television and stage actress. An eight-time Academy Award nominee, she was nominated for "Hondo" (1953), "Summer and Smoke" (1961), "Sweet Bird of Youth" (1962), "You're a Big Boy ...

#### hotpot_hardneg:5a792ad055429907847277d1:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9629`
- baseline_score: `0.9657`
- target_minus_baseline: `-0.0028`
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?
- candidate_answer: `Mickey's PhilharMagic`

Clean evidence:
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

First perturbation evidence:
- query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie?  Please verify each supporting hop.
- `Mickey's Twice Upon a Christmas`: Mickey's Twice Upon a Christmas is a 2004 computer-animated direct-to-video fantasy comedy anthology film produced by Disney Toon Studios and the sequel to 1999's "Mickey's Once Upon a Christmas". The segments in this video feature Mickey Mouse, Minnie Mous...
- `Mickey's PhilharMagic`: Mickey's PhilharMagic is a 4-D film attraction found at the Magic Kingdom theme park in the Walt Disney World Resort, Hong Kong Disneyland, and at Tokyo Disneyland. The film was directed by George Scribner, who is best known for directing Disney's 1988 anim...

#### hotpot_hardneg:5a8ba3ff55429971feec4744:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9628`
- baseline_score: `0.9654`
- target_minus_baseline: `-0.0026`
- query: Stokely Webster has paintings can be found at the official residence of whom?
- candidate_answer: `Mayor of the City of New York`

Clean evidence:
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...

First perturbation evidence:
- query: Stokely Webster has paintings can be found at the official residence of whom? Please verify each supporting hop.
- `Stokely Webster`: Stokely Webster (1912 – 2001) was best known as an American impressionist painter who studied in Paris. His paintings can be found in the permanent collections of many museums, including the Metropolitan Museum of Art in New York, the National Museum of Ame...
- `Gracie Mansion`: Archibald Gracie Mansion (commonly called Gracie Mansion) is the official residence of the Mayor of the City of New York. Built in 1799, it is located in Carl Schurz Park, at East End Avenue and 88th Street in the Yorkville neighborhood of Manhattan. The ma...
