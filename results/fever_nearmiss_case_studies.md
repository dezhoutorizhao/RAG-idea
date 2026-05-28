# Case Studies

Input: `results\fever_orbits_nearmiss_corm_1200.jsonl`

Thresholds at 30% coverage:

- `corm_max_clean`: 0.682095
- `single_set_sure_style`: 0.670000
- `naive_orbit_average`: 0.670000
- `csrm`: 0.582250

## naive_false_accept_csrm_reject

### fever:f7c3d399da82434fce9ec8abf22bfc2c:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.7910, csrm=0.5710, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Byron Howard co-directed at least one animated film.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Byron Howard co-directed at least one animated film.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:ddf6774ac03614ee08ab8a1017d9f9e6:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.1782, csrm=0.5710, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: The Indian Army is a military force.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: The Indian Army is a military force.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:0a4f033494e9a5da1eb72db1efa3e600:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.1945, csrm=0.5710, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: There was a grouping of French colonial territories called French Indochina.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: There was a grouping of French colonial territories called French Indochina.
- First perturbation support key: `near_miss:REFUTES:0`

## corm_false_accept_csrm_reject

### fever:a5b7cd05c31b6190e7c09ba3dba6435b:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9284, csrm=0.2138, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Carlos Santana was born in the forties.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Carlos Santana was born in the forties.
- First perturbation support key: `opposite:REFUTES`

### fever:f6f646454394aa0e8b5b6a9317b01e0b:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9264, csrm=0.2138, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Michael Vick has a middle name.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Michael Vick has a middle name.
- First perturbation support key: `opposite:REFUTES`

### fever:4c40695ae3dd9b59eea95c4cb42f9252:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.9197, csrm=0.2138, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Paris (Paris Hilton album) incorporates elements of a music genre that originated in Jamaica in the late 1960s.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Paris (Paris Hilton album) incorporates elements of a music genre that originated in Jamaica in the late 1960s.
- First perturbation support key: `opposite:REFUTES`

## csrm_true_accept

### fever:e894f9d46a585a32306b364c04530f10:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5258, csrm=0.8185, naive_orbit_average=0.6700, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Homer Hickman has written best-selling memoirs.
- First perturbation: Using only the evidence, fact-check this claim: Homer Hickman has written best-selling memoirs.
- First perturbation support key: `Homer_Hickam:2`

### fever:c5089595a76ab788ceddae2ff756821f:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.0696, csrm=0.8185, naive_orbit_average=0.6700, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Arizona is in the southern United States.
- First perturbation: Using only the evidence, fact-check this claim: Arizona is in the southern United States.
- First perturbation support key: `Arizona:0`

### fever:f0293348b72ec3cc523410e040daa287:stable

- Split: `fever_stable_evidence`
- Label answerable: `True`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.0613, csrm=0.8185, naive_orbit_average=0.6700, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Sikkim is host to Kanchenjunga, the highest peak in India.
- First perturbation: Using only the evidence, fact-check this claim: Sikkim is host to Kanchenjunga, the highest peak in India.
- First perturbation support key: `Sikkim:4`

## csrm_false_accept_failure

### fever:e894f9d46a585a32306b364c04530f10:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.5258, csrm=0.5899, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Homer Hickman has written best-selling memoirs.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Homer Hickman has written best-selling memoirs.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:c5089595a76ab788ceddae2ff756821f:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.0696, csrm=0.5899, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Arizona is in the southern United States.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Arizona is in the southern United States.
- First perturbation support key: `near_miss:REFUTES:0`

### fever:f0293348b72ec3cc523410e040daa287:near_miss_dilution

- Split: `fever_near_miss_dilution`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.0613, csrm=0.5899, naive_orbit_average=0.7000, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Sikkim is host to Kanchenjunga, the highest peak in India.
- First perturbation: Fact-check this claim with highly plausible but potentially mismatched evidence set 0: Sikkim is host to Kanchenjunga, the highest peak in India.
- First perturbation support key: `near_miss:REFUTES:0`

## single_set_false_accept_csrm_reject

### fever:f7c3d399da82434fce9ec8abf22bfc2c:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.7910, csrm=0.2038, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: Byron Howard co-directed at least one animated film.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: Byron Howard co-directed at least one animated film.
- First perturbation support key: `opposite:REFUTES`

### fever:ddf6774ac03614ee08ab8a1017d9f9e6:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.1782, csrm=0.2038, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: The Indian Army is a military force.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: The Indian Army is a military force.
- First perturbation support key: `opposite:REFUTES`

### fever:0a4f033494e9a5da1eb72db1efa3e600:conflict

- Split: `fever_conflicting_evidence`
- Label answerable: `False`
- Answer: `SUPPORTS`
- Scores: corm_max_clean=0.1945, csrm=0.2038, naive_orbit_average=0.3350, single_set_sure_style=0.6700
- Clean query: Determine whether this claim is supported or refuted: There was a grouping of French colonial territories called French Indochina.
- First perturbation: Assuming the evidence may indicate REFUTES, fact-check this claim: There was a grouping of French colonial territories called French Indochina.
- First perturbation support key: `opposite:REFUTES`
