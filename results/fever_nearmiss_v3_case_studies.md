# Case Studies

Input: `results\fever_orbits_nearmiss_corm_1200_v3.jsonl`

Thresholds at 30% coverage:

- `corm_max_clean`: 0.662185
- `single_set_sure_style`: 0.389167
- `naive_orbit_average`: 0.381667
- `csrm`: 0.423667

## naive_false_accept_csrm_reject

### fever:e8f235cdc9269c5928f507f9603929fa:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.6586, csrm=0.4103, naive_orbit_average=0.5747, single_set_sure_style=0.5233
- Clean query: Determine whether this claim is supported or refuted: Dreamer (2005 film) was directed by an American screenwriter, director, and actor.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Dreamer (2005 film) was directed by an American screenwriter, director, and actor.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:3701d7097c281592457c545c8b475704:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9606, csrm=0.4103, naive_orbit_average=0.5747, single_set_sure_style=0.5233
- Clean query: Determine whether this claim is supported or refuted: An American band is responsible for the song Happiness in Slavery.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: An American band is responsible for the song Happiness in Slavery.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:8fabe2eb5111f4588d1f81c9ebdb0d73:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5342, csrm=0.4134, naive_orbit_average=0.5448, single_set_sure_style=0.3742
- Clean query: Determine whether this claim is supported or refuted: Stephen Colbert is an American.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Stephen Colbert is an American.
- First perturbation support key: `near_miss:REFUTES:0`

## corm_false_accept_csrm_reject

### fever:3701d7097c281592457c545c8b475704:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9606, csrm=0.1854, naive_orbit_average=0.2617, single_set_sure_style=0.5233
- Clean query: Determine whether this claim is supported or refuted: An American band is responsible for the song Happiness in Slavery.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: An American band is responsible for the song Happiness in Slavery.
- First perturbation support key: `opposite:REFUTES`

### fever:3701d7097c281592457c545c8b475704:distractor

- Split: `fever_distractor_only`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9606, csrm=0.2104, naive_orbit_average=0.2617, single_set_sure_style=0.5233
- Clean query: Determine whether this claim is supported or refuted: An American band is responsible for the song Happiness in Slavery.
- First perturbation: Fact-check the claim using only background evidence if direct evidence is absent: An American band is responsible for the song Happiness in Slavery.
- First perturbation support key: `distractor_only`

### fever:5e85124bcdf4cc6586d31b0a34d39834:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9606, csrm=0.2139, naive_orbit_average=0.1871, single_set_sure_style=0.3742
- Clean query: Determine whether this claim is supported or refuted: An American band is responsible for the song Happiness in Slavery.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: An American band is responsible for the song Happiness in Slavery.
- First perturbation support key: `opposite:REFUTES`

## csrm_true_accept

### fever:b9144b8ad4737b2b369fc117e1d73f09:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.6797, csrm=0.7580, naive_orbit_average=0.5600, single_set_sure_style=0.5600
- Clean query: Determine whether this claim is supported or refuted: Wales has a large region rich in coal deposits.
- First perturbation: Using only the evidence, fact-check this claim: Wales has a large region rich in coal deposits.
- First perturbation support key: `Mining_in_Wales:4|Mining_in_Wales:5|Wales:16`

### fever:7bd377e3aebc282b40b278ed40d991a0:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5460, csrm=0.7509, naive_orbit_average=0.5600, single_set_sure_style=0.5600
- Clean query: Determine whether this claim is supported or refuted: Eric Church is an American singer.
- First perturbation: Using only the evidence, fact-check this claim: Eric Church is an American singer.
- First perturbation support key: `Eric_Church:2|Sinners_Like_Me:0|Two_Pink_Lines:0`

### fever:3afbac0242cbb668d6e754a15f3e72ec:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.5500, csrm=0.7044, naive_orbit_average=0.4625, single_set_sure_style=0.4625
- Clean query: Determine whether this claim is supported or refuted: Home for the Holidays stars no actors or actresses.
- First perturbation: Using only the evidence, fact-check this claim: Home for the Holidays stars no actors or actresses.
- First perturbation support key: `Dylan_McDermott:0|Holly_Hunter:0|Home_for_the_Holidays_-LRB-1995_film-RRB-:5`

## csrm_false_accept_failure

### fever:3afbac0242cbb668d6e754a15f3e72ec:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.5500, csrm=0.4710, naive_orbit_average=0.5625, single_set_sure_style=0.4625
- Clean query: Determine whether this claim is supported or refuted: Home for the Holidays stars no actors or actresses.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Home for the Holidays stars no actors or actresses.
- First perturbation support key: `near_miss:SUPPORTS:0`

### fever:bc97f82071c90fc4f43fb43105b8f5b9:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.2244, csrm=0.4710, naive_orbit_average=0.5625, single_set_sure_style=0.4625
- Clean query: Determine whether this claim is supported or refuted: Vedam stars only Canadian film actors and actresses.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Vedam stars only Canadian film actors and actresses.
- First perturbation support key: `near_miss:SUPPORTS:0`

### fever:4d5dc8f109518520f3c4f2fe6609e414:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.8753, csrm=0.4710, naive_orbit_average=0.5625, single_set_sure_style=0.4625
- Clean query: Determine whether this claim is supported or refuted: Eric Church is unable to write songs.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Eric Church is unable to write songs.
- First perturbation support key: `near_miss:SUPPORTS:0`

## single_set_false_accept_csrm_reject

### fever:7bd377e3aebc282b40b278ed40d991a0:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5460, csrm=0.1900, naive_orbit_average=0.2800, single_set_sure_style=0.5600
- Clean query: Determine whether this claim is supported or refuted: Eric Church is an American singer.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Eric Church is an American singer.
- First perturbation support key: `opposite:REFUTES`

### fever:b9144b8ad4737b2b369fc117e1d73f09:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.6797, csrm=0.1900, naive_orbit_average=0.2800, single_set_sure_style=0.5600
- Clean query: Determine whether this claim is supported or refuted: Wales has a large region rich in coal deposits.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Wales has a large region rich in coal deposits.
- First perturbation support key: `opposite:REFUTES`

### fever:7bd377e3aebc282b40b278ed40d991a0:distractor

- Split: `fever_distractor_only`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5460, csrm=0.2067, naive_orbit_average=0.2800, single_set_sure_style=0.5600
- Clean query: Determine whether this claim is supported or refuted: Eric Church is an American singer.
- First perturbation: Fact-check the claim using only background evidence if direct evidence is absent: Eric Church is an American singer.
- First perturbation support key: `distractor_only`
