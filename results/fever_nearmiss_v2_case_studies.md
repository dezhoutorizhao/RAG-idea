# Case Studies

Input: `results\fever_orbits_nearmiss_corm_1200_v2.jsonl`

Thresholds at 30% coverage:

- `corm_max_clean`: 0.691023
- `single_set_sure_style`: 0.670000
- `naive_orbit_average`: 0.670000
- `csrm`: 0.576076

## naive_false_accept_csrm_reject

### fever:2a276e2022df54b04d64be48c3ed7501:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.8197, csrm=0.5710, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Shadowhunters premiered in the 21st century.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Shadowhunters premiered in the 21st century.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:b25e32964523c07fd47e9cd1bb68b845:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.4868, csrm=0.5710, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: The Armenian Genocide occurred during the Second Constitutional Era.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: The Armenian Genocide occurred during the Second Constitutional Era.
- First perturbation support key: `near_miss:REFUTES:0`

## corm_false_accept_csrm_reject

### fever:a5b7cd05c31b6190e7c09ba3dba6435b:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9284, csrm=0.2083, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Carlos Santana was born in the forties.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Carlos Santana was born in the forties.
- First perturbation support key: `opposite:REFUTES`

### fever:9293053261bd11864297fff006954b5d:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9037, csrm=0.2083, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Libya is one of the top ten largest countries on its continent.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Libya is one of the top ten largest countries on its continent.
- First perturbation support key: `opposite:REFUTES`

### fever:08687c396180e95e1e1bdee2702b73eb:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.8889, csrm=0.2083, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Bethany Hamilton's biopic was directed by Sean McNamara.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Bethany Hamilton's biopic was directed by Sean McNamara.
- First perturbation support key: `opposite:REFUTES`

## csrm_true_accept

### fever:4f99160cf65dc9e25cb7a99e04e8688c:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5306, csrm=0.8185, naive_orbit_average=0.6700, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Kelly Preston starred in films.
- First perturbation: Using only the evidence, fact-check this claim: Kelly Preston starred in films.
- First perturbation support key: `Kelly_Preston:1`

### fever:4336a732d713a27fc558b61c90f0f440:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.7864, csrm=0.8185, naive_orbit_average=0.6700, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: The Bloods was founded in Los Angeles, California.
- First perturbation: Using only the evidence, fact-check this claim: The Bloods was founded in Los Angeles, California.
- First perturbation support key: `Bloods:0`

### fever:8b32776efdf86e56e1a42226239b351f:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.8464, csrm=0.8185, naive_orbit_average=0.6700, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Princess Mononoke has a dark atmosphere.
- First perturbation: Using only the evidence, fact-check this claim: Princess Mononoke has a dark atmosphere.
- First perturbation support key: `Princess_Mononoke:7`

## csrm_false_accept_failure

### fever:9a2ce22de1acef55d9f23bc0b2c12e26:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.4708, csrm=0.6042, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Camden, New Jersey is a country.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Camden, New Jersey is a country.
- First perturbation support key: `near_miss:SUPPORTS:0`

### fever:5906c0b9404671c031ce851ac076ac6c:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.0567, csrm=0.5935, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: XHamster's The Sex Factor makes eight men and eight women compete to become a novelist.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: XHamster's The Sex Factor makes eight men and eight women compete to become a novelist.
- First perturbation support key: `near_miss:SUPPORTS:0`

### fever:65995ca6f567ff1296003ff9a09ad24c:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `REFUTES`
- Scores: corm_max_clean=0.6514, csrm=0.5935, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Gray Matter Interactive Studios, Inc. was only a agency.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Gray Matter Interactive Studios, Inc. was only a agency.
- First perturbation support key: `near_miss:SUPPORTS:0`

## single_set_false_accept_csrm_reject

### fever:2a276e2022df54b04d64be48c3ed7501:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.8197, csrm=0.2038, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Shadowhunters premiered in the 21st century.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Shadowhunters premiered in the 21st century.
- First perturbation support key: `opposite:REFUTES`

### fever:b25e32964523c07fd47e9cd1bb68b845:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.4868, csrm=0.2038, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: The Armenian Genocide occurred during the Second Constitutional Era.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: The Armenian Genocide occurred during the Second Constitutional Era.
- First perturbation support key: `opposite:REFUTES`

### fever:4f99160cf65dc9e25cb7a99e04e8688c:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5306, csrm=0.2083, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Kelly Preston starred in films.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Kelly Preston starred in films.
- First perturbation support key: `opposite:REFUTES`
