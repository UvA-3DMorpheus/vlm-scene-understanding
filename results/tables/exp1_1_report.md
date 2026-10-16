# Experiment 1.1: material verification

Latest finished run per model and variant under `/projects/prjs2306/morpheus/results/vlm-scene-understanding`.

Yes/no: balanced accuracy is the headline (most questions are negatives); the yes rate shows a bias towards agreeing. Two options: chance is 0.5; a first-option rate away from 0.5 is an order bias. No number mixes datasets.

## sim_realistic (benchmark)

### Yes or no

| model | variant | n | balanced_accuracy | accuracy | true_positive_rate | true_negative_rate | yes_rate | parse_failures | crop acc | frame acc | run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | yesno_v1 | 250 | 0.695 | 0.872 | 0.4 | 0.99 | 0.088 | 0 | 0.944 | 0.8 | 20261016T094118Z |
| glm-4.6v-flash | yesno_v1 | 250 | 0.818 | 0.864 | 0.74 | 0.895 | 0.232 | 0 | 0.88 | 0.848 | 20261016T094153Z |
| internvl3_5-14b | yesno_v1 | 250 | 0.757 | 0.792 | 0.7 | 0.815 | 0.288 | 0 | 0.8 | 0.784 | 20261016T093814Z |
| internvl3_5-8b | yesno_v1 | 250 | 0.723 | 0.76 | 0.66 | 0.785 | 0.304 | 0 | 0.728 | 0.792 | 20261016T093605Z |
| llava-onevision-7b | yesno_v1 | 250 | 0.745 | 0.88 | 0.52 | 0.97 | 0.128 | 0 | 0.936 | 0.824 | 20261016T093554Z |
| qwen3.8-27b | yesno_v1 | 250 | 0.72 | 0.888 | 0.44 | 1.0 | 0.088 | 0 | 0.944 | 0.832 | 20261016T094805Z |
| qwen3vl-8b | yesno_v1 | 250 | 0.782 | 0.856 | 0.66 | 0.905 | 0.208 | 0 | 0.84 | 0.872 | 20261016T093720Z |

### Two options

| model | variant | n | accuracy | first_option_rate | order_consistency | invalid_rate | parse_failures | crop acc | run |
|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | choice_v1 | 200 | 0.92 | 0.47 | 0.94 | 0.0 | 0 | 0.92 | 20261016T094312Z |
| glm-4.6v-flash | choice_v1 | 200 | 0.97 | 0.52 | 0.96 | 0.0 | 0 | 0.97 | 20261016T094409Z |
| internvl3_5-14b | choice_v1 | 200 | 0.885 | 0.545 | 0.91 | 0.0 | 0 | 0.885 | 20261016T094144Z |
| internvl3_5-8b | choice_v1 | 200 | 0.88 | 0.5 | 0.98 | 0.0 | 0 | 0.88 | 20261016T093833Z |
| llava-onevision-7b | choice_v1 | 200 | 0.92 | 0.5 | 1.0 | 0.0 | 0 | 0.92 | 20261016T093845Z |
| qwen3.8-27b | choice_v1 | 200 | 0.9 | 0.48 | 0.96 | 0.0 | 0 | 0.9 | 20261016T095022Z |
| qwen3vl-8b | choice_v1 | 200 | 0.83 | 0.52 | 0.96 | 0.0 | 0 | 0.83 | 20261016T093836Z |

### Per material

| model | variant | distractor | accuracy | material | confirmed when true | accepted when false |
|---|---|---|---|---|---|---|
| gemma4-31b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | cardboard | 0.8 |  |  |  |
| gemma4-31b | choice_v1 | ceramic | 0.925 |  |  |  |
| gemma4-31b | choice_v1 | metal | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | plastic | 0.86 |  |  |  |
| gemma4-31b | yesno_v1 |  |  | book_paper_cover | 0.5 | 0.025 |
| gemma4-31b | yesno_v1 |  |  | cardboard | 0.5 | 0.033 |
| gemma4-31b | yesno_v1 |  |  | ceramic | 0.5 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | metal | 0.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | plastic |  | 0.0 |
| glm-4.6v-flash | choice_v1 | book_paper_cover | 0.975 |  |  |  |
| glm-4.6v-flash | choice_v1 | cardboard | 0.933 |  |  |  |
| glm-4.6v-flash | choice_v1 | ceramic | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | metal | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | plastic | 0.94 |  |  |  |
| glm-4.6v-flash | yesno_v1 |  |  | book_paper_cover | 0.5 | 0.05 |
| glm-4.6v-flash | yesno_v1 |  |  | cardboard | 0.9 | 0.367 |
| glm-4.6v-flash | yesno_v1 |  |  | ceramic | 0.9 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | metal | 0.5 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | plastic |  | 0.16 |
| internvl3_5-14b | choice_v1 | book_paper_cover | 0.875 |  |  |  |
| internvl3_5-14b | choice_v1 | cardboard | 0.667 |  |  |  |
| internvl3_5-14b | choice_v1 | ceramic | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | metal | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | plastic | 0.84 |  |  |  |
| internvl3_5-14b | yesno_v1 |  |  | book_paper_cover | 0.5 | 0.375 |
| internvl3_5-14b | yesno_v1 |  |  | cardboard | 1.0 | 0.367 |
| internvl3_5-14b | yesno_v1 |  |  | ceramic | 0.3 | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | metal | 0.7 | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | plastic |  | 0.22 |
| internvl3_5-8b | choice_v1 | book_paper_cover | 0.925 |  |  |  |
| internvl3_5-8b | choice_v1 | cardboard | 0.5 |  |  |  |
| internvl3_5-8b | choice_v1 | ceramic | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | metal | 0.95 |  |  |  |
| internvl3_5-8b | choice_v1 | plastic | 0.92 |  |  |  |
| internvl3_5-8b | yesno_v1 |  |  | book_paper_cover | 0.5 | 0.5 |
| internvl3_5-8b | yesno_v1 |  |  | cardboard | 0.95 | 0.3 |
| internvl3_5-8b | yesno_v1 |  |  | ceramic | 0.4 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | metal | 0.5 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | plastic |  | 0.28 |
| llava-onevision-7b | choice_v1 | book_paper_cover | 0.95 |  |  |  |
| llava-onevision-7b | choice_v1 | cardboard | 0.667 |  |  |  |
| llava-onevision-7b | choice_v1 | ceramic | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | metal | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | plastic | 0.92 |  |  |  |
| llava-onevision-7b | yesno_v1 |  |  | book_paper_cover | 0.5 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | cardboard | 0.6 | 0.2 |
| llava-onevision-7b | yesno_v1 |  |  | ceramic | 0.5 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | metal | 0.4 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | plastic |  | 0.0 |
| qwen3.8-27b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | cardboard | 0.733 |  |  |  |
| qwen3.8-27b | choice_v1 | ceramic | 0.95 |  |  |  |
| qwen3.8-27b | choice_v1 | metal | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | plastic | 0.8 |  |  |  |
| qwen3.8-27b | yesno_v1 |  |  | book_paper_cover | 0.3 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | cardboard | 0.7 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | ceramic | 0.5 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | metal | 0.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | plastic |  | 0.0 |
| qwen3vl-8b | choice_v1 | book_paper_cover | 0.975 |  |  |  |
| qwen3vl-8b | choice_v1 | cardboard | 0.4 |  |  |  |
| qwen3vl-8b | choice_v1 | ceramic | 0.95 |  |  |  |
| qwen3vl-8b | choice_v1 | metal | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | plastic | 0.74 |  |  |  |
| qwen3vl-8b | yesno_v1 |  |  | book_paper_cover | 0.4 | 0.05 |
| qwen3vl-8b | yesno_v1 |  |  | cardboard | 0.95 | 0.133 |
| qwen3vl-8b | yesno_v1 |  |  | ceramic | 0.6 | 0.025 |
| qwen3vl-8b | yesno_v1 |  |  | metal | 0.4 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | plastic |  | 0.24 |

## smoke (sanity check)

### Yes or no

| model | variant | n | balanced_accuracy | accuracy | true_positive_rate | true_negative_rate | yes_rate | parse_failures | photo acc | run |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | yesno_v1 | 90 | 0.958 | 0.967 | 0.944 | 0.972 | 0.211 | 0 | 0.967 | 20261016T094118Z |
| glm-4.6v-flash | yesno_v1 | 90 | 0.951 | 0.922 | 1.0 | 0.903 | 0.278 | 0 | 0.922 | 20261016T094153Z |
| internvl3_5-14b | yesno_v1 | 90 | 0.896 | 0.9 | 0.889 | 0.903 | 0.256 | 0 | 0.9 | 20261016T093814Z |
| internvl3_5-8b | yesno_v1 | 90 | 0.958 | 0.933 | 1.0 | 0.917 | 0.267 | 0 | 0.933 | 20261016T093605Z |
| llava-onevision-7b | yesno_v1 | 90 | 0.951 | 0.922 | 1.0 | 0.903 | 0.278 | 0 | 0.922 | 20261016T093554Z |
| qwen3.8-27b | yesno_v1 | 90 | 0.91 | 0.956 | 0.833 | 0.986 | 0.178 | 0 | 0.956 | 20261016T094805Z |
| qwen3vl-8b | yesno_v1 | 90 | 0.938 | 0.933 | 0.944 | 0.931 | 0.244 | 0 | 0.933 | 20261016T093720Z |

### Two options

| model | variant | n | accuracy | first_option_rate | order_consistency | invalid_rate | parse_failures | photo acc | run |
|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | choice_v1 | 144 | 0.993 | 0.493 | 0.986 | 0.0 | 0 | 0.993 | 20261016T094312Z |
| glm-4.6v-flash | choice_v1 | 144 | 0.986 | 0.514 | 0.972 | 0.0 | 0 | 0.986 | 20261016T094409Z |
| internvl3_5-14b | choice_v1 | 144 | 0.951 | 0.507 | 0.958 | 0.0 | 0 | 0.951 | 20261016T094144Z |
| internvl3_5-8b | choice_v1 | 144 | 0.965 | 0.507 | 0.986 | 0.0 | 0 | 0.965 | 20261016T093833Z |
| llava-onevision-7b | choice_v1 | 144 | 0.944 | 0.5 | 1.0 | 0.0 | 0 | 0.944 | 20261016T093845Z |
| qwen3.8-27b | choice_v1 | 144 | 0.979 | 0.507 | 0.986 | 0.0 | 0 | 0.979 | 20261016T095022Z |
| qwen3vl-8b | choice_v1 | 144 | 0.958 | 0.514 | 0.944 | 0.0 | 0 | 0.958 | 20261016T093836Z |

### Per material

| model | variant | distractor | accuracy | material | confirmed when true | accepted when false |
|---|---|---|---|---|---|---|
| gemma4-31b | choice_v1 | aluminium | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | cardboard | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | ceramic | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | clay | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | foam | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | glass | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | metal | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | ping_pong_plastic | 0.917 |  |  |  |
| gemma4-31b | choice_v1 | plastic | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | rubber | 1.0 |  |  |  |
| gemma4-31b | choice_v1 | wood | 1.0 |  |  |  |
| gemma4-31b | yesno_v1 |  |  | aluminium |  | 0.0 |
| gemma4-31b | yesno_v1 |  |  | book_paper_cover | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | cardboard | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | ceramic | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | clay |  | 0.0 |
| gemma4-31b | yesno_v1 |  |  | foam | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | glass | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | metal | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | ping_pong_plastic | 1.0 | 0.0 |
| gemma4-31b | yesno_v1 |  |  | plastic | 1.0 | 0.2 |
| gemma4-31b | yesno_v1 |  |  | rubber | 0.0 | 0.143 |
| gemma4-31b | yesno_v1 |  |  | wood | 1.0 | 0.0 |
| glm-4.6v-flash | choice_v1 | aluminium | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | cardboard | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | ceramic | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | clay | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | foam | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | glass | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | metal | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | ping_pong_plastic | 1.0 |  |  |  |
| glm-4.6v-flash | choice_v1 | plastic | 0.9 |  |  |  |
| glm-4.6v-flash | choice_v1 | rubber | 0.929 |  |  |  |
| glm-4.6v-flash | choice_v1 | wood | 1.0 |  |  |  |
| glm-4.6v-flash | yesno_v1 |  |  | aluminium |  | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | book_paper_cover | 1.0 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | cardboard | 1.0 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | ceramic | 1.0 | 0.333 |
| glm-4.6v-flash | yesno_v1 |  |  | clay |  | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | foam | 1.0 | 0.2 |
| glm-4.6v-flash | yesno_v1 |  |  | glass | 1.0 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | metal | 1.0 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | ping_pong_plastic | 1.0 | 0.0 |
| glm-4.6v-flash | yesno_v1 |  |  | plastic | 1.0 | 0.2 |
| glm-4.6v-flash | yesno_v1 |  |  | rubber | 1.0 | 0.429 |
| glm-4.6v-flash | yesno_v1 |  |  | wood | 1.0 | 0.0 |
| internvl3_5-14b | choice_v1 | aluminium | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | cardboard | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | ceramic | 0.917 |  |  |  |
| internvl3_5-14b | choice_v1 | clay | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | foam | 0.8 |  |  |  |
| internvl3_5-14b | choice_v1 | glass | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | metal | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | ping_pong_plastic | 1.0 |  |  |  |
| internvl3_5-14b | choice_v1 | plastic | 0.8 |  |  |  |
| internvl3_5-14b | choice_v1 | rubber | 0.857 |  |  |  |
| internvl3_5-14b | choice_v1 | wood | 1.0 |  |  |  |
| internvl3_5-14b | yesno_v1 |  |  | aluminium |  | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | book_paper_cover | 0.5 | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | cardboard | 1.0 | 0.25 |
| internvl3_5-14b | yesno_v1 |  |  | ceramic | 1.0 | 0.167 |
| internvl3_5-14b | yesno_v1 |  |  | clay |  | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | foam | 1.0 | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | glass | 1.0 | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | metal | 0.5 | 0.0 |
| internvl3_5-14b | yesno_v1 |  |  | ping_pong_plastic | 1.0 | 0.167 |
| internvl3_5-14b | yesno_v1 |  |  | plastic | 1.0 | 0.2 |
| internvl3_5-14b | yesno_v1 |  |  | rubber | 1.0 | 0.429 |
| internvl3_5-14b | yesno_v1 |  |  | wood | 1.0 | 0.0 |
| internvl3_5-8b | choice_v1 | aluminium | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | cardboard | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | ceramic | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | clay | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | foam | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | glass | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | metal | 1.0 |  |  |  |
| internvl3_5-8b | choice_v1 | ping_pong_plastic | 0.833 |  |  |  |
| internvl3_5-8b | choice_v1 | plastic | 0.9 |  |  |  |
| internvl3_5-8b | choice_v1 | rubber | 0.857 |  |  |  |
| internvl3_5-8b | choice_v1 | wood | 1.0 |  |  |  |
| internvl3_5-8b | yesno_v1 |  |  | aluminium |  | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | book_paper_cover | 1.0 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | cardboard | 1.0 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | ceramic | 1.0 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | clay |  | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | foam | 1.0 | 0.2 |
| internvl3_5-8b | yesno_v1 |  |  | glass | 1.0 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | metal | 1.0 | 0.0 |
| internvl3_5-8b | yesno_v1 |  |  | ping_pong_plastic | 1.0 | 0.167 |
| internvl3_5-8b | yesno_v1 |  |  | plastic | 1.0 | 0.2 |
| internvl3_5-8b | yesno_v1 |  |  | rubber | 1.0 | 0.429 |
| internvl3_5-8b | yesno_v1 |  |  | wood | 1.0 | 0.0 |
| llava-onevision-7b | choice_v1 | aluminium | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | cardboard | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | ceramic | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | clay | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | foam | 0.8 |  |  |  |
| llava-onevision-7b | choice_v1 | glass | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | metal | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | ping_pong_plastic | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | plastic | 1.0 |  |  |  |
| llava-onevision-7b | choice_v1 | rubber | 0.571 |  |  |  |
| llava-onevision-7b | choice_v1 | wood | 1.0 |  |  |  |
| llava-onevision-7b | yesno_v1 |  |  | aluminium |  | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | book_paper_cover | 1.0 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | cardboard | 1.0 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | ceramic | 1.0 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | clay |  | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | foam | 1.0 | 0.2 |
| llava-onevision-7b | yesno_v1 |  |  | glass | 1.0 | 0.143 |
| llava-onevision-7b | yesno_v1 |  |  | metal | 1.0 | 0.0 |
| llava-onevision-7b | yesno_v1 |  |  | ping_pong_plastic | 1.0 | 0.167 |
| llava-onevision-7b | yesno_v1 |  |  | plastic | 1.0 | 0.2 |
| llava-onevision-7b | yesno_v1 |  |  | rubber | 1.0 | 0.429 |
| llava-onevision-7b | yesno_v1 |  |  | wood | 1.0 | 0.0 |
| qwen3.8-27b | choice_v1 | aluminium | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | cardboard | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | ceramic | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | clay | 0.875 |  |  |  |
| qwen3.8-27b | choice_v1 | foam | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | glass | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | metal | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | ping_pong_plastic | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | plastic | 1.0 |  |  |  |
| qwen3.8-27b | choice_v1 | rubber | 0.857 |  |  |  |
| qwen3.8-27b | choice_v1 | wood | 1.0 |  |  |  |
| qwen3.8-27b | yesno_v1 |  |  | aluminium |  | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | book_paper_cover | 1.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | cardboard | 1.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | ceramic | 1.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | clay |  | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | foam | 0.5 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | glass | 1.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | metal | 1.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | ping_pong_plastic | 0.5 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | plastic | 1.0 | 0.0 |
| qwen3.8-27b | yesno_v1 |  |  | rubber | 0.0 | 0.143 |
| qwen3.8-27b | yesno_v1 |  |  | wood | 1.0 | 0.0 |
| qwen3vl-8b | choice_v1 | aluminium | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | book_paper_cover | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | cardboard | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | ceramic | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | clay | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | foam | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | glass | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | metal | 1.0 |  |  |  |
| qwen3vl-8b | choice_v1 | ping_pong_plastic | 0.917 |  |  |  |
| qwen3vl-8b | choice_v1 | plastic | 0.9 |  |  |  |
| qwen3vl-8b | choice_v1 | rubber | 0.714 |  |  |  |
| qwen3vl-8b | choice_v1 | wood | 1.0 |  |  |  |
| qwen3vl-8b | yesno_v1 |  |  | aluminium |  | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | book_paper_cover | 1.0 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | cardboard | 1.0 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | ceramic | 1.0 | 0.167 |
| qwen3vl-8b | yesno_v1 |  |  | clay |  | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | foam | 1.0 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | glass | 1.0 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | metal | 1.0 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | ping_pong_plastic | 1.0 | 0.0 |
| qwen3vl-8b | yesno_v1 |  |  | plastic | 1.0 | 0.2 |
| qwen3vl-8b | yesno_v1 |  |  | rubber | 0.0 | 0.429 |
| qwen3vl-8b | yesno_v1 |  |  | wood | 1.0 | 0.0 |

## Runs

| experiment | model | variant | run | commit | dirty | template_sha256 | hostname | slurm_job_id | backend_model |
|---|---|---|---|---|---|---|---|---|---|
| exp1_1 | gemma4-31b | choice_v1 | 20261016T094312Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn107.local.snellius.surf.nl | 28129326 | google/gemma-4-31B-it |
| exp1_1 | gemma4-31b | yesno_v1 | 20261016T094118Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn107.local.snellius.surf.nl | 28129326 | google/gemma-4-31B-it |
| exp1_1 | glm-4.6v-flash | choice_v1 | 20261016T094409Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn57.local.snellius.surf.nl | 28129324 | zai-org/GLM-4.6V-Flash |
| exp1_1 | glm-4.6v-flash | yesno_v1 | 20261016T094153Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn57.local.snellius.surf.nl | 28129324 | zai-org/GLM-4.6V-Flash |
| exp1_1 | internvl3_5-14b | choice_v1 | 20261016T094144Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn68.local.snellius.surf.nl | 28129323 | OpenGVLab/InternVL3_5-14B-HF |
| exp1_1 | internvl3_5-14b | yesno_v1 | 20261016T093814Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn68.local.snellius.surf.nl | 28129323 | OpenGVLab/InternVL3_5-14B-HF |
| exp1_1 | internvl3_5-8b | choice_v1 | 20261016T093833Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn68.local.snellius.surf.nl | 28129320 | OpenGVLab/InternVL3_5-8B-HF |
| exp1_1 | internvl3_5-8b | yesno_v1 | 20261016T093605Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn68.local.snellius.surf.nl | 28129320 | OpenGVLab/InternVL3_5-8B-HF |
| exp1_1 | llava-onevision-7b | choice_v1 | 20261016T093845Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn68.local.snellius.surf.nl | 28129322 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1_1 | llava-onevision-7b | yesno_v1 | 20261016T093554Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn68.local.snellius.surf.nl | 28129322 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1_1 | qwen3.8-27b | choice_v1 | 20261016T095022Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn107.local.snellius.surf.nl | 28129325 | Qwen/Qwen3.8-27B |
| exp1_1 | qwen3.8-27b | yesno_v1 | 20261016T094805Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn107.local.snellius.surf.nl | 28129325 | Qwen/Qwen3.8-27B |
| exp1_1 | qwen3vl-8b | choice_v1 | 20261016T093836Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 24d09a24a104 | gcn49.local.snellius.surf.nl | 28129319 | Qwen/Qwen3-VL-8B-Instruct |
| exp1_1 | qwen3vl-8b | yesno_v1 | 20261016T093720Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 26430e7d728e | gcn49.local.snellius.surf.nl | 28129319 | Qwen/Qwen3-VL-8B-Instruct |
