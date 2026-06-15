# Class Imbalance

## What it is

Class imbalance is when one class in your dataset appears far more often than the other. In SickNote, 79.7% of recordings were labeled "abnormal" and only 20.3% were "healthy." That's a 4:1 ratio. The model can score 79.7% accuracy by doing nothing except predicting "abnormal" every single time. High accuracy, completely useless model.

## Why it matters

Accuracy lies to you on imbalanced data. A model that always predicts the majority class looks good on paper. But if you care about catching the minority class (and you usually do), you are optimizing for the wrong thing from the start. In medical or safety-critical applications, missing the minority class is often the actual failure mode you need to prevent. Imbalance warps what the model learns to do.

## How it works (conceptually)

There are four main ways to address class imbalance. They are not mutually exclusive.

**Loss-level weighting** is the cleanest fix. You tell the loss function that mistakes on the minority class cost more. In PyTorch binary classification, that means setting `pos_weight` in `BCEWithLogitsLoss`. For multi-class problems, pass `weight` to `CrossEntropyLoss`. The model still sees the original data distribution, but the gradient signal is rebalanced so minority class errors hurt more.

**Oversampling** duplicates or synthesizes minority class examples to balance the dataset. SMOTE generates synthetic in-between examples rather than just copying. This can help, but it risks overfitting on synthetic data. Always apply SMOTE only after splitting your data, never before, or you leak synthetic versions of your test examples into training.

**Undersampling** randomly removes majority class examples to balance the dataset. It costs you real data and usually performs worse than weighting. Avoid it unless your dataset is enormous and you cannot afford to train on all of it.

**Threshold adjustment** does not change training at all. After you train the model, you shift the decision threshold away from 0.5 toward the minority class. This trades sensitivity for specificity (or vice versa). Use the ROC curve and Youden's J statistic to find the threshold that balances the tradeoff you actually care about.

**Focal loss** is a variant of cross-entropy that downweights easy examples. If most of your majority class examples are confidently classified and contribute little useful gradient, focal loss tells the model to ignore them and focus on the hard cases. It was developed for object detection but applies anywhere you have heavy class imbalance with many easy majority examples.

## Real example

In SickNote, the primary fix for the 79.7%/20.3% imbalance was `pos_weight=3.9` in `BCEWithLogitsLoss`. The value 3.9 comes from the inverse class frequency ratio: 79.7 / 20.3. This told the model that a false negative on a healthy cough costs 3.9 times more than a false positive. After training, I also used Youden's J statistic on the validation ROC curve to find the optimal decision threshold, which was not 0.5. The combined result was sensitivity=0.82 and specificity=0.77. I also tried SMOTE oversampling on top of the loss weighting. It gave no additional benefit. The loss weighting had already solved the core problem.

## Key intuitions

- Fix imbalance at the loss level first. It is the cleanest intervention and has no side effects. Try oversampling only if loss weighting is not enough.
- Accuracy is not a valid metric for imbalanced problems. Use sensitivity, specificity, F1, or AUC instead.
- `pos_weight` is just the ratio of negative to positive examples. If you have 4x more negatives than positives, set `pos_weight=4`.
- SMOTE and the test set must never overlap. Synthetic examples generated from real test examples make your evaluation numbers meaningless.
- Threshold 0.5 is arbitrary. After training, always check whether a different threshold gives you a better tradeoff for your specific use case.

## Common mistakes

- Don't report accuracy on imbalanced data because a model that ignores your minority class entirely will look accurate.
- Don't apply SMOTE before your train/test split because synthetic examples derived from test data will leak into training and inflate your metrics.
- Don't try oversampling without first checking if loss weighting already solved it because stacking interventions adds complexity without guaranteed benefit.
- Don't forget that pos_weight changes training behavior but not the output threshold. You still need to evaluate the ROC curve and pick the right operating point after training.

## Links

- [PyTorch BCEWithLogitsLoss pos_weight](https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)
- [imbalanced-learn: SMOTE and oversampling toolkit](https://imbalanced-learn.org/stable/)
- [Focal Loss paper (Lin et al., 2017)](https://arxiv.org/abs/1708.02002)
- [Youden's J and ROC threshold selection](https://en.wikipedia.org/wiki/Youden%27s_J_statistic)
