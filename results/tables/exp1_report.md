# Experiment 1: material recognition

Latest finished run per model and variant under `/projects/prjs2306/morpheus/results/vlm-scene-understanding`.

The **sim** dataset is the benchmark and the only one to quote. The smoke dataset is a sanity check that the pipeline works on real photos; its numbers are reported apart and never mixed with the benchmark.

## sim (benchmark)

### Accuracy and macro F1 per condition

| model | variant | n | accuracy | exact_label_rate | parse_failures | crop acc | crop macro_f1 | frame acc | frame macro_f1 | mean_latency_s | run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dummy | v1 | 10 | 0.0 | 1.0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 20261014T123348Z |
| dummy | v2 | 10 | 0.4 | 1.0 | 0 | 0.8 | 0.833 | 0.0 | 0.0 | 0.0 | 20261014T123349Z |
| dummy | v3 | 10 | 0.2 | 1.0 | 0 | 0.0 | 0.0 | 0.4 | 0.292 | 0.0 | 20261014T123349Z |
| internvl3_5-8b | v1 | 10 | 0.0 | 1.0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.38 | 20261014T123926Z |
| internvl3_5-8b | v2 | 10 | 0.4 | 0.4 | 0 | 0.4 | 0.2 | 0.4 | 0.25 | 0.88 | 20261014T124037Z |
| internvl3_5-8b | v3 | 10 | 0.1 | 1.0 | 0 | 0.2 | 0.167 | 0.0 | 0.0 | 3.37 | 20261014T124102Z |
| llava-onevision-7b | v1 | 10 | 0.5 | 1.0 | 0 | 0.4 | 0.333 | 0.6 | 0.45 | 0.5 | 20261014T123926Z |
| llava-onevision-7b | v2 | 10 | 0.2 | 0.6 | 0 | 0.4 | 0.2 | 0.0 | 0.0 | 0.88 | 20261014T124034Z |
| llava-onevision-7b | v3 | 10 | 0.4 | 0.9 | 0 | 0.4 | 0.2 | 0.4 | 0.167 | 3.33 | 20261014T124059Z |
| qwen3vl-8b | v1 | 10 | 0.5 | 1.0 | 0 | 0.6 | 0.5 | 0.4 | 0.292 | 0.21 | 20261014T123926Z |
| qwen3vl-8b | v2 | 10 | 0.4 | 0.2 | 0 | 0.4 | 0.2 | 0.4 | 0.25 | 0.7 | 20261014T124032Z |
| qwen3vl-8b | v3 | 10 | 0.5 | 1.0 | 0 | 0.6 | 0.5 | 0.4 | 0.2 | 4.92 | 20261014T124052Z |

### Agreement across prompt variants

| model | variants | n_common | all_agree | fleiss_kappa | agree v1-v2 | agree v1-v3 | agree v2-v3 |
|---|---|---|---|---|---|---|---|
| dummy | v1,v2,v3 | 10 | 0.0 | 0.06 | 0.3 | 0.4 | 0.1 |
| internvl3_5-8b | v1,v2,v3 | 10 | 0.4 | 0.298 | 0.4 | 0.7 | 0.5 |
| llava-onevision-7b | v1,v2,v3 | 10 | 0.3 | 0.292 | 0.4 | 0.6 | 0.5 |
| qwen3vl-8b | v1,v2,v3 | 10 | 0.4 | 0.416 | 0.4 | 0.6 | 0.7 |

### Per material recall (which materials are recognisable at all)

| model | variant | condition | material | support | recall | precision | f1 |
|---|---|---|---|---|---|---|---|
| dummy | v1 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| dummy | v1 | crop | cardboard | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | crop | ceramic | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | crop | metal | 1 | 0.0 |  | 0.0 |
| dummy | v1 | frame | book_paper_cover | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| dummy | v1 | frame | ceramic | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
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
| internvl3_5-8b | v1 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | crop | cardboard | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v1 | frame | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v1 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | crop | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| internvl3_5-8b | v2 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v2 | frame | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | frame | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| internvl3_5-8b | v2 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v2 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | crop | cardboard | 2 | 0.5 | 1.0 | 0.667 |
| internvl3_5-8b | v3 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | frame | book_paper_cover | 1 | 0.0 | 0.0 | 0.0 |
| internvl3_5-8b | v3 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| internvl3_5-8b | v3 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v1 | crop | book_paper_cover | 1 | 1.0 | 0.5 | 0.667 |
| llava-onevision-7b | v1 | crop | cardboard | 2 | 0.5 | 1.0 | 0.667 |
| llava-onevision-7b | v1 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v1 | frame | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| llava-onevision-7b | v1 | frame | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v1 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v1 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v2 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | crop | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v2 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v2 | frame | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v2 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v3 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | crop | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| llava-onevision-7b | v3 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| llava-onevision-7b | v3 | frame | book_paper_cover | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | frame | cardboard | 2 | 1.0 | 0.5 | 0.667 |
| llava-onevision-7b | v3 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| llava-onevision-7b | v3 | frame | metal | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | crop | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | crop | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v1 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v1 | frame | book_paper_cover | 1 | 1.0 | 0.333 | 0.5 |
| qwen3vl-8b | v1 | frame | cardboard | 2 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v1 | frame | metal | 1 | 1.0 | 0.5 | 0.667 |
| qwen3vl-8b | v2 | crop | book_paper_cover | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | crop | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| qwen3vl-8b | v2 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | crop | metal | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | frame | book_paper_cover | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | frame | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v2 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v2 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v3 | crop | book_paper_cover | 1 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | crop | cardboard | 2 | 1.0 | 1.0 | 1.0 |
| qwen3vl-8b | v3 | crop | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | crop | metal | 1 | 0.0 | 0.0 | 0.0 |
| qwen3vl-8b | v3 | frame | book_paper_cover | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | frame | cardboard | 2 | 1.0 | 0.667 | 0.8 |
| qwen3vl-8b | v3 | frame | ceramic | 1 | 0.0 |  | 0.0 |
| qwen3vl-8b | v3 | frame | metal | 1 | 0.0 | 0.0 | 0.0 |

### Confusion matrices

#### dummy/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### dummy/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| metal | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| book_paper_cover | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

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

#### internvl3_5-8b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

#### internvl3_5-8b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

#### internvl3_5-8b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### internvl3_5-8b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

#### internvl3_5-8b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

#### internvl3_5-8b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

#### llava-onevision-7b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### llava-onevision-7b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### llava-onevision-7b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### llava-onevision-7b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

#### llava-onevision-7b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### llava-onevision-7b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### qwen3vl-8b/v1/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3vl-8b/v1/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3vl-8b/v2/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

#### qwen3vl-8b/v2/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

#### qwen3vl-8b/v3/crop

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

#### qwen3vl-8b/v3/frame

| true \ predicted | ceramic | metal | plastic | cardboard | book_paper_cover | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

## smoke (sanity check)

### Accuracy and macro F1 per condition

| model | variant | n | accuracy | exact_label_rate | parse_failures | photo acc | photo macro_f1 | mean_latency_s | run |
|---|---|---|---|---|---|---|---|---|---|
| dummy | v1 | 18 | 0.056 | 1.0 | 0 | 0.056 | 0.04 | 0.0 | 20261014T123348Z |
| dummy | v2 | 18 | 0.111 | 1.0 | 0 | 0.111 | 0.083 | 0.0 | 20261014T123349Z |
| dummy | v3 | 18 | 0.056 | 1.0 | 0 | 0.056 | 0.033 | 0.0 | 20261014T123349Z |
| internvl3_5-8b | v1 | 18 | 0.667 | 1.0 | 0 | 0.667 | 0.613 | 0.38 | 20261014T123926Z |
| internvl3_5-8b | v2 | 18 | 0.556 | 0.556 | 0 | 0.556 | 0.467 | 0.88 | 20261014T124037Z |
| internvl3_5-8b | v3 | 18 | 0.667 | 1.0 | 0 | 0.667 | 0.613 | 3.37 | 20261014T124102Z |
| llava-onevision-7b | v1 | 18 | 0.722 | 1.0 | 0 | 0.722 | 0.68 | 0.5 | 20261014T123926Z |
| llava-onevision-7b | v2 | 18 | 0.556 | 0.667 | 0 | 0.556 | 0.447 | 0.88 | 20261014T124034Z |
| llava-onevision-7b | v3 | 18 | 0.611 | 1.0 | 0 | 0.611 | 0.513 | 3.33 | 20261014T124059Z |
| qwen3vl-8b | v1 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.78 | 0.21 | 20261014T123926Z |
| qwen3vl-8b | v2 | 18 | 0.556 | 0.222 | 0 | 0.556 | 0.433 | 0.7 | 20261014T124032Z |
| qwen3vl-8b | v3 | 18 | 0.833 | 1.0 | 0 | 0.833 | 0.78 | 4.92 | 20261014T124052Z |

### Agreement across prompt variants

| model | variants | n_common | all_agree | fleiss_kappa | agree v1-v2 | agree v1-v3 | agree v2-v3 |
|---|---|---|---|---|---|---|---|
| dummy | v1,v2,v3 | 18 | 0.0 | -0.079 | 0.222 | 0.056 | 0.167 |
| internvl3_5-8b | v1,v2,v3 | 18 | 0.778 | 0.83 | 0.778 | 1.0 | 0.778 |
| llava-onevision-7b | v1,v2,v3 | 18 | 0.778 | 0.824 | 0.833 | 0.778 | 0.944 |
| qwen3vl-8b | v1,v2,v3 | 18 | 0.667 | 0.748 | 0.667 | 1.0 | 0.667 |

### Per material recall (which materials are recognisable at all)

| model | variant | condition | material | support | recall | precision | f1 |
|---|---|---|---|---|---|---|---|
| dummy | v1 | photo | book_paper_cover | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | photo | cardboard | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | photo | ceramic | 2 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | photo | foam | 2 | 0.0 |  | 0.0 |
| dummy | v1 | photo | glass | 2 | 0.0 |  | 0.0 |
| dummy | v1 | photo | metal | 2 | 0.5 | 0.333 | 0.4 |
| dummy | v1 | photo | ping_pong_plastic | 2 | 0.0 |  | 0.0 |
| dummy | v1 | photo | plastic | 1 | 0.0 | 0.0 | 0.0 |
| dummy | v1 | photo | rubber | 1 | 0.0 |  | 0.0 |
| dummy | v1 | photo | wood | 2 | 0.0 |  | 0.0 |
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

#### dummy/v1/photo

| true \ predicted | ceramic | metal | aluminium | plastic | ping_pong_plastic | rubber | wood | glass | foam | cardboard | book_paper_cover | clay | <other> | <unparsed> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceramic | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| metal | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| aluminium | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| plastic | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| ping_pong_plastic | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rubber | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| wood | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| glass | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| foam | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| cardboard | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| book_paper_cover | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| clay | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

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
| exp1 | dummy | v1 | 20261014T123348Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 880c81b387b5 | int4.local.snellius.surf.nl |  | dummy |
| exp1 | dummy | v2 | 20261014T123349Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 958a9e9ec6a8 | int4.local.snellius.surf.nl |  | dummy |
| exp1 | dummy | v3 | 20261014T123349Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 2b3d48ffff02 | int4.local.snellius.surf.nl |  | dummy |
| exp1 | internvl3_5-8b | v1 | 20261014T123926Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 880c81b387b5 | gcn27.local.snellius.surf.nl | 28076775 | OpenGVLab/InternVL3_5-8B-HF |
| exp1 | internvl3_5-8b | v2 | 20261014T124037Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 958a9e9ec6a8 | gcn27.local.snellius.surf.nl | 28076775 | OpenGVLab/InternVL3_5-8B-HF |
| exp1 | internvl3_5-8b | v3 | 20261014T124102Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 2b3d48ffff02 | gcn27.local.snellius.surf.nl | 28076775 | OpenGVLab/InternVL3_5-8B-HF |
| exp1 | llava-onevision-7b | v1 | 20261014T123926Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 880c81b387b5 | gcn62.local.snellius.surf.nl | 28076776 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1 | llava-onevision-7b | v2 | 20261014T124034Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 958a9e9ec6a8 | gcn62.local.snellius.surf.nl | 28076776 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1 | llava-onevision-7b | v3 | 20261014T124059Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 2b3d48ffff02 | gcn62.local.snellius.surf.nl | 28076776 | llava-hf/llava-onevision-qwen2-7b-ov-hf |
| exp1 | qwen3vl-8b | v1 | 20261014T123926Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 880c81b387b5 | gcn27.local.snellius.surf.nl | 28076774 | Qwen/Qwen3-VL-8B-Instruct |
| exp1 | qwen3vl-8b | v2 | 20261014T124032Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 958a9e9ec6a8 | gcn27.local.snellius.surf.nl | 28076774 | Qwen/Qwen3-VL-8B-Instruct |
| exp1 | qwen3vl-8b | v3 | 20261014T124052Z | b81949ee732fb5e3ba52bc5af4aa377c52946077 | True | 2b3d48ffff02 | gcn27.local.snellius.surf.nl | 28076774 | Qwen/Qwen3-VL-8B-Instruct |
