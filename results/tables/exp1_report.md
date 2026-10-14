# Experiment 1: material recognition

Latest finished run per model and variant under `/projects/prjs2306/morpheus/results/vlm-scene-understanding`.

The **sim** dataset is the benchmark and the only one to quote. The smoke dataset is a sanity check that the pipeline works on real photos; its numbers are reported apart and never mixed with the benchmark.

## sim (benchmark)

### Accuracy and macro F1 per condition

| model | variant | n | accuracy | exact_label_rate | parse_failures | crop acc | crop macro_f1 | frame acc | frame macro_f1 | mean_latency_s | run | multiview acc | multiview macro_f1 | outline acc | outline macro_f1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dummy | v2 | 10 | 0.4 | 1.0 | 0 | 0.8 | 0.833 | 0.0 | 0.0 | 0.0 | 20261014T123349Z |  |  |  |  |
| dummy | v3 | 10 | 0.2 | 1.0 | 0 | 0.0 | 0.0 | 0.4 | 0.292 | 0.0 | 20261014T123349Z |  |  |  |  |
| gemma4-31b | v1 | 80 | 0.637 | 1.0 | 0 | 0.68 | 0.643 | 0.72 | 0.686 | 0.33 | 20261014T214733Z | 0.8 | 0.75 | 0.48 | 0.455 |
| gemma4-31b | v2 | 80 | 0.45 | 0.637 | 0 | 0.48 | 0.343 | 0.44 | 0.301 | 1.47 | 20261014T214925Z | 0.6 | 0.45 | 0.4 | 0.192 |
| gemma4-31b | v3 | 80 | 0.6 | 1.0 | 0 | 0.72 | 0.688 | 0.56 | 0.461 | 6.42 | 20261014T215150Z | 0.8 | 0.75 | 0.48 | 0.411 |
| glm-4.6v-flash | v1 | 80 | 0.6 | 1.0 | 0 | 0.72 | 0.689 | 0.68 | 0.638 | 0.0 | 20261014T224037Z | 0.4 | 0.333 | 0.44 | 0.428 |
| glm-4.6v-flash | v2 | 80 | 0.487 | 0.512 | 0 | 0.52 | 0.414 | 0.52 | 0.418 | 0.0 | 20261014T224139Z | 0.4 | 0.2 | 0.44 | 0.289 |
| glm-4.6v-flash | v3 | 80 | 0.4 | 0.988 | 1 | 0.48 | 0.488 | 0.52 | 0.534 | 18.54 | 20261014T223220Z | 0.4 | 0.333 | 0.2 | 0.157 |
| internvl3_5-14b | v1 | 80 | 0.438 | 1.0 | 0 | 0.52 | 0.434 | 0.44 | 0.421 | 0.72 | 20261014T214428Z | 0.2 | 0.1 | 0.4 | 0.359 |
| internvl3_5-14b | v2 | 80 | 0.388 | 0.6 | 0 | 0.4 | 0.208 | 0.36 | 0.225 | 1.4 | 20261014T214713Z | 0.4 | 0.2 | 0.4 | 0.217 |
| internvl3_5-14b | v3 | 80 | 0.375 | 1.0 | 0 | 0.44 | 0.393 | 0.44 | 0.299 | 4.06 | 20261014T214931Z | 0.2 | 0.1 | 0.28 | 0.243 |
| internvl3_5-8b | v1 | 80 | 0.412 | 1.0 | 0 | 0.4 | 0.432 | 0.48 | 0.468 | 0.78 | 20261014T214428Z | 0.8 | 0.667 | 0.28 | 0.333 |
| internvl3_5-8b | v2 | 80 | 0.412 | 0.412 | 0 | 0.48 | 0.335 | 0.4 | 0.227 | 1.34 | 20261014T214605Z | 0.4 | 0.2 | 0.36 | 0.18 |
| internvl3_5-8b | v3 | 80 | 0.312 | 1.0 | 0 | 0.48 | 0.412 | 0.24 | 0.143 | 3.87 | 20261014T214646Z | 0.4 | 0.292 | 0.2 | 0.155 |
| llava-onevision-7b | v1 | 80 | 0.475 | 1.0 | 0 | 0.56 | 0.452 | 0.48 | 0.304 | 0.44 | 20261014T214428Z | 0.4 | 0.167 | 0.4 | 0.272 |
| llava-onevision-7b | v2 | 80 | 0.388 | 0.725 | 0 | 0.4 | 0.2 | 0.32 | 0.211 | 0.83 | 20261014T214550Z | 0.2 | 0.167 | 0.48 | 0.304 |
| llava-onevision-7b | v3 | 80 | 0.338 | 0.963 | 0 | 0.24 | 0.15 | 0.4 | 0.172 | 3.03 | 20261014T214616Z | 0.4 | 0.2 | 0.36 | 0.18 |
| qwen3.8-27b | v1 | 80 | 0.4 | 1.0 | 0 | 0.56 | 0.556 | 0.28 | 0.217 | 0.4 | 20261014T214628Z | 0.6 | 0.5 | 0.32 | 0.317 |
| qwen3.8-27b | v2 | 80 | 0.4 | 0.325 | 0 | 0.44 | 0.357 | 0.4 | 0.217 | 1.39 | 20261014T214850Z | 0.4 | 0.2 | 0.36 | 0.188 |
| qwen3.8-27b | v3 | 80 | 0.45 | 1.0 | 0 | 0.48 | 0.487 | 0.52 | 0.482 | 10.32 | 20261014T215107Z | 0.8 | 0.75 | 0.28 | 0.24 |
| qwen3vl-8b | v1 | 80 | 0.388 | 1.0 | 0 | 0.56 | 0.52 | 0.36 | 0.303 | 0.23 | 20261014T214428Z | 0.2 | 0.125 | 0.28 | 0.278 |
| qwen3vl-8b | v2 | 80 | 0.388 | 0.263 | 0 | 0.52 | 0.444 | 0.28 | 0.206 | 0.71 | 20261014T214549Z | 0.4 | 0.25 | 0.36 | 0.205 |
| qwen3vl-8b | v3 | 80 | 0.438 | 1.0 | 0 | 0.6 | 0.57 | 0.4 | 0.303 | 5.32 | 20261014T214611Z | 0.6 | 0.5 | 0.28 | 0.233 |

### Accuracy per camera (viewpoint robustness)

| model | variant | front (n=10) | all (n=5) | front (n=15) | high (n=15) | left (n=15) | low (n=15) | right (n=15) |
|---|---|---|---|---|---|---|---|---|
| dummy | v2 | 0.4 |  |  |  |  |  |  |
| dummy | v3 | 0.2 |  |  |  |  |  |  |
| gemma4-31b | v1 |  | 0.8 | 0.467 | 0.667 | 0.667 | 0.667 | 0.667 |
| gemma4-31b | v2 |  | 0.6 | 0.4 | 0.467 | 0.4 | 0.533 | 0.4 |
| gemma4-31b | v3 |  | 0.8 | 0.467 | 0.533 | 0.6 | 0.6 | 0.733 |
| glm-4.6v-flash | v1 |  | 0.4 | 0.667 | 0.667 | 0.533 | 0.533 | 0.667 |
| glm-4.6v-flash | v2 |  | 0.4 | 0.4 | 0.533 | 0.533 | 0.533 | 0.467 |
| glm-4.6v-flash | v3 |  | 0.4 | 0.467 | 0.267 | 0.4 | 0.467 | 0.4 |
| internvl3_5-14b | v1 |  | 0.2 | 0.533 | 0.4 | 0.333 | 0.4 | 0.6 |
| internvl3_5-14b | v2 |  | 0.4 | 0.333 | 0.4 | 0.4 | 0.4 | 0.4 |
| internvl3_5-14b | v3 |  | 0.2 | 0.333 | 0.333 | 0.467 | 0.333 | 0.467 |
| internvl3_5-8b | v1 |  | 0.8 | 0.0 | 0.533 | 0.467 | 0.467 | 0.467 |
| internvl3_5-8b | v2 |  | 0.4 | 0.4 | 0.467 | 0.333 | 0.467 | 0.4 |
| internvl3_5-8b | v3 |  | 0.4 | 0.133 | 0.267 | 0.267 | 0.4 | 0.467 |
| llava-onevision-7b | v1 |  | 0.4 | 0.467 | 0.533 | 0.4 | 0.6 | 0.4 |
| llava-onevision-7b | v2 |  | 0.2 | 0.267 | 0.4 | 0.4 | 0.467 | 0.467 |
| llava-onevision-7b | v3 |  | 0.4 | 0.4 | 0.4 | 0.267 | 0.267 | 0.333 |
| qwen3.8-27b | v1 |  | 0.6 | 0.333 | 0.4 | 0.4 | 0.4 | 0.4 |
| qwen3.8-27b | v2 |  | 0.4 | 0.267 | 0.4 | 0.4 | 0.467 | 0.467 |
| qwen3.8-27b | v3 |  | 0.8 | 0.467 | 0.533 | 0.2 | 0.333 | 0.6 |
| qwen3vl-8b | v1 |  | 0.2 | 0.4 | 0.467 | 0.267 | 0.533 | 0.333 |
| qwen3vl-8b | v2 |  | 0.4 | 0.333 | 0.333 | 0.4 | 0.467 | 0.4 |
| qwen3vl-8b | v3 |  | 0.6 | 0.333 | 0.4 | 0.333 | 0.6 | 0.467 |

### Agreement across prompt variants

| model | variants | n_common | all_agree | fleiss_kappa | agree v1-v2 | agree v1-v3 | agree v2-v3 |
|---|---|---|---|---|---|---|---|
| dummy | v1,v2,v3 | 0 |  |  |  |  |  |
| gemma4-31b | v1,v2,v3 | 80 | 0.6 | 0.587 | 0.625 | 0.887 | 0.625 |
| glm-4.6v-flash | v1,v2,v3 | 80 | 0.35 | 0.41 | 0.463 | 0.725 | 0.475 |
| internvl3_5-14b | v1,v2,v3 | 80 | 0.237 | 0.253 | 0.325 | 0.613 | 0.425 |
| internvl3_5-8b | v1,v2,v3 | 80 | 0.425 | 0.378 | 0.5 | 0.675 | 0.525 |
| llava-onevision-7b | v1,v2,v3 | 80 | 0.375 | 0.251 | 0.45 | 0.575 | 0.562 |
| qwen3.8-27b | v1,v2,v3 | 80 | 0.287 | 0.304 | 0.3 | 0.637 | 0.475 |
| qwen3vl-8b | v1,v2,v3 | 80 | 0.375 | 0.423 | 0.412 | 0.775 | 0.5 |

### Per material recall (which materials are recognisable at all)

| model | variant | condition | material | support | recall | precision | f1 |
|---|---|---|---|---|---|---|---|
| dummy | v2 | crop | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| dummy | v2 | crop | cardboard | 2 | 0.5 | 1.0 | 0.667 |
| dummy | v2 | crop | ceramic | 1 | 1.0 | 0.5 | 0.667 |
| dummy | v2 | crop | metal | 1 | 1.0 | 1.0 | 1.0 |
| dummy | v2 | frame | book_paper_cover | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v2 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| dummy | v2 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| dummy | v2 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| dummy | v3 | crop | cardboard | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | crop | ceramic | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | frame | book_paper_cover | 1 | 1.0 | 0.333 | 0.5 |
| dummy | v3 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| dummy | v3 | frame | ceramic | 1 | 1.0 | 0.5 | 0.667 |
| dummy | v3 | frame | metal | 1 | 0.0 |  | 0.0 |
| gemma4-31b | v1 | crop | book_paper_cover | 5 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | crop | cardboard | 10 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | crop | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| gemma4-31b | v1 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v1 | frame | book_paper_cover | 5 | 1.0 | 0.833 | 0.909 |
| gemma4-31b | v1 | frame | cardboard | 10 | 0.9 | 1.0 | 0.947 |
| gemma4-31b | v1 | frame | ceramic | 5 | 0.8 | 1.0 | 0.889 |
| gemma4-31b | v1 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v1 | multiview | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | multiview | ceramic | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | multiview | metal | 1 | 0.0 |  | 0.0 |
| gemma4-31b | v1 | outline | book_paper_cover | 5 | 0.8 | 0.364 | 0.5 |
| gemma4-31b | v1 | outline | cardboard | 10 | 0.6 | 1.0 | 0.75 |
| gemma4-31b | v1 | outline | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| gemma4-31b | v1 | outline | metal | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | crop | cardboard | 10 | 1.0 | 0.667 | 0.8 |
| gemma4-31b | v2 | crop | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| gemma4-31b | v2 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | frame | cardboard | 10 | 1.0 | 0.769 | 0.87 |
| gemma4-31b | v2 | frame | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| gemma4-31b | v2 | frame | metal | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | multiview | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| gemma4-31b | v2 | multiview | ceramic | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v2 | multiview | metal | 1 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | outline | cardboard | 10 | 1.0 | 0.625 | 0.769 |
| gemma4-31b | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | outline | metal | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v3 | crop | book_paper_cover | 5 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | crop | cardboard | 10 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | crop | ceramic | 5 | 0.6 | 1.0 | 0.75 |
| gemma4-31b | v3 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v3 | frame | book_paper_cover | 5 | 0.8 | 0.667 | 0.727 |
| gemma4-31b | v3 | frame | cardboard | 10 | 0.9 | 0.692 | 0.783 |
| gemma4-31b | v3 | frame | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| gemma4-31b | v3 | frame | metal | 5 | 0.0 |  | 0.0 |
| gemma4-31b | v3 | multiview | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | multiview | ceramic | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | multiview | metal | 1 | 0.0 |  | 0.0 |
| gemma4-31b | v3 | outline | book_paper_cover | 5 | 0.8 | 0.4 | 0.533 |
| gemma4-31b | v3 | outline | cardboard | 10 | 0.7 | 0.875 | 0.778 |
| gemma4-31b | v3 | outline | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| gemma4-31b | v3 | outline | metal | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v1 | crop | book_paper_cover | 5 | 0.8 | 1.0 | 0.889 |
| glm-4.6v-flash | v1 | crop | cardboard | 10 | 1.0 | 0.909 | 0.952 |
| glm-4.6v-flash | v1 | crop | ceramic | 5 | 0.6 | 0.75 | 0.667 |
| glm-4.6v-flash | v1 | crop | metal | 5 | 0.2 | 0.333 | 0.25 |
| glm-4.6v-flash | v1 | frame | book_paper_cover | 5 | 1.0 | 0.5 | 0.667 |
| glm-4.6v-flash | v1 | frame | cardboard | 10 | 0.7 | 1.0 | 0.824 |
| glm-4.6v-flash | v1 | frame | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| glm-4.6v-flash | v1 | frame | metal | 5 | 0.8 | 0.667 | 0.727 |
| glm-4.6v-flash | v1 | multiview | book_paper_cover | 1 | 1.0 | 0.5 | 0.667 |
| glm-4.6v-flash | v1 | multiview | cardboard | 2 | 0.5 | 1.0 | 0.667 |
| glm-4.6v-flash | v1 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v1 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v1 | outline | book_paper_cover | 5 | 0.8 | 0.333 | 0.471 |
| glm-4.6v-flash | v1 | outline | cardboard | 10 | 0.2 | 1.0 | 0.333 |
| glm-4.6v-flash | v1 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v1 | outline | metal | 5 | 1.0 | 0.833 | 0.909 |
| glm-4.6v-flash | v2 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | crop | cardboard | 10 | 1.0 | 0.667 | 0.8 |
| glm-4.6v-flash | v2 | crop | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| glm-4.6v-flash | v2 | crop | metal | 5 | 0.2 | 0.5 | 0.286 |
| glm-4.6v-flash | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | frame | cardboard | 10 | 1.0 | 0.625 | 0.769 |
| glm-4.6v-flash | v2 | frame | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| glm-4.6v-flash | v2 | frame | metal | 5 | 0.2 | 1.0 | 0.333 |
| glm-4.6v-flash | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | multiview | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| glm-4.6v-flash | v2 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | outline | cardboard | 10 | 1.0 | 0.769 | 0.87 |
| glm-4.6v-flash | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | outline | metal | 5 | 0.2 | 0.5 | 0.286 |
| glm-4.6v-flash | v3 | crop | book_paper_cover | 5 | 0.8 | 1.0 | 0.889 |
| glm-4.6v-flash | v3 | crop | cardboard | 10 | 0.7 | 0.875 | 0.778 |
| glm-4.6v-flash | v3 | crop | ceramic | 5 | 0.2 | 0.5 | 0.286 |
| glm-4.6v-flash | v3 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v3 | frame | book_paper_cover | 5 | 0.8 | 0.444 | 0.571 |
| glm-4.6v-flash | v3 | frame | cardboard | 10 | 0.6 | 0.857 | 0.706 |
| glm-4.6v-flash | v3 | frame | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| glm-4.6v-flash | v3 | frame | metal | 5 | 0.2 | 0.5 | 0.286 |
| glm-4.6v-flash | v3 | multiview | book_paper_cover | 1 | 1.0 | 0.5 | 0.667 |
| glm-4.6v-flash | v3 | multiview | cardboard | 2 | 0.5 | 1.0 | 0.667 |
| glm-4.6v-flash | v3 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v3 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v3 | outline | book_paper_cover | 5 | 0.8 | 0.308 | 0.444 |
| glm-4.6v-flash | v3 | outline | cardboard | 10 | 0.1 | 1.0 | 0.182 |
| glm-4.6v-flash | v3 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v3 | outline | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-14b | v1 | crop | book_paper_cover | 5 | 0.6 | 0.75 | 0.667 |
| internvl3_5-14b | v1 | crop | cardboard | 10 | 0.9 | 0.75 | 0.818 |
| internvl3_5-14b | v1 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | crop | metal | 5 | 0.2 | 0.333 | 0.25 |
| internvl3_5-14b | v1 | frame | book_paper_cover | 5 | 0.4 | 0.286 | 0.333 |
| internvl3_5-14b | v1 | frame | cardboard | 10 | 0.6 | 0.6 | 0.6 |
| internvl3_5-14b | v1 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | frame | metal | 5 | 0.6 | 1.0 | 0.75 |
| internvl3_5-14b | v1 | multiview | book_paper_cover | 1 | 1.0 | 0.25 | 0.4 |
| internvl3_5-14b | v1 | multiview | cardboard | 2 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | multiview | metal | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | outline | book_paper_cover | 5 | 0.8 | 0.267 | 0.4 |
| internvl3_5-14b | v1 | outline | cardboard | 10 | 0.2 | 0.667 | 0.308 |
| internvl3_5-14b | v1 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | outline | metal | 5 | 0.8 | 0.667 | 0.727 |
| internvl3_5-14b | v2 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | crop | cardboard | 10 | 1.0 | 0.714 | 0.833 |
| internvl3_5-14b | v2 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-14b | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | frame | cardboard | 10 | 0.9 | 0.9 | 0.9 |
| internvl3_5-14b | v2 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | frame | metal | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | multiview | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| internvl3_5-14b | v2 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | multiview | metal | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | outline | cardboard | 10 | 1.0 | 0.769 | 0.87 |
| internvl3_5-14b | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | outline | metal | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | crop | book_paper_cover | 5 | 0.6 | 0.5 | 0.545 |
| internvl3_5-14b | v3 | crop | cardboard | 10 | 0.7 | 0.875 | 0.778 |
| internvl3_5-14b | v3 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | crop | metal | 5 | 0.2 | 0.333 | 0.25 |
| internvl3_5-14b | v3 | frame | book_paper_cover | 5 | 0.6 | 0.429 | 0.5 |
| internvl3_5-14b | v3 | frame | cardboard | 10 | 0.8 | 0.615 | 0.696 |
| internvl3_5-14b | v3 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | frame | metal | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | multiview | book_paper_cover | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-14b | v3 | multiview | cardboard | 2 | 0.5 | 0.333 | 0.4 |
| internvl3_5-14b | v3 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | multiview | metal | 1 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | outline | book_paper_cover | 5 | 0.4 | 0.2 | 0.267 |
| internvl3_5-14b | v3 | outline | cardboard | 10 | 0.4 | 0.444 | 0.421 |
| internvl3_5-14b | v3 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | outline | metal | 5 | 0.2 | 0.5 | 0.286 |
| internvl3_5-8b | v1 | crop | book_paper_cover | 5 | 0.4 | 1.0 | 0.571 |
| internvl3_5-8b | v1 | crop | cardboard | 10 | 0.7 | 1.0 | 0.824 |
| internvl3_5-8b | v1 | crop | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| internvl3_5-8b | v1 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v1 | frame | book_paper_cover | 5 | 0.2 | 0.5 | 0.286 |
| internvl3_5-8b | v1 | frame | cardboard | 10 | 0.8 | 0.667 | 0.727 |
| internvl3_5-8b | v1 | frame | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| internvl3_5-8b | v1 | frame | metal | 5 | 0.2 | 0.5 | 0.286 |
| internvl3_5-8b | v1 | multiview | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v1 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v1 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | multiview | metal | 1 | 1.0 | 0.5 | 0.667 |
| internvl3_5-8b | v1 | outline | book_paper_cover | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v1 | outline | cardboard | 10 | 0.4 | 0.667 | 0.5 |
| internvl3_5-8b | v1 | outline | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| internvl3_5-8b | v1 | outline | metal | 5 | 0.4 | 0.667 | 0.5 |
| internvl3_5-8b | v2 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | crop | cardboard | 10 | 1.0 | 0.625 | 0.769 |
| internvl3_5-8b | v2 | crop | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| internvl3_5-8b | v2 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | frame | cardboard | 10 | 1.0 | 0.833 | 0.909 |
| internvl3_5-8b | v2 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | multiview | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| internvl3_5-8b | v2 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | outline | cardboard | 10 | 0.9 | 0.6 | 0.72 |
| internvl3_5-8b | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | outline | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | crop | book_paper_cover | 5 | 0.6 | 1.0 | 0.75 |
| internvl3_5-8b | v3 | crop | cardboard | 10 | 0.9 | 0.9 | 0.9 |
| internvl3_5-8b | v3 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | frame | book_paper_cover | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | frame | cardboard | 10 | 0.6 | 0.545 | 0.571 |
| internvl3_5-8b | v3 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | multiview | book_paper_cover | 1 | 1.0 | 0.5 | 0.667 |
| internvl3_5-8b | v3 | multiview | cardboard | 2 | 0.5 | 0.5 | 0.5 |
| internvl3_5-8b | v3 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | multiview | metal | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | outline | book_paper_cover | 5 | 0.2 | 0.2 | 0.2 |
| internvl3_5-8b | v3 | outline | cardboard | 10 | 0.4 | 0.444 | 0.421 |
| internvl3_5-8b | v3 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | outline | metal | 5 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v1 | crop | book_paper_cover | 5 | 1.0 | 0.833 | 0.909 |
| llava-onevision-7b | v1 | crop | cardboard | 10 | 0.9 | 0.9 | 0.9 |
| llava-onevision-7b | v1 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v1 | frame | book_paper_cover | 5 | 0.4 | 1.0 | 0.571 |
| llava-onevision-7b | v1 | frame | cardboard | 10 | 1.0 | 0.476 | 0.645 |
| llava-onevision-7b | v1 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v1 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | multiview | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| llava-onevision-7b | v1 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | multiview | metal | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | outline | book_paper_cover | 5 | 1.0 | 0.417 | 0.588 |
| llava-onevision-7b | v1 | outline | cardboard | 10 | 0.5 | 0.5 | 0.5 |
| llava-onevision-7b | v1 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | outline | metal | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | crop | cardboard | 10 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v2 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | frame | cardboard | 10 | 0.8 | 0.889 | 0.842 |
| llava-onevision-7b | v2 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | multiview | cardboard | 2 | 0.5 | 1.0 | 0.667 |
| llava-onevision-7b | v2 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | multiview | metal | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | outline | cardboard | 10 | 1.0 | 0.556 | 0.714 |
| llava-onevision-7b | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | outline | metal | 5 | 0.4 | 0.667 | 0.5 |
| llava-onevision-7b | v3 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | crop | cardboard | 10 | 0.6 | 0.6 | 0.6 |
| llava-onevision-7b | v3 | crop | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v3 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | frame | cardboard | 10 | 1.0 | 0.526 | 0.69 |
| llava-onevision-7b | v3 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | frame | metal | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | multiview | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v3 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | multiview | metal | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | outline | cardboard | 10 | 0.9 | 0.6 | 0.72 |
| llava-onevision-7b | v3 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | outline | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v1 | crop | book_paper_cover | 5 | 1.0 | 0.5 | 0.667 |
| qwen3.8-27b | v1 | crop | cardboard | 10 | 0.5 | 1.0 | 0.667 |
| qwen3.8-27b | v1 | crop | ceramic | 5 | 0.8 | 1.0 | 0.889 |
| qwen3.8-27b | v1 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v1 | frame | book_paper_cover | 5 | 1.0 | 0.278 | 0.435 |
| qwen3.8-27b | v1 | frame | cardboard | 10 | 0.1 | 1.0 | 0.182 |
| qwen3.8-27b | v1 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v1 | frame | metal | 5 | 0.2 | 0.333 | 0.25 |
| qwen3.8-27b | v1 | multiview | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3.8-27b | v1 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v1 | outline | book_paper_cover | 5 | 1.0 | 0.278 | 0.435 |
| qwen3.8-27b | v1 | outline | cardboard | 10 | 0.0 |  | 0.0 |
| qwen3.8-27b | v1 | outline | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| qwen3.8-27b | v1 | outline | metal | 5 | 0.4 | 0.667 | 0.5 |
| qwen3.8-27b | v2 | crop | book_paper_cover | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | crop | cardboard | 10 | 0.9 | 0.818 | 0.857 |
| qwen3.8-27b | v2 | crop | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| qwen3.8-27b | v2 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | frame | cardboard | 10 | 1.0 | 0.769 | 0.87 |
| qwen3.8-27b | v2 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | multiview | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| qwen3.8-27b | v2 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | multiview | metal | 1 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | outline | cardboard | 10 | 0.9 | 0.643 | 0.75 |
| qwen3.8-27b | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | outline | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v3 | crop | book_paper_cover | 5 | 0.8 | 0.444 | 0.571 |
| qwen3.8-27b | v3 | crop | cardboard | 10 | 0.5 | 0.833 | 0.625 |
| qwen3.8-27b | v3 | crop | ceramic | 5 | 0.6 | 1.0 | 0.75 |
| qwen3.8-27b | v3 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v3 | frame | book_paper_cover | 5 | 1.0 | 0.625 | 0.769 |
| qwen3.8-27b | v3 | frame | cardboard | 10 | 0.7 | 1.0 | 0.824 |
| qwen3.8-27b | v3 | frame | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| qwen3.8-27b | v3 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v3 | multiview | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | multiview | ceramic | 1 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | multiview | metal | 1 | 0.0 |  | 0.0 |
| qwen3.8-27b | v3 | outline | book_paper_cover | 5 | 0.4 | 0.286 | 0.333 |
| qwen3.8-27b | v3 | outline | cardboard | 10 | 0.5 | 0.833 | 0.625 |
| qwen3.8-27b | v3 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3.8-27b | v3 | outline | metal | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | crop | book_paper_cover | 5 | 0.8 | 0.8 | 0.8 |
| qwen3vl-8b | v1 | crop | cardboard | 10 | 0.9 | 1.0 | 0.947 |
| qwen3vl-8b | v1 | crop | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| qwen3vl-8b | v1 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v1 | frame | book_paper_cover | 5 | 1.0 | 0.357 | 0.526 |
| qwen3vl-8b | v1 | frame | cardboard | 10 | 0.3 | 1.0 | 0.462 |
| qwen3vl-8b | v1 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | frame | metal | 5 | 0.2 | 0.25 | 0.222 |
| qwen3vl-8b | v1 | multiview | book_paper_cover | 1 | 1.0 | 0.333 | 0.5 |
| qwen3vl-8b | v1 | multiview | cardboard | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v1 | outline | book_paper_cover | 5 | 0.8 | 0.308 | 0.444 |
| qwen3vl-8b | v1 | outline | cardboard | 10 | 0.2 | 1.0 | 0.333 |
| qwen3vl-8b | v1 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | outline | metal | 5 | 0.2 | 1.0 | 0.333 |
| qwen3vl-8b | v2 | crop | book_paper_cover | 5 | 0.2 | 1.0 | 0.333 |
| qwen3vl-8b | v2 | crop | cardboard | 10 | 1.0 | 0.769 | 0.87 |
| qwen3vl-8b | v2 | crop | ceramic | 5 | 0.4 | 1.0 | 0.571 |
| qwen3vl-8b | v2 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v2 | frame | book_paper_cover | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | frame | cardboard | 10 | 0.7 | 1.0 | 0.824 |
| qwen3vl-8b | v2 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v2 | multiview | book_paper_cover | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v2 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | multiview | metal | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v2 | outline | book_paper_cover | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | outline | cardboard | 10 | 0.9 | 0.75 | 0.818 |
| qwen3vl-8b | v2 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | outline | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v3 | crop | book_paper_cover | 5 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | crop | cardboard | 10 | 0.9 | 1.0 | 0.947 |
| qwen3vl-8b | v3 | crop | ceramic | 5 | 0.2 | 1.0 | 0.333 |
| qwen3vl-8b | v3 | crop | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v3 | frame | book_paper_cover | 5 | 0.6 | 0.5 | 0.545 |
| qwen3vl-8b | v3 | frame | cardboard | 10 | 0.7 | 0.636 | 0.667 |
| qwen3vl-8b | v3 | frame | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | frame | metal | 5 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v3 | multiview | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | multiview | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | multiview | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | multiview | metal | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | outline | book_paper_cover | 5 | 0.8 | 0.333 | 0.471 |
| qwen3vl-8b | v3 | outline | cardboard | 10 | 0.3 | 1.0 | 0.462 |
| qwen3vl-8b | v3 | outline | ceramic | 5 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | outline | metal | 5 | 0.0 |  | 0.0 |

### Confusion matrices

#### dummy/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### dummy/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| book_paper_cover | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

#### dummy/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

#### dummy/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### gemma4-31b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 2 | 1 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### gemma4-31b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 9 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### gemma4-31b/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### gemma4-31b/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 3 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 6 | 4 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

#### gemma4-31b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 1 | 1 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### gemma4-31b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 2 | 0 | 0 | 2 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 3 | 0 | 1 | 0 |

#### gemma4-31b/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### gemma4-31b/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 3 | 2 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 4 | 0 | 0 | 0 |

#### gemma4-31b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 3 | 1 | 1 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### gemma4-31b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 3 | 1 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 9 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 4 | 0 | 0 |

#### gemma4-31b/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### gemma4-31b/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 1 | 0 | 3 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 7 | 3 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 4 | 0 | 0 |

#### glm-4.6v-flash/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 3 | 2 | 0 | 0 | 0 | 0 | 0 |
| metal | 1 | 1 | 3 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 4 | 0 | 0 |

#### glm-4.6v-flash/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 2 | 0 | 0 | 2 | 0 | 0 |
| metal | 0 | 4 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 7 | 3 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### glm-4.6v-flash/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### glm-4.6v-flash/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| metal | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 8 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

#### glm-4.6v-flash/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 1 | 1 | 0 | 0 | 1 | 0 |
| metal | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### glm-4.6v-flash/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 1 | 1 | 0 | 1 | 0 |
| metal | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### glm-4.6v-flash/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### glm-4.6v-flash/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 3 | 0 | 0 | 1 | 0 |
| metal | 0 | 1 | 3 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 3 | 0 | 1 | 0 |

#### glm-4.6v-flash/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 1 | 3 | 0 | 0 | 0 | 0 |
| metal | 1 | 0 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 3 | 7 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 4 | 0 | 0 |

#### glm-4.6v-flash/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 1 | 0 | 0 | 1 | 0 | 1 |
| metal | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 6 | 4 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 4 | 0 | 0 |

#### glm-4.6v-flash/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### glm-4.6v-flash/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 3 | 0 | 1 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 1 | 8 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

#### internvl3_5-14b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 2 | 1 | 0 | 0 | 0 |
| metal | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 9 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 2 | 3 | 0 | 0 |

#### internvl3_5-14b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 3 | 1 | 1 | 0 | 0 |
| metal | 0 | 3 | 2 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 6 | 4 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 3 | 2 | 0 | 0 |

#### internvl3_5-14b/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### internvl3_5-14b/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 0 | 1 | 2 | 0 | 0 |
| metal | 0 | 4 | 0 | 0 | 1 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 8 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

#### internvl3_5-14b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 4 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 4 | 0 | 1 | 0 |

#### internvl3_5-14b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 5 | 0 |
| metal | 0 | 0 | 3 | 0 | 0 | 2 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 9 | 0 | 1 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 4 | 0 |

#### internvl3_5-14b/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### internvl3_5-14b/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 1 | 0 | 0 | 4 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 3 | 0 | 0 | 0 |

#### internvl3_5-14b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 3 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 7 | 3 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 1 | 3 | 0 | 0 |

#### internvl3_5-14b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 2 | 2 | 1 | 0 | 0 |
| metal | 0 | 0 | 3 | 1 | 1 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 8 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 2 | 3 | 0 | 0 |

#### internvl3_5-14b/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### internvl3_5-14b/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 1 | 2 | 1 | 0 | 0 |
| metal | 0 | 1 | 3 | 0 | 1 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 4 | 6 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 3 | 2 | 0 | 0 |

#### internvl3_5-8b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 2 | 2 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 3 | 7 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 3 | 0 | 2 | 0 | 0 |

#### internvl3_5-8b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 1 | 0 | 1 | 1 | 0 | 0 |
| metal | 0 | 1 | 3 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 2 | 8 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 2 | 1 | 0 | 0 |

#### internvl3_5-8b/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### internvl3_5-8b/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| metal | 0 | 2 | 3 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 4 | 4 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 4 | 1 | 0 | 0 | 0 |

#### internvl3_5-8b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 1 | 0 | 1 | 0 | 1 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### internvl3_5-8b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 0 | 0 | 0 | 3 | 0 |
| metal | 0 | 0 | 2 | 0 | 0 | 3 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 2 | 0 | 3 | 0 |

#### internvl3_5-8b/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### internvl3_5-8b/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 0 | 3 | 0 | 0 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 3 | 0 | 0 | 0 |

#### internvl3_5-8b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 1 | 3 | 0 | 0 |

#### internvl3_5-8b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 1 | 2 | 1 | 0 | 0 |
| metal | 0 | 0 | 4 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 6 | 4 | 0 | 0 |
| book_paper_cover | 0 | 0 | 3 | 2 | 0 | 0 | 0 |

#### internvl3_5-8b/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### internvl3_5-8b/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| metal | 0 | 0 | 4 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 2 | 4 | 4 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 2 | 1 | 0 | 0 |

#### llava-onevision-7b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 2 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 9 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### llava-onevision-7b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 4 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 4 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 3 | 2 | 0 | 0 |

#### llava-onevision-7b/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### llava-onevision-7b/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 4 | 1 | 0 | 0 |
| metal | 0 | 0 | 3 | 1 | 1 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 5 | 5 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### llava-onevision-7b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 3 | 1 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### llava-onevision-7b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 0 | 0 | 0 | 3 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 4 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 8 | 0 | 2 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 4 | 0 |

#### llava-onevision-7b/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

#### llava-onevision-7b/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 2 | 0 | 2 | 0 |
| metal | 0 | 2 | 1 | 1 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### llava-onevision-7b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 3 | 2 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 4 | 6 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 4 | 0 | 0 | 0 |

#### llava-onevision-7b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 3 | 0 | 2 | 0 |
| metal | 0 | 0 | 4 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### llava-onevision-7b/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### llava-onevision-7b/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 3 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 4 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 4 | 0 | 0 | 0 |

#### qwen3.8-27b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 5 | 5 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### qwen3.8-27b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 0 | 0 | 3 | 0 | 0 |
| metal | 0 | 1 | 3 | 0 | 1 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 9 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### qwen3.8-27b/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3.8-27b/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 1 | 0 | 0 | 3 | 0 | 0 |
| metal | 0 | 2 | 3 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 10 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### qwen3.8-27b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 2 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 2 | 0 | 2 | 0 |

#### qwen3.8-27b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 3 | 0 | 0 | 0 | 2 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 3 | 0 | 0 | 0 |

#### qwen3.8-27b/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### qwen3.8-27b/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 4 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 5 | 0 | 0 | 0 |

#### qwen3.8-27b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 3 | 1 | 1 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 5 | 5 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 4 | 0 | 0 |

#### qwen3.8-27b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 2 | 2 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 7 | 3 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### qwen3.8-27b/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3.8-27b/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 4 | 0 | 1 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 5 | 4 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 1 | 2 | 0 | 0 |

#### qwen3vl-8b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 2 | 2 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 9 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

#### qwen3vl-8b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 3 | 1 | 0 | 1 | 0 | 0 |
| metal | 0 | 1 | 3 | 0 | 1 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 3 | 7 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### qwen3vl-8b/v1/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3vl-8b/v1/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 4 | 0 | 1 | 0 | 0 |
| metal | 0 | 1 | 4 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 8 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

#### qwen3vl-8b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 2 | 2 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 3 | 1 | 0 | 0 |

#### qwen3vl-8b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 3 | 0 | 0 | 0 | 2 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 7 | 0 | 3 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 5 | 0 |

#### qwen3vl-8b/v2/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

#### qwen3vl-8b/v2/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 2 | 1 | 0 | 0 | 2 | 0 |
| metal | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 2 | 3 | 0 | 0 | 0 |

#### qwen3vl-8b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 1 | 1 | 3 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 9 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 5 | 0 | 0 |

#### qwen3vl-8b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 7 | 3 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 2 | 3 | 0 | 0 |

#### qwen3vl-8b/v3/multiview

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3vl-8b/v3/outline

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 4 | 0 | 1 | 0 | 0 |
| metal | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 3 | 7 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 4 | 0 | 0 |

## smoke (sanity check)

### Accuracy and macro F1 per condition

| model | variant | n | accuracy | exact_label_rate | parse_failures | photo acc | photo macro_f1 | mean_latency_s | run |
|---|---|---|---|---|---|---|---|---|---|
| dummy | v2 | 18 | 0.111 | 1.0 | 0 | 0.111 | 0.083 | 0.0 | 20261014T123349Z |
| dummy | v3 | 18 | 0.056 | 1.0 | 0 | 0.056 | 0.033 | 0.0 | 20261014T123349Z |
| gemma4-31b | v1 | 18 | 0.889 | 1.0 | 0 | 0.889 | 0.847 | 0.33 | 20261014T214733Z |
| gemma4-31b | v2 | 18 | 0.667 | 0.556 | 0 | 0.667 | 0.563 | 1.47 | 20261014T214925Z |
| gemma4-31b | v3 | 18 | 0.889 | 1.0 | 0 | 0.889 | 0.847 | 6.42 | 20261014T215150Z |
| glm-4.6v-flash | v1 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.75 | 0.0 | 20261014T224037Z |
| glm-4.6v-flash | v2 | 18 | 0.611 | 0.556 | 0 | 0.611 | 0.5 | 0.0 | 20261014T224139Z |
| glm-4.6v-flash | v3 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.75 | 18.54 | 20261014T223220Z |
| internvl3_5-14b | v1 | 18 | 0.778 | 1.0 | 0 | 0.778 | 0.713 | 0.72 | 20261014T214428Z |
| internvl3_5-14b | v2 | 18 | 0.611 | 0.556 | 0 | 0.611 | 0.5 | 1.4 | 20261014T214713Z |
| internvl3_5-14b | v3 | 18 | 0.778 | 1.0 | 0 | 0.778 | 0.707 | 4.06 | 20261014T214931Z |
| internvl3_5-8b | v1 | 18 | 0.667 | 1.0 | 0 | 0.667 | 0.613 | 0.78 | 20261014T214428Z |
| internvl3_5-8b | v2 | 18 | 0.556 | 0.556 | 0 | 0.556 | 0.467 | 1.34 | 20261014T214605Z |
| internvl3_5-8b | v3 | 18 | 0.667 | 1.0 | 0 | 0.667 | 0.613 | 3.87 | 20261014T214646Z |
| llava-onevision-7b | v1 | 18 | 0.722 | 1.0 | 0 | 0.722 | 0.68 | 0.44 | 20261014T214428Z |
| llava-onevision-7b | v2 | 18 | 0.556 | 0.667 | 0 | 0.556 | 0.447 | 0.83 | 20261014T214550Z |
| llava-onevision-7b | v3 | 18 | 0.611 | 1.0 | 0 | 0.611 | 0.513 | 3.03 | 20261014T214616Z |
| qwen3.8-27b | v1 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.8 | 0.4 | 20261014T214628Z |
| qwen3.8-27b | v2 | 18 | 0.556 | 0.167 | 0 | 0.556 | 0.427 | 1.39 | 20261014T214850Z |
| qwen3.8-27b | v3 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.793 | 10.32 | 20261014T215107Z |
| qwen3vl-8b | v1 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.78 | 0.23 | 20261014T214428Z |
| qwen3vl-8b | v2 | 18 | 0.556 | 0.222 | 0 | 0.556 | 0.433 | 0.71 | 20261014T214549Z |
| qwen3vl-8b | v3 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.78 | 5.32 | 20261014T214611Z |

### Agreement across prompt variants

| model | variants | n_common | all_agree | fleiss_kappa | agree v1-v2 | agree v1-v3 | agree v2-v3 |
|---|---|---|---|---|---|---|---|
| dummy | v1,v2,v3 | 0 |  |  |  |  |  |
| gemma4-31b | v1,v2,v3 | 18 | 0.778 | 0.833 | 0.778 | 1.0 | 0.778 |
| glm-4.6v-flash | v1,v2,v3 | 18 | 0.778 | 0.83 | 0.778 | 1.0 | 0.778 |
| internvl3_5-14b | v1,v2,v3 | 18 | 0.611 | 0.704 | 0.611 | 0.889 | 0.722 |
| internvl3_5-8b | v1,v2,v3 | 18 | 0.778 | 0.83 | 0.778 | 1.0 | 0.778 |
| llava-onevision-7b | v1,v2,v3 | 18 | 0.778 | 0.824 | 0.833 | 0.778 | 0.944 |
| qwen3.8-27b | v1,v2,v3 | 18 | 0.611 | 0.706 | 0.611 | 0.889 | 0.722 |
| qwen3vl-8b | v1,v2,v3 | 18 | 0.667 | 0.748 | 0.667 | 1.0 | 0.667 |

### Per material recall (which materials are recognisable at all)

| model | variant | condition | material | support | recall | precision | f1 |
|---|---|---|---|---|---|---|---|
| dummy | v2 | photo | book_paper_cover | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v2 | photo | cardboard | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v2 | photo | ceramic | 2 | 0.5 | 0.25 | 0.333 |
| dummy | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| dummy | v2 | photo | glass | 2 | 0.0 |  | 0.0 |
| dummy | v2 | photo | metal | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| dummy | v2 | photo | plastic | 1 | 1.0 | 0.333 | 0.5 |
| dummy | v2 | photo | rubber | 1 | 0.0 |  | 0.0 |
| dummy | v2 | photo | wood | 2 | 0.0 |  | 0.0 |
| dummy | v3 | photo | book_paper_cover | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | photo | cardboard | 2 | 0.5 | 0.25 | 0.333 |
| dummy | v3 | photo | ceramic | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | photo | foam | 2 | 0.0 |  | 0.0 |
| dummy | v3 | photo | glass | 2 | 0.0 |  | 0.0 |
| dummy | v3 | photo | metal | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| dummy | v3 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v3 | photo | rubber | 1 | 0.0 |  | 0.0 |
| dummy | v3 | photo | wood | 2 | 0.0 |  | 0.0 |
| gemma4-31b | v1 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | photo | foam | 2 | 0.5 | 1.0 | 0.667 |
| gemma4-31b | v1 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| gemma4-31b | v1 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| gemma4-31b | v2 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v2 | photo | foam | 2 | 0.5 | 1.0 | 0.667 |
| gemma4-31b | v2 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| gemma4-31b | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| gemma4-31b | v2 | photo | plastic | 1 | 1.0 | 0.333 | 0.5 |
| gemma4-31b | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | foam | 2 | 0.5 | 1.0 | 0.667 |
| gemma4-31b | v3 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| gemma4-31b | v3 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| gemma4-31b | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| gemma4-31b | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | foam | 2 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v1 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v1 | photo | plastic | 1 | 1.0 | 0.333 | 0.5 |
| glm-4.6v-flash | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| glm-4.6v-flash | v2 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v2 | photo | plastic | 1 | 1.0 | 0.2 | 0.333 |
| glm-4.6v-flash | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | foam | 2 | 0.0 |  | 0.0 |
| glm-4.6v-flash | v3 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| glm-4.6v-flash | v3 | photo | plastic | 1 | 1.0 | 0.333 | 0.5 |
| glm-4.6v-flash | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| glm-4.6v-flash | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v1 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v1 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v1 | photo | foam | 2 | 0.0 |  | 0.0 |
| internvl3_5-14b | v1 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v1 | photo | metal | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-14b | v1 | photo | ping_pong_plastic | 2 | 1.0 | 0.667 | 0.8 |
| internvl3_5-14b | v1 | photo | plastic | 1 | 1.0 | 0.5 | 0.667 |
| internvl3_5-14b | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-14b | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| internvl3_5-14b | v2 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| internvl3_5-14b | v2 | photo | plastic | 1 | 1.0 | 0.2 | 0.333 |
| internvl3_5-14b | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-14b | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v3 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v3 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v3 | photo | foam | 2 | 0.0 |  | 0.0 |
| internvl3_5-14b | v3 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v3 | photo | metal | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-14b | v3 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-14b | v3 | photo | plastic | 1 | 1.0 | 0.25 | 0.4 |
| internvl3_5-14b | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-14b | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v1 | photo | book_paper_cover | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-8b | v1 | photo | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| internvl3_5-8b | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v1 | photo | foam | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v1 | photo | metal | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-8b | v1 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v1 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| internvl3_5-8b | v2 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v3 | photo | book_paper_cover | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-8b | v3 | photo | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| internvl3_5-8b | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v3 | photo | foam | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | photo | glass | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v3 | photo | metal | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-8b | v3 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v3 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | photo | foam | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v1 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| llava-onevision-7b | v2 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | photo | plastic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v3 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| llava-onevision-7b | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v3 | photo | foam | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v3 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v3 | photo | ping_pong_plastic | 2 | 0.5 | 1.0 | 0.667 |
| llava-onevision-7b | v3 | photo | plastic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | photo | foam | 2 | 0.5 | 1.0 | 0.667 |
| qwen3.8-27b | v1 | photo | glass | 2 | 1.0 | 0.5 | 0.667 |
| qwen3.8-27b | v1 | photo | metal | 2 | 0.5 | 1.0 | 0.667 |
| qwen3.8-27b | v1 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| qwen3.8-27b | v2 | photo | ceramic | 2 | 1.0 | 0.667 | 0.8 |
| qwen3.8-27b | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| qwen3.8-27b | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| qwen3.8-27b | v2 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | photo | book_paper_cover | 2 | 0.5 | 1.0 | 0.667 |
| qwen3.8-27b | v3 | photo | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| qwen3.8-27b | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | photo | foam | 2 | 0.5 | 1.0 | 0.667 |
| qwen3.8-27b | v3 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| qwen3.8-27b | v3 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| qwen3.8-27b | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| qwen3.8-27b | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | foam | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| qwen3vl-8b | v1 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v1 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v2 | photo | book_paper_cover | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | photo | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| qwen3vl-8b | v2 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v2 | photo | foam | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | photo | glass | 2 | 1.0 | 0.5 | 0.667 |
| qwen3vl-8b | v2 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v2 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v2 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v2 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | book_paper_cover | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | ceramic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | foam | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | photo | glass | 2 | 1.0 | 0.667 | 0.8 |
| qwen3vl-8b | v3 | photo | metal | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | ping_pong_plastic | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | plastic | 1 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | photo | rubber | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v3 | photo | wood | 2 | 1.0 | 1.0 | 1.0 |

### Confusion matrices

#### dummy/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| wood | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| glass | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| cardboard | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| book_paper_cover | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### dummy/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| metal | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| foam | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### gemma4-31b/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### gemma4-31b/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### gemma4-31b/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### glm-4.6v-flash/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### glm-4.6v-flash/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### glm-4.6v-flash/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### internvl3_5-14b/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### internvl3_5-14b/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### internvl3_5-14b/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### internvl3_5-8b/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### internvl3_5-8b/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### internvl3_5-8b/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### llava-onevision-7b/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### llava-onevision-7b/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### llava-onevision-7b/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### qwen3.8-27b/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### qwen3.8-27b/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### qwen3.8-27b/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### qwen3vl-8b/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### qwen3vl-8b/v2/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

#### qwen3vl-8b/v3/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Runs

| experiment | model | variant | run | commit | dirty | template_sha256 | hostname | slurm_job_id | backend_model |
|---|---|---|---|---|---|---|---|---|---|
| exp1 | dummy | v1 | 20261014T214232Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | int5.local.snellius.surf.nl |  | dummy |
| exp1 | dummy | v2 | 20261014T123349Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 958a9e9ec6a8 | int4.local.snellius.surf.nl |  | dummy |
| exp1 | dummy | v3 | 20261014T123349Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 2b3d48ffff02 | int4.local.snellius.surf.nl |  | dummy |
| exp1 | gemma4-31b | v1 | 20261014T214733Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn126.local.snellius.surf.nl | 28094248 | google/gemma-4-31B-it |
| exp1 | gemma4-31b | v2 | 20261014T214925Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn126.local.snellius.surf.nl | 28094248 | google/gemma-4-31B-it |
| exp1 | gemma4-31b | v3 | 20261014T215150Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn126.local.snellius.surf.nl | 28094248 | google/gemma-4-31B-it |
| exp1 | glm-4.6v-flash | v1 | 20261014T224037Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn15.local.snellius.surf.nl | 28094839 | zai-org/GLM-4.6V-Flash |
| exp1 | glm-4.6v-flash | v2 | 20261014T224139Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn15.local.snellius.surf.nl | 28094839 | zai-org/GLM-4.6V-Flash |
| exp1 | glm-4.6v-flash | v3 | 20261014T223220Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn23.local.snellius.surf.nl | 28094506 | zai-org/GLM-4.6V-Flash |
| exp1 | internvl3_5-14b | v1 | 20261014T214428Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn32.local.snellius.surf.nl | 28094246 | OpenGVLab/InternVL3_5-14B-HF |
| exp1 | internvl3_5-14b | v2 | 20261014T214713Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn32.local.snellius.surf.nl | 28094246 | OpenGVLab/InternVL3_5-14B-HF |
| exp1 | internvl3_5-14b | v3 | 20261014T214931Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn32.local.snellius.surf.nl | 28094246 | OpenGVLab/InternVL3_5-14B-HF |
| exp1 | internvl3_5-8b | v1 | 20261014T214428Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn23.local.snellius.surf.nl | 28094244 | OpenGVLab/InternVL3_5-8B-HF |
| exp1 | internvl3_5-8b | v2 | 20261014T214605Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn23.local.snellius.surf.nl | 28094244 | OpenGVLab/InternVL3_5-8B-HF |
| exp1 | internvl3_5-8b | v3 | 20261014T214646Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn23.local.snellius.surf.nl | 28094244 | OpenGVLab/InternVL3_5-8B-HF |
| exp1 | llava-onevision-7b | v1 | 20261014T214428Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn28.local.snellius.surf.nl | 28094245 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1 | llava-onevision-7b | v2 | 20261014T214550Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn28.local.snellius.surf.nl | 28094245 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1 | llava-onevision-7b | v3 | 20261014T214616Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn28.local.snellius.surf.nl | 28094245 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1 | qwen3.8-27b | v1 | 20261014T214628Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn113.local.snellius.surf.nl | 28094247 | Qwen/Qwen3.8-27B |
| exp1 | qwen3.8-27b | v2 | 20261014T214850Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn113.local.snellius.surf.nl | 28094247 | Qwen/Qwen3.8-27B |
| exp1 | qwen3.8-27b | v3 | 20261014T215107Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn113.local.snellius.surf.nl | 28094247 | Qwen/Qwen3.8-27B |
| exp1 | qwen3vl-8b | v1 | 20261014T214428Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 880c81b387b5 | gcn23.local.snellius.surf.nl | 28094243 | Qwen/Qwen3-VL-8B-Instruct |
| exp1 | qwen3vl-8b | v2 | 20261014T214549Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 958a9e9ec6a8 | gcn23.local.snellius.surf.nl | 28094243 | Qwen/Qwen3-VL-8B-Instruct |
| exp1 | qwen3vl-8b | v3 | 20261014T214611Z | 488c3710eb3ef4214d168f31ff97e1177897487e | True | 2b3d48ffff02 | gcn23.local.snellius.surf.nl | 28094243 | Qwen/Qwen3-VL-8B-Instruct |
