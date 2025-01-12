# Pattern-Exploiting Training (PET)

python3 cli.py --method pet --pattern_ids 0 1 2 3 4 --data_dir /home/percent1/models/nlp/data/yahoo --model_type roberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/roberta-base --task_name yahoo --output_dir yahoo-roberta-output-example-10-seed-2333 --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --lm_training --sc_max_steps 5000 --pet_repetitions 1 --seed 2333 --unlabeled_examples 20000

python3 cli.py --method pet --pattern_ids 0 1 2 3 4 --data_dir /home/percent1/models/nlp/data/yelp --model_type roberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/roberta-base --task_name yelp-full --output_dir yelp-roberta-output-example-10-seed-2333 --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --lm_training --sc_max_steps 5000 --pet_repetitions 1 --seed 2333 --unlabeled_examples 20000

This repository contains the code for [Exploiting Cloze Questions for Few-Shot Text Classification and Natural Language Inference](https://arxiv.org/abs/2001.07676) and [It's Not Just Size That Matters: Small Language Models Are Also Few-Shot Learners](https://arxiv.org/abs/2009.07118). The papers introduce pattern-exploiting training (PET), a semi-supervised training procedure that reformulates input examples as cloze-style phrases. In low-resource settings, PET and iPET significantly outperform regular supervised training, various semi-supervised baselines and even GPT-3 despite requiring 99.9% less parameters. The iterative variant of PET (iPET) trains multiple generations of models and can even be used without any training data.

<table>
    <tr>
        <th>#Examples</th>
        <th>Training Mode</th>
        <th>Yelp (Full)</th>
        <th>AG's News</th>
        <th>Yahoo Questions</th>
        <th>MNLI</th>
    </tr>
    <tr>
        <td rowspan="2" align="center"><b>0</b></td>
        <td>unsupervised</td>
        <td align="right">33.8</td>
        <td align="right">69.5</td>
        <td align="right">44.0</td>
        <td align="right">39.1</td>
    </tr>
    <tr>
        <td>iPET</td>
        <td align="right"><b>56.7</b></td>
        <td align="right"><b>87.5</b></td>
        <td align="right"><b>70.7</b></td>
        <td align="right"><b>53.6</b></td>
    </tr>
    <tr>
        <td rowspan="3" align="center"><b>100</b></td>
        <td>supervised</td>
        <td align="right">53.0</td>
        <td align="right">86.0</td>
        <td align="right">62.9</td>
        <td align="right">47.9</td>
    </tr>
    <tr>
        <td>PET</td>
        <td align="right">61.9</td>
        <td align="right">88.3</td>
        <td align="right">69.2</td>
        <td align="right">74.7</td>
    </tr>
    <tr>
        <td>iPET</td>
        <td align="right"><b>62.9</b></td>
        <td align="right"><b>89.6</b></td>
        <td align="right"><b>71.2</b></td>
        <td align="right"><b>78.4</b></td>
    </tr>
</table>
    
<sup>*Note*: To exactly reproduce the above results, make sure to use v1.1.0 (`--branch v1.1.0`).</sup>

## 📑 Contents

**[🔧 Setup](#-setup)**

**[💬 CLI Usage](#-cli-usage)**

**[💻 API Usage](#-api-usage)**

**[🐶 Train your own PET](#-train-your-own-pet)**

**[📕 Citation](#-citation)**

## 🔧 Setup

All requirements for PET can be found in `requirements.txt`. You can install all required packages with `pip install -r requirements.txt`.

## 💬 CLI Usage

The command line interface `cli.py` in this repository currently supports three different training modes (PET, iPET, supervised training), two additional evaluation methods (unsupervised and priming) and 13 different tasks. For Yelp Reviews, AG's News, Yahoo Questions, MNLI and X-Stance, see [the original paper](https://arxiv.org/abs/2001.07676) for further details. For the 8 SuperGLUE tasks, see [this paper](https://arxiv.org/abs/2009.07118).

### PET Training and Evaluation

To train and evaluate a PET model for one of the supported tasks, simply run the following command:

    python3 cli.py \
	--method pet \
	--pattern_ids $PATTERN_IDS \
	--data_dir $DATA_DIR \
	--model_type $MODEL_TYPE \
	--model_name_or_path $MODEL_NAME_OR_PATH \
	--task_name $TASK \
	--output_dir $OUTPUT_DIR \
	--do_train \
	--do_eval
    
 where
 - `$PATTERN_IDS` specifies the PVPs to use. For example, if you want to use *all* patterns, specify `PATTERN_IDS 0 1 2 3 4` for AG's News and Yahoo Questions or `PATTERN_IDS 0 1 2 3` for Yelp Reviews and MNLI.
 - `$DATA_DIR` is the directory containing the train and test files (check `tasks.py` to see how these files should be named and formatted for each task).
 - `$MODEL_TYPE` is the name of the model being used, e.g. `albert`, `bert` or `roberta`.
 - `$MODEL_NAME` is the name of a pretrained model (e.g., `roberta-large` or `albert-xxlarge-v2`) or the path to a pretrained model.
 - `$TASK_NAME` is the name of the task to train and evaluate on.
 - `$OUTPUT_DIR` is the name of the directory in which the trained model and evaluation results are saved.
 
You can additionally specify various training parameters for both the ensemble of PET models corresponding to individual PVPs (prefix `--pet_`) and for the final sequence classification model (prefix `--sc_`). For example, the default parameters used for our SuperGLUE evaluation are:
 
 	--pet_per_gpu_eval_batch_size 8 \
	--pet_per_gpu_train_batch_size 2 \
	--pet_gradient_accumulation_steps 8 \
	--pet_max_steps 250 \
	--pet_max_seq_length 256 \
    --pet_repetitions 3 \
	--sc_per_gpu_train_batch_size 2 \
	--sc_per_gpu_unlabeled_batch_size 2 \
	--sc_gradient_accumulation_steps 8 \
	--sc_max_steps 5000 \
	--sc_max_seq_length 256 \
    --sc_repetitions 1
    
For each pattern `$P` and repetition `$I`, running the above command creates a directory `$OUTPUT_DIR/p$P-i$I` that contains the following files:
  - `pytorch_model.bin`: the finetuned model, possibly along with some model-specific files (e.g, `spiece.model`, `special_tokens_map.json`)
  - `wrapper_config.json`: the configuration of the model being used
  - `train_config.json`: the configuration used for training
  - `eval_config.json`: the configuration used for evaluation
  - `logits.txt`: the model's predictions on the unlabeled data
  - `eval_logits.txt`: the model's prediction on the evaluation data
  - `results.json`: a json file containing results such as the model's final accuracy
  - `predictions.jsonl`: a prediction file for the evaluation set in the SuperGlue format
  
The final (distilled) model for each repetition `$I` can be found in `$OUTPUT_DIR/final/p0-i$I`, which contains the same files as described above.

🚨 If your GPU runs out of memory during training, you can try decreasing both the `pet_per_gpu_train_batch_size` and the `sc_per_gpu_unlabeled_batch_size` while increasing both `pet_gradient_accumulation_steps` and `sc_gradient_accumulation_steps`.


### iPET Training and Evaluation

To train and evaluate an iPET model for one of the supported tasks, simply run the same command as above, but replace `--method pet` with `--method ipet`. There are various additional iPET parameters that you can modify; all of them are prefixed with `--ipet_`.

For each generation `$G`, pattern `$P` and iteration `$I`, this creates a directory `$OUTPUT_DIR/g$G/p$P-i$I` that is structured as for regular PET. The final (distilled) model can again be found in `$OUTPUT_DIR/final/p0-i$I`.

🚨 If you use iPET with zero training examples, you need to specify how many examples for each label should be chosen in the first generation and you need to change the reduction strategy to mean: `--ipet_n_most_likely 100 --reduction mean`.

### Supervised Training and Evaluation

To train and evaluate a regular sequence classifier in a supervised fashion, simply run the same command as above, but replace `--method pet` with `--method sequence_classifier`. There are various additional parameters for the sequence classifier that you can modify; all of them are prefixed with `--sc_`.

### Unsupervised Evaluation

To evaluate a pretrained language model with the default PET patterns and verbalizers, but without fine-tuning, remove the argument `--do_train` and add `--no_distillation` so that no final distillation is performed.

### Priming

If you want to use priming, remove the argument `--do_train` and add the arguments `--priming --no_distillation` so that all training examples are used for priming and no final distillation is performed. 

🚨 Remember that you may need to increase the maximum sequence length to a much larger value, e.g. `--pet_max_seq_length 5000`. This only works with language models that support such long sequences, e.g. XLNet. For using XLNet, you can specify `--model_type xlnet --model_name_or_path xlnet-large-cased --wrapper_type plm`.

## 💻 API Usage

Instead of using the command line interface, you can also directly use the PET API, most of which is defined in `pet.modeling`. By including `import pet`, you can access methods such as `train_pet`, `train_ipet` and `train_classifier`. Check out their documentation for more information.

## 🐶 Train your own PET

To use PET for custom tasks, you need to define two things: 

- a **DataProcessor**, responsible for loading training and test data. See `examples/custom_task_processor.py` for an example.
- a **PVP**, responsible for applying patterns to inputs and mapping labels to natural language verbalizations. See `examples/custom_task_pvp.py` for an example.

After having implemented the DataProcessor and the PVP, you can train a PET model using the command line as [described above](#pet-training-and-evaluation). Below, you can find additional information on how to define the two components of a PVP, *verbalizers* and *patterns*.

### Verbalizers

Verbalizers are used to map task labels to words in natural language. For example, in a binary sentiment classification task, you could map the positive label (`+1`) to the word `good` and the negative label (`-1`) to the word `bad`. Verbalizers are realized through a PVP's `verbalize()` method. The simplest way of defining a verbalizer is to use a dictionary:

```python
VERBALIZER = {"+1": ["good"], "-1": ["bad"]}
    
def verbalize(self, label) -> List[str]:
    return self.VERBALIZER[label]       
```

Importantly, in PET's current version, verbalizers are by default restricted to **single tokens** in the underlying LMs vocabulary (for using more than one token, [see below](#pet-with-multiple-masks)). Given a language model's tokenizer, you can easily check whether a word corresponds to a single token by verifying that `len(tokenizer.tokenize(word)) == 1`.

You can also define multiple verbalizations for a single label. For example, if you are unsure which words best represent the labels in a binary sentiment classification task, you could define your verbalizer as follows:

```python
VERBALIZER = {"+1": ["great", "good", "wonderful", "perfect"], "-1": ["bad", "terrible", "horrible"]}
```

### Patterns

Patterns are used to make the language model understand a given task; they must contain exactly one `<MASK>` token which is to be filled using the verbalizer. For binary sentiment classification based on a review's summary (`<A>`) and body (`<B>`), a suitable pattern may be `<A>. <B>. Overall, it was <MASK>.` Patterns are realized through a PVP's `get_parts()` method, which returns a pair of text sequences (where each sequence is represented by a list of strings):

```python
def get_parts(self, example: InputExample):
    return [example.text_a, '.', example.text_b, '.'], ['Overall, it was ', self.mask]
```

If you do not want to use a pair of sequences, you can simply leave the second sequence empty:

```python
def get_parts(self, example: InputExample):
    return [example.text_a, '.', example.text_b, '. Overall, it was ', self.mask], []
```
            
If you want to define several patterns, simply use the `PVP`s `pattern_id` attribute:

```python
def get_parts(self, example: InputExample):
    if self.pattern_id == 1:
        return [example.text_a, '.', example.text_b, '.'], ['Overall, it was ', self.mask]
    elif self.pattern_id == 2:
        return ['It was just ', self.mask, '!', example.text_a, '.', example.text_b, '.'], []
```

When training the model using the command line, specify all patterns to be used (e.g., `--pattern_ids 1 2`).

Importantly, if a sequence is longer than the specified maximum sequence length of the underlying LM, PET must know which parts of the input can be shortened and which ones cannot (for example, the mask token must always be there). Therefore, `PVP` provides a `shortenable()` method to indicate that a piece of text can be shortened:

```python
def get_parts(self, example: InputExample):
    text_a = self.shortenable(example.text_a)
    text_b = self.shortenable(example.text_b)
    return [text_a, '.', text_b, '. Overall, it was ', self.mask], []
```

### PET with Multiple Masks

By default, the current implementation of PET and iPET only supports a fixed set of labels that is shared across all examples and verbalizers that correspond to a single token. 
However, for some tasks it may be necessary to use verbalizers that correspond to multiple tokens ([as described here](http://arxiv.org/abs/2009.07118)).
To do so, you simply need the following two modifications:

1) Add the following lines in your task's **DataProcessor** (see `examples/custom_task_processor.py`):
 
   ```python
   from pet.tasks import TASK_HELPERS
   from pet.task_helpers import MultiMaskTaskHelper
   TASK_HELPERS['my_task'] = MultiMaskTaskHelper
   ```
   where ```'my_task'``` is the name of your task. 

2) In your **PVP**, make sure that the ``get_parts()`` method always inserts **the maximum number of mask tokens** required for any verbalization. For example, if your verbalizer maps ``+1`` to "really awesome" and ``-1`` to "terrible" and if those are tokenized as ``["really", "awe", "##some"]`` and ``["terrible"]``, respectively, your ``get_parts()`` method should always return a sequence that contains exactly 3 mask tokens.

With this modification, you can now use verbalizers consisting of multiple tokens:
```python
VERBALIZER = {"+1": ["really good"], "-1": ["just bad"]}
```
However, there are several limitations to consider:

- When using a ``MultiMaskTaskHelper``, the maximum batch size for evaluation is 1.
- As using multiple masks requires multiple forward passes during evaluation, the time required for evaluation scales about linearly with the length of the longest verbalizer. If you require verbalizers that consist of 10 or more tokens, [using a generative LM](https://arxiv.org/abs/2012.11926) might be a better approach.
- The ``MultiMaskTaskHelper`` class is an experimental feature that is not thoroughly tested. In particular, this feature has only been tested for PET and not for iPET. If you observe something strange, please raise an issue.

For more flexibility, you can also write a custom `TaskHelper`. As a starting point, you can check out the classes `CopaTaskHelper`, `WscTaskHelper` and `RecordTaskHelper` in `pet/task_helpers.py`.

## 📕 Citation

If you make use of the code in this repository, please cite the following papers:

    @article{schick2020exploiting,
      title={Exploiting Cloze Questions for Few-Shot Text Classification and Natural Language Inference},
      author={Timo Schick and Hinrich Schütze},
      journal={Computing Research Repository},
      volume={arXiv:2001.07676},
      url={http://arxiv.org/abs/2001.07676},
      year={2020}
    }

    @article{schick2020small,
      title={It's Not Just Size That Matters: Small Language Models Are Also Few-Shot Learners},
      author={Timo Schick and Hinrich Schütze},
      journal={Computing Research Repository},
      volume={arXiv:2009.07118},
      url={http://arxiv.org/abs/2009.07118},
      year={2020}
    }

# Run project

```
CUDA_VISIBLE_DEVICES=1 python3 cli.py \
--method pet \
--pattern_ids 0 1 2 3 4 5 \
--data_dir /home/percent1/models/nlp/data/ag_news \
--model_type bert \
--model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/bert-base-uncased \
--task_name agnews \
--output_dir agnews-output \
--do_train \
--do_eval \
--train_examples 10 \
--split_examples_evenly \
--pet_max_steps 250 \
--lm_training \
--sc_max_steps 5000 \
--pet_repetitions 1

CUDA_VISIBLE_DEVICES=1 python3 cli.py \
--method ipet \
--pattern_ids 0 1 2 3 4 5 \
--data_dir /home/percent1/models/nlp/data/ag_news \
--model_type bert \
--model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/bert-base-uncased \
--task_name agnews \
--output_dir agnews-output \
--do_train \
--do_eval \
--train_examples 10 \
--split_examples_evenly \
--sc_max_steps 5000 \
--pet_repetitions 1
```

```
2022-11-26 23:31:05,833 - INFO - modeling - {'acc': 0.8094736842105263}
2022-11-26 23:31:05,981 - INFO - modeling - === OVERALL RESULTS ===
2022-11-26 23:31:05,982 - INFO - modeling - acc-p0: 0.8094736842105263 +- 0
2022-11-26 23:31:05,982 - INFO - modeling - acc-all-p: 0.8094736842105263 +- 0

CUDA_VISIBLE_DEVICES=1 python3 cli.py --method pet --pattern_ids 0 1 2 3 4 5 --data_dir /home/percent1/models/nlp/data/ag_news --model_type bert --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/bert-base-uncased --task_name agnews --output_dir agnews-output --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --lm_training --sc_max_steps 5000 --pet_repetitions 1
```

```
CUDA_VISIBLE_DEVICES=1 python3 cli.py --method pet --pattern_ids 0 1 2 3 4 5 --data_dir /home/percent1/models/nlp/data/ag_news --model_type deberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/deberta-base --task_name agnews --output_dir agnews-deberta-output --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --lm_training --sc_max_steps 5000 --pet_repetitions 1

2022-11-27 13:39:24,006 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-11-27 13:39:24,007 - INFO - modeling - {'acc': 0.6397368421052632}
2022-11-27 13:39:24,187 - INFO - modeling - === OVERALL RESULTS ===
2022-11-27 13:39:24,188 - INFO - modeling - acc-p0: 0.6397368421052632 +- 0
2022-11-27 13:39:24,188 - INFO - modeling - acc-all-p: 0.6397368421052632 +- 0

acc-p0: 0.5285526315789474 +- 0
acc-p1: 0.5743421052631579 +- 0
acc-p2: 0.4236842105263158 +- 0
acc-p3: 0.45473684210526316 +- 0
acc-p4: 0.5792105263157895 +- 0
acc-p5: 0.5725 +- 0
acc-all-p: 0.5221710526315789 +- 0.06752196472424073

CUDA_VISIBLE_DEVICES=1 python3 cli.py --method pet --pattern_ids 0 1 2 3 4 5 --data_dir /home/percent1/models/nlp/data/ag_news --model_type deberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/deberta-v3-base --task_name agnews --output_dir agnews-output --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --sc_max_steps 5000 --pet_repetitions 1
```

```
acc-p0: 0.8163157894736842 +- 0
acc-p1: 0.8475 +- 0
acc-p2: 0.8060526315789474 +- 0
acc-p3: 0.8305263157894737 +- 0
acc-p4: 0.8330263157894737 +- 0
acc-p5: 0.7835526315789474 +- 0
acc-all-p: 0.8194956140350877 +- 0.02267917526645072

CUDA_VISIBLE_DEVICES=1 python3 cli.py --method pet --pattern_ids 0 1 2 3 4 5 --data_dir /home/percent1/models/nlp/data/ag_news --model_type roberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/roberta-base --task_name agnews --output_dir agnews-roberta-output --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --lm_training --sc_max_steps 5000 --pet_repetitions 1 --seed 2333

2022-11-27 18:40:19,208 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-11-27 18:40:19,208 - INFO - modeling - {'acc': 0.8471052631578947}
2022-11-27 18:40:19,444 - INFO - modeling - === OVERALL RESULTS ===
2022-11-27 18:40:19,445 - INFO - modeling - acc-p0: 0.8471052631578947 +- 0
2022-11-27 18:40:19,445 - INFO - modeling - acc-all-p: 0.8471052631578947 +- 0
```


```
g0
acc-p0: 0.8163157894736842 +- 0
acc-p1: 0.8475 +- 0
acc-p2: 0.8060526315789474 +- 0
acc-p3: 0.8305263157894737 +- 0
acc-p4: 0.8330263157894737 +- 0
acc-p5: 0.7835526315789474 +- 0
acc-all-p: 0.8194956140350877 +- 0.02267917526645072

g1
acc-p0: 0.8311842105263157 +- 0
acc-p1: 0.8268421052631579 +- 0
acc-p2: 0.8307894736842105 +- 0
acc-p3: 0.8419736842105263 +- 0
acc-p4: 0.795921052631579 +- 0
acc-p5: 0.8464473684210526 +- 0
acc-all-p: 0.8288596491228071 +- 0.017773323926547

g2
acc-p0: 0.8407894736842105 +- 0
acc-p1: 0.8718421052631579 +- 0
acc-p2: 0.8626315789473684 +- 0
acc-p3: 0.8480263157894737 +- 0
acc-p4: 0.8576315789473684 +- 0
acc-p5: 0.8252631578947368 +- 0
acc-all-p: 0.851030701754386 +- 0.016668184372263663


2022-11-28 00:18:29,779 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-11-28 00:18:29,779 - INFO - modeling - {'acc': 0.8653947368421052}
2022-11-28 00:18:29,942 - INFO - modeling - === OVERALL RESULTS ===
2022-11-28 00:18:29,943 - INFO - modeling - acc-p0: 0.8653947368421052 +- 0
2022-11-28 00:18:29,943 - INFO - modeling - acc-all-p: 0.8653947368421052 +- 0

CUDA_VISIBLE_DEVICES=0 python3 cli.py --method ipet --pattern_ids 0 1 2 3 4 5 --data_dir /home/percent1/models/nlp/data/ag_news --model_type roberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/roberta-base --task_name agnews --output_dir agnews-iroberta-output --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --lm_training --sc_max_steps 5000 --pet_repetitions 1 --seed 2333

change to another seed

2022-12-04 15:46:07,082 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-04 15:46:07,083 - INFO - modeling - {'acc': 0.8556578947368421}
2022-12-04 15:46:07,196 - INFO - modeling - === OVERALL RESULTS ===
2022-12-04 15:46:07,196 - INFO - modeling - acc-p0: 0.8556578947368421 +- 0
2022-12-04 15:46:07,196 - INFO - modeling - acc-all-p: 0.8556578947368421 +- 0
```


```
CUDA_VISIBLE_DEVICES=1 python3 cli.py --method pet --pattern_ids 0 1 2 3 4 5 --data_dir /home/percent1/models/nlp/data/ag_news --model_type roberta --model_name_or_path /home/percent1/models/nlp/text-classification/pretrained/roberta-base --task_name agnews --output_dir agnews-roberta1-output --do_train --do_eval --train_examples 10 --split_examples_evenly --pet_max_steps 250 --sc_max_steps 5000 --pet_repetitions 1
```

```
deberta v1

acc-p0: 0.4313157894736842 +- 0
acc-p1: 0.7242105263157895 +- 0
acc-p2: 0.3406578947368421 +- 0
acc-p3: 0.5746052631578947 +- 0
acc-p4: 0.7761842105263158 +- 0
acc-p5: 0.5163157894736842 +- 0
acc-all-p: 0.560548245614035 +- 0.1676252460314671

2022-11-30 00:20:59,782 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-11-30 00:20:59,782 - INFO - modeling - {'acc': 0.6735526315789474}
2022-11-30 00:21:00,020 - INFO - modeling - === OVERALL RESULTS ===
2022-11-30 00:21:00,020 - INFO - modeling - acc-p0: 0.6735526315789474 +- 0
2022-11-30 00:21:00,020 - INFO - modeling - acc-all-p: 0.6735526315789474 +- 0
```

```
fgm(for all models) + roberta + pet

acc-p0: 0.7544736842105263 +- 0
acc-p1: 0.8394736842105263 +- 0
acc-p2: 0.7936842105263158 +- 0
acc-p3: 0.8265789473684211 +- 0
acc-p4: 0.809078947368421 +- 0
acc-p5: 0.7781578947368422 +- 0
acc-all-p: 0.8002412280701754 +- 0.03142070182589439

2022-12-01 19:43:25,670 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-01 19:43:25,670 - INFO - modeling - {'acc': 0.8328947368421052}
2022-12-01 19:43:25,822 - INFO - modeling - === OVERALL RESULTS ===
2022-12-01 19:43:25,822 - INFO - modeling - acc-p0: 0.8328947368421052 +- 0
2022-12-01 19:43:25,823 - INFO - modeling - acc-all-p: 0.8328947368421052 +- 0
```


```
pgd(for all models) + roberta + pet

acc-p0: 0.7428947368421053 +- 0
acc-p1: 0.8451315789473685 +- 0
acc-p2: 0.8151315789473684 +- 0
acc-p3: 0.83 +- 0
acc-p4: 0.8276315789473684 +- 0
acc-p5: 0.8060526315789474 +- 0
acc-all-p: 0.8111403508771929 +- 0.036006469358182504

2022-12-01 23:49:20,650 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-01 23:49:20,650 - INFO - modeling - {'acc': 0.8515789473684211}
2022-12-01 23:49:20,776 - INFO - modeling - === OVERALL RESULTS ===
2022-12-01 23:49:20,777 - INFO - modeling - acc-p0: 0.8515789473684211 +- 0
2022-12-01 23:49:20,777 - INFO - modeling - ence pairs with the 'longest_first' truncati
```

```
pgd(for all models) + roberta + ipet

acc-p0: 0.7428947368421053 +- 0
acc-p1: 0.8451315789473685 +- 0
acc-p2: 0.8151315789473684 +- 0
acc-p3: 0.83 +- 0
acc-p4: 0.8276315789473684 +- 0
acc-p5: 0.8060526315789474 +- 0
acc-all-p: 0.8111403508771929 +- 0.036006469358182504

acc-p0: 0.8539473684210527 +- 0
acc-p1: 0.8559210526315789 +- 0
acc-p2: 0.8064473684210526 +- 0
acc-p3: 0.8043421052631579 +- 0
acc-p4: 0.8075 +- 0
acc-p5: 0.8463157894736842 +- 0
acc-all-p: 0.829078947368421 +- 0.025399985822405383

acc-p0: 0.7971052631578948 +- 0
acc-p1: 0.8503947368421053 +- 0
acc-p2: 0.8555263157894737 +- 0
acc-p3: 0.8530263157894736 +- 0
acc-p4: 0.8502631578947368 +- 0
acc-p5: 0.8606578947368421 +- 0
acc-all-p: 0.8444956140350877 +- 0.023535412209806365

acc-p0: 0.8502631578947368 +- 0
acc-all-p: 0.8502631578947368 +- 0
```


```
smart + roberta + pet

acc-p0: 0.8186842105263158 +- 0
acc-p1: 0.8510526315789474 +- 0
acc-p2: 0.8357894736842105 +- 0
acc-p3: 0.8323684210526315 +- 0
acc-p4: 0.8603947368421052 +- 0
acc-p5: 0.8101315789473684 +- 0
acc-all-p: 0.8347368421052631 +- 0.018943895880619004

acc-p0: 0.8547368421052631 +- 0
acc-all-p: 0.8547368421052631 +- 0
```

```
smart + roberta + ipet(attack all generations)

acc-p0: 0.8186842105263158 +- 0
acc-p1: 0.8510526315789474 +- 0
acc-p2: 0.8357894736842105 +- 0
acc-p3: 0.8323684210526315 +- 0
acc-p4: 0.8603947368421052 +- 0
acc-p5: 0.8101315789473684 +- 0
acc-all-p: 0.8347368421052631 +- 0.018943895880619004

acc-p0: 0.8602631578947368 +- 0
acc-p1: 0.8336842105263158 +- 0
acc-p2: 0.8403947368421053 +- 0
acc-p3: 0.8202631578947368 +- 0
acc-p4: 0.8356578947368422 +- 0
acc-p5: 0.8236842105263158 +- 0
acc-all-p: 0.8356578947368422 +- 0.014227572622013978

acc-p0: 0.8561842105263158 +- 0
acc-p1: 0.8278947368421052 +- 0
acc-p2: 0.8222368421052632 +- 0
acc-p3: 0.8318421052631579 +- 0
acc-p4: 0.8453947368421053 +- 0
acc-p5: 0.84 +- 0
acc-all-p: 0.8372587719298246 +- 0.012446399391084986

acc-p0: 0.848421052631579 +- 0
acc-all-p: 0.848421052631579 +- 0

smart + roberta + ipet(attack first generation)

acc-p0: 0.8186842105263158 +- 0
acc-p1: 0.8510526315789474 +- 0
acc-p2: 0.8357894736842105 +- 0
acc-p3: 0.8323684210526315 +- 0
acc-p4: 0.8603947368421052 +- 0
acc-p5: 0.8101315789473684 +- 0
acc-all-p: 0.8347368421052631 +- 0.018943895880619004

acc-p0: 0.8525 +- 0
acc-p1: 0.8371052631578947 +- 0
acc-p2: 0.844078947368421 +- 0
acc-p3: 0.8311842105263157 +- 0
acc-p4: 0.8459210526315789 +- 0
acc-p5: 0.8221052631578948 +- 0
acc-all-p: 0.8388157894736842 +- 0.011007740917681667

acc-p0: 0.8542105263157894 +- 0
acc-p1: 0.805 +- 0
acc-p2: 0.8356578947368422 +- 0
acc-p3: 0.8396052631578947 +- 0
acc-p4: 0.8378947368421052 +- 0
acc-p5: 0.8393421052631579 +- 0
acc-all-p: 0.8352850877192982 +- 0.016232260009148937

2022-12-04 03:02:47,759 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-04 03:02:47,759 - INFO - modeling - {'acc': 0.8467105263157895}
2022-12-04 03:02:47,876 - INFO - modeling - === OVERALL RESULTS ===
2022-12-04 03:02:47,877 - INFO - modeling - acc-p0: 0.8467105263157895 +- 0
2022-12-04 03:02:47,877 - INFO - modeling - acc-all-p: 0.8467105263157895 +- 0

smart + roberta + ipet(attack last generation)

acc-p0: 0.8163157894736842 +- 0
acc-p1: 0.8475 +- 0
acc-p2: 0.8060526315789474 +- 0
acc-p3: 0.8305263157894737 +- 0
acc-p4: 0.8330263157894737 +- 0
acc-p5: 0.7835526315789474 +- 0
acc-all-p: 0.8194956140350877 +- 0.02267917526645072

acc-p0: 0.8311842105263157 +- 0
acc-p1: 0.8268421052631579 +- 0
acc-p2: 0.8307894736842105 +- 0
acc-p3: 0.8419736842105263 +- 0
acc-p4: 0.795921052631579 +- 0
acc-p5: 0.8464473684210526 +- 0
acc-all-p: 0.8288596491228071 +- 0.017773323926547

acc-p0: 0.8446052631578947 +- 0
acc-p1: 0.8717105263157895 +- 0
acc-p2: 0.8638157894736842 +- 0
acc-p3: 0.8510526315789474 +- 0
acc-p4: 0.8681578947368421 +- 0
acc-p5: 0.8436842105263158 +- 0
acc-all-p: 0.857171052631579 +- 0.01227589975038247

2022-12-04 15:38:34,527 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-04 15:38:34,527 - INFO - modeling - {'acc': 0.8694736842105263}
2022-12-04 15:38:34,644 - INFO - modeling - === OVERALL RESULTS ===
2022-12-04 15:38:34,645 - INFO - modeling - acc-p0: 0.8694736842105263 +- 0
2022-12-04 15:38:34,645 - INFO - modeling - acc-all-p: 0.8694736842105263 +- 0
```

```
50 training examples

without smart:
acc-p0: 0.8661842105263158 +- 0
acc-p1: 0.8514473684210526 +- 0
acc-p2: 0.8672368421052632 +- 0
acc-p3: 0.85 +- 0
acc-p4: 0.8567105263157895 +- 0
acc-p5: 0.8556578947368421 +- 0
acc-all-p: 0.8578728070175439 +- 0.007297789607042763
2022-12-03 13:33:54,507 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-03 13:33:54,508 - INFO - modeling - {'acc': 0.863421052631579}
2022-12-03 13:33:54,728 - INFO - modeling - === OVERALL RESULTS ===
2022-12-03 13:33:54,728 - INFO - modeling - acc-p0: 0.863421052631579 +- 0
2022-12-03 13:33:54,728 - INFO - modeling - acc-all-p: 0.863421052631579 +- 0

with smart:
2022-12-03 12:03:17,584 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-03 12:03:17,584 - INFO - modeling - {'acc': 0.8585526315789473}
2022-12-03 12:03:17,717 - INFO - modeling - === OVERALL RESULTS ===
2022-12-03 12:03:17,718 - INFO - modeling - acc-p0: 0.8585526315789473 +- 0
2022-12-03 12:03:17,718 - INFO - modeling - acc-all-p: 0.8585526315789473 +- 0
```

```
100 training examples

without smart:
acc-p0: 0.8673684210526316 +- 0
acc-p1: 0.8777631578947368 +- 0
acc-p2: 0.8692105263157894 +- 0
acc-p3: 0.8740789473684211 +- 0
acc-p4: 0.8748684210526316 +- 0
acc-p5: 0.8671052631578947 +- 0
acc-all-p: 0.8717324561403509 +- 0.004439042866397422
2022-12-03 18:45:17,241 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-03 18:45:17,241 - INFO - modeling - {'acc': 0.8825}
2022-12-03 18:45:17,340 - INFO - modeling - === OVERALL RESULTS ===
2022-12-03 18:45:17,341 - INFO - modeling - acc-p0: 0.8825 +- 0
2022-12-03 18:45:17,341 - INFO - modeling - acc-all-p: 0.8825 +- 0

with smart:
acc-p0: 0.8607894736842105 +- 0
acc-p1: 0.8796052631578948 +- 0
acc-p2: 0.8786842105263157 +- 0
acc-p3: 0.8817105263157895 +- 0
acc-p4: 0.878421052631579 +- 0
acc-p5: 0.8592105263157894 +- 0
acc-all-p: 0.8730701754385966 +- 0.01020213527520549
2022-12-03 21:50:46,585 - INFO - modeling - --- RESULT (pattern_id=0, iteration=0) ---
2022-12-03 21:50:46,585 - INFO - modeling - {'acc': 0.8842105263157894}
2022-12-03 21:50:46,681 - INFO - modeling - === OVERALL RESULTS ===
2022-12-03 21:50:46,681 - INFO - modeling - acc-p0: 0.8842105263157894 +- 0
2022-12-03 21:50:46,681 - INFO - modeling - acc-all-p: 0.8842105263157894 +- 0
```
