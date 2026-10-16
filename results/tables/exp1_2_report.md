# Experiment 1.2: material matching between two objects

Latest finished run per model and variant under `/projects/prjs2306/morpheus/results/vlm-scene-understanding`.

Each pair is asked in four forms (both image orders, both asked materials). Chance accuracy is 0.5; the solved rate counts pairs with all four forms right; an A rate away from 0.5 is a position bias. No number mixes datasets.

## sim_realistic (benchmark)

| model | variant | n | pairs | accuracy | solved_rate | a_rate | image_order_consistency | label_consistency | parse_failures | separate acc | sidebyside acc | run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | v1 | 360 | 90 | 1.0 | 1.0 | 0.5 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | 20261016T094445Z |
| glm-4.6v-flash | v1 | 360 | 90 | 0.986 | 0.944 | 0.514 | 0.972 | 0.972 | 0 | 0.983 | 0.989 | 20261016T094552Z |
| internvl3_5-14b | v1 | 360 | 90 | 0.936 | 0.867 | 0.514 | 0.95 | 0.906 | 0 | 0.944 | 0.928 | 20261016T094430Z |
| internvl3_5-8b | v1 | 360 | 90 | 0.969 | 0.889 | 0.469 | 0.939 | 0.939 | 0 | 0.972 | 0.967 | 20261016T094030Z |
| llava-onevision-7b | v1 | 360 | 90 | 0.992 | 0.967 | 0.497 | 0.983 | 0.983 | 0 | 0.983 | 1.0 | 20261016T094039Z |
| qwen3.8-27b | v1 | 360 | 90 | 1.0 | 1.0 | 0.5 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | 20261016T095219Z |
| qwen3vl-8b | v1 | 360 | 90 | 0.997 | 0.989 | 0.497 | 0.994 | 0.994 | 0 | 0.994 | 1.0 | 20261016T093937Z |

### Accuracy per pair of materials

| model | variant | materials | accuracy |
|---|---|---|---|
| gemma4-31b | v1 | book_paper_cover vs cardboard | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs ceramic | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs metal | 1.0 |
| gemma4-31b | v1 | cardboard vs ceramic | 1.0 |
| gemma4-31b | v1 | cardboard vs metal | 1.0 |
| gemma4-31b | v1 | ceramic vs metal | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs cardboard | 0.938 |
| glm-4.6v-flash | v1 | book_paper_cover vs ceramic | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs metal | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs ceramic | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs metal | 1.0 |
| glm-4.6v-flash | v1 | ceramic vs metal | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs cardboard | 0.713 |
| internvl3_5-14b | v1 | book_paper_cover vs ceramic | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs metal | 1.0 |
| internvl3_5-14b | v1 | cardboard vs ceramic | 1.0 |
| internvl3_5-14b | v1 | cardboard vs metal | 1.0 |
| internvl3_5-14b | v1 | ceramic vs metal | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs cardboard | 0.887 |
| internvl3_5-8b | v1 | book_paper_cover vs ceramic | 0.975 |
| internvl3_5-8b | v1 | book_paper_cover vs metal | 0.975 |
| internvl3_5-8b | v1 | cardboard vs ceramic | 1.0 |
| internvl3_5-8b | v1 | cardboard vs metal | 1.0 |
| internvl3_5-8b | v1 | ceramic vs metal | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs cardboard | 0.975 |
| llava-onevision-7b | v1 | book_paper_cover vs ceramic | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs metal | 1.0 |
| llava-onevision-7b | v1 | cardboard vs ceramic | 0.988 |
| llava-onevision-7b | v1 | cardboard vs metal | 1.0 |
| llava-onevision-7b | v1 | ceramic vs metal | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs cardboard | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs ceramic | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs metal | 1.0 |
| qwen3.8-27b | v1 | cardboard vs ceramic | 1.0 |
| qwen3.8-27b | v1 | cardboard vs metal | 1.0 |
| qwen3.8-27b | v1 | ceramic vs metal | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs cardboard | 0.988 |
| qwen3vl-8b | v1 | book_paper_cover vs ceramic | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs metal | 1.0 |
| qwen3vl-8b | v1 | cardboard vs ceramic | 1.0 |
| qwen3vl-8b | v1 | cardboard vs metal | 1.0 |
| qwen3vl-8b | v1 | ceramic vs metal | 1.0 |

## smoke (sanity check)

| model | variant | n | pairs | accuracy | solved_rate | a_rate | image_order_consistency | label_consistency | parse_failures | separate acc | sidebyside acc | run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | v1 | 160 | 40 | 1.0 | 1.0 | 0.5 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | 20261016T094445Z |
| glm-4.6v-flash | v1 | 160 | 40 | 1.0 | 1.0 | 0.5 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | 20261016T094552Z |
| internvl3_5-14b | v1 | 160 | 40 | 0.994 | 0.975 | 0.506 | 0.988 | 0.988 | 0 | 1.0 | 0.988 | 20261016T094430Z |
| internvl3_5-8b | v1 | 160 | 40 | 0.994 | 0.975 | 0.494 | 0.988 | 0.988 | 0 | 1.0 | 0.988 | 20261016T094030Z |
| llava-onevision-7b | v1 | 160 | 40 | 0.981 | 0.95 | 0.506 | 0.988 | 0.963 | 0 | 0.988 | 0.975 | 20261016T094039Z |
| qwen3.8-27b | v1 | 160 | 40 | 0.994 | 0.975 | 0.506 | 0.988 | 0.988 | 0 | 1.0 | 0.988 | 20261016T095219Z |
| qwen3vl-8b | v1 | 160 | 40 | 0.988 | 0.95 | 0.512 | 0.975 | 0.975 | 0 | 0.988 | 0.988 | 20261016T093937Z |

### Accuracy per pair of materials

| model | variant | materials | accuracy |
|---|---|---|---|
| gemma4-31b | v1 | book_paper_cover vs cardboard | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs ceramic | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs glass | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs metal | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| gemma4-31b | v1 | book_paper_cover vs rubber | 1.0 |
| gemma4-31b | v1 | cardboard vs foam | 1.0 |
| gemma4-31b | v1 | cardboard vs glass | 1.0 |
| gemma4-31b | v1 | cardboard vs metal | 1.0 |
| gemma4-31b | v1 | cardboard vs ping_pong_plastic | 1.0 |
| gemma4-31b | v1 | cardboard vs wood | 1.0 |
| gemma4-31b | v1 | ceramic vs glass | 1.0 |
| gemma4-31b | v1 | ceramic vs ping_pong_plastic | 1.0 |
| gemma4-31b | v1 | ceramic vs plastic | 1.0 |
| gemma4-31b | v1 | foam vs metal | 1.0 |
| gemma4-31b | v1 | foam vs ping_pong_plastic | 1.0 |
| gemma4-31b | v1 | glass vs wood | 1.0 |
| gemma4-31b | v1 | metal vs wood | 1.0 |
| gemma4-31b | v1 | ping_pong_plastic vs wood | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs cardboard | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs ceramic | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs glass | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs metal | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| glm-4.6v-flash | v1 | book_paper_cover vs rubber | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs foam | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs glass | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs metal | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs ping_pong_plastic | 1.0 |
| glm-4.6v-flash | v1 | cardboard vs wood | 1.0 |
| glm-4.6v-flash | v1 | ceramic vs glass | 1.0 |
| glm-4.6v-flash | v1 | ceramic vs ping_pong_plastic | 1.0 |
| glm-4.6v-flash | v1 | ceramic vs plastic | 1.0 |
| glm-4.6v-flash | v1 | foam vs metal | 1.0 |
| glm-4.6v-flash | v1 | foam vs ping_pong_plastic | 1.0 |
| glm-4.6v-flash | v1 | glass vs wood | 1.0 |
| glm-4.6v-flash | v1 | metal vs wood | 1.0 |
| glm-4.6v-flash | v1 | ping_pong_plastic vs wood | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs cardboard | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs ceramic | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs glass | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs metal | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| internvl3_5-14b | v1 | book_paper_cover vs rubber | 0.875 |
| internvl3_5-14b | v1 | cardboard vs foam | 1.0 |
| internvl3_5-14b | v1 | cardboard vs glass | 1.0 |
| internvl3_5-14b | v1 | cardboard vs metal | 1.0 |
| internvl3_5-14b | v1 | cardboard vs ping_pong_plastic | 1.0 |
| internvl3_5-14b | v1 | cardboard vs wood | 1.0 |
| internvl3_5-14b | v1 | ceramic vs glass | 1.0 |
| internvl3_5-14b | v1 | ceramic vs ping_pong_plastic | 1.0 |
| internvl3_5-14b | v1 | ceramic vs plastic | 1.0 |
| internvl3_5-14b | v1 | foam vs metal | 1.0 |
| internvl3_5-14b | v1 | foam vs ping_pong_plastic | 1.0 |
| internvl3_5-14b | v1 | glass vs wood | 1.0 |
| internvl3_5-14b | v1 | metal vs wood | 1.0 |
| internvl3_5-14b | v1 | ping_pong_plastic vs wood | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs cardboard | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs ceramic | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs glass | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs metal | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| internvl3_5-8b | v1 | book_paper_cover vs rubber | 1.0 |
| internvl3_5-8b | v1 | cardboard vs foam | 1.0 |
| internvl3_5-8b | v1 | cardboard vs glass | 1.0 |
| internvl3_5-8b | v1 | cardboard vs metal | 1.0 |
| internvl3_5-8b | v1 | cardboard vs ping_pong_plastic | 1.0 |
| internvl3_5-8b | v1 | cardboard vs wood | 1.0 |
| internvl3_5-8b | v1 | ceramic vs glass | 1.0 |
| internvl3_5-8b | v1 | ceramic vs ping_pong_plastic | 1.0 |
| internvl3_5-8b | v1 | ceramic vs plastic | 0.875 |
| internvl3_5-8b | v1 | foam vs metal | 1.0 |
| internvl3_5-8b | v1 | foam vs ping_pong_plastic | 1.0 |
| internvl3_5-8b | v1 | glass vs wood | 1.0 |
| internvl3_5-8b | v1 | metal vs wood | 1.0 |
| internvl3_5-8b | v1 | ping_pong_plastic vs wood | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs cardboard | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs ceramic | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs glass | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs metal | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| llava-onevision-7b | v1 | book_paper_cover vs rubber | 1.0 |
| llava-onevision-7b | v1 | cardboard vs foam | 1.0 |
| llava-onevision-7b | v1 | cardboard vs glass | 1.0 |
| llava-onevision-7b | v1 | cardboard vs metal | 1.0 |
| llava-onevision-7b | v1 | cardboard vs ping_pong_plastic | 1.0 |
| llava-onevision-7b | v1 | cardboard vs wood | 1.0 |
| llava-onevision-7b | v1 | ceramic vs glass | 1.0 |
| llava-onevision-7b | v1 | ceramic vs ping_pong_plastic | 1.0 |
| llava-onevision-7b | v1 | ceramic vs plastic | 1.0 |
| llava-onevision-7b | v1 | foam vs metal | 1.0 |
| llava-onevision-7b | v1 | foam vs ping_pong_plastic | 0.625 |
| llava-onevision-7b | v1 | glass vs wood | 1.0 |
| llava-onevision-7b | v1 | metal vs wood | 1.0 |
| llava-onevision-7b | v1 | ping_pong_plastic vs wood | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs cardboard | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs ceramic | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs glass | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs metal | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| qwen3.8-27b | v1 | book_paper_cover vs rubber | 1.0 |
| qwen3.8-27b | v1 | cardboard vs foam | 1.0 |
| qwen3.8-27b | v1 | cardboard vs glass | 1.0 |
| qwen3.8-27b | v1 | cardboard vs metal | 1.0 |
| qwen3.8-27b | v1 | cardboard vs ping_pong_plastic | 1.0 |
| qwen3.8-27b | v1 | cardboard vs wood | 1.0 |
| qwen3.8-27b | v1 | ceramic vs glass | 1.0 |
| qwen3.8-27b | v1 | ceramic vs ping_pong_plastic | 1.0 |
| qwen3.8-27b | v1 | ceramic vs plastic | 0.875 |
| qwen3.8-27b | v1 | foam vs metal | 1.0 |
| qwen3.8-27b | v1 | foam vs ping_pong_plastic | 1.0 |
| qwen3.8-27b | v1 | glass vs wood | 1.0 |
| qwen3.8-27b | v1 | metal vs wood | 1.0 |
| qwen3.8-27b | v1 | ping_pong_plastic vs wood | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs cardboard | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs ceramic | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs glass | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs metal | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs ping_pong_plastic | 1.0 |
| qwen3vl-8b | v1 | book_paper_cover vs rubber | 1.0 |
| qwen3vl-8b | v1 | cardboard vs foam | 1.0 |
| qwen3vl-8b | v1 | cardboard vs glass | 1.0 |
| qwen3vl-8b | v1 | cardboard vs metal | 1.0 |
| qwen3vl-8b | v1 | cardboard vs ping_pong_plastic | 1.0 |
| qwen3vl-8b | v1 | cardboard vs wood | 1.0 |
| qwen3vl-8b | v1 | ceramic vs glass | 1.0 |
| qwen3vl-8b | v1 | ceramic vs ping_pong_plastic | 1.0 |
| qwen3vl-8b | v1 | ceramic vs plastic | 1.0 |
| qwen3vl-8b | v1 | foam vs metal | 1.0 |
| qwen3vl-8b | v1 | foam vs ping_pong_plastic | 0.75 |
| qwen3vl-8b | v1 | glass vs wood | 1.0 |
| qwen3vl-8b | v1 | metal vs wood | 1.0 |
| qwen3vl-8b | v1 | ping_pong_plastic vs wood | 1.0 |

## Runs

| experiment | model | variant | run | commit | dirty | template_sha256 | hostname | slurm_job_id | backend_model |
|---|---|---|---|---|---|---|---|---|---|
| exp1_2 | gemma4-31b | v1 | 20261016T094445Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn107.local.snellius.surf.nl | 28129326 | google/gemma-4-31B-it |
| exp1_2 | glm-4.6v-flash | v1 | 20261016T094552Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn57.local.snellius.surf.nl | 28129324 | zai-org/GLM-4.6V-Flash |
| exp1_2 | internvl3_5-14b | v1 | 20261016T094430Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn68.local.snellius.surf.nl | 28129323 | OpenGVLab/InternVL3_5-14B-HF |
| exp1_2 | internvl3_5-8b | v1 | 20261016T094030Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn68.local.snellius.surf.nl | 28129320 | OpenGVLab/InternVL3_5-8B-HF |
| exp1_2 | llava-onevision-7b | v1 | 20261016T094039Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn68.local.snellius.surf.nl | 28129322 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1_2 | qwen3.8-27b | v1 | 20261016T095219Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn107.local.snellius.surf.nl | 28129325 | Qwen/Qwen3.8-27B |
| exp1_2 | qwen3vl-8b | v1 | 20261016T093937Z | a428e66372e79c0847876010b81a31f37f994d85 | True | 81be58f26ad6 | gcn49.local.snellius.surf.nl | 28129319 | Qwen/Qwen3-VL-8B-Instruct |
