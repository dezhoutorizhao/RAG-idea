# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 0.8706 | 0.0833 | 0.2105 | 0.7161 | 0.3723 |
| baseline_calibrated_logistic_orbit | 0.8735 | 0.1667 | 0.1579 | 0.7386 | 0.3479 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| distractor | 8 | 0 | 8 | 0.1658 | 0.1658 | -0.0001 |
| false_premise | 5 | 0 | 5 | 0.5669 | 0.4653 | 0.1016 |
| missing_hop | 4 | 0 | 4 | 0.5423 | 0.5653 | -0.0230 |
| stable | 20 | 20 | 0 | 0.7161 | 0.7386 | -0.0225 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| verifier_entropy | 0.5018 | 0.4358 | 0.0659 |
| min_sufficiency | 0.1976 | 0.1340 | 0.0635 |
| clean_to_worst_gap | 0.0074 | 0.0682 | -0.0607 |
| naive_orbit_average | 0.2022 | 0.1698 | 0.0323 |
| mean_sufficiency | 0.2022 | 0.1698 | 0.0323 |
| retrieval_overlap | 0.5279 | 0.4989 | 0.0290 |
| max_conflict | 0.0822 | 0.1064 | -0.0242 |
| mean_missing | 0.7584 | 0.7751 | -0.0167 |
| context_sufficiency_clean | 0.2050 | 0.2022 | 0.0028 |
| clean_sufficiency | 0.2050 | 0.2022 | 0.0028 |
| sufficiency_variance | 0.0000 | 0.0023 | -0.0023 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### hotpot:5ab28e2a5542993be8fa9947:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.8051`
- baseline_score: `0.7976`
- target_minus_baseline: `0.0075`
- query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"?
- candidate_answer: `Eddie "The Eagle" Edwards`

Clean evidence:
- `Eddie &quot;The Eagle&quot; Edwards`: Michael Edwards (born 5 December 1963), best known as "Eddie the Eagle", is a British skier who in 1988 became the first competitor since 1929 to represent Great Britain in Olympic ski jumping, finishing last in the 70 m and 90 m events. He became the Briti...
- `The Jump`: The Jump is a British television series that follows celebrities as they try to master various winter sports including skeleton, bobsleigh, snowskates, ski cross, and giant slalom. Davina McCall and Alex Brooker presented the first series, with McCall retur...

First perturbation evidence:
- query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"? Answer using only one supporting hop if possible.
- `Eddie &quot;The Eagle&quot; Edwards`: Michael Edwards (born 5 December 1963), best known as "Eddie the Eagle", is a British skier who in 1988 became the first competitor since 1929 to represent Great Britain in Olympic ski jumping, finishing last in the 70 m and 90 m events. He became the Briti...
- `Åsarna IK`: Åsarna IK, founded in 1924, is a Swedish sports club in Åsarna. The club has had many prominent competitors in cross country skiing, which is evident in the nickname of the village Åsarna, "Guldbyn" (golden village), which was coined after the 1988 Winter O...

#### hotpot:5ae4cf975542990ba0bbb151:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6885`
- baseline_score: `0.5854`
- target_minus_baseline: `0.1030`
- query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- candidate_answer: `action figure toyline`

Clean evidence:
- `Movie Masters`: Movie Masters is an action figure toyline from Mattel based on popular movie franchises most notably DC Comics. The line has featured characters from the films "Superman", "Avatar", "The Dark Knight" trilogy, "Green Lantern", and "Man of Steel". Figures in ...
- `Batman in film`: The fictional superhero Batman, who appears in American comic books published by DC Comics, has appeared in various films since his inception. Created by Bob Kane and Bill Finger, the character first starred in two serial films in the 1940s, "Batman" and "B...

First perturbation evidence:
- query: Assuming the answer is not action figure toyline, What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- `Movie Masters`: Movie Masters is an action figure toyline from Mattel based on popular movie franchises most notably DC Comics. The line has featured characters from the films "Superman", "Avatar", "The Dark Knight" trilogy, "Green Lantern", and "Man of Steel". Figures in ...
- `Bill Finger`: Milton "Bill" Finger (February 8, 1914 – January 18, 1974) was an American comic strip and comic book writer best known as the co-creator, with Bob Kane, of the DC Comics character Batman, and the co-architect of the series' development. Although Finger did...

#### hotpot:5a888fe6554299206df2b2f7:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.6783`
- baseline_score: `0.6811`
- target_minus_baseline: `-0.0028`
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon?
- candidate_answer: `T. R. M. Howard`

Clean evidence:
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `David T. Beito`: David T. Beito (born 1956) is a historian and professor of history at the University of Alabama. He is the author of "Taxpayers in Revolt: Tax Resistance during the Great Depression" (1989); "From Mutual Aid to the Welfare State: Fraternal Societies and Soc...

First perturbation evidence:
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon? Answer using only one supporting hop if possible.
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `A. Maceo Smith`: Antonio Maceo Smith (April 16, 1903 - December 19, 1977) was a pioneer civil rights leader in Dallas, Texas, whose years of activism with the National Association for the Advancement of Colored People (NAACP) and other civil rights and community groups led ...

#### hotpot:5adc1af75542994650320c75:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.6587`
- baseline_score: `0.7679`
- target_minus_baseline: `-0.1092`
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- candidate_answer: `1998`

Clean evidence:
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

First perturbation evidence:
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released? Prefer background context even if direct evidence is absent.
- `Can't Speak French`: "Can't Speak French" is a song performed by British all-female pop group Girls Aloud, taken from their fourth studio album "Tangled Up" (2007). The song was written by Miranda Cooper, Brian Higgins and his production team Xenomania, and produced by Higgins ...
- `Long Hot Summer (Girls Aloud song)`: "Long Hot Summer" is a song by British all-female pop group Girls Aloud, taken from their third studio album "Chemistry" (2005). The song was written by Miranda Cooper, Brian Higgins and his production team Xenomania, and produced by Higgins and Xenomania. ...

#### hotpot:5adfe0de55429925eb1afae9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6281`
- baseline_score: `0.5686`
- target_minus_baseline: `0.0596`
- query: Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- candidate_answer: `George Martin`

Clean evidence:
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

First perturbation evidence:
- query: Assuming the answer is not George Martin, Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

#### hotpot:5adc1af75542994650320c75:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.6127`
- baseline_score: `0.7352`
- target_minus_baseline: `-0.1225`
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- candidate_answer: `1998`

Clean evidence:
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

First perturbation evidence:
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released? Answer using only one supporting hop if possible.
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Can't Speak French`: "Can't Speak French" is a song performed by British all-female pop group Girls Aloud, taken from their fourth studio album "Tangled Up" (2007). The song was written by Miranda Cooper, Brian Higgins and his production team Xenomania, and produced by Higgins ...

#### hotpot:5a8e296f554299068b959e71:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6126`
- baseline_score: `0.3567`
- target_minus_baseline: `0.2559`
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- candidate_answer: `United States`

Clean evidence:
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

First perturbation evidence:
- query: Assuming the answer is not United States, What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- `Baltimore–Washington International Airport`: Baltimore/Washington International Thurgood Marshall Airport (IATA: BWI, ICAO: KBWI, FAA LID: BWI) is an international airport located in Linthicum in northern unincorporated Anne Arundel County, Maryland. The airport is 9 miles south of downtown Baltimore ...
- `Washington Dulles International Airport`: Washington Dulles International Airport (IATA: IAD, ICAO: KIAD, FAA LID: IAD) is an international airport in Loudoun and Fairfax counties in Virginia, United States, 26 miles (42 km) west of downtown Washington, D.C. The airport serves the Baltimore–Washing...

#### hotpot:5a8eed625542995085b374b9:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.6003`
- baseline_score: `0.5185`
- target_minus_baseline: `0.0818`
- query: Which system of parliament was modeled after the United Kingdom and is also used in Canada? 
- candidate_answer: `Westminster system`

Clean evidence:
- `Constitution of Alberta`: The Constitution of Alberta describes the fundamental rules under which the Canadian province of Alberta is governed. As is typical of all Canadian provinces, and Westminster systems more generally, Alberta's is an unwritten constitution. Alberta's constitu...
- `Westminster system`: The Westminster system is a parliamentary system of government modelled after that which developed in the United Kingdom. This term comes from the Palace of Westminster, the seat of the British parliament.

First perturbation evidence:
- query: Which system of parliament was modeled after the United Kingdom and is also used in Canada?  Prefer background context even if direct evidence is absent.
- `Governance of England`: There has not been a government of England since 1707 when the Kingdom of England ceased to exist as a sovereign state, as it merged with the Kingdom of Scotland to form the Kingdom of Great Britain. Kingdom of Great Britain continued from 1707 until 1801 w...
- `Australian Public Service`: The Australian Public Service (APS) is the federal civil service of the Commonwealth of Australia responsible for the public administration, public policy, and public services of the departments and executive and statutory agencies of the Government of Aust...


### Low-scoring false negatives

#### hotpot:5ab6ecd85542991d322236cf:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.3882`
- baseline_score: `0.3347`
- target_minus_baseline: `0.0535`
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- candidate_answer: `Latin American culture`

Clean evidence:
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

First perturbation evidence:
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America? Please verify each supporting hop.
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

#### hotpot:5adc1af75542994650320c75:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5968`
- baseline_score: `0.7583`
- target_minus_baseline: `-0.1616`
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- candidate_answer: `1998`

Clean evidence:
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

First perturbation evidence:
- query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released? Please verify each supporting hop.
- `The Very Best of Cher`: The Very Best of Cher is the eighth compilation album by American singer-actress Cher, released on April 1, 2003. The album includes many of Cher's most popular songs, such as "If I Could Turn Back Time", "Believe", "Gypsies, Tramps and Thieves" and "Take M...
- `Believe (Cher song)`: "Believe" is a song recorded by American singer-actress Cher. It is the title track from her twenty-second album of the same name (1998), and was released as the lead single from the album on October 19, 1998 by Warner Bros. Records. It was written by Brian...

#### hotpot:5a7cb993554299452d57b9c2:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6189`
- baseline_score: `0.6473`
- target_minus_baseline: `-0.0285`
- query: How much change in elevation is there at the site of the 1999 FIA GT Hockenheim 500km?
- candidate_answer: `very little`

Clean evidence:
- `Hockenheimring`: The is a motor racing circuit situated in the Rhine valley near the town of Hockenheim in Baden-Württemberg, Germany, located on Bertha Benz Memorial Route. Amongst other motor racing events, it biennially hosts the German Grand Prix, with the most recent b...
- `1999 FIA GT Hockenheim 500km`: The 1999 FIA GT Hockenheim 500 km was the third round the 1999 FIA GT Championship season. It took place at the Hockenheimring Short Circuit, Germany, on June 27, 1999.

First perturbation evidence:
- query: How much change in elevation is there at the site of the 1999 FIA GT Hockenheim 500km? Please verify each supporting hop.
- `Hockenheimring`: The is a motor racing circuit situated in the Rhine valley near the town of Hockenheim in Baden-Württemberg, Germany, located on Bertha Benz Memorial Route. Amongst other motor racing events, it biennially hosts the German Grand Prix, with the most recent b...
- `1999 FIA GT Hockenheim 500km`: The 1999 FIA GT Hockenheim 500 km was the third round the 1999 FIA GT Championship season. It took place at the Hockenheimring Short Circuit, Germany, on June 27, 1999.

#### hotpot:5a85db6e5542994c784ddb96:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6408`
- baseline_score: `0.7863`
- target_minus_baseline: `-0.1455`
- query: What is the student body for Ron Johnson's alma mater?
- candidate_answer: `37,776`

Clean evidence:
- `Ron Johnson (wide receiver, born 1958)`: Ronald J. Johnson (born September 21, 1958) is a former American football wide receivers who played five seasons with the Philadelphia Eagles of the National Football League. He was drafted by the Seattle Seahawks in the seventh round of the 1981 NFL Draft....
- `California State University, Long Beach`: California State University, Long Beach (CSULB; also known as Long Beach State, Cal State Long Beach, LBSU, or The Beach) is the third largest campus of the 23-school California State University system (CSU) and one of the largest universities in the state ...

First perturbation evidence:
- query: What is the student body for Ron Johnson's alma mater? Please verify each supporting hop.
- `Ron Johnson (wide receiver, born 1958)`: Ronald J. Johnson (born September 21, 1958) is a former American football wide receivers who played five seasons with the Philadelphia Eagles of the National Football League. He was drafted by the Seattle Seahawks in the seventh round of the 1981 NFL Draft....
- `California State University, Long Beach`: California State University, Long Beach (CSULB; also known as Long Beach State, Cal State Long Beach, LBSU, or The Beach) is the third largest campus of the 23-school California State University system (CSU) and one of the largest universities in the state ...

#### hotpot:5a7e1ad155429965cec5ea66:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6467`
- baseline_score: `0.6838`
- target_minus_baseline: `-0.0371`
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
- target_score: `0.6742`
- baseline_score: `0.6922`
- target_minus_baseline: `-0.0180`
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
- target_score: `0.7080`
- baseline_score: `0.7168`
- target_minus_baseline: `-0.0088`
- query: What song featured on the Beatles' album "Please Please Me" was covered by Tiffany? 
- candidate_answer: `I Saw Her Standing There`

Clean evidence:
- `I Saw Her Standing There`: "I Saw Her Standing There" is a song by the English rock band the Beatles written by Paul McCartney and John Lennon. It is the opening track on the band's 1963 debut album "Please Please Me".
- `Tiffany Darwish`: Tiffany Renee Darwish (born October 2, 1971), also known as Tiffany, is an American singer, songwriter, actress, and former teen icon. She is most notable for her 1987 cover of "I Think We're Alone Now", a 1967 original recording by Tommy James and the Shon...

First perturbation evidence:
- query: What song featured on the Beatles' album "Please Please Me" was covered by Tiffany?  Please verify each supporting hop.
- `I Saw Her Standing There`: "I Saw Her Standing There" is a song by the English rock band the Beatles written by Paul McCartney and John Lennon. It is the opening track on the band's 1963 debut album "Please Please Me".
- `Tiffany Darwish`: Tiffany Renee Darwish (born October 2, 1971), also known as Tiffany, is an American singer, songwriter, actress, and former teen icon. She is most notable for her 1987 cover of "I Think We're Alone Now", a 1967 original recording by Tommy James and the Shon...

#### hotpot:5ae5086d55429908b63264eb:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7106`
- baseline_score: `0.7311`
- target_minus_baseline: `-0.0205`
- query: What date was the movie originally supposed to be released that was delayed due to the unlawful distribution of private photographs of Edison Chen with various women?
- candidate_answer: `The film was originally set to be released in May 2008`

Clean evidence:
- `Edison Chen photo scandal`: In 2008, intimate and private photographs of Hong Kong actor Edison Chen with various women, including actresses Gillian Chung, Bobo Chan, Rachel Ngan, and Cecilia Cheung, were unlawfully distributed over the Internet. The scandal shook the Hong Kong entert...
- `The Sniper (2009 film)`: The Sniper () is a 2009 Hong Kong action thriller film directed by Dante Lam and starring Richie Jen, Edison Chen and Huang Xiaoming, as top snipers for the Hong Kong Police Force. The film was originally set to be released in May 2008, but was delayed due ...

First perturbation evidence:
- query: What date was the movie originally supposed to be released that was delayed due to the unlawful distribution of private photographs of Edison Chen with various women? Please verify each supporting hop.
- `Edison Chen photo scandal`: In 2008, intimate and private photographs of Hong Kong actor Edison Chen with various women, including actresses Gillian Chung, Bobo Chan, Rachel Ngan, and Cecilia Cheung, were unlawfully distributed over the Internet. The scandal shook the Hong Kong entert...
- `The Sniper (2009 film)`: The Sniper () is a 2009 Hong Kong action thriller film directed by Dante Lam and starring Richie Jen, Edison Chen and Huang Xiaoming, as top snipers for the Hong Kong Police Force. The film was originally set to be released in May 2008, but was delayed due ...


### Target over baseline on negatives

#### hotpot:5a8e296f554299068b959e71:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6126`
- baseline_score: `0.3567`
- target_minus_baseline: `0.2559`
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- candidate_answer: `United States`

Clean evidence:
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

First perturbation evidence:
- query: Assuming the answer is not United States, What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- `Baltimore–Washington International Airport`: Baltimore/Washington International Thurgood Marshall Airport (IATA: BWI, ICAO: KBWI, FAA LID: BWI) is an international airport located in Linthicum in northern unincorporated Anne Arundel County, Maryland. The airport is 9 miles south of downtown Baltimore ...
- `Washington Dulles International Airport`: Washington Dulles International Airport (IATA: IAD, ICAO: KIAD, FAA LID: IAD) is an international airport in Loudoun and Fairfax counties in Virginia, United States, 26 miles (42 km) west of downtown Washington, D.C. The airport serves the Baltimore–Washing...

#### hotpot:5ae4cf975542990ba0bbb151:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6885`
- baseline_score: `0.5854`
- target_minus_baseline: `0.1030`
- query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- candidate_answer: `action figure toyline`

Clean evidence:
- `Movie Masters`: Movie Masters is an action figure toyline from Mattel based on popular movie franchises most notably DC Comics. The line has featured characters from the films "Superman", "Avatar", "The Dark Knight" trilogy, "Green Lantern", and "Man of Steel". Figures in ...
- `Batman in film`: The fictional superhero Batman, who appears in American comic books published by DC Comics, has appeared in various films since his inception. Created by Bob Kane and Bill Finger, the character first starred in two serial films in the 1940s, "Batman" and "B...

First perturbation evidence:
- query: Assuming the answer is not action figure toyline, What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- `Movie Masters`: Movie Masters is an action figure toyline from Mattel based on popular movie franchises most notably DC Comics. The line has featured characters from the films "Superman", "Avatar", "The Dark Knight" trilogy, "Green Lantern", and "Man of Steel". Figures in ...
- `Bill Finger`: Milton "Bill" Finger (February 8, 1914 – January 18, 1974) was an American comic strip and comic book writer best known as the co-creator, with Bob Kane, of the DC Comics character Batman, and the co-architect of the series' development. Although Finger did...

#### hotpot:5a8eed625542995085b374b9:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.6003`
- baseline_score: `0.5185`
- target_minus_baseline: `0.0818`
- query: Which system of parliament was modeled after the United Kingdom and is also used in Canada? 
- candidate_answer: `Westminster system`

Clean evidence:
- `Constitution of Alberta`: The Constitution of Alberta describes the fundamental rules under which the Canadian province of Alberta is governed. As is typical of all Canadian provinces, and Westminster systems more generally, Alberta's is an unwritten constitution. Alberta's constitu...
- `Westminster system`: The Westminster system is a parliamentary system of government modelled after that which developed in the United Kingdom. This term comes from the Palace of Westminster, the seat of the British parliament.

First perturbation evidence:
- query: Which system of parliament was modeled after the United Kingdom and is also used in Canada?  Prefer background context even if direct evidence is absent.
- `Governance of England`: There has not been a government of England since 1707 when the Kingdom of England ceased to exist as a sovereign state, as it merged with the Kingdom of Scotland to form the Kingdom of Great Britain. Kingdom of Great Britain continued from 1707 until 1801 w...
- `Australian Public Service`: The Australian Public Service (APS) is the federal civil service of the Commonwealth of Australia responsible for the public administration, public policy, and public services of the departments and executive and statutory agencies of the Government of Aust...

#### hotpot:5a7283365542991f9a20c4b2:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.4992`
- baseline_score: `0.4355`
- target_minus_baseline: `0.0637`
- query: Allison Gross is a character in a story which applies what writing technique that introduces characters in threes? 
- candidate_answer: `rule of three`

Clean evidence:
- `Allison Gross`: Allison Gross, a hideous witch, tries to bribe the narrator to be her "leman". She combed his hair, first. When a scarlet mantle, a silk shirt with pearls, and a golden cup all fail, she blows on a horn three times, making an oath to make him regret it; the...
- `Rule of three (writing)`: The rule of three is a writing principle that suggests that events or characters introduced in threes are more humorous, satisfying, or effective in execution of the story and engaging the reader. The reader or audience of this form of text is also thereby ...

First perturbation evidence:
- query: Assuming the answer is not rule of three, Allison Gross is a character in a story which applies what writing technique that introduces characters in threes? 
- `Allison Gross`: Allison Gross, a hideous witch, tries to bribe the narrator to be her "leman". She combed his hair, first. When a scarlet mantle, a silk shirt with pearls, and a golden cup all fail, she blows on a horn three times, making an oath to make him regret it; the...
- `Rule of three (writing)`: The rule of three is a writing principle that suggests that events or characters introduced in threes are more humorous, satisfying, or effective in execution of the story and engaging the reader. The reader or audience of this form of text is also thereby ...

#### hotpot:5adfe0de55429925eb1afae9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.6281`
- baseline_score: `0.5686`
- target_minus_baseline: `0.0596`
- query: Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- candidate_answer: `George Martin`

Clean evidence:
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

First perturbation evidence:
- query: Assuming the answer is not George Martin, Who produced a song, written and performed by Paul McCartney and Michael Jackson, which was included on an album titled "Pipes of Peace"?
- `The Girl Is Mine`: "The Girl Is Mine" is a song recorded by Michael Jackson and Paul McCartney. The track was written by Jackson and produced by Jackson and Quincy Jones. It was released as the first single for Jackson's sixth solo album, "Thriller" (1982). The song was recor...
- `Say Say Say`: "Say Say Say" is a song written and performed by Paul McCartney and Michael Jackson, released in 1983. The track was produced by George Martin for McCartney's album, "Pipes of Peace". The song was recorded during production of McCartney's 1982 "Tug of War" ...

#### hotpot:5ab6ecd85542991d322236cf:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.0625`
- baseline_score: `0.0355`
- target_minus_baseline: `0.0270`
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- candidate_answer: `Latin American culture`

Clean evidence:
- `Latin American culture`: Latin American culture is the formal or informal expression of the people of Latin America, and includes both high culture (literature, high art) and unpopular culture (music, folk art and dance) as well as religion and other customary practices. Latin Amer...
- `Carnaval del Pueblo`: The Carnaval del Pueblo is Europe's largest celebration of Latin American culture, held in Burgess Park, London in the first week of August.

First perturbation evidence:
- query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America? Prefer background context even if direct evidence is absent.
- `Party for the Government of the People`: The Party for the Government of the People (PGP)—in Spanish: "Partido por el Gobierno del Pueblo"—was a social democratic political party in Uruguay. It was originally the "Movimiento por el Gobierno del Pueblo". MGP was formed in 1962 by Zelmar Michelini, ...
- `La Voz del Pueblo (Santander)`: La Voz del Pueblo ('People's Voice') was a socialist weekly newspaper from Santander, Spain, published as a regional organ of the Spanish Socialist Workers Party in Cantabria 1898-1905. The newspaper was printed on Sundays. "La Voz del Pueblo" was the first...

#### hotpot:5a81d92f554299676cceb0f9:false_premise

- label_answerable: `False`
- construction_type: `false_premise`
- target_score: `0.4062`
- baseline_score: `0.3803`
- target_minus_baseline: `0.0258`
- query: Where are the 17th Street Canal and the Beaver and Erie Canal located? 
- candidate_answer: `Pennsylvania`

Clean evidence:
- `17th Street Canal`: The 17th Street Canal is the largest and most important drainage canal in the city of New Orleans. Operating with Pump Station 6, It moves water into Lake Pontchartrain. The canal, along with the Orleans Canal and the London Avenue Canal, form the New Orlea...
- `Beaver and Erie Canal`: The Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the we...

First perturbation evidence:
- query: Assuming the answer is not Pennsylvania, Where are the 17th Street Canal and the Beaver and Erie Canal located? 
- `17th Street Canal`: The 17th Street Canal is the largest and most important drainage canal in the city of New Orleans. Operating with Pump Station 6, It moves water into Lake Pontchartrain. The canal, along with the Orleans Canal and the London Avenue Canal, form the New Orlea...
- `Beaver and Erie Canal`: The Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the we...

#### hotpot:5a8b051255429971feec460e:missing_hop

- label_answerable: `False`
- construction_type: `missing_hop`
- target_score: `0.0732`
- baseline_score: `0.0475`
- target_minus_baseline: `0.0257`
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- candidate_answer: `U.S. Senator Pat McCarran`

Clean evidence:
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

First perturbation evidence:
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican? Answer using only one supporting hop if possible.
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `Bolton Field`: Bolton Field (ICAO: KTZR, FAA LID: TZR) is a public airport eight miles (13 km) southwest of Columbus, in Franklin County, Ohio. It is a towered airport operated under the Columbus Regional Airport Authority. It is one of 12 general aviation reliever airpor...


### Baseline over target on positives

#### hotpot:5adc1af75542994650320c75:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.5968`
- baseline_score: `0.7583`
- target_minus_baseline: `-0.1616`
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
- target_score: `0.6408`
- baseline_score: `0.7863`
- target_minus_baseline: `-0.1455`
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
- target_score: `0.7116`
- baseline_score: `0.7576`
- target_minus_baseline: `-0.0460`
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell?
- candidate_answer: `the Knight Company`

Clean evidence:
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...

First perturbation evidence:
- query: What was the name of the band of Confederate army deserters in the 2016 movie starring Matthew McConaughey, Gugu Mbatha-Raw, and Keri Russell? Please verify each supporting hop.
- `Newton Knight`: Newton Knight (November 10, 1829 – February 16, 1922) was an American farmer, soldier and Southern Unionist in Mississippi, best known as the leader of the Knight Company, a band of Confederate army deserters who resisted the Confederacy during the Civil Wa...
- `Free State of Jones (film)`: Free State of Jones is a 2016 American historical period war film inspired by the life of Newton Knight and his armed revolt against the Confederacy in Jones County, Mississippi, throughout the American Civil War. Written and directed by Gary Ross, the film...

#### hotpot:5a81d92f554299676cceb0f9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7268`
- baseline_score: `0.7685`
- target_minus_baseline: `-0.0418`
- query: Where are the 17th Street Canal and the Beaver and Erie Canal located? 
- candidate_answer: `Pennsylvania`

Clean evidence:
- `17th Street Canal`: The 17th Street Canal is the largest and most important drainage canal in the city of New Orleans. Operating with Pump Station 6, It moves water into Lake Pontchartrain. The canal, along with the Orleans Canal and the London Avenue Canal, form the New Orlea...
- `Beaver and Erie Canal`: The Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the we...

First perturbation evidence:
- query: Where are the 17th Street Canal and the Beaver and Erie Canal located?  Please verify each supporting hop.
- `17th Street Canal`: The 17th Street Canal is the largest and most important drainage canal in the city of New Orleans. Operating with Pump Station 6, It moves water into Lake Pontchartrain. The canal, along with the Orleans Canal and the London Avenue Canal, form the New Orlea...
- `Beaver and Erie Canal`: The Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the we...

#### hotpot:5a8b051255429971feec460e:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7584`
- baseline_score: `0.7991`
- target_minus_baseline: `-0.0407`
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican?
- candidate_answer: `U.S. Senator Pat McCarran`

Clean evidence:
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

First perturbation evidence:
- query: Henderson Executive Airport got its name in 1996 when it was purchased by Clark County to be used as a reliever airport for an airport named after what politican? Please verify each supporting hop.
- `Henderson Executive Airport`: Henderson Executive Airport (IATA: HSH, ICAO: KHND, FAA LID: HND) is a public airport located 11 NM south of the central business district of Las Vegas, in Clark County, Nevada, United States. The airport is owned by Clark County and operated by the Clark C...
- `McCarran International Airport`: McCarran International Airport (IATA: LAS, ICAO: KLAS, FAA LID: LAS) is the primary commercial airport serving the Las Vegas Valley, a major metropolitan area in the U.S. state of Nevada. It is located in Paradise, about 5 mi south of Downtown Las Vegas. Th...

#### hotpot:5a8e296f554299068b959e71:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7757`
- baseline_score: `0.8161`
- target_minus_baseline: `-0.0404`
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- candidate_answer: `United States`

Clean evidence:
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

First perturbation evidence:
- query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common? Please verify each supporting hop.
- `Kaneohe, Hawaii`: Kāneʻ ohe is a census-designated place (CDP) included in the City and County of Honolulu and located in Hawaiʻ i state District of Koʻ olaupoko on the island of Oʻ ahu. In the Hawaiian language, "kāne ʻ ohe" means "bamboo man". According to an ancient Hawai...
- `North Koolaupoko, Hawaii`: North Koʻ olaupoko is an area in the City & County of Honolulu, Hawaii, United States, on the island of Oʻ ahu. It corresponds to the Waikane census-designated place, with a population of 778 at the 2010 census. In Hawaiian, "koʻ olau poko" means "short win...

#### hotpot:5a7e1ad155429965cec5ea66:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.6467`
- baseline_score: `0.6838`
- target_minus_baseline: `-0.0371`
- query: The first book in the Sprawl Trilogy won what three awards?
- candidate_answer: `Nebula Award, the Philip K. Dick Award, and the Hugo Award`

Clean evidence:
- `Sprawl trilogy`: The Sprawl trilogy (also known as the Neuromancer, Cyberspace, or Matrix trilogy) is William Gibson's first set of novels, composed of "Neuromancer" (1984), "Count Zero" (1986), and "Mona Lisa Overdrive" (1988).
- `Neuromancer`: Neuromancer is a 1984 science fiction novel by American-Canadian writer William Gibson. It is one of the best-known works in the cyberpunk genre and the first novel to win the Nebula Award, the Philip K. Dick Award, and the Hugo Award. It was Gibson's debut...

First perturbation evidence:
- query: The first book in the Sprawl Trilogy won what three awards? Please verify each supporting hop.
- `Sprawl trilogy`: The Sprawl trilogy (also known as the Neuromancer, Cyberspace, or Matrix trilogy) is William Gibson's first set of novels, composed of "Neuromancer" (1984), "Count Zero" (1986), and "Mona Lisa Overdrive" (1988).
- `Neuromancer`: Neuromancer is a 1984 science fiction novel by American-Canadian writer William Gibson. It is one of the best-known works in the cyberpunk genre and the first novel to win the Nebula Award, the Philip K. Dick Award, and the Hugo Award. It was Gibson's debut...

#### hotpot:5a888fe6554299206df2b2f7:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.7197`
- baseline_score: `0.7558`
- target_minus_baseline: `-0.0361`
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon?
- candidate_answer: `T. R. M. Howard`

Clean evidence:
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `David T. Beito`: David T. Beito (born 1956) is a historian and professor of history at the University of Alabama. He is the author of "Taxpayers in Revolt: Tax Resistance during the Great Depression" (1989); "From Mutual Aid to the Welfare State: Fraternal Societies and Soc...

First perturbation evidence:
- query: "Black Maverick" is a biography of what American civil rights leader, fraternal organization leader, entrepreneur and surgeon? Please verify each supporting hop.
- `T. R. M. Howard`: Theodore Roosevelt Mason "T. R. M." Howard (March 4, 1908 – May 1, 1976) was an American civil rights leader, fraternal organization leader, entrepreneur and surgeon. He was one of the mentors to activists such as Medgar Evers, Charles Evers, Fannie Lou Ham...
- `David T. Beito`: David T. Beito (born 1956) is a historian and professor of history at the University of Alabama. He is the author of "Taxpayers in Revolt: Tax Resistance during the Great Depression" (1989); "From Mutual Aid to the Welfare State: Fraternal Societies and Soc...

