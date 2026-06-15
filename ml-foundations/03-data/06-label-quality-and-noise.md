# Label Quality and Noise

## What it is

Label noise means some of your training examples have incorrect labels. When you train a model, it learns to predict labels, including the wrong ones. The model has no way to know which labels are correct and which are not. It just fits to whatever you give it.

There are three types of noise worth distinguishing. Random noise is when labels are wrong in no particular pattern, like a coin flip. Systematic noise is when a specific annotator always makes the same error, or a labeling process is biased in a consistent direction. Ambiguous labels are when the true label is genuinely uncertain, and even a domain expert would hesitate.

## Why it matters

Label noise places a ceiling on model performance. No matter how deep your network is or how much data you have, the ceiling is set by how clean your labels are. You can tune hyperparameters forever and never break through it.

The dangerous part is that noisy labels look like a model failure. You see high validation loss or poor specificity, and you start adjusting architecture or adding regularization. But the problem is upstream in the data, not the model.

## How it works (conceptually)

Early in training, models learn general patterns. Late in training, they start fitting the noise. This is because the easy examples get memorized first. By epoch 20 or 30, the model is increasingly spending its capacity on examples that are mislabeled.

You can detect this. Look at per-example loss late in training. Examples with consistently high loss after convergence are often mislabeled, because the model has learned everything else and is still failing on these. A confusion matrix can reveal systematic errors too. If one class is consistently predicted as another, the error may be in the labels, not the features.

Confident learning is a more formal approach. You estimate which examples have a higher probability of being mislabeled based on the model's predicted confidence versus the given label. Libraries like `cleanlab` implement this directly.

Label smoothing is a softer mitigation. Instead of training against hard 0/1 targets, you train against soft targets like 0.05/0.95. This prevents the model from becoming overconfident on any individual label. One line in PyTorch: `BCEWithLogitsLoss(label_smoothing=0.1)`. It regularizes against the noise without requiring you to identify which examples are wrong.

For high-stakes applications, gold standard re-labeling is the right answer. Have multiple domain experts re-label a subset independently and use majority vote. It is expensive. It is also the only way to actually fix the ceiling.

## Real example

In SickNote, the COUGHVID dataset labels come from self-reported health status. A person records themselves coughing and reports whether they feel healthy. Someone reporting "healthy" might actually have an early respiratory infection. Someone reporting "symptomatic" might have allergies. This is systematic label noise, and it is the primary reason SickNote's performance ceiling is lower than the architecture would otherwise allow.

To test this, I reviewed a random sample of 50 validation errors by listening to the audio. About 30% were genuinely ambiguous cases where the cough sounded intermediate between healthy and abnormal. Any reasonable listener would have trouble labeling them. About 10% appeared to be outright mislabels, clearly healthy coughs labeled as abnormal.

Adding label smoothing with epsilon=0.1 helped. The model stopped trying to fit the noisy labels so aggressively, and calibration improved. It did not fix the ceiling, but it meant the model's confidence scores were more trustworthy.

DinoTracker takes a different route. When label quality is fundamentally limited by human categorization, like disputed taxonomy for dinosaur footprints, you can skip labels entirely. The beta-VAE learns latent representations without supervision. You compare footprint shapes in latent space rather than relying on expert-labeled categories that experts themselves disagree on.

## Key intuitions

- Assume your labels have noise. They almost always do. Act accordingly from the start.
- High loss late in training on specific examples is a signal, not just bad luck. Look at those examples.
- Systematic noise is worse than random noise because the model learns a wrong pattern confidently.
- Label smoothing is a cheap first step. Confident learning and manual review are more expensive but more effective.
- If your labels are fundamentally unreliable, consider whether you need labels at all.

## Common mistakes

- Don't assume your labels are ground truth, because when the model fails you will diagnose architecture problems instead of data problems, and you will waste weeks.
- Don't apply label smoothing without first checking whether your labels are actually noisy, because on clean labels it can hurt calibration by making the model artificially uncertain.
- Don't use per-class accuracy alone to detect label noise, because systematic mislabeling within a class is invisible to that metric. Look at per-example loss and confusion patterns.
- Don't try to fix label noise by collecting more of the same data, because more data with the same labeling process just gives you more noise at scale.

## Links

- [Confident Learning paper (Northcutt et al., 2021)](https://arxiv.org/abs/1911.00068)
- [cleanlab library](https://github.com/cleanlab/cleanlab)
- [COUGHVID dataset](https://zenodo.org/record/4048312)
- [Label Smoothing Explained (fast.ai)](https://www.fast.ai/posts/2020-07-23-label-smoothing-pytorch.html)
