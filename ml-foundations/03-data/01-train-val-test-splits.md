# Train/Val/Test Splits

## What it is

A train/val/test split divides your dataset into three non-overlapping subsets. The training set is what the model learns from. The validation set is what you use to tune hyperparameters and make decisions during development. The test set is a one-time final evaluation you run only after all decisions are made. You never touch the test set until you are done.

Typical splits are 70/15/15 or 80/10/10. For large datasets these proportions work well. For small datasets (under 1000 examples), use k-fold cross-validation instead.

## Why it matters

If you evaluate on the test set while making decisions, you are leaking information. Your choices get optimized toward the test set, and you end up overfitting to it without realizing it. The test set only gives you an honest estimate of generalization if you have never seen it during development.

The validation set exists so that your hyperparameter tuning has a target that is not the training data. Without it, you have no way to know if a change improves generalization or just memorization.

## How it works (conceptually)

Split your data once, before any training. Keep the test set in a drawer and do not open it.

During development, train on the training set and evaluate on the validation set. Change your learning rate, architecture depth, regularization strength, or any other hyperparameter based on validation metrics. When you are done making decisions, run on the test set exactly once and report that number.

For imbalanced datasets, use stratified splitting. This means each split gets the same class ratio as the full dataset. If your full dataset is 80% class A and 20% class B, your training, validation, and test sets should each be 80/20. Without this, small sets can end up with very different ratios by chance, which distorts your reported metrics.

For time-series data, never shuffle before splitting. Put the earliest data in training, the next chunk in validation, and the most recent data in test. Shuffling leaks future information into training and makes your model look better than it will perform in the real world.

k-fold cross-validation is an alternative for small datasets. Divide the data into k equal folds. Train on k-1 folds and validate on the remaining fold. Rotate through all k combinations and average the results. This gives you a more reliable estimate of generalization because every example gets used for validation exactly once.

## Real example

In SickNote, I used an 80/10/10 stratified split on COUGHVID to preserve the 79.7%/20.3% abnormal/healthy ratio across all three sets. Before I added stratification, a random split gave the validation set 85% abnormal recordings by chance. The validation accuracy looked inflated during training because the model could score well by leaning harder into the majority class. When I ran on the test set, the numbers dropped. Adding stratification fixed the mismatch and gave consistent metrics across all three sets.

## Key intuitions

- The test set is sacred. You touch it once. If you are checking test metrics more than once, you are overusing it and the number is no longer trustworthy.
- Validation loss tells you how well your model generalizes to unseen data during development. If validation loss goes up while training loss goes down, you are overfitting.
- Stratification is not optional when classes are imbalanced. A small validation set without stratification can easily end up with a different class ratio than training, and your metrics will mislead you.
- With small datasets, a single val/test split is unreliable. k-fold gives you more stable estimates by rotating which examples are held out.
- For time-series, the split must respect time order. The model cannot have seen the future during training.

## Common mistakes

- Don't use the test set to pick your best model or tune hyperparameters, because you are leaking information and your final number will be optimistic. That is what the validation set is for.
- Don't shuffle time-series data before splitting, because future data bleeds into the training window and your model learns to cheat rather than generalize.
- Don't skip stratification on imbalanced classes, because random splits introduce distribution mismatch between sets and your validation metrics will not reflect real performance.
- Don't use a single val/test split on a dataset with fewer than 1000 examples, because the metric variance is too high to trust. Use k-fold instead.

## Links

- [scikit-learn: train_test_split with stratify](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
- [scikit-learn: KFold and StratifiedKFold](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Andrej Karpathy: A Recipe for Training Neural Networks (data splits section)](http://karpathy.github.io/2019/04/25/recipe/)
- [fast.ai: Lesson 2, data splits and validation sets](https://course.fast.ai/)
