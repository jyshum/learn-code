# Model Selection Cheat Sheet

## What it is

This is a decision guide for choosing the right model given your data type, task, and dataset size. It does not go deep on any single model. It gives you a starting point so you stop staring at a blank notebook wondering whether you need a neural network.

## Why it matters

Picking the wrong model wastes time and produces worse results. A neural network trained on 80 tabular rows will almost always lose to XGBoost. A custom CNN trained from scratch on images will almost always lose to a pretrained ResNet. The model family matters more than hyperparameter tuning. Get the family right first.

## How it works (conceptually)

Start by asking: what is my input type?

**Tabular data (rows and columns of numbers or categories):**
- Under 100k rows and under 50 features: start with XGBoost or random forest.
- Need interpretability for stakeholders or regulators: use logistic regression or a single decision tree.
- Very large dataset over 500k rows: a simple neural network can compete, but try XGBoost first anyway.

**Image data (pixels, spectrograms, spatial grids):**
- Classification (what is this image?): use ResNet-18 or EfficientNet pretrained on ImageNet. Fine-tune on your data.
- Segmentation (label every pixel): use U-Net.
- Unsupervised exploration (find similar images, no labels): use a beta-VAE.

**Audio data:**
- Convert to a mel spectrogram first. Then treat it as an image and use a pretrained ResNet-18. Do not try to work with raw waveforms unless you have a strong reason.

**Very few labeled examples:**
- Use transfer learning with a pretrained model. Fine-tune on your small labeled set.
- Or go unsupervised with an autoencoder or beta-VAE and skip labels entirely.

**No labels at all:**
- Use an autoencoder or beta-VAE for representation learning.
- Then run clustering (k-means or DBSCAN) on the learned features.

---

### Summary table

| Input | Task | Model | Loss |
|-------|------|-------|------|
| Tabular | Binary classification | XGBoost | logloss |
| Tabular | Regression | XGBoost | RMSE |
| Image | Classification | ResNet-18 (pretrained) | CrossEntropyLoss |
| Spectrogram | Binary classification | ResNet-18 (pretrained) | BCEWithLogitsLoss |
| Image | Segmentation | U-Net | Dice loss |
| Any | Unsupervised representation | beta-VAE | Reconstruction + KL |

## Real example

For paleo body mass estimation, the task was predicting body mass of extinct dinosaurs from limb proportions and skeletal measurements. The dataset had around 80 extant mammal specimens used for training. The inputs were structured numerical features: femur length, hip width, body length. That is a tabular regression problem with a small dataset. XGBoost was the right first choice. Not a neural network. Not a CNN. The dataset is too small and the inputs are not images. A three-layer MLP trained on 80 rows would overfit immediately and lose to a well-regularized XGBoost tree. Starting with XGBoost also gave feature importances for free, which mattered when explaining which skeletal measurements drove the predictions.

## Key intuitions

- Start simple. A model you understand is better than a model that slightly outperforms on one metric.
- Pretrained beats scratch. If your input is an image, a pretrained ResNet trained on ImageNet knows more about visual features than your training loop will learn from your 500 examples.
- Tabular data is XGBoost territory. Neural networks almost never win on tabular data under 10k rows.
- Unsupervised is underused. If you have no labels and limited time, a beta-VAE or autoencoder gives you a way to explore structure without annotation work.
- Complexity is a cost. Every layer you add is another thing that can go wrong, overfit, or take longer to train.

## Common mistakes

- Don't reach for a neural network before establishing a simple baseline, because you lose the ability to tell whether the complexity is helping.
- Don't use a neural network for tabular data under 10k rows, because XGBoost will almost certainly win and train in seconds instead of minutes.
- Don't build a custom CNN from scratch for image classification, because a pretrained ResNet-18 fine-tuned for two epochs will outperform it unless you have hundreds of thousands of images.
- Don't treat audio as a 1D signal and pass it raw into an MLP, because converting to a mel spectrogram first lets you use every piece of pretrained image infrastructure that already exists.

## Links

- [scikit-learn model selection guide](https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html)
- [PyTorch pretrained ResNet fine-tuning tutorial](https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html)
- [XGBoost documentation](https://xgboost.readthedocs.io/en/stable/)
- [U-Net original paper (Ronneberger et al., 2015)](https://arxiv.org/abs/1505.04597)
