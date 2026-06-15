# Data Leakage

## What it is

Data leakage is when information from your validation or test set somehow influences the training process. The model appears to generalize well, but it is actually seeing held-out or future information during training. The result is a model that looks great on paper and fails in production.

There are three main flavors.

**Target leakage** is when a feature in your training data is derived from or correlated with the target in a way that would not be available at inference time. Example: using "prescribed medication" as a feature when predicting "patient has disease." The prescription happens after diagnosis, so it would never exist at the moment you need to make a prediction.

**Train-test contamination** is when preprocessing steps are fit on the entire dataset before splitting. Your test set statistics bleed into the training normalization. The model has effectively "seen" the test set, just indirectly.

**Look-ahead bias** applies to time series. You accidentally use features computed from future time steps to predict the present. The future is not available at inference time, so the model learns patterns it could never actually exploit.

## Why it matters

Leakage gives you a false sense of model quality. You ship the model. Performance collapses on real data. You have no idea why because your metrics looked fine.

The dangerous part is that leakage is often subtle. You do not notice it until the model is live and failing in ways that are hard to diagnose.

## How it works (conceptually)

Imagine your test set contains recordings with an average volume of 0.42. If you normalize all recordings using that average before splitting, your training normalization is anchored to a number that includes test data. The training set and test set are now statistically coupled. The model trains on data that is subtly aligned with test-set statistics, and your evaluation metric reflects that alignment rather than true generalization.

The fix is always the same direction: fit preprocessing on training data only, then apply it to val and test.

```python
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)
```

Any step that involves "fitting" to data must only see training data. This includes StandardScaler, MinMaxScaler, mean imputation, label encoding fit, and feature selection thresholds.

## Real example

In an early SickNote experiment, mel spectrogram normalization was computed across all recordings before splitting into train, val, and test. The mean and standard deviation used to normalize each spectrogram were derived from the full dataset, including the val and test splits.

This caused val set statistics to influence the training normalization. Val AUC was inflated by about 0.03. Fixing it to compute normalization only on the training recordings dropped val AUC slightly, but gave a more honest estimate of what the model could actually do on new audio.

The fix was simple: compute the mean and std from `X_train` only, then apply the same values to `X_val` and `X_test`. The model did not change. Only the honesty of the evaluation did.

## Key intuitions

- If your model performs suspiciously well (very high AUC, near-perfect accuracy on a hard problem), suspect leakage before celebrating.
- The question to ask for every feature: "Would this value exist at the moment I need to make this prediction?" If no, it is target leakage.
- Preprocessing is not neutral. Fitting a scaler is a statistical operation. That operation must happen inside the training boundary, not outside it.
- Performance that drops dramatically on truly new data, but was fine on your held-out test set, is a strong signal of contamination.
- In time series, always split by time, not randomly. A random split creates look-ahead bias by construction.

## Common mistakes

- Don't fit scalers or encoders on the full dataset before splitting, because test set statistics contaminate training and inflate your evaluation metrics.
- Don't include post-event features as model inputs, because those values do not exist at prediction time and the model learns a pattern it can never replicate in production.
- Don't reuse your test set for multiple evaluation rounds, because repeated evaluation on the same test set causes you to implicitly tune toward it, which is a soft form of leakage.
- Don't assume that leakage is always obvious, because it often hides inside helper functions or pipeline steps that "helpfully" operate on the full dataset.

## Links

- [Scikit-learn: Pipelines to prevent leakage](https://scikit-learn.org/stable/modules/compose.html#pipeline)
- [Kaggle: Data Leakage explainer](https://www.kaggle.com/learn/feature-engineering) (see the leakage section)
- [scikit-learn cross_val_score vs manual splits](https://scikit-learn.org/stable/modules/cross_validation.html)
