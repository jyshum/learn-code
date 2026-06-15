# ML Foundations Knowledge Base — Build Spec

## Purpose

A private GitHub repo (`ml-foundations`) that serves as a personal, concept-organized machine learning knowledge base. Written at Level 2 depth: understand what each concept does, when to use it, how to diagnose problems with it, and why it matters. No mathematical derivations. Every concept grounded in real project examples (SickNote, DinoTracker, paleo-tech, REACH).

## Target reader

The future version of you, mid-build, trying to remember why your loss curve looks weird or whether to use focal loss vs. BCEWithLogitsLoss. These notes should be scannable, practical, and written in your own voice.

---

## Repo Structure

```
ml-foundations/
├── README.md
├── 01-models-and-representations/
│   ├── 01-what-is-a-model.md
│   ├── 02-supervised-vs-unsupervised.md
│   ├── 03-task-types.md
│   ├── 04-tabular-models.md
│   ├── 05-neural-networks.md
│   ├── 06-cnns.md
│   ├── 07-autoencoders-and-vaes.md
│   ├── 08-segmentation-architectures.md
│   └── 09-decision-tree-when-to-pick-what.md
├── 02-training-evaluation-debugging/
│   ├── 01-the-training-loop.md
│   ├── 02-loss-functions.md
│   ├── 03-optimizers-and-learning-rate.md
│   ├── 04-reading-loss-curves.md
│   ├── 05-overfitting-and-regularization.md
│   ├── 06-transfer-learning.md
│   ├── 07-evaluation-metrics.md
│   ├── 08-explainability.md
│   └── 09-debugging-checklist.md
├── 03-data/
│   ├── 01-train-val-test-splits.md
│   ├── 02-data-leakage.md
│   ├── 03-class-imbalance.md
│   ├── 04-data-augmentation.md
│   ├── 05-preprocessing-and-normalization.md
│   ├── 06-label-quality-and-noise.md
│   └── 07-distribution-shift.md
├── 04-paleo-tech/
│   ├── 01-landscape.md
│   ├── 02-footprint-analysis.md
│   ├── 03-ct-scan-segmentation.md
│   ├── 04-body-mass-estimation.md
│   ├── 05-key-research-groups.md
│   └── 06-open-problems.md
└── resources.md
```

---

## Format Template

Every `.md` file follows this structure. Do NOT deviate.

```markdown
# [Concept Name]

## What it is

[2-4 sentences. Plain language. No jargon without immediate definition. Explain what this concept DOES, not the math behind it.]

## Why it matters

[1-3 sentences. Connect to a real decision you'd face while building. Frame as: "Without understanding this, you'd..." or "This matters because..."]

## How it works (conceptually)

[The core explanation. Use analogies where helpful. Can be longer — 1-3 paragraphs. Include sub-sections if the concept has distinct components. NO mathematical equations unless absolutely unavoidable (and even then, keep to a single line and explain in words what it means). Use diagrams described in text if a visual would help (e.g., "Think of it as: input → [encoder] → bottleneck → [decoder] → output").]

## Real example

[Ground this in SickNote, DinoTracker, paleo-tech, or REACH. Show the concept in action with a specific decision, result, or failure. This section is what makes these notes yours, not a textbook.]

## Key intuitions

[Bullet list of 3-5 "remember this" takeaways. These are the things you'd want to recall mid-build.]

## Common mistakes

[Bullet list of 2-4 pitfalls. Frame as: "Don't do X because Y happens."]

## Links

[2-4 links max. Prioritize: MLU-Explain interactive essays, CNN Explainer, 3Blue1Brown videos, aladdinpersson YouTube walkthroughs, relevant papers. Only include links that are genuinely useful, not padding.]
```

---

## Writing Rules

1. Write in second person ("you") or first person ("I"). Not third person academic tone.
2. No hedging language. Don't say "it's worth noting that..." — just say the thing.
3. No em dashes. Use commas or periods instead.
4. Keep sentences short. If a sentence has more than one comma, split it.
5. Use code snippets only when they clarify a concept (e.g., showing what a loss function call looks like in PyTorch). Keep snippets under 5 lines.
6. Every file should be readable in under 3 minutes. If it's longer, split the concept.
7. The "Real example" section is mandatory and must reference a specific project, not a hypothetical.
8. Do NOT include content about transformers, attention mechanisms, GANs, reinforcement learning, or diffusion models. These are out of scope for now.

---

## Example Section (use this as the tone/depth reference)

Below is a fully written example of what `02-training-evaluation-debugging/02-loss-functions.md` should look like. Claude Code should match this voice, depth, and structure for every file.

```markdown
# Loss Functions

## What it is

A loss function is a formula that calculates a single number representing how wrong your model's predictions are. The optimizer uses this number to adjust the model's weights. A smaller loss means the model's predictions are closer to the correct answers.

## Why it matters

Choosing a loss function is choosing what your model considers a mistake. Different loss functions penalize different types of errors differently. If you pick the wrong one, your model optimizes for the wrong thing, and no amount of training will fix that.

## How it works (conceptually)

Every loss function compares the model's prediction against the true label and produces an error score. The key insight is that different loss functions weight errors differently:

**BCEWithLogitsLoss** (binary cross-entropy with logits) is the standard for binary classification. It takes the model's raw output (before sigmoid), applies sigmoid internally, and penalizes predictions that are far from the true 0 or 1 label. The further off the prediction, the steeper the penalty. The `pos_weight` parameter lets you tell the model "a false negative costs X times more than a false positive." Setting pos_weight=3 means missing a positive example is 3x worse than falsely flagging a negative.

**CrossEntropyLoss** is the multi-class version. Used when you have more than two categories.

**MSE (Mean Squared Error)** is for regression (predicting a continuous number, like dinosaur body mass). It squares the error, which means large errors get penalized much more heavily than small ones. This is usually what you want, but it also means outliers dominate training.

**MAE (Mean Absolute Error)** is also for regression but treats all errors equally regardless of size. More robust to outliers than MSE, but the training signal is noisier.

**Focal Loss** modifies BCE by downweighting easy examples (where the model is already confident and correct) and focusing training on hard, ambiguous cases. Useful when most of your data is easy to classify and the interesting cases are the hard ones.

**Dice Loss** is for segmentation tasks. Instead of evaluating per-pixel accuracy, it measures the overlap between the predicted mask and the true mask. Better for imbalanced segmentation (when the object you're segmenting is small relative to the background, like bone in a CT scan surrounded by rock matrix).

**Label smoothing** isn't a separate loss function but a modification: instead of training against hard labels (0.0 and 1.0), you train against soft labels (0.05 and 0.95). This tells the model "the labels might be slightly wrong, don't be overconfident." Useful when your labels have noise.

## Real example

In SickNote, I used BCEWithLogitsLoss with pos_weight to handle the class imbalance (79.7% of recordings were abnormal). Without pos_weight, the model learned to mostly predict "abnormal" because that was right most of the time, but it missed healthy coughs. With pos_weight tuned, the model was forced to take false negatives more seriously, which brought specificity up to 0.77.

The threshold tuning with Youden's J was a separate optimization on top of the loss function. The loss function determined how the model trained; the threshold determined where I drew the line between "healthy" and "abnormal" after training.

## Key intuitions

- The loss function defines what the model cares about. Everything else (architecture, data, training) only matters in the context of what the loss is optimizing for.
- pos_weight is not a magic fix for imbalance. It trades sensitivity for specificity. You're choosing which type of error is more acceptable.
- For regression problems (like body mass estimation), MSE penalizes large errors quadratically. If your data has outliers, consider MAE or Huber loss instead.
- Dice loss is almost always better than pixel-wise cross-entropy for segmentation when the foreground object is small.
- Label smoothing is underused. Any time your labels come from human judgment (expert annotations, crowdsourced labels), they contain noise. Smoothing handles that gracefully.

## Common mistakes

- Using accuracy as your loss function. Accuracy isn't differentiable, so the optimizer can't use it. You train with a loss function and evaluate with metrics like accuracy. They're different things.
- Ignoring class imbalance in the loss function and trying to fix it only with data resampling. Both approaches work, but you should at least consider loss-level weighting.
- Using MSE for classification or BCE for regression. The loss function must match the task type.
- Not comparing different loss functions. You should always try at least two and measure the difference. In SickNote, comparing BCEWithLogitsLoss vs. focal loss would show whether hard examples are the bottleneck.

## Links

- [MLU-Explain: Cross Entropy Loss](https://mlu-explain.github.io/cross-entropy/) - interactive visual
- [PyTorch Loss Functions Documentation](https://pytorch.org/docs/stable/nn.html#loss-functions) - reference for all available losses
- [Focal Loss paper summary](https://arxiv.org/abs/1708.02002) - read the abstract and Figure 1 only
```

---

## Content Guidance Per Folder

### Folder 1: Models & Representations

Frame every model as an answer to "what kind of function maps my input to my output?" Start with the simplest (linear regression: a line) and build up. For each model type, emphasize: what input it expects, what output it produces, what makes it different from alternatives, and when you'd pick it. The final file (09-decision-tree) should be a practical cheat sheet.

Anchor projects: SickNote (CNN for audio classification), DinoTracker (beta-VAE for unsupervised footprint analysis), REACH (tabular/XGBoost for reachability scoring), paleo CT segmentation (U-Net).

### Folder 2: Training, Evaluation & Debugging

This is the most important folder. Frame everything as "what do I observe, what does it mean, what do I do about it." Loss curves, metric changes, explainability outputs. The debugging checklist (09) should be a practical reference you can scan in 30 seconds when something breaks.

Anchor projects: SickNote experiments (kill pos_weight, overfit on purpose, swap loss function, ablate ensemble, interrogate Grad-CAM).

### Folder 3: Data

Frame as upstream decisions that constrain everything downstream. Every section should include "how to detect the problem" and "how to fix it." Distribution shift (07) should specifically address the paleo-ML challenge of training on extant animals and predicting on extinct ones.

Anchor projects: SickNote's COUGHVID dataset (imbalance, label noise), DinoTracker (unsupervised approach bypassing label bias), paleo body mass estimation (training on modern mammals, predicting on dinosaurs).

### Folder 4: Paleo-Tech

This folder is domain knowledge, not ML concepts. Write it as a field guide. Each file should cover: what's been done, what worked, what didn't, and what's open. Include paper citations with year and journal. This folder is what makes the whole repo differentiated.

Key papers to reference:
- Hartmann et al. (2026), PNAS - beta-VAE footprint classification
- Lallensack et al. (2022) - supervised DCNN footprint work
- Knutsen & Konovalov (2024), Scientific Reports - few-shot CT segmentation
- Yu et al. (2022) - first DL dinosaur CT segmentation
- Zhao et al. (2025), Scientific Reports - DL segmentation + biomechanical FEA
- Packard (2009) - allometric regression bias critique
- Sellers et al. (2012) - convex hull mass estimation
- Brassey (2017) - volumetric mass estimation review
- Yu et al. (2024), Earth-Science Reviews - comprehensive AI in paleontology survey

### resources.md

Flat file with categorized links:
- Interactive tools: CNN Explainer, MLU-Explain, Transformer Explainer
- Video: 3Blue1Brown neural network series, aladdinpersson YouTube
- Repos: aladdinpersson/Machine-Learning-Collection, gregh83/DinoTracker, poloclub/cnn-explainer
- Papers: all paleo-tech papers listed above
- Courses: Stanford CS231N (CNNs), fast.ai practical deep learning

### README.md

Short. 5-10 lines max. State what this repo is, who it's for (yourself), and the folder structure. No badges, no fluff. Something like:

"Personal ML knowledge base organized by decision domain, not by algorithm. Written at practitioner depth: what each concept does, when it breaks, and how to fix it. Grounded in real project work (SickNote, DinoTracker, paleo-tech research). Not a textbook. Not a course. A reference I actually use."

---

## Instructions for Claude Code

1. Create the repo structure (all folders and files).
2. Write README.md and resources.md first.
3. Write Folder 2 first (training/evaluation/debugging) since that's where active learning is happening.
4. Write Folder 1 second, Folder 3 third, Folder 4 last.
5. Follow the format template exactly for every file.
6. Match the tone and depth of the example section (loss functions) for every file.
7. Every "Real example" section must reference a specific project. Use SickNote as the primary anchor, DinoTracker/paleo-tech as secondary, REACH for tabular concepts.
8. Keep every file under 3 minutes reading time.
9. No mathematical equations unless showing a single-line PyTorch call (e.g., `loss = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([3.0]))`).
10. No em dashes anywhere.
