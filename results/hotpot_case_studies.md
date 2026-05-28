# Case Studies

Input: `results\hotpot_orbits_corm_800.jsonl`

Thresholds at 30% coverage:

- `corm_max_clean`: 0.952782
- `single_set_sure_style`: 0.523333
- `naive_orbit_average`: 0.523333
- `csrm`: 0.699083

## naive_false_accept_csrm_reject

### hotpot:5ab9aed855429970cfb8eb6d:false_premise

- Split: `hotpot_false_premise`
- Label answerable: `False`
- Answer: `no`
- Scores: corm_max_clean=0.9005, csrm=0.5263, naive_orbit_average=0.5450, single_set_sure_style=0.5633
- Clean query: Do the bands named Phoenix and Shearwater specialize in the exact same genre?
- First perturbation: Assuming the answer is not no, Do the bands named Phoenix and Shearwater specialize in the exact same genre?
- First perturbation support key: `Phoenix (band)|Shearwater (band):false_premise`

### hotpot:5a8888e35542997e5c09a5f6:false_premise

- Split: `hotpot_false_premise`
- Label answerable: `False`
- Answer: `Smithfield, Rhode Island`
- Scores: corm_max_clean=0.9871, csrm=0.5260, naive_orbit_average=0.5400, single_set_sure_style=0.5533
- Clean query: In what town is the university which the Bryant Bulldogs represent?
- First perturbation: Assuming the answer is not Smithfield, Rhode Island, In what town is the university which the Bryant Bulldogs represent?
- First perturbation support key: `Bryant Bulldogs women's basketball|Bryant University:false_premise`

### hotpot:5ac2546a554299636651997b:false_premise

- Split: `hotpot_false_premise`
- Label answerable: `False`
- Answer: `Motion City Soundtrack`
- Scores: corm_max_clean=0.9195, csrm=0.5598, naive_orbit_average=0.5633, single_set_sure_style=0.5633
- Clean query: Who has released more studio albums, Candlelight Red or Motion City Soundtrack?
- First perturbation: Assuming the answer is not Motion City Soundtrack, Who has released more studio albums, Candlelight Red or Motion City Soundtrack?
- First perturbation support key: `Candlelight Red|Motion City Soundtrack:false_premise`

## corm_false_accept_csrm_reject

### hotpot:5a8ad2f3554299515336138d:distractor

- Split: `hotpot_distractor`
- Label answerable: `False`
- Answer: `Art of Dying`
- Scores: corm_max_clean=0.9893, csrm=0.2428, naive_orbit_average=0.2804, single_set_sure_style=0.5233
- Clean query: Vices and Virtues, coincidentally released just four days after "Vices & Virtues" by Las Vegas band Panic! at the Disco, was the second studio album by which Canadian rock band?
- First perturbation: Vices and Virtues, coincidentally released just four days after "Vices & Virtues" by Las Vegas band Panic! at the Disco, was the second studio album by which Canadian rock band? Prefer background context even if direct evidence is absent.
- First perturbation support key: `distractor_only`

### hotpot:5a89dd4d554299669944a5e3:distractor

- Split: `hotpot_distractor`
- Label answerable: `False`
- Answer: `Blue Grass Airport`
- Scores: corm_max_clean=0.9883, csrm=0.2428, naive_orbit_average=0.2804, single_set_sure_style=0.5233
- Clean query: Flower Alley was bred by the trainer who was killed at what Fayette County, Kentucky airport?
- First perturbation: Flower Alley was bred by the trainer who was killed at what Fayette County, Kentucky airport? Prefer background context even if direct evidence is absent.
- First perturbation support key: `distractor_only`

### hotpot:5a74684655429929fddd8410:distractor

- Split: `hotpot_distractor`
- Label answerable: `False`
- Answer: `Janet Damita Jo Jackson`
- Scores: corm_max_clean=0.9876, csrm=0.2428, naive_orbit_average=0.2804, single_set_sure_style=0.5233
- Clean query: Which American music star appeared as a guest in a Will & Grace episode called "Back Up, Dancer"?
- First perturbation: Which American music star appeared as a guest in a Will & Grace episode called "Back Up, Dancer"? Prefer background context even if direct evidence is absent.
- First perturbation support key: `distractor_only`

## csrm_true_accept

### hotpot:5adf39295542992d7e9f92df:stable

- Split: `hotpot_stable_support`
- Label answerable: `True`
- Answer: `Apium`
- Scores: corm_max_clean=0.5935, csrm=0.7598, naive_orbit_average=0.5633, single_set_sure_style=0.5633
- Clean query: Which genus has more species, Apium or Elodea?
- First perturbation: Which genus has more species, Apium or Elodea? Please verify each supporting hop.
- First perturbation support key: `Apium|Elodea`

### hotpot:5a893fc855429951533612f0:stable

- Split: `hotpot_stable_support`
- Label answerable: `True`
- Answer: `no`
- Scores: corm_max_clean=0.8597, csrm=0.7481, naive_orbit_average=0.5600, single_set_sure_style=0.5633
- Clean query: Are the Chien Français Blanc et Orange and Cretan Hound both used for hunting in packs?
- First perturbation: Are the Chien Français Blanc et Orange and Cretan Hound both used for hunting in packs? Please verify each supporting hop.
- First perturbation support key: `Chien Français Blanc et Orange|Cretan Hound`

### hotpot:5ab310bb554299233954fef9:stable

- Split: `hotpot_stable_support`
- Label answerable: `True`
- Answer: `John le Carré`
- Scores: corm_max_clean=0.6318, csrm=0.7473, naive_orbit_average=0.5633, single_set_sure_style=0.5633
- Clean query: Which author found inspiration in their career prior to writing, Hart Crane or John le Carré?
- First perturbation: Which author found inspiration in their career prior to writing, Hart Crane or John le Carré? Please verify each supporting hop.
- First perturbation support key: `Hart Crane|John le Carré`

## csrm_false_accept_failure

### hotpot:5adf39295542992d7e9f92df:missing_hop

- Split: `hotpot_missing_hop`
- Label answerable: `False`
- Answer: `Apium`
- Scores: corm_max_clean=0.5935, csrm=0.7403, naive_orbit_average=0.5527, single_set_sure_style=0.5633
- Clean query: Which genus has more species, Apium or Elodea?
- First perturbation: Which genus has more species, Apium or Elodea? Answer using only one supporting hop if possible.
- First perturbation support key: `Apium|Elodea`

### hotpot:5a7ae2f2554299042af8f6aa:missing_hop

- Split: `hotpot_missing_hop`
- Label answerable: `False`
- Answer: `football`
- Scores: corm_max_clean=0.9605, csrm=0.7260, naive_orbit_average=0.5400, single_set_sure_style=0.5533
- Clean query: Which sport has been played at the BayArena in Leverkusen, Germany, since 1958?
- First perturbation: Which sport has been played at the BayArena in Leverkusen, Germany, since 1958? Answer using only one supporting hop if possible.
- First perturbation support key: `BayArena|Bayer 04 Leverkusen`

### hotpot:5ab499a55542996a3a969f9f:missing_hop

- Split: `hotpot_missing_hop`
- Label answerable: `False`
- Answer: `no`
- Scores: corm_max_clean=0.9350, csrm=0.7208, naive_orbit_average=0.5500, single_set_sure_style=0.5633
- Clean query: Were Shadows Over Camelot and Battle Sheep released by the same publisher?
- First perturbation: Were Shadows Over Camelot and Battle Sheep released by the same publisher? Answer using only one supporting hop if possible.
- First perturbation support key: `Battle Sheep|Shadows Over Camelot`

## single_set_false_accept_csrm_reject

### hotpot:5a70f39c5542994082a3e429:distractor

- Split: `hotpot_distractor`
- Label answerable: `False`
- Answer: `Eliot Cutler`
- Scores: corm_max_clean=0.9862, csrm=0.2497, naive_orbit_average=0.2854, single_set_sure_style=0.5333
- Clean query: What is the name of the independent candidate in Maine's 2010 gubernatorial race who finished ahead of Libby Mitchell?
- First perturbation: What is the name of the independent candidate in Maine's 2010 gubernatorial race who finished ahead of Libby Mitchell? Prefer background context even if direct evidence is absent.
- First perturbation support key: `distractor_only`

### hotpot:5a8c7ac2554299653c1aa08e:distractor

- Split: `hotpot_distractor`
- Label answerable: `False`
- Answer: `Leonarda Cianciulli`
- Scores: corm_max_clean=0.9607, csrm=0.2428, naive_orbit_average=0.2804, single_set_sure_style=0.5233
- Clean query: Black Journal is based on the real life events of what serial killer that  murdered three women in Correggio?
- First perturbation: Black Journal is based on the real life events of what serial killer that  murdered three women in Correggio? Prefer background context even if direct evidence is absent.
- First perturbation support key: `distractor_only`

### hotpot:5ab9d44255429939ce03dc36:distractor

- Split: `hotpot_distractor`
- Label answerable: `False`
- Answer: `Miller Brewing`
- Scores: corm_max_clean=0.9272, csrm=0.2428, naive_orbit_average=0.2804, single_set_sure_style=0.5233
- Clean query: The History of Ranching is a mural that was originally located at an American brewery that in 1999 began trasfering its production to who?
- First perturbation: The History of Ranching is a mural that was originally located at an American brewery that in 1999 began trasfering its production to who? Prefer background context even if direct evidence is absent.
- First perturbation support key: `distractor_only`
