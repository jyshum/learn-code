# Evaluation Metrics

## What it is

Evaluation metrics are numbers that tell you how well your model is performing. Loss tells you how training is going. Metrics tell you whether the model is actually useful. They are not the same thing, and optimizing one does not guarantee the other.

The most important metrics for classification are built from four numbers: true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN). Everything else is a combination of these.

## Why it matters

Accuracy looks clean and simple. It is also the most misleading metric you can report on an imbalanced dataset.

In SickNote, 79.7% of recordings were labeled abnormal. A model that predicts "abnormal" for every single input gets 0.797 accuracy without learning anything. It would be useless in a clinic. But if you only look at accuracy, it looks nearly as good as a well-trained model.

Choosing the wrong metric means you ship a model that looks good on paper and fails in practice. The metric you optimize is the behavior you get.

## How it works (conceptually)

Start with the confusion matrix. Every prediction your model makes falls into one of four buckets:

- TP: model said positive, label was positive. Correct.
- FP: model said positive, label was negative. False alarm.
- TN: model said negative, label was negative. Correct.
- FN: model said negative, label was positive. Missed it.

From these four numbers, you get everything else.

**Precision** is how trustworthy your positive predictions are. Of every time you said "positive," how often were you right? `TP / (TP + FP)`. High precision means few false alarms.

**Recall (sensitivity)** is how well you catch actual positives. Of every true positive case, how many did you find? `TP / (TP + FN)`. High recall means few misses.

**Specificity** is recall for the negative class. Of all actual negatives, how many did you correctly call negative? `TN / (TN + FP)`. This is critical in medical settings where false alarms have real costs.

**F1 score** is the harmonic mean of precision and recall. It penalizes models that sacrifice one for the other. It is more informative than accuracy on imbalanced data, but it still collapses two numbers into one and hides the tradeoff between precision and recall.

**ROC curve** plots sensitivity against 1-specificity at every possible classification threshold. **AUC** (area under the ROC curve) summarizes this into one number. AUC of 0.5 means your model is guessing randomly. AUC of 1.0 means it is perfect. AUC measures discrimination ability across all thresholds, regardless of which threshold you actually use.

**Precision-Recall curve** plots precision against recall at every threshold. For highly imbalanced datasets, this is more informative than ROC because it focuses entirely on the positive class and does not give credit for correctly predicting negatives.

**Youden's J index** is `sensitivity + specificity - 1`. You can compute it at every point on the ROC curve and pick the threshold that maximizes it. This gives you an optimal operating point that balances catching true positives and avoiding false alarms.

For **regression tasks**, the key metrics are:
- MAE (mean absolute error): average absolute difference between predictions and targets. Easy to interpret.
- RMSE (root mean squared error): penalizes large errors more heavily than MAE.
- R-squared: proportion of variance in the target explained by the model. Closer to 1.0 is better.

For **segmentation tasks**, the key metrics are:
- IoU (Intersection over Union): overlap between predicted mask and true mask, divided by their union. Standard for object detection and segmentation.
- Dice coefficient: `2 * (overlap) / (sum of both masks)`. Closely related to F1. Common in medical image segmentation.

## Real example

In SickNote, I initially reported F1 score during development. It looked reasonable. But when I broke it down, I found the model was sacrificing specificity to get high sensitivity, which made F1 look decent while generating too many false positives.

The clinical framing changed everything. A false negative (missing a sick patient) and a false positive (telling a healthy person they are sick) have different costs. F1 treats them as equivalent. They are not.

I switched to reporting both sensitivity and specificity separately, then used Youden's J index to pick the classification threshold instead of defaulting to 0.5. Maximizing Youden's J gave specificity of 0.77 and sensitivity of 0.82. Those numbers matched the clinical requirements better than anything F1 optimization had found.

The default 0.5 threshold was not wrong in principle. It was just wrong for this problem.

## Key intuitions

- Accuracy on an imbalanced dataset is almost meaningless. Always check the class distribution before trusting it.
- Sensitivity and specificity together tell the full story for binary classifiers. One number is not enough.
- The classification threshold is a hyperparameter. The default 0.5 is a guess. Optimize it using Youden's J or your domain requirements.
- AUC measures how good your model is across all thresholds. Your chosen threshold determines how you actually use it. Both matter, but they answer different questions.
- Precision-Recall curves are more useful than ROC curves when the negative class heavily outnumbers the positive class.

## Common mistakes

- Don't report only accuracy on imbalanced datasets because a model that ignores the minority class can score very high and still be useless.
- Don't use 0.5 as your default threshold because the optimal threshold depends on your class distribution and the relative cost of false positives versus false negatives.
- Don't collapse everything into a single metric like F1 because it hides the precision-recall tradeoff, which often matters more than the aggregate score.
- Don't confuse AUC with performance at your actual operating threshold because a model with high AUC can still have poor precision or recall at the threshold you deploy.

## Links

- [scikit-learn: Classification metrics guide](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [Youden's J statistic (Wikipedia)](https://en.wikipedia.org/wiki/Youden%27s_J_statistic)
- [The Precision-Recall Plot Is More Informative than the ROC Plot (Davis & Goadrich, 2006)](https://dl.acm.org/doi/10.1145/1143844.1143874)
- [torchmetrics documentation](https://torchmetrics.readthedocs.io/en/stable/)
