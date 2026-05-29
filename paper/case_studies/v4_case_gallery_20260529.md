# V4 Case Study Gallery

Generated: `2026-05-29T06:56:05.350870+00:00`

Inputs: `6` failure-analysis files.
Exported cases: `192`.

## Coverage

| Bucket | Cases |
|---|---:|
| baseline_over_target_on_positive | 48 |
| target_high_false_positive | 48 |
| target_low_false_negative | 48 |
| target_over_baseline_on_negative | 48 |

## Construction Types

| Construction type | Cases |
|---|---:|
| conflict | 4 |
| distractor | 8 |
| false_premise | 17 |
| fragile_mixed | 2 |
| hard_missing_hop | 16 |
| missing | 6 |
| missing_hop | 10 |
| near_miss_dilution | 1 |
| semantic_swap | 16 |
| stable | 96 |
| wrong_answer | 16 |

## Representative Cases

### fever_v4_n100_structbalanced / baseline_over_target_on_positive / rank 1

- Orbit: `fever:b695f4e8ca6d6ead33ef6c9177345b1b:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9018`; baseline score: `0.9080`; target-baseline gap: `-0.0062`.
- Query: Determine whether this claim is supported or refuted: The World Trade Center featured one building.
- Candidate answer: REFUTES
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### fever_v4_n100_structbalanced / baseline_over_target_on_positive / rank 2

- Orbit: `fever:419c7444c231c70cf176ce8c678cfe04:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9483`; baseline score: `0.9532`; target-baseline gap: `-0.0049`.
- Query: Determine whether this claim is supported or refuted: Stephen Colbert hosts talk shows.
- Candidate answer: SUPPORTS
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### fever_v4_n100_structbalanced / target_high_false_positive / rank 1

- Orbit: `fever:419c7444c231c70cf176ce8c678cfe04:missing`
- Construction: `missing`; label answerable: `False`.
- Target score: `0.4846`; baseline score: `0.5215`; target-baseline gap: `-0.0370`.
- Query: Determine whether this claim is supported or refuted: Stephen Colbert hosts talk shows.
- Candidate answer: SUPPORTS
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8662

### fever_v4_n100_structbalanced / target_high_false_positive / rank 2

- Orbit: `fever:5fb08243710e06fb61b2d533ba6dde68:missing`
- Construction: `missing`; label answerable: `False`.
- Target score: `0.3099`; baseline score: `0.2740`; target-baseline gap: `0.0359`.
- Query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- Candidate answer: SUPPORTS
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8689

### fever_v4_n100_structbalanced / target_low_false_negative / rank 1

- Orbit: `fever:b695f4e8ca6d6ead33ef6c9177345b1b:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9018`; baseline score: `0.9080`; target-baseline gap: `-0.0062`.
- Query: Determine whether this claim is supported or refuted: The World Trade Center featured one building.
- Candidate answer: REFUTES
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### fever_v4_n100_structbalanced / target_low_false_negative / rank 2

- Orbit: `fever:d8d4b897f4420729c6a9bfb50ef9fe65:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9274`; baseline score: `0.9293`; target-baseline gap: `-0.0019`.
- Query: Determine whether this claim is supported or refuted: Weekly Idol is hosted by Future.
- Candidate answer: REFUTES
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### fever_v4_n100_structbalanced / target_over_baseline_on_negative / rank 1

- Orbit: `fever:5fb08243710e06fb61b2d533ba6dde68:missing`
- Construction: `missing`; label answerable: `False`.
- Target score: `0.3099`; baseline score: `0.2740`; target-baseline gap: `0.0359`.
- Query: Determine whether this claim is supported or refuted: Randy Savage is a professional at a fighting sport.
- Candidate answer: SUPPORTS
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8689

### fever_v4_n100_structbalanced / target_over_baseline_on_negative / rank 2

- Orbit: `fever:1d0ee37d49d54fde9eb4a0c3939f5ec9:distractor`
- Construction: `distractor`; label answerable: `False`.
- Target score: `0.0650`; baseline score: `0.0352`; target-baseline gap: `0.0297`.
- Query: Determine whether this claim is supported or refuted: Southampton F.C. is only a cricket club.
- Candidate answer: REFUTES
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8724

### hotpot_v4_hardneg_n100 / baseline_over_target_on_positive / rank 1

- Orbit: `hotpot_hardneg:5ac213805542992f1f2b37e7:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9532`; baseline score: `0.9582`; target-baseline gap: `-0.0050`.
- Query: When did the animated series Kent Scott wrote end after beginning in September of 2002 on "Nick on CBS"?
- Candidate answer: November
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_hardneg_n100 / baseline_over_target_on_positive / rank 2

- Orbit: `hotpot_hardneg:5adce88b5542992c1e3a249a:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9633`; baseline score: `0.9681`; target-baseline gap: `-0.0048`.
- Query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- Candidate answer: 320 years
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_hardneg_n100 / target_high_false_positive / rank 1

- Orbit: `hotpot_hardneg:5adce88b5542992c1e3a249a:hard_missing_hop`
- Construction: `hard_missing_hop`; label answerable: `False`.
- Target score: `0.1345`; baseline score: `0.1473`; target-baseline gap: `-0.0128`.
- Query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- Candidate answer: 320 years
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7895

### hotpot_v4_hardneg_n100 / target_high_false_positive / rank 2

- Orbit: `hotpot_hardneg:5a881cbb55429938390d3ee7:hard_missing_hop`
- Construction: `hard_missing_hop`; label answerable: `False`.
- Target score: `0.1327`; baseline score: `0.1557`; target-baseline gap: `-0.0230`.
- Query: St. John of the Cross Episcopal Church has a rectory that was in a style that was a product of what earlier style?
- Candidate answer: Hellenism
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7917

### hotpot_v4_hardneg_n100 / target_low_false_negative / rank 1

- Orbit: `hotpot_hardneg:5abd1b6e55429933744ab729:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.8964`; baseline score: `0.8797`; target-baseline gap: `0.0166`.
- Query: Which of the following cities is a county-level city, Jingzhou or Zixing?
- Candidate answer: Zixing
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_hardneg_n100 / target_low_false_negative / rank 2

- Orbit: `hotpot_hardneg:5a79332555429907847277e7:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9440`; baseline score: `0.9365`; target-baseline gap: `0.0075`.
- Query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- Candidate answer: Juan Carlos Onetti
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_hardneg_n100 / target_over_baseline_on_negative / rank 1

- Orbit: `hotpot_hardneg:5a79332555429907847277e7:hard_missing_hop`
- Construction: `hard_missing_hop`; label answerable: `False`.
- Target score: `0.0571`; baseline score: `0.0507`; target-baseline gap: `0.0064`.
- Query: Who died first, Bryce Courtenay or Juan Carlos Onetti?
- Candidate answer: Juan Carlos Onetti
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, retrieval_overlap=0.7143

### hotpot_v4_hardneg_n100 / target_over_baseline_on_negative / rank 2

- Orbit: `hotpot_hardneg:5abd8c295542992ac4f382ab:hard_missing_hop`
- Construction: `hard_missing_hop`; label answerable: `False`.
- Target score: `0.0664`; baseline score: `0.0607`; target-baseline gap: `0.0057`.
- Query:  The Minnesota State High School Mathematics League was founded by a professor at a private coeducational liberal arts college founded in what year? 
- Candidate answer: 1874
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7702

### hotpot_v4_n100_hardmatched / baseline_over_target_on_positive / rank 1

- Orbit: `hotpot:5adc1af75542994650320c75:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.4458`; baseline score: `0.7240`; target-baseline gap: `-0.2783`.
- Query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- Candidate answer: 1998
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7558

### hotpot_v4_n100_hardmatched / baseline_over_target_on_positive / rank 2

- Orbit: `hotpot:5a85db6e5542994c784ddb96:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.4280`; baseline score: `0.6902`; target-baseline gap: `-0.2622`.
- Query: What is the student body for Ron Johnson's alma mater?
- Candidate answer: 37,776
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8148

### hotpot_v4_n100_hardmatched / target_high_false_positive / rank 1

- Orbit: `hotpot:5ae4cf975542990ba0bbb151:missing_hop`
- Construction: `missing_hop`; label answerable: `False`.
- Target score: `0.6931`; baseline score: `0.7010`; target-baseline gap: `-0.0079`.
- Query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- Candidate answer: action figure toyline
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7817

### hotpot_v4_n100_hardmatched / target_high_false_positive / rank 2

- Orbit: `hotpot:5a8e296f554299068b959e71:missing_hop`
- Construction: `missing_hop`; label answerable: `False`.
- Target score: `0.6703`; baseline score: `0.7345`; target-baseline gap: `-0.0642`.
- Query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- Candidate answer: United States
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7183

### hotpot_v4_n100_hardmatched / target_low_false_negative / rank 1

- Orbit: `hotpot:5a85db6e5542994c784ddb96:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.4280`; baseline score: `0.6902`; target-baseline gap: `-0.2622`.
- Query: What is the student body for Ron Johnson's alma mater?
- Candidate answer: 37,776
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8148

### hotpot_v4_n100_hardmatched / target_low_false_negative / rank 2

- Orbit: `hotpot:5adc1af75542994650320c75:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.4458`; baseline score: `0.7240`; target-baseline gap: `-0.2783`.
- Query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- Candidate answer: 1998
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7558

### hotpot_v4_n100_hardmatched / target_over_baseline_on_negative / rank 1

- Orbit: `hotpot:5a810221554299260e20a1f9:false_premise`
- Construction: `false_premise`; label answerable: `False`.
- Target score: `0.4796`; baseline score: `0.1040`; target-baseline gap: `0.3756`.
- Query: Who wrote the 1970 international hit song Murray Head is most recognized for?
- Candidate answer: Andrew Lloyd Webber and Tim Rice
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_n100_hardmatched / target_over_baseline_on_negative / rank 2

- Orbit: `hotpot:5ab6ecd85542991d322236cf:false_premise`
- Construction: `false_premise`; label answerable: `False`.
- Target score: `0.6452`; baseline score: `0.5118`; target-baseline gap: `0.1334`.
- Query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- Candidate answer: Latin American culture
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_n100_structbalanced / baseline_over_target_on_positive / rank 1

- Orbit: `hotpot:5adc1af75542994650320c75:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.5968`; baseline score: `0.7583`; target-baseline gap: `-0.1616`.
- Query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- Candidate answer: 1998
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7558

### hotpot_v4_n100_structbalanced / baseline_over_target_on_positive / rank 2

- Orbit: `hotpot:5a85db6e5542994c784ddb96:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.6408`; baseline score: `0.7863`; target-baseline gap: `-0.1455`.
- Query: What is the student body for Ron Johnson's alma mater?
- Candidate answer: 37,776
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.8148

### hotpot_v4_n100_structbalanced / target_high_false_positive / rank 1

- Orbit: `hotpot:5ab28e2a5542993be8fa9947:missing_hop`
- Construction: `missing_hop`; label answerable: `False`.
- Target score: `0.8051`; baseline score: `0.7976`; target-baseline gap: `0.0075`.
- Query: Who holds the world record for jumping over 6 buses and appeared on the British television series "The Jump"?
- Candidate answer: Eddie "The Eagle" Edwards
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7790

### hotpot_v4_n100_structbalanced / target_high_false_positive / rank 2

- Orbit: `hotpot:5ae4cf975542990ba0bbb151:false_premise`
- Construction: `false_premise`; label answerable: `False`.
- Target score: `0.6885`; baseline score: `0.5854`; target-baseline gap: `0.1030`.
- Query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- Candidate answer: action figure toyline
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7769

### hotpot_v4_n100_structbalanced / target_low_false_negative / rank 1

- Orbit: `hotpot:5ab6ecd85542991d322236cf:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.3882`; baseline score: `0.3347`; target-baseline gap: `0.0535`.
- Query: The Carnaval del Pueblo is Eurpoe's largest celebration of what expression of the people of Latin America?
- Candidate answer: Latin American culture
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_n100_structbalanced / target_low_false_negative / rank 2

- Orbit: `hotpot:5adc1af75542994650320c75:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.5968`; baseline score: `0.7583`; target-baseline gap: `-0.1616`.
- Query: In which year was this single by Cher, written by  Brian Higgins and included in the album The Very Best of Cher, released?
- Candidate answer: 1998
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7558

### hotpot_v4_n100_structbalanced / target_over_baseline_on_negative / rank 1

- Orbit: `hotpot:5a8e296f554299068b959e71:false_premise`
- Construction: `false_premise`; label answerable: `False`.
- Target score: `0.6126`; baseline score: `0.3567`; target-baseline gap: `0.2559`.
- Query: What country does Washington Dulles International Airport and Baltimore–Washington metropolitan area have in common?
- Candidate answer: United States
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.6888

### hotpot_v4_n100_structbalanced / target_over_baseline_on_negative / rank 2

- Orbit: `hotpot:5ae4cf975542990ba0bbb151:false_premise`
- Construction: `false_premise`; label answerable: `False`.
- Target score: `0.6885`; baseline score: `0.5854`; target-baseline gap: `0.1030`.
- Query: What line featured characters from a DC Comic creator by Bob Kane and Bill Finger?
- Candidate answer: action figure toyline
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, perturbation_count=1.0000, mean_missing=0.7769

### hotpot_v4_semanticswap_n100 / baseline_over_target_on_positive / rank 1

- Orbit: `hotpot_semanticswap:5adf3e835542993a75d26442:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.7704`; baseline score: `0.7914`; target-baseline gap: `-0.0210`.
- Query: Which comic series involves characters such as Nick Fury and Baron von Strucker?
- Candidate answer: Marvel
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / baseline_over_target_on_positive / rank 2

- Orbit: `hotpot_semanticswap:5ae1fced5542997283cd230e:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.7845`; baseline score: `0.8012`; target-baseline gap: `-0.0167`.
- Query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- Candidate answer: Naguib Mahfouz
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / target_high_false_positive / rank 1

- Orbit: `hotpot_semanticswap:5a8303c255429954d2e2ec01:semantic_swap`
- Construction: `semantic_swap`; label answerable: `False`.
- Target score: `0.8872`; baseline score: `0.8974`; target-baseline gap: `-0.0102`.
- Query: The Plymouth fury produced from 1955 to 1989  was replaced by what for police and fleet applications?
- Candidate answer: Chrysler K platform
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / target_high_false_positive / rank 2

- Orbit: `hotpot_semanticswap:5ae55b8255429908b63265ef:semantic_swap`
- Construction: `semantic_swap`; label answerable: `False`.
- Target score: `0.8859`; baseline score: `0.8877`; target-baseline gap: `-0.0018`.
- Query: What chef is the owner of a Japanese restaurant in the Tribeca neighborhood and also owns two Bar Masas in New York and Nevada?
- Candidate answer: Masayoshi "Masa" Takayama
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / target_low_false_negative / rank 1

- Orbit: `hotpot_semanticswap:5adf3e835542993a75d26442:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.7704`; baseline score: `0.7914`; target-baseline gap: `-0.0210`.
- Query: Which comic series involves characters such as Nick Fury and Baron von Strucker?
- Candidate answer: Marvel
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / target_low_false_negative / rank 2

- Orbit: `hotpot_semanticswap:5ae1fced5542997283cd230e:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.7845`; baseline score: `0.8012`; target-baseline gap: `-0.0167`.
- Query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- Candidate answer: Naguib Mahfouz
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / target_over_baseline_on_negative / rank 1

- Orbit: `hotpot_semanticswap:5a8ba3ff55429971feec4744:semantic_swap`
- Construction: `semantic_swap`; label answerable: `False`.
- Target score: `0.4979`; baseline score: `0.4224`; target-baseline gap: `0.0756`.
- Query: Stokely Webster has paintings can be found at the official residence of whom?
- Candidate answer: Mayor of the City of New York
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_semanticswap_n100 / target_over_baseline_on_negative / rank 2

- Orbit: `hotpot_semanticswap:5ac31602554299741d48a1bf:semantic_swap`
- Construction: `semantic_swap`; label answerable: `False`.
- Target score: `0.8172`; baseline score: `0.8036`; target-baseline gap: `0.0136`.
- Query: Which of the actress starred in  Zombie Night appeared in the 1998 erotic thriller "Wild Things"?
- Candidate answer: Jennifer Taylor
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_supportpreserve_n100 / baseline_over_target_on_positive / rank 1

- Orbit: `hotpot_supportpreserve:5adce88b5542992c1e3a249a:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9884`; baseline score: `0.9762`; target-baseline gap: `0.0122`.
- Query: How long did the state exist whose army ransacked and looted the city, Halebidu, twice in the 14th century ?
- Candidate answer: 320 years
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_supportpreserve_n100 / baseline_over_target_on_positive / rank 2

- Orbit: `hotpot_supportpreserve:5a792ad055429907847277d1:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9888`; baseline score: `0.9763`; target-baseline gap: `0.0125`.
- Query: What 4-D film attraction at Walt Disney World is based off a 2004 computer-animated Christmas movie? 
- Candidate answer: Mickey's PhilharMagic
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_supportpreserve_n100 / target_high_false_positive / rank 1

- Orbit: `hotpot_supportpreserve:5a764c0b55429976ec32bd89:wrong_answer`
- Construction: `wrong_answer`; label answerable: `False`.
- Target score: `0.0179`; baseline score: `0.0533`; target-baseline gap: `-0.0354`.
- Query: What criteria subjectively qualifies the Houston Astrodome to be called the Eighth Wonder of the World?
- Candidate answer: comparable to the seven Wonders of the World
- Top features: retrieval_overlap=1.0000, orbit_answer_flip_rate=1.0000, perturbation_count=1.0000, mean_missing=0.7707

### hotpot_v4_supportpreserve_n100 / target_high_false_positive / rank 2

- Orbit: `hotpot_supportpreserve:5a80522b5542996402f6a4c1:wrong_answer`
- Construction: `wrong_answer`; label answerable: `False`.
- Target score: `0.0178`; baseline score: `0.0636`; target-baseline gap: `-0.0457`.
- Query: What population ranking is the Oklahoma city located south of a wilderness area spanning over 5000 acres?
- Candidate answer: fifth-largest
- Top features: retrieval_overlap=1.0000, orbit_answer_flip_rate=1.0000, perturbation_count=1.0000, mean_missing=0.7517

### hotpot_v4_supportpreserve_n100 / target_low_false_negative / rank 1

- Orbit: `hotpot_supportpreserve:5ae1fced5542997283cd230e:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9878`; baseline score: `0.9718`; target-baseline gap: `0.0160`.
- Query: Which writer won the Nobel Prize, William H. Gass or Naguib Mahfouz?
- Candidate answer: Naguib Mahfouz
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_supportpreserve_n100 / target_low_false_negative / rank 2

- Orbit: `hotpot_supportpreserve:5ae25d2b554299495565da46:stable`
- Construction: `stable`; label answerable: `True`.
- Target score: `0.9880`; baseline score: `0.9726`; target-baseline gap: `0.0154`.
- Query: Who has more singles titles, Brian Gottfried or Peter Fleming?
- Candidate answer: 21
- Top features: answer_consistency=1.0000, support_signature_consistency=1.0000, retrieval_overlap=1.0000, perturbation_count=1.0000

### hotpot_v4_supportpreserve_n100 / target_over_baseline_on_negative / rank 1

- Orbit: `hotpot_supportpreserve:5ab90fdd55429916710eb0fc:wrong_answer`
- Construction: `wrong_answer`; label answerable: `False`.
- Target score: `0.0041`; baseline score: `0.0020`; target-baseline gap: `0.0021`.
- Query: Wheelock Whitney is just one member of the Whitney Family. Where did this American family originate from?
- Candidate answer: London, England
- Top features: retrieval_overlap=1.0000, orbit_answer_flip_rate=1.0000, perturbation_count=1.0000, mean_missing=0.8077

### hotpot_v4_supportpreserve_n100 / target_over_baseline_on_negative / rank 2

- Orbit: `hotpot_supportpreserve:5ac26ac15542992f1f2b38bc:wrong_answer`
- Construction: `wrong_answer`; label answerable: `False`.
- Target score: `0.0032`; baseline score: `0.0013`; target-baseline gap: `0.0019`.
- Query: Who is the film dedicated to that Paramount Classics and MTV Films co-purchased the rights to?
- Candidate answer: Sam Phillips
- Top features: retrieval_overlap=1.0000, orbit_answer_flip_rate=1.0000, perturbation_count=1.0000, mean_missing=0.8225

## Claim Boundary

This gallery is a paper-facing diagnostic artifact exported from private-label v4 failure analyses. It is useful for selecting qualitative examples, but it is not human-adjudicated evidence and must not be used as a substitute for human audit v4.
