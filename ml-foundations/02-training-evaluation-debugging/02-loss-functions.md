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
