# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 0.8000 | 0.3333 | 0.3000 | 0.6143 | 0.3525 |
| baseline_calibrated_logistic_orbit | 0.8575 | 0.1667 | 0.1500 | 0.6463 | 0.3180 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| distractor | 1 | 0 | 1 | 0.3811 | 0.2517 | 0.1294 |
| false_premise | 7 | 0 | 7 | 0.3758 | 0.2637 | 0.1122 |
| missing_hop | 12 | 0 | 12 | 0.3365 | 0.3552 | -0.0187 |
| stable | 20 | 20 | 0 | 0.6143 | 0.6463 | -0.0320 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| retrieval_overlap | 0.5279 | 0.5862 | -0.0583 |
| min_sufficiency | 0.1976 | 0.1590 | 0.0385 |
| clean_to_worst_gap | 0.0074 | 0.0459 | -0.0385 |
| verifier_entropy | 0.5018 | 0.4657 | 0.0360 |
| naive_orbit_average | 0.2022 | 0.1838 | 0.0184 |
| mean_sufficiency | 0.2022 | 0.1838 | 0.0184 |
| mean_missing | 0.7584 | 0.7696 | -0.0112 |
| sufficiency_variance | 0.0000 | 0.0012 | -0.0011 |
| max_conflict | 0.0822 | 0.0825 | -0.0003 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |
| corm_mean_clean | 0.5000 | 0.5000 | 0.0000 |
| context_sufficiency_clean | 0.2050 | 0.2050 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### hotpot:5ae4cf975542990ba0bbb151:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.6931`
- baseline_score: `0.7010`
- target_minus_baseline: `-0.0079`
- query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- candidate_answer: `action figure toyline`

Clean evidence:
- `Movie Masters`: Movie Masters is an action figure toyline from Mattel based on popular movie franchises most notably DC Comics. The line has featured characters from the films "Superman", "Avatar", "The Dark Knight" trilogy, "Green Lantern", and "Man of Steel". Figures in ...
- `Batman in film`: The fictional superhero Batman, who appears in American comic books published by DC Comics, has appeared in various films since his inception. Created by Bob Kane and Bill Finger, the character first starred in two serial films in the 1940s, "Batman" and "B...

First perturbation evidence:
- query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger? Answer using only one supporting hop if possible.
- `Movie Masters`: Movie Masters is an action figure toyline from Mattel based on popular movie franchises most notably DC Comics. The line has featured characters from the films "Superman", "Avatar", "The Dark Knight" trilogy, "Green Lantern", and "Man of Steel". Figures in ...
- `Vicki Vale`: Victoria "Vicki" Vale is a fictional character appearing in American comic books published by DC Comics, commonly in association with the superhero Batman. Created by Bob Kane and Bill Finger, the character debuted in "Batman" #49 (October 1948). Vicky Vale...

#### hotpot:5a8e296f554299068b959e71:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.6703`
- baseline_score: `0.7345`
- target_minus_baseline: `-0.0642`
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- candidate_answer: `United States`

Clean evidence:
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

First perturbation evidence:
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common? Answer using only one supporting hop if possible.
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `Sterling Park, Virginia`: Sterling Park is a community in Sterling, Virginia and a part of the Washington metropolitan area. The community opened in 1963 on former farmland near Dulles International Airport in Loudoun County. The land where Sterling Park was built was mainly made up...

#### hotpot:5adfe0de55429925eb1afae9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6614`
- baseline_score: `0.6040`
- target_minus_baseline: `0.0574`
- query: Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- candidate_answer: `George Martin`

Clean evidence:
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

First perturbation evidence:
- query: Assuming the answer is not George Martin, Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

#### hotpot:5ab6ecd85542991d322236cf:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6452`
- baseline_score: `0.5118`
- target_minus_baseline: `0.1334`
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- candidate_answer: `Latin American culture`

Clean evidence:
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

First perturbation evidence:
- query: Assuming the answer is not Latin American culture, The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...

#### hotpot:5ab28e2a5542993be8fa9947:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.5977`
- baseline_score: `0.5457`
- target_minus_baseline: `0.0520`
- query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"?
- candidate_answer: `Eddie "The Eagle" Edwards`

Clean evidence:
- `Eddie &quot;The Eagle&quot; Edwards`: Michael Edwards (born 5 December 1963), best known as "Eddie the Eagle", is a British skier who in 1988 became the first competitor since 1929 to represent Great Britain in Olympic ski jumping, finishing last in the 70 m and 90 m events. He became the Briti...
- `The Jump`: The Jump is a British television series that follows celebrities as they try to master various winter sports including skeleton, bobsleigh, snowskates, ski cross, and giant slalom. Davina McCall and Alex Brooker presented the first series, with McCall retur...

First perturbation evidence:
- query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"? Answer using only one supporting hop if possible.
- `Eddie &quot;The Eagle&quot; Edwards`: Michael Edwards (born 5 December 1963), best known as "Eddie the Eagle", is a British skier who in 1988 became the first competitor since 1929 to represent Great Britain in Olympic ski jumping, finishing last in the 70 m and 90 m events. He became the Briti...
- `Åsarna IK`: Åsarna IK, founded in 1924, is a Swedish sports club in Åsarna. The club has had many prominent competitors in cross country skiing, which is evident in the nickname of the village Åsarna, "Guldbyn" (golden village), which was coined after the 1988 Winter O...

#### hotpot:5a7cb993554299452d57b9c2:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.5968`
- baseline_score: `0.6414`
- target_minus_baseline: `-0.0446`
- query: How much change in elevation is there at the site of the 1999 FIA GT Hockenheim 500km?
- candidate_answer: `very little`

Clean evidence:
- `Hockenheimring`: The is a motor racing circuit situated in the Rhine valley near the town of Hockenheim in Baden-Württemberg, Germany, located on Bertha Benz Memorial Route. Amongst other motor racing events, it biennially hosts the German Grand Prix, with the most recent b...
- `1999 FIA GT Hockenheim 500km`: The 1999 FIA GT Hockenheim 500 km was the third round the 1999 FIA GT Championship season. It took place at the Hockenheimring Short Circuit, Germany, on June 27, 1999.

First perturbation evidence:
- query: How much change in elevation is there at the site of the 1999 FIA GT Hockenheim 500km? Answer using only one supporting hop if possible.
- `Hockenheimring`: The is a motor racing circuit situated in the Rhine valley near the town of Hockenheim in Baden-Württemberg, Germany, located on Bertha Benz Memorial Route. Amongst other motor racing events, it biennially hosts the German Grand Prix, with the most recent b...
- `1999 FIA GT Zhuhai 500km`: The 1999 FIA GT Zhuhai 500 km was the tenth and final round the 1999 FIA GT Championship season. It took place at the Zhuhai International Circuit, China, on November 26, 1999.

#### hotpot:5a888fe6554299206df2b2f7:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.5359`
- baseline_score: `0.5418`
- target_minus_baseline: `-0.0059`
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon?
- candidate_answer: `T. R. M. Howard`

Clean evidence:
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `David T. Beito`: David T. Beito (born 1956) is a historian and professor of history at the University of Alabama. He is the author of "Taxpayers in Revolt: Tax Resistance during the Great Depression" (1989); "From Mutual Aid to the Welfare State: Fraternal Societies and Soc...

First perturbation evidence:
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon? Answer using only one supporting hop if possible.
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `A. Maceo Smith`: Antonio Maceo Smith (April 16, 1903 - December 19, 1977) was a pioneer civil rights leader in Dallas, Texas, whose years of activism with the National Association for the Advancement of Colored People (NAACP) and other civil rights and community groups led ...

#### hotpot:5a8b051255429971feec460e:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.5108`
- baseline_score: `0.4340`
- target_minus_baseline: `0.0768`
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- candidate_answer: `U.S. Senator Pat McCarran`

Clean evidence:
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

First perturbation evidence:
- query: Assuming the answer is not U.S. Senator Pat McCarran, Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `Indianapolis Executive Airport`: Indianapolis Executive Airport (ICAO: KTYQ, FAA LID: TYQ) is a public airport at 11329 E. State Road 32, five miles north of Zionsville, just west of Jolietville in Boone County, Indiana, United States. The airport is owned by the Hamilton County Airport Au...


### Low-scoring false negatives

#### hotpot:5a85db6e5542994c784ddb96:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.4280`
- baseline_score: `0.6902`
- target_minus_baseline: `-0.2622`
- query: What is the student body for Ron Johnson's alma mater?
- candidate_answer: `37,776`

Clean evidence:
- `Ron Johnson (wide receiver, born 1958)`: Ronald J. Johnson (born September 21, 1958) is a former American football wide receivers who played five seasons with the Philadelphia Eagles of the National Football League. He was drafted by the Seattle Seahawks in the seventh round of the 1981 NFL Draft....
- `California State University, Long Beach`: California State University, Long Beach (CSULB; also known as Long Beach State, Cal State Long Beach, LBSU, or The Beach) is the third largest campus of the 23-school California State University system (CSU) and one of the largest universities in the state ...

First perturbation evidence:
- query: What is the student body for Ron Johnson's alma mater? Please verify each supporting hop.
- `Ron Johnson (wide receiver, born 1958)`: Ronald J. Johnson (born September 21, 1958) is a former American football wide receivers who played five seasons with the Philadelphia Eagles of the National Football League. He was drafted by the Seattle Seahawks in the seventh round of the 1981 NFL Draft....
- `California State University, Long Beach`: California State University, Long Beach (CSULB; also known as Long Beach State, Cal State Long Beach, LBSU, or The Beach) is the third largest campus of the 23-school California State University system (CSU) and one of the largest universities in the state ...

#### hotpot:5adc1af75542994650320c75:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.4458`
- baseline_score: `0.7240`
- target_minus_baseline: `-0.2783`
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- candidate_answer: `1998`

Clean evidence:
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

First perturbation evidence:
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released? Please verify each supporting hop.
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

#### hotpot:5ab6ecd85542991d322236cf:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5150`
- baseline_score: `0.4568`
- target_minus_baseline: `0.0582`
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- candidate_answer: `Latin American culture`

Clean evidence:
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

First perturbation evidence:
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America? Please verify each supporting hop.
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

#### hotpot:5a7cb993554299452d57b9c2:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5576`
- baseline_score: `0.6073`
- target_minus_baseline: `-0.0497`
- query: How much change in elevation is there at the site of the 1999 FIA GT Hockenheim 500km?
- candidate_answer: `very little`

Clean evidence:
- `Hockenheimring`: The is a motor racing circuit situated in the Rhine valley near the town of Hockenheim in Baden-Württemberg, Germany, located on Bertha Benz Memorial Route. Amongst other motor racing events, it biennially hosts the German Grand Prix, with the most recent b...
- `1999 FIA GT Hockenheim 500km`: The 1999 FIA GT Hockenheim 500 km was the third round the 1999 FIA GT Championship season. It took place at the Hockenheimring Short Circuit, Germany, on June 27, 1999.

First perturbation evidence:
- query: How much change in elevation is there at the site of the 1999 FIA GT Hockenheim 500km? Please verify each supporting hop.
- `Hockenheimring`: The is a motor racing circuit situated in the Rhine valley near the town of Hockenheim in Baden-Württemberg, Germany, located on Bertha Benz Memorial Route. Amongst other motor racing events, it biennially hosts the German Grand Prix, with the most recent b...
- `1999 FIA GT Hockenheim 500km`: The 1999 FIA GT Hockenheim 500 km was the third round the 1999 FIA GT Championship season. It took place at the Hockenheimring Short Circuit, Germany, on June 27, 1999.

#### hotpot:5a7e1ad155429965cec5ea66:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5763`
- baseline_score: `0.6373`
- target_minus_baseline: `-0.0610`
- query: The first book in the Sprawl Trilogy won what three awards?
- candidate_answer: `Nebula Award, the Philip K. Dick Award, and the Hugo Award`

Clean evidence:
- `Sprawl trilogy`: The Sprawl trilogy (also known as the Neuromancer, Cyberspace, or Matrix trilogy) is William Gibson's first set of novels, composed of "Neuromancer" (1984), "Count Zero" (1986), and "Mona Lisa Overdrive" (1988).
- `Neuromancer`: Neuromancer is a 1984 science fiction novel by American-Canadian writer William Gibson. It is one of the best-known works in the cyberpunk genre and the first novel to win the Nebula Award, the Philip K. Dick Award, and the Hugo Award. It was Gibson's debut...

First perturbation evidence:
- query: The first book in the Sprawl Trilogy won what three awards? Please verify each supporting hop.
- `Sprawl trilogy`: The Sprawl trilogy (also known as the Neuromancer, Cyberspace, or Matrix trilogy) is William Gibson's first set of novels, composed of "Neuromancer" (1984), "Count Zero" (1986), and "Mona Lisa Overdrive" (1988).
- `Neuromancer`: Neuromancer is a 1984 science fiction novel by American-Canadian writer William Gibson. It is one of the best-known works in the cyberpunk genre and the first novel to win the Nebula Award, the Philip K. Dick Award, and the Hugo Award. It was Gibson's debut...

#### hotpot:5a810221554299260e20a1f9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5833`
- baseline_score: `0.6260`
- target_minus_baseline: `-0.0427`
- query: Who wrote the 1970 international hit song Murray Head is most recognized for?
- candidate_answer: `Andrew Lloyd Webber and Tim Rice`

Clean evidence:
- `Superstar (Jesus Christ Superstar song)`: "Superstar" is the title song from the 1970 rock opera "Jesus Christ Superstar" written by Andrew Lloyd Webber and Tim Rice.
- `Murray Head`: Murray Seafield St George Head (born 5 March 1946) is an English actor and singer, most recognised for his international hit songs "Superstar" (from the 1970 rock opera "Jesus Christ Superstar") and "One Night in Bangkok" (the 1984 single from the musical "...

First perturbation evidence:
- query: Who wrote the 1970 international hit song Murray Head is most recognized for? Please verify each supporting hop.
- `Superstar (Jesus Christ Superstar song)`: "Superstar" is the title song from the 1970 rock opera "Jesus Christ Superstar" written by Andrew Lloyd Webber and Tim Rice.
- `Murray Head`: Murray Seafield St George Head (born 5 March 1946) is an English actor and singer, most recognised for his international hit songs "Superstar" (from the 1970 rock opera "Jesus Christ Superstar") and "One Night in Bangkok" (the 1984 single from the musical "...

#### hotpot:5adfd42555429942ec259b52:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6173`
- baseline_score: `0.6382`
- target_minus_baseline: `-0.0209`
- query: What song featured on the Beatles' album "Please Please Me" was covered by Tiffany?
- candidate_answer: `I Saw Her Standing There`

Clean evidence:
- `I Saw Her Standing There`: "I Saw Her Standing There" is a song by the English rock band the Beatles written by Paul McCartney and John Lennon. It is the opening track on the band's 1963 debut album "Please Please Me".
- `Tiffany Darwish`: Tiffany Renee Darwish (born October 2, 1971), also known as Tiffany, is an American singer, songwriter, actress, and former teen icon. She is most notable for her 1987 cover of "I Think We're Alone Now", a 1967 original recording by Tommy James and the Shon...

First perturbation evidence:
- query: What song featured on the Beatles' album "Please Please Me" was covered by Tiffany?  Please verify each supporting hop.
- `I Saw Her Standing There`: "I Saw Her Standing There" is a song by the English rock band the Beatles written by Paul McCartney and John Lennon. It is the opening track on the band's 1963 debut album "Please Please Me".
- `Tiffany Darwish`: Tiffany Renee Darwish (born October 2, 1971), also known as Tiffany, is an American singer, songwriter, actress, and former teen icon. She is most notable for her 1987 cover of "I Think We're Alone Now", a 1967 original recording by Tommy James and the Shon...

#### hotpot:5ae712fa554299572ea546b9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6183`
- baseline_score: `0.6847`
- target_minus_baseline: `-0.0664`
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell?
- candidate_answer: `the Knight Company`

Clean evidence:
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...

First perturbation evidence:
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell? Please verify each supporting hop.
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...


### Target over baseline on negatives

#### hotpot:5a810221554299260e20a1f9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.4796`
- baseline_score: `0.1040`
- target_minus_baseline: `0.3756`
- query: Who wrote the 1970 international hit song Murray Head is most recognized for?
- candidate_answer: `Andrew Lloyd Webber and Tim Rice`

Clean evidence:
- `Superstar (Jesus Christ Superstar song)`: "Superstar" is the title song from the 1970 rock opera "Jesus Christ Superstar" written by Andrew Lloyd Webber and Tim Rice.
- `Murray Head`: Murray Seafield St George Head (born 5 March 1946) is an English actor and singer, most recognised for his international hit songs "Superstar" (from the 1970 rock opera "Jesus Christ Superstar") and "One Night in Bangkok" (the 1984 single from the musical "...

First perturbation evidence:
- query: Assuming the answer is not Andrew Lloyd Webber and Tim Rice, Who wrote the 1970 international hit song Murray Head is most recognized for?
- `Irene Cara`: Irene Cara Escalera (born March 18, 1959) is an American singer, songwriter, and actress. She sang and co-wrote the international hit song 'Flashdance... What a Feeling' (from the movie "Flashdance"), for which she won an Academy Award for Best Original Son...
- `Murray Head`: Murray Seafield St George Head (born 5 March 1946) is an English actor and singer, most recognised for his international hit songs "Superstar" (from the 1970 rock opera "Jesus Christ Superstar") and "One Night in Bangkok" (the 1984 single from the musical "...

#### hotpot:5ab6ecd85542991d322236cf:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6452`
- baseline_score: `0.5118`
- target_minus_baseline: `0.1334`
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- candidate_answer: `Latin American culture`

Clean evidence:
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

First perturbation evidence:
- query: Assuming the answer is not Latin American culture, The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...

#### hotpot:5a8eed625542995085b374b9:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.3811`
- baseline_score: `0.2517`
- target_minus_baseline: `0.1294`
- query: Which system of parliament was modeled after the United Kingdom and is also used in Canada?
- candidate_answer: `Westminster system`

Clean evidence:
- `Constitution of Alberta`: The Constitution of Alberta describes the fundamental rules under which the Canadian province of Alberta is governed. As is typical of all Canadian provinces, and Westminster systems more generally, Alberta's is an unwritten constitution. Alberta's constitu...
- `Westminster system`: The Westminster system is a parliamentary system of government modelled after that which developed in the United Kingdom. This term comes from the Palace of Westminster, the seat of the British parliament.

First perturbation evidence:
- query: Which system of parliament was modeled after the United Kingdom and is also used in Canada?  Prefer background context even if direct evidence is absent.
- `Governance of England`: There has not been a government of England since 1707 when the Kingdom of England ceased to exist as a sovereign state, as it merged with the Kingdom of Scotland to form the Kingdom of Great Britain. Kingdom of Great Britain continued from 1707 until 1801 w...
- `Australian Public Service`: The Australian Public Service (APS) is the federal civil service of the Commonwealth of Australia responsible for the public administration, public policy, and public services of the departments and executive and statutory agencies of the Government of Aust...

#### hotpot:5a8b051255429971feec460e:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.5108`
- baseline_score: `0.4340`
- target_minus_baseline: `0.0768`
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- candidate_answer: `U.S. Senator Pat McCarran`

Clean evidence:
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

First perturbation evidence:
- query: Assuming the answer is not U.S. Senator Pat McCarran, Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `Indianapolis Executive Airport`: Indianapolis Executive Airport (ICAO: KTYQ, FAA LID: TYQ) is a public airport at 11329 E. State Road 32, five miles north of Zionsville, just west of Jolietville in Boone County, Indiana, United States. The airport is owned by the Hamilton County Airport Au...

#### hotpot:5adfd42555429942ec259b52:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.2046`
- baseline_score: `0.1303`
- target_minus_baseline: `0.0743`
- query: What song featured on the Beatles' album "Please Please Me" was covered by Tiffany?
- candidate_answer: `I Saw Her Standing There`

Clean evidence:
- `I Saw Her Standing There`: "I Saw Her Standing There" is a song by the English rock band the Beatles written by Paul McCartney and John Lennon. It is the opening track on the band's 1963 debut album "Please Please Me".
- `Tiffany Darwish`: Tiffany Renee Darwish (born October 2, 1971), also known as Tiffany, is an American singer, songwriter, actress, and former teen icon. She is most notable for her 1987 cover of "I Think We're Alone Now", a 1967 original recording by Tommy James and the Shon...

First perturbation evidence:
- query: Assuming the answer is not I Saw Her Standing There, What song featured on the Beatles' album "Please Please Me" was covered by Tiffany?
- `Tiffany Darwish`: Tiffany Renee Darwish (born October 2, 1971), also known as Tiffany, is an American singer, songwriter, actress, and former teen icon. She is most notable for her 1987 cover of "I Think We're Alone Now", a 1967 original recording by Tommy James and the Shon...
- `Tonight's the Night (The Shirelles album)`: Tonight's the Night is the debut album by American girl group quartet The Shirelles, released in 1961. It contains the hit song "Will You Love Me Tomorrow". Although Shirley Owens was the group's main lead singer, "Tonight's the Night" also features lead vo...

#### hotpot:5adfe0de55429925eb1afae9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6614`
- baseline_score: `0.6040`
- target_minus_baseline: `0.0574`
- query: Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- candidate_answer: `George Martin`

Clean evidence:
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

First perturbation evidence:
- query: Assuming the answer is not George Martin, Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

#### hotpot:5ab28e2a5542993be8fa9947:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.5977`
- baseline_score: `0.5457`
- target_minus_baseline: `0.0520`
- query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"?
- candidate_answer: `Eddie "The Eagle" Edwards`

Clean evidence:
- `Eddie &quot;The Eagle&quot; Edwards`: Michael Edwards (born 5 December 1963), best known as "Eddie the Eagle", is a British skier who in 1988 became the first competitor since 1929 to represent Great Britain in Olympic ski jumping, finishing last in the 70 m and 90 m events. He became the Briti...
- `The Jump`: The Jump is a British television series that follows celebrities as they try to master various winter sports including skeleton, bobsleigh, snowskates, ski cross, and giant slalom. Davina McCall and Alex Brooker presented the first series, with McCall retur...

First perturbation evidence:
- query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"? Answer using only one supporting hop if possible.
- `Eddie &quot;The Eagle&quot; Edwards`: Michael Edwards (born 5 December 1963), best known as "Eddie the Eagle", is a British skier who in 1988 became the first competitor since 1929 to represent Great Britain in Olympic ski jumping, finishing last in the 70 m and 90 m events. He became the Briti...
- `Åsarna IK`: Åsarna IK, founded in 1924, is a Swedish sports club in Åsarna. The club has had many prominent competitors in cross country skiing, which is evident in the nickname of the village Åsarna, "Guldbyn" (golden village), which was coined after the 1988 Winter O...

#### hotpot:5ae712fa554299572ea546b9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.0935`
- baseline_score: `0.0490`
- target_minus_baseline: `0.0444`
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell?
- candidate_answer: `the Knight Company`

Clean evidence:
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...

First perturbation evidence:
- query: Assuming the answer is not the Knight Company, What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell?
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...
- `USADIP`: USADIP (United States Army Deserter Information Point) serves as the focal point for U.S. Army deserter reporting by U.S. Army commanders. Its mission is to maintain, verify, and disseminate information on regular Army, Army Reserve and Army National Guard ...


### Baseline over target on positives

#### hotpot:5adc1af75542994650320c75:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.4458`
- baseline_score: `0.7240`
- target_minus_baseline: `-0.2783`
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- candidate_answer: `1998`

Clean evidence:
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

First perturbation evidence:
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released? Please verify each supporting hop.
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

#### hotpot:5a85db6e5542994c784ddb96:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.4280`
- baseline_score: `0.6902`
- target_minus_baseline: `-0.2622`
- query: What is the student body for Ron Johnson's alma mater?
- candidate_answer: `37,776`

Clean evidence:
- `Ron Johnson (wide receiver, born 1958)`: Ronald J. Johnson (born September 21, 1958) is a former American football wide receivers who played five seasons with the Philadelphia Eagles of the National Football League. He was drafted by the Seattle Seahawks in the seventh round of the 1981 NFL Draft....
- `California State University, Long Beach`: California State University, Long Beach (CSULB; also known as Long Beach State, Cal State Long Beach, LBSU, or The Beach) is the third largest campus of the 23-school California State University system (CSU) and one of the largest universities in the state ...

First perturbation evidence:
- query: What is the student body for Ron Johnson's alma mater? Please verify each supporting hop.
- `Ron Johnson (wide receiver, born 1958)`: Ronald J. Johnson (born September 21, 1958) is a former American football wide receivers who played five seasons with the Philadelphia Eagles of the National Football League. He was drafted by the Seattle Seahawks in the seventh round of the 1981 NFL Draft....
- `California State University, Long Beach`: California State University, Long Beach (CSULB; also known as Long Beach State, Cal State Long Beach, LBSU, or The Beach) is the third largest campus of the 23-school California State University system (CSU) and one of the largest universities in the state ...

#### hotpot:5ae712fa554299572ea546b9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6183`
- baseline_score: `0.6847`
- target_minus_baseline: `-0.0664`
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell?
- candidate_answer: `the Knight Company`

Clean evidence:
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...

First perturbation evidence:
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell? Please verify each supporting hop.
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...

#### hotpot:5a8b051255429971feec460e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6351`
- baseline_score: `0.7012`
- target_minus_baseline: `-0.0661`
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- candidate_answer: `U.S. Senator Pat McCarran`

Clean evidence:
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

First perturbation evidence:
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican? Please verify each supporting hop.
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

#### hotpot:5a81d92f554299676cceb0f9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6196`
- baseline_score: `0.6825`
- target_minus_baseline: `-0.0629`
- query: Where are the 17th Street Canal and the Beaver and Erie Canal located?
- candidate_answer: `Pennsylvania`

Clean evidence:
- `17th Street Canal`: The 17th Street Canal is the largest and most important drainage canal in the city of New Orleans. Operating with Pump Station 6, It moves water into Lake Pontchartrain. The canal, along with the Orleans Canal and the London Avenue Canal, form the New Orlea...
- `Beaver and Erie Canal`: The Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the we...

First perturbation evidence:
- query: Where are the 17th Street Canal and the Beaver and Erie Canal located?  Please verify each supporting hop.
- `17th Street Canal`: The 17th Street Canal is the largest and most important drainage canal in the city of New Orleans. Operating with Pump Station 6, It moves water into Lake Pontchartrain. The canal, along with the Orleans Canal and the London Avenue Canal, form the New Orlea...
- `Beaver and Erie Canal`: The Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the we...

#### hotpot:5a7e1ad155429965cec5ea66:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5763`
- baseline_score: `0.6373`
- target_minus_baseline: `-0.0610`
- query: The first book in the Sprawl Trilogy won what three awards?
- candidate_answer: `Nebula Award, the Philip K. Dick Award, and the Hugo Award`

Clean evidence:
- `Sprawl trilogy`: The Sprawl trilogy (also known as the Neuromancer, Cyberspace, or Matrix trilogy) is William Gibson's first set of novels, composed of "Neuromancer" (1984), "Count Zero" (1986), and "Mona Lisa Overdrive" (1988).
- `Neuromancer`: Neuromancer is a 1984 science fiction novel by American-Canadian writer William Gibson. It is one of the best-known works in the cyberpunk genre and the first novel to win the Nebula Award, the Philip K. Dick Award, and the Hugo Award. It was Gibson's debut...

First perturbation evidence:
- query: The first book in the Sprawl Trilogy won what three awards? Please verify each supporting hop.
- `Sprawl trilogy`: The Sprawl trilogy (also known as the Neuromancer, Cyberspace, or Matrix trilogy) is William Gibson's first set of novels, composed of "Neuromancer" (1984), "Count Zero" (1986), and "Mona Lisa Overdrive" (1988).
- `Neuromancer`: Neuromancer is a 1984 science fiction novel by American-Canadian writer William Gibson. It is one of the best-known works in the cyberpunk genre and the first novel to win the Nebula Award, the Philip K. Dick Award, and the Hugo Award. It was Gibson's debut...

#### hotpot:5a8e296f554299068b959e71:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6636`
- baseline_score: `0.7240`
- target_minus_baseline: `-0.0604`
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- candidate_answer: `United States`

Clean evidence:
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

First perturbation evidence:
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common? Please verify each supporting hop.
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

#### hotpot:5a888fe6554299206df2b2f7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6207`
- baseline_score: `0.6765`
- target_minus_baseline: `-0.0558`
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon?
- candidate_answer: `T. R. M. Howard`

Clean evidence:
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `David T. Beito`: David T. Beito (born 1956) is a historian and professor of history at the University of Alabama. He is the author of "Taxpayers in Revolt: Tax Resistance during the Great Depression" (1989); "From Mutual Aid to the Welfare State: Fraternal Societies and Soc...

First perturbation evidence:
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon? Please verify each supporting hop.
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `David T. Beito`: David T. Beito (born 1956) is a historian and professor of history at the University of Alabama. He is the author of "Taxpayers in Revolt: Tax Resistance during the Great Depression" (1989); "From Mutual Aid to the Welfare State: Fraternal Societies and Soc...
