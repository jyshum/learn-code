# Tabular Models (XGBoost, Random Forests, Logistic Regression)

## What it is

Tabular data is structured data in rows and columns. Each row is a sample. Each column is a feature. Think spreadsheets, database exports, survey responses, clinical records. This is the opposite of images, audio, or text.

Tabular models are classifiers and regressors built for this format. The main ones you will use:

- **Logistic regression**: a linear function of your features passed through a sigmoid. Outputs a probability. Simple, fast, and interpretable.
- **Decision trees**: recursively split the data on feature thresholds. Each split is a yes/no question. Easy to inspect but overfits badly on its own.
- **Random forests**: an ensemble of many decision trees. Each tree trains on a random subset of data and features. Final prediction is the average across trees. Much more stable than a single tree.
- **XGBoost (Gradient Boosted Trees)**: builds trees sequentially. Each new tree corrects the errors of the previous ones. Currently the state-of-the-art for most tabular ML tasks.


## Why it matters

Most real-world ML problems are tabular. Healthcare records, logistics data, customer behavior, sensor readings. All tabular.

You do not need a neural network for most of these. XGBoost or a random forest will often match or beat a neural network, train in seconds, and give you built-in feature importance for free.

Picking the right model class is faster than tuning the wrong one.


## How it works (conceptually)

**Logistic regression** learns a weight for each feature. Bigger weight means that feature pushes the prediction harder. The output is a sigmoid of the weighted sum. If the relationship between your features and your target is roughly linear, logistic regression will work well and is easy to explain to stakeholders.

**Decision trees** ask a sequence of yes/no questions about your features. "Is distance_to_facility greater than 12km? Yes. Is transport_mode equal to walking? Yes. Predict: unreachable." The tree learns which questions to ask and in what order by finding splits that best separate classes. A single tree goes deep and memorizes the training data.

**Random forests** fix the overfitting problem by training hundreds of trees on different random slices of your data and features. No single tree sees the full picture. Their errors are uncorrelated, so averaging them washes out noise and gives you a much more reliable prediction.

**XGBoost** goes further. Instead of training trees independently, it trains them sequentially. Tree 1 makes predictions. Tree 2 learns to fix Tree 1's residual errors. Tree 3 fixes what Tree 2 still got wrong. This boosting process concentrates model capacity on the hardest examples and converges to very accurate predictions with relatively few trees. It also handles missing values natively and deals gracefully with mixed feature types.


## Real example

In REACH, I used XGBoost to predict reachability scores from structured features: distance to facility, transport mode, demographic indicators, and geographic zone. The training loop was straightforward. No image processing. No tokenization. Just a feature matrix and a target column.

After training, I pulled the feature importance scores. Transport mode came out as the strongest predictor by a large margin, stronger than raw distance. That was not a model artifact. It matched exactly what the field team had been saying anecdotally. Surfacing that with a number gave the intervention design team something concrete to act on.

XGBoost trained in under a minute on that dataset. A neural network would have taken far longer to tune and given me less interpretability for the same accuracy.


## Key intuitions

- For tabular data under 100k rows, try XGBoost first. It is fast to train and wins more often than not.
- Tree-based models are scale-invariant. They split on thresholds. Whether a feature is measured in meters or kilometers does not matter.
- Feature importance from XGBoost and random forests is genuinely useful. It is not just a diagnostic. It tells you what the model actually learned to rely on.
- Neural networks start to win on tabular data when you have very large datasets (hundreds of thousands of rows or more) or when feature interactions are extremely high-dimensional.
- Logistic regression is not a consolation prize. If your problem is roughly linear, it is the right tool. It trains instantly and is trivial to audit.


## Common mistakes

- Don't normalize features before feeding them to XGBoost or a random forest, because trees are scale-invariant and normalization adds unnecessary preprocessing with zero benefit.
- Don't skip cross-validation when tuning XGBoost hyperparameters, because a single train/val split gives you a noisy estimate and you will overfit your hyperparameters to one lucky split.
- Don't ignore feature importance outputs, because they tell you whether your model learned something real or latched onto a spurious correlation, and catching that early saves you from deploying a broken model.
- Don't reach for a neural network by default on tabular data, because tree-based models are faster to train, easier to interpret, and often more accurate at small-to-medium dataset sizes.


## Links

- [XGBoost documentation](https://xgboost.readthedocs.io/en/stable/)
- [Scikit-learn: Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)
- [Why tree-based models still outperform deep learning on tabular data (Grinsztajn et al., 2022)](https://arxiv.org/abs/2207.08815)
- [Kaggle: How to win with XGBoost](https://www.kaggle.com/code/stuarthallows/using-xgboost-with-scikit-learn)
