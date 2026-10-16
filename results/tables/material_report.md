# Material recognition: overview of Experiments 1.0, 1.1 and 1.2

Per model and answer mode (direct: answer only; reasoning: a short reasoning step first). Identification (1.0) names the material; yes/no and two options (1.1) verify a named material; matching (1.2) tells two objects apart. Consistency columns compare a task's answers with the model's own 1.0 label for the same object and view, right or wrong. Chance: identification 0.2 (five labels), yes/no balanced accuracy 0.5, two options 0.5, matching 0.5. Views: identification is over all its views (frame, crop, outline, multiview), yes/no over frames and crops, two options and matching over crops.

## sim_realistic (benchmark)

| model | mode | identify acc | yes/no bal. acc | yes rate | two options acc | matching acc | matching solved | yes/no vs 1.0 | two options vs 1.0 | matching vs 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | direct | 0.713 | 0.695 | 0.088 | 0.92 | 1.0 | 1.0 | 0.872 | 0.976 | 1.0 |
| gemma4-31b | reasoning | 0.675 |  |  |  |  |  |  |  |  |
| glm-4.6v-flash | direct | 0.863 | 0.818 | 0.232 | 0.97 | 0.986 | 0.944 | 0.88 | 0.969 | 0.991 |
| glm-4.6v-flash | reasoning | 0.738 |  |  |  |  |  |  |  |  |
| internvl3_5-14b | direct | 0.588 | 0.757 | 0.288 | 0.885 | 0.936 | 0.867 | 0.84 | 0.921 | 0.972 |
| internvl3_5-14b | reasoning | 0.512 |  |  |  |  |  |  |  |  |
| internvl3_5-8b | direct | 0.725 | 0.723 | 0.304 | 0.88 | 0.969 | 0.889 | 0.784 | 0.912 | 0.974 |
| internvl3_5-8b | reasoning | 0.6 |  |  |  |  |  |  |  |  |
| llava-onevision-7b | direct | 0.65 | 0.745 | 0.128 | 0.92 | 0.992 | 0.967 | 0.872 | 0.945 | 1.0 |
| llava-onevision-7b | reasoning | 0.575 |  |  |  |  |  |  |  |  |
| qwen3.8-27b | direct | 0.6 | 0.72 | 0.088 | 0.9 | 1.0 | 1.0 | 0.872 | 0.943 | 1.0 |
| qwen3.8-27b | reasoning | 0.688 |  |  |  |  |  |  |  |  |
| qwen3vl-8b | direct | 0.625 | 0.782 | 0.208 | 0.83 | 0.997 | 0.989 | 0.792 | 0.918 | 0.996 |
| qwen3vl-8b | reasoning | 0.637 |  |  |  |  |  |  |  |  |

## sim_preview (comparison)

| model | mode | identify acc | yes/no bal. acc | yes rate | two options acc | matching acc | matching solved | yes/no vs 1.0 | two options vs 1.0 | matching vs 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | direct | 0.637 |  |  |  |  |  |  |  |  |
| gemma4-31b | reasoning | 0.6 |  |  |  |  |  |  |  |  |
| glm-4.6v-flash | direct | 0.637 |  |  |  |  |  |  |  |  |
| glm-4.6v-flash | reasoning | 0.512 |  |  |  |  |  |  |  |  |
| internvl3_5-14b | direct | 0.438 |  |  |  |  |  |  |  |  |
| internvl3_5-14b | reasoning | 0.375 |  |  |  |  |  |  |  |  |
| internvl3_5-8b | direct | 0.412 |  |  |  |  |  |  |  |  |
| internvl3_5-8b | reasoning | 0.312 |  |  |  |  |  |  |  |  |
| llava-onevision-7b | direct | 0.475 |  |  |  |  |  |  |  |  |
| llava-onevision-7b | reasoning | 0.338 |  |  |  |  |  |  |  |  |
| qwen3.8-27b | direct | 0.4 |  |  |  |  |  |  |  |  |
| qwen3.8-27b | reasoning | 0.45 |  |  |  |  |  |  |  |  |
| qwen3vl-8b | direct | 0.388 |  |  |  |  |  |  |  |  |
| qwen3vl-8b | reasoning | 0.438 |  |  |  |  |  |  |  |  |

## smoke (sanity check)

| model | mode | identify acc | yes/no bal. acc | yes rate | two options acc | matching acc | matching solved | yes/no vs 1.0 | two options vs 1.0 | matching vs 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-31b | direct | 0.889 | 0.958 | 0.211 | 0.993 | 1.0 | 1.0 | 0.967 | 1.0 | 1.0 |
| gemma4-31b | reasoning | 0.889 |  |  |  |  |  |  |  |  |
| glm-4.6v-flash | direct | 0.833 | 0.951 | 0.278 | 0.986 | 1.0 | 1.0 | 0.9 | 0.992 | 1.0 |
| glm-4.6v-flash | reasoning | 0.778 |  |  |  |  |  |  |  |  |
| internvl3_5-14b | direct | 0.778 | 0.896 | 0.256 | 0.951 | 0.994 | 0.975 | 0.9 | 0.922 | 1.0 |
| internvl3_5-14b | reasoning | 0.778 |  |  |  |  |  |  |  |  |
| internvl3_5-8b | direct | 0.667 | 0.958 | 0.267 | 0.965 | 0.994 | 0.975 | 0.878 | 1.0 | 1.0 |
| internvl3_5-8b | reasoning | 0.667 |  |  |  |  |  |  |  |  |
| llava-onevision-7b | direct | 0.722 | 0.951 | 0.278 | 0.944 | 0.981 | 0.95 | 0.9 | 1.0 | 1.0 |
| llava-onevision-7b | reasoning | 0.611 |  |  |  |  |  |  |  |  |
| qwen3.8-27b | direct | 0.833 | 0.91 | 0.178 | 0.979 | 0.994 | 0.975 | 0.944 | 0.952 | 0.993 |
| qwen3.8-27b | reasoning | 0.833 |  |  |  |  |  |  |  |  |
| qwen3vl-8b | direct | 0.833 | 0.938 | 0.244 | 0.958 | 0.988 | 0.95 | 0.933 | 0.984 | 1.0 |
| qwen3vl-8b | reasoning | 0.833 |  |  |  |  |  |  |  |  |
