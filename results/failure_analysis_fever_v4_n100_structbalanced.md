# V4 Failure Analysis

Seed: `31`

## Metrics

| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |
|---|---:|---:|---:|---:|---:|
| target | 1.0000 | 0.0000 | 0.0476 | 0.9705 | 0.0425 |
| baseline_calibrated_logistic_orbit | 1.0000 | 0.0000 | 0.0476 | 0.9717 | 0.0404 |

## Construction Types

| Type | n | positive | negative | target mean | baseline mean | target-baseline |
|---|---:|---:|---:|---:|---:|---:|
| conflict | 5 | 0 | 5 | 0.0015 | 0.0014 | 0.0001 |
| distractor | 2 | 0 | 2 | 0.0332 | 0.0178 | 0.0153 |
| fragile_mixed | 5 | 0 | 5 | 0.0006 | 0.0004 | 0.0002 |
| missing | 5 | 0 | 5 | 0.1627 | 0.1604 | 0.0024 |
| near_miss_dilution | 4 | 0 | 4 | 0.0006 | 0.0004 | 0.0002 |
| stable | 20 | 20 | 0 | 0.9705 | 0.9717 | -0.0012 |

## Largest Feature Gaps

| Feature | positive mean | negative mean | gap |
|---|---:|---:|---:|
| retrieval_overlap | 1.0000 | 0.3993 | 0.6007 |
| verifier_entropy | 0.1833 | 0.1208 | 0.0625 |
| clean_to_worst_gap | 0.0017 | 0.0403 | -0.0386 |
| min_sufficiency | 0.0464 | 0.0094 | 0.0370 |
| naive_orbit_average | 0.0472 | 0.0295 | 0.0177 |
| mean_sufficiency | 0.0472 | 0.0295 | 0.0177 |
| mean_missing | 0.8626 | 0.8679 | -0.0053 |
| context_sufficiency_clean | 0.0481 | 0.0496 | -0.0016 |
| clean_sufficiency | 0.0481 | 0.0496 | -0.0016 |
| sufficiency_variance | 0.0000 | 0.0006 | -0.0006 |
| corm_max_clean | 0.5000 | 0.5000 | 0.0000 |
| corm_mean_clean | 0.5000 | 0.5000 | 0.0000 |

## Case Gallery


### High-scoring false positives

#### fever:419c7444c231c70cf176ce8c678cfe04:missing

- label_answerable: `False`
- construction_type: `missing`
- target_score: `0.4846`
- baseline_score: `0.5215`
- target_minus_baseline: `-0.0370`
- query: Determine whether this claim is supported or refuted: Stephen Colbert hosts talk shows.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `The Colbert Report`: Furthermore , the show satirized conservative personality-driven political talk programs , particularly Fox News 's The O'Reilly Factor .

First perturbation evidence:
- query: Fact-check the claim with incomplete evidence if possible: Stephen Colbert hosts talk shows.
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:5fb08243710e06fb61b2d533ba6dde68:missing

- label_answerable: `False`
- construction_type: `missing`
- target_score: `0.3099`
- baseline_score: `0.2740`
- target_minus_baseline: `0.0359`
- query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

First perturbation evidence:
- query: Fact-check the claim with incomplete evidence if possible: Randy Savage is a professional at a fighting sport.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:1d0ee37d49d54fde9eb4a0c3939f5ec9:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.0650`
- baseline_score: `0.0352`
- target_minus_baseline: `0.0297`
- query: Determine whether this claim is supported or refuted: Southampton F.C. is only a cricket club.
- candidate_answer: `REFUTES`

Clean evidence:
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Fact-check the claim using only background evidence if direct evidence is absent: Southampton F.C. is only a cricket club.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:dc1923d6c06e0387b37b6d1d6f4c5876:missing

- label_answerable: `False`
- construction_type: `missing`
- target_score: `0.0187`
- baseline_score: `0.0061`
- target_minus_baseline: `0.0126`
- query: Determine whether this claim is supported or refuted: Avenged Sevenfold is by a British band.
- candidate_answer: `REFUTES`

Clean evidence:
- `Avenged Sevenfold (album)`: Avenged Sevenfold is the eponymous fourth studio album by American heavy metal band Avenged Sevenfold , released on October 30 , 2007 by Warner Bros. .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Fact-check the claim with incomplete evidence if possible: Avenged Sevenfold is by a British band.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:419c7444c231c70cf176ce8c678cfe04:conflict

- label_answerable: `False`
- construction_type: `conflict`
- target_score: `0.0029`
- baseline_score: `0.0031`
- target_minus_baseline: `-0.0003`
- query: Determine whether this claim is supported or refuted: Stephen Colbert hosts talk shows.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `The Colbert Report`: Furthermore , the show satirized conservative personality-driven political talk programs , particularly Fox News 's The O'Reilly Factor .

First perturbation evidence:
- query: Assuming the evidence may indicate REFUTES, fact-check this claim: Stephen Colbert hosts talk shows.
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .
- `Ian Brennan (writer)`: He is best known for his work on the American television shows Glee and Scream Queens .

#### fever:5fb08243710e06fb61b2d533ba6dde68:conflict

- label_answerable: `False`
- construction_type: `conflict`
- target_score: `0.0027`
- baseline_score: `0.0027`
- target_minus_baseline: `-0.0000`
- query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

First perturbation evidence:
- query: Assuming the evidence may indicate REFUTES, fact-check this claim: Randy Savage is a professional at a fighting sport.
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .
- `Ian Brennan (writer)`: He is best known for his work on the American television shows Glee and Scream Queens .

#### fever:d8d4b897f4420729c6a9bfb50ef9fe65:fragile_mixed

- label_answerable: `False`
- construction_type: `fragile_mixed`
- target_score: `0.0024`
- baseline_score: `0.0017`
- target_minus_baseline: `0.0007`
- query: Determine whether this claim is supported or refuted: Weekly Idol is hosted by Future.
- candidate_answer: `REFUTES`

Clean evidence:
- `Weekly Idol`: The show is hosted by comedian Jeong Hyeong-don and rapper Defconn .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Assuming the evidence may indicate SUPPORTS, fact-check this claim: Weekly Idol is hosted by Future.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .

#### fever:25dc4f70725e49253af408b42070e0c8:conflict

- label_answerable: `False`
- construction_type: `conflict`
- target_score: `0.0019`
- baseline_score: `0.0012`
- target_minus_baseline: `0.0007`
- query: Determine whether this claim is supported or refuted: Girl is by at least one singer.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .
- `Come Get It Bae`: `` Come Get It Bae '' is a song written , produced , and performed by American singer and songwriter Pharrell Williams from his second studio album Girl -LRB- 2014 -RRB- .

First perturbation evidence:
- query: Assuming the evidence may indicate REFUTES, fact-check this claim: Girl is by at least one singer.
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .
- `Ian Brennan (writer)`: He is best known for his work on the American television shows Glee and Scream Queens .


### Low-scoring false negatives

#### fever:b695f4e8ca6d6ead33ef6c9177345b1b:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9018`
- baseline_score: `0.9080`
- target_minus_baseline: `-0.0062`
- query: Determine whether this claim is supported or refuted: The World Trade Center featured one building.
- candidate_answer: `REFUTES`

Clean evidence:
- `World Trade Center (1973–2001)`: It featured landmark twin towers , which opened on April 4 , 1973 , and were destroyed as a result of the September 11 attacks .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: The World Trade Center featured one building.
- `World Trade Center (1973–2001)`: It featured landmark twin towers , which opened on April 4 , 1973 , and were destroyed as a result of the September 11 attacks .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:d8d4b897f4420729c6a9bfb50ef9fe65:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9274`
- baseline_score: `0.9293`
- target_minus_baseline: `-0.0019`
- query: Determine whether this claim is supported or refuted: Weekly Idol is hosted by Future.
- candidate_answer: `REFUTES`

Clean evidence:
- `Weekly Idol`: The show is hosted by comedian Jeong Hyeong-don and rapper Defconn .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Weekly Idol is hosted by Future.
- `Weekly Idol`: The show is hosted by comedian Jeong Hyeong-don and rapper Defconn .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:c0182fa98dd12d789469371a6f112945:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9316`
- baseline_score: `0.9348`
- target_minus_baseline: `-0.0032`
- query: Determine whether this claim is supported or refuted: Janelle Monáe is a tomato.
- candidate_answer: `REFUTES`

Clean evidence:
- `Janelle Monáe`: Janelle Monáe Robinson -LRB- born December 1 , 1985 -RRB- -LRB- -LSB- dʒəˈnɛl_moʊˈneɪ -RSB- -RRB- is an American singer , songwriter , actress , and model signed to her own imprint , Wondaland Arts Society , and Atlantic Records .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Janelle Monáe is a tomato.
- `Janelle Monáe`: Janelle Monáe Robinson -LRB- born December 1 , 1985 -RRB- -LRB- -LSB- dʒəˈnɛl_moʊˈneɪ -RSB- -RRB- is an American singer , songwriter , actress , and model signed to her own imprint , Wondaland Arts Society , and Atlantic Records .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:25dc4f70725e49253af408b42070e0c8:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9430`
- baseline_score: `0.9448`
- target_minus_baseline: `-0.0018`
- query: Determine whether this claim is supported or refuted: Girl is by at least one singer.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .
- `Come Get It Bae`: `` Come Get It Bae '' is a song written , produced , and performed by American singer and songwriter Pharrell Williams from his second studio album Girl -LRB- 2014 -RRB- .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Girl is by at least one singer.
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .
- `Come Get It Bae`: `` Come Get It Bae '' is a song written , produced , and performed by American singer and songwriter Pharrell Williams from his second studio album Girl -LRB- 2014 -RRB- .

#### fever:4ba8157c90daf69a2d3cf7a755ca29aa:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9430`
- baseline_score: `0.9448`
- target_minus_baseline: `-0.0018`
- query: Determine whether this claim is supported or refuted: John Krasinski is a car.
- candidate_answer: `REFUTES`

Clean evidence:
- `John Krasinski`: His film credits include Away We Go -LRB- 2009 -RRB- , Leatherheads -LRB- 2008 -RRB- , License to Wed -LRB- 2007 -RRB- , Big Miracle -LRB- 2012 -RRB- , Something Borrowed -LRB- 2011 -RRB- , It 's Complicated -LRB- 2009 -RRB- , Promised Land -LRB- 2012 -RRB-...
- `Aloha (film)`: The film , starring Bradley Cooper , Emma Stone , Rachel McAdams , Bill Murray , John Krasinski , Danny McBride , and Alec Baldwin , was released on May 29 , 2015 .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: John Krasinski is a car.
- `John Krasinski`: His film credits include Away We Go -LRB- 2009 -RRB- , Leatherheads -LRB- 2008 -RRB- , License to Wed -LRB- 2007 -RRB- , Big Miracle -LRB- 2012 -RRB- , Something Borrowed -LRB- 2011 -RRB- , It 's Complicated -LRB- 2009 -RRB- , Promised Land -LRB- 2012 -RRB-...
- `Aloha (film)`: The film , starring Bradley Cooper , Emma Stone , Rachel McAdams , Bill Murray , John Krasinski , Danny McBride , and Alec Baldwin , was released on May 29 , 2015 .

#### fever:419c7444c231c70cf176ce8c678cfe04:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9483`
- baseline_score: `0.9532`
- target_minus_baseline: `-0.0049`
- query: Determine whether this claim is supported or refuted: Stephen Colbert hosts talk shows.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `The Colbert Report`: Furthermore , the show satirized conservative personality-driven political talk programs , particularly Fox News 's The O'Reilly Factor .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Stephen Colbert hosts talk shows.
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `The Colbert Report`: Furthermore , the show satirized conservative personality-driven political talk programs , particularly Fox News 's The O'Reilly Factor .

#### fever:1d0ee37d49d54fde9eb4a0c3939f5ec9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9504`
- baseline_score: `0.9535`
- target_minus_baseline: `-0.0031`
- query: Determine whether this claim is supported or refuted: Southampton F.C. is only a cricket club.
- candidate_answer: `REFUTES`

Clean evidence:
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Southampton F.C. is only a cricket club.
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:5fb08243710e06fb61b2d533ba6dde68:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9529`
- baseline_score: `0.9557`
- target_minus_baseline: `-0.0028`
- query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Randy Savage is a professional at a fighting sport.
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .


### Target over baseline on negatives

#### fever:5fb08243710e06fb61b2d533ba6dde68:missing

- label_answerable: `False`
- construction_type: `missing`
- target_score: `0.3099`
- baseline_score: `0.2740`
- target_minus_baseline: `0.0359`
- query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

First perturbation evidence:
- query: Fact-check the claim with incomplete evidence if possible: Randy Savage is a professional at a fighting sport.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:1d0ee37d49d54fde9eb4a0c3939f5ec9:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.0650`
- baseline_score: `0.0352`
- target_minus_baseline: `0.0297`
- query: Determine whether this claim is supported or refuted: Southampton F.C. is only a cricket club.
- candidate_answer: `REFUTES`

Clean evidence:
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Fact-check the claim using only background evidence if direct evidence is absent: Southampton F.C. is only a cricket club.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:dc1923d6c06e0387b37b6d1d6f4c5876:missing

- label_answerable: `False`
- construction_type: `missing`
- target_score: `0.0187`
- baseline_score: `0.0061`
- target_minus_baseline: `0.0126`
- query: Determine whether this claim is supported or refuted: Avenged Sevenfold is by a British band.
- candidate_answer: `REFUTES`

Clean evidence:
- `Avenged Sevenfold (album)`: Avenged Sevenfold is the eponymous fourth studio album by American heavy metal band Avenged Sevenfold , released on October 30 , 2007 by Warner Bros. .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Fact-check the claim with incomplete evidence if possible: Avenged Sevenfold is by a British band.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:d26a12b4429d8dfa13442ef3750c3d3b:distractor

- label_answerable: `False`
- construction_type: `distractor`
- target_score: `0.0013`
- baseline_score: `0.0004`
- target_minus_baseline: `0.0009`
- query: Determine whether this claim is supported or refuted: Kenneth Lonergan is the director of Pacific Rim.
- candidate_answer: `REFUTES`

Clean evidence:
- `Kenneth Lonergan`: Kenneth Lonergan -LRB- born October 16 , 1962 -RRB- is an American playwright , screenwriter , and director .
- `Pacific Rim (film)`: Pacific Rim is a 2013 American science fiction monster film directed by Guillermo del Toro , and starring Charlie Hunnam , Idris Elba , Rinko Kikuchi , Charlie Day , Burn Gorman , Robert Kazinsky , Max Martini and Ron Perlman .

First perturbation evidence:
- query: Fact-check the claim using only background evidence if direct evidence is absent: Kenneth Lonergan is the director of Pacific Rim.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:25dc4f70725e49253af408b42070e0c8:conflict

- label_answerable: `False`
- construction_type: `conflict`
- target_score: `0.0019`
- baseline_score: `0.0012`
- target_minus_baseline: `0.0007`
- query: Determine whether this claim is supported or refuted: Girl is by at least one singer.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .
- `Come Get It Bae`: `` Come Get It Bae '' is a song written , produced , and performed by American singer and songwriter Pharrell Williams from his second studio album Girl -LRB- 2014 -RRB- .

First perturbation evidence:
- query: Assuming the evidence may indicate REFUTES, fact-check this claim: Girl is by at least one singer.
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .
- `Ian Brennan (writer)`: He is best known for his work on the American television shows Glee and Scream Queens .

#### fever:1d0ee37d49d54fde9eb4a0c3939f5ec9:near_miss_dilution

- label_answerable: `False`
- construction_type: `near_miss_dilution`
- target_score: `0.0018`
- baseline_score: `0.0011`
- target_minus_baseline: `0.0007`
- query: Determine whether this claim is supported or refuted: Southampton F.C. is only a cricket club.
- candidate_answer: `REFUTES`

Clean evidence:
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Southampton F.C. is only a cricket club.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .

#### fever:d8d4b897f4420729c6a9bfb50ef9fe65:fragile_mixed

- label_answerable: `False`
- construction_type: `fragile_mixed`
- target_score: `0.0024`
- baseline_score: `0.0017`
- target_minus_baseline: `0.0007`
- query: Determine whether this claim is supported or refuted: Weekly Idol is hosted by Future.
- candidate_answer: `REFUTES`

Clean evidence:
- `Weekly Idol`: The show is hosted by comedian Jeong Hyeong-don and rapper Defconn .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Assuming the evidence may indicate SUPPORTS, fact-check this claim: Weekly Idol is hosted by Future.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .

#### fever:c1d92c0f60eb777c06a68ee38ec7c717:missing

- label_answerable: `False`
- construction_type: `missing`
- target_score: `0.0003`
- baseline_score: `0.0001`
- target_minus_baseline: `0.0002`
- query: Determine whether this claim is supported or refuted: Michigan is the largest country by total area east of the Mississippi River.
- candidate_answer: `REFUTES`

Clean evidence:
- `Michigan`: Michigan is the tenth most populous of the 50 United States , with the 11th most extensive total area -LRB- the largest state by total area east of the Mississippi River -RRB- .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Fact-check the claim with incomplete evidence if possible: Michigan is the largest country by total area east of the Mississippi River.
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .


### Baseline over target on positives

#### fever:b695f4e8ca6d6ead33ef6c9177345b1b:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9018`
- baseline_score: `0.9080`
- target_minus_baseline: `-0.0062`
- query: Determine whether this claim is supported or refuted: The World Trade Center featured one building.
- candidate_answer: `REFUTES`

Clean evidence:
- `World Trade Center (1973–2001)`: It featured landmark twin towers , which opened on April 4 , 1973 , and were destroyed as a result of the September 11 attacks .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: The World Trade Center featured one building.
- `World Trade Center (1973–2001)`: It featured landmark twin towers , which opened on April 4 , 1973 , and were destroyed as a result of the September 11 attacks .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:419c7444c231c70cf176ce8c678cfe04:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9483`
- baseline_score: `0.9532`
- target_minus_baseline: `-0.0049`
- query: Determine whether this claim is supported or refuted: Stephen Colbert hosts talk shows.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `The Colbert Report`: Furthermore , the show satirized conservative personality-driven political talk programs , particularly Fox News 's The O'Reilly Factor .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Stephen Colbert hosts talk shows.
- `Stephen Colbert`: Following The Daily Shows news-parody concept , The Colbert Report was a parody of personality-driven political opinion shows including The O'Reilly Factor , in which he portrayed a caricatured version of conservative political pundits .
- `The Colbert Report`: Furthermore , the show satirized conservative personality-driven political talk programs , particularly Fox News 's The O'Reilly Factor .

#### fever:c0182fa98dd12d789469371a6f112945:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9316`
- baseline_score: `0.9348`
- target_minus_baseline: `-0.0032`
- query: Determine whether this claim is supported or refuted: Janelle Monáe is a tomato.
- candidate_answer: `REFUTES`

Clean evidence:
- `Janelle Monáe`: Janelle Monáe Robinson -LRB- born December 1 , 1985 -RRB- -LRB- -LSB- dʒəˈnɛl_moʊˈneɪ -RSB- -RRB- is an American singer , songwriter , actress , and model signed to her own imprint , Wondaland Arts Society , and Atlantic Records .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Janelle Monáe is a tomato.
- `Janelle Monáe`: Janelle Monáe Robinson -LRB- born December 1 , 1985 -RRB- -LRB- -LSB- dʒəˈnɛl_moʊˈneɪ -RSB- -RRB- is an American singer , songwriter , actress , and model signed to her own imprint , Wondaland Arts Society , and Atlantic Records .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:1d0ee37d49d54fde9eb4a0c3939f5ec9:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9504`
- baseline_score: `0.9535`
- target_minus_baseline: `-0.0031`
- query: Determine whether this claim is supported or refuted: Southampton F.C. is only a cricket club.
- candidate_answer: `REFUTES`

Clean evidence:
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Southampton F.C. is only a cricket club.
- `Southampton F.C.`: Southampton Football Club -LSB- saʊθˈæmptən , _ - hæmptən -RSB- is a professional association football club based in Southampton , Hampshire , England , which plays in the Premier League , the top tier of English football .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:5fb08243710e06fb61b2d533ba6dde68:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9529`
- baseline_score: `0.9557`
- target_minus_baseline: `-0.0028`
- query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Randy Savage is a professional at a fighting sport.
- `Randy Savage`: Savage is widely regarded as one of the greatest professional wrestlers in history ; a number of peers have ranked Savage among the industry 's top performers of all time .
- `Marvel vs. Capcom-COLON- Infinite`: Marvel vs. Capcom : Infinite is an upcoming fighting video game in development by Capcom .

#### fever:d8d4b897f4420729c6a9bfb50ef9fe65:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9274`
- baseline_score: `0.9293`
- target_minus_baseline: `-0.0019`
- query: Determine whether this claim is supported or refuted: Weekly Idol is hosted by Future.
- candidate_answer: `REFUTES`

Clean evidence:
- `Weekly Idol`: The show is hosted by comedian Jeong Hyeong-don and rapper Defconn .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Weekly Idol is hosted by Future.
- `Weekly Idol`: The show is hosted by comedian Jeong Hyeong-don and rapper Defconn .
- `Tata Motors`: Tata Motors is listed on the -LRB- BSE -RRB- Bombay Stock Exchange , where it is a constituent of the BSE SENSEX index , the National Stock Exchange of India , and the New York Stock Exchange .

#### fever:25dc4f70725e49253af408b42070e0c8:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9430`
- baseline_score: `0.9448`
- target_minus_baseline: `-0.0018`
- query: Determine whether this claim is supported or refuted: Girl is by at least one singer.
- candidate_answer: `SUPPORTS`

Clean evidence:
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .
- `Come Get It Bae`: `` Come Get It Bae '' is a song written , produced , and performed by American singer and songwriter Pharrell Williams from his second studio album Girl -LRB- 2014 -RRB- .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: Girl is by at least one singer.
- `Girl (Pharrell Williams album)`: Follow-up singles `` Marilyn Monroe '' , `` Come Get It Bae '' and `` Gust of Wind '' have achieved moderate success .
- `Come Get It Bae`: `` Come Get It Bae '' is a song written , produced , and performed by American singer and songwriter Pharrell Williams from his second studio album Girl -LRB- 2014 -RRB- .

#### fever:4ba8157c90daf69a2d3cf7a755ca29aa:stable

- label_answerable: `True`
- construction_type: `stable`
- target_score: `0.9430`
- baseline_score: `0.9448`
- target_minus_baseline: `-0.0018`
- query: Determine whether this claim is supported or refuted: John Krasinski is a car.
- candidate_answer: `REFUTES`

Clean evidence:
- `John Krasinski`: His film credits include Away We Go -LRB- 2009 -RRB- , Leatherheads -LRB- 2008 -RRB- , License to Wed -LRB- 2007 -RRB- , Big Miracle -LRB- 2012 -RRB- , Something Borrowed -LRB- 2011 -RRB- , It 's Complicated -LRB- 2009 -RRB- , Promised Land -LRB- 2012 -RRB-...
- `Aloha (film)`: The film , starring Bradley Cooper , Emma Stone , Rachel McAdams , Bill Murray , John Krasinski , Danny McBride , and Alec Baldwin , was released on May 29 , 2015 .

First perturbation evidence:
- query: Using only the evidence, fact-check this claim: John Krasinski is a car.
- `John Krasinski`: His film credits include Away We Go -LRB- 2009 -RRB- , Leatherheads -LRB- 2008 -RRB- , License to Wed -LRB- 2007 -RRB- , Big Miracle -LRB- 2012 -RRB- , Something Borrowed -LRB- 2011 -RRB- , It 's Complicated -LRB- 2009 -RRB- , Promised Land -LRB- 2012 -RRB-...
- `Aloha (film)`: The film , starring Bradley Cooper , Emma Stone , Rachel McAdams , Bill Murray , John Krasinski , Danny McBride , and Alec Baldwin , was released on May 29 , 2015 .

