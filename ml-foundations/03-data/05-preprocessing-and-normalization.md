# Preprocessing and Normalization

## What it is

Preprocessing is everything you do to raw data before it touches your model. Normalization is one part of that: rescaling your input features so they live on a comparable numeric range. The goal is to give your model inputs that are clean, consistent, and well-scaled.

## Why it matters

Neural networks learn by gradient descent. Gradients flow back through the network and nudge weights toward better predictions. If one feature ranges from 0 to 1,000,000 and another ranges from 0 to 1, the first feature dominates the loss landscape. The optimizer will take huge steps in some directions and tiny steps in others. Training becomes slow, unstable, or broken entirely.

Normalization puts every feature on a level playing field. The optimizer can then move through the loss landscape with consistent step sizes in every direction.

## How it works (conceptually)

There are three normalization strategies you will reach for most often.

**Z-score normalization (standardization):** Subtract the mean and divide by the standard deviation. The output has mean 0 and standard deviation 1. This is the right default for neural networks when you do not know the theoretical range of your data.

**Min-max normalization:** Scale all values to [0, 1] using the observed min and max. Use this when you know the theoretical bounds of your data. It is sensitive to outliers because one extreme value can compress everything else into a narrow band.

**ImageNet normalization:** When you load a pretrained CNN (ResNet, EfficientNet, etc.), the weights were trained on images normalized with specific constants: mean=[0.485, 0.456, 0.406] and std=[0.229, 0.224, 0.225] per channel. You must apply this same normalization to your inputs. Skipping it breaks transfer learning because the model's learned features assume those exact input statistics.

```python
transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
```

**Mel spectrograms** are their own case. You convert raw audio to a Short-Time Fourier Transform, apply a mel filterbank, then apply log compression. That log compression is itself a normalization step. It compresses the amplitude scale to match how human perception works, and it is what makes spectrograms trainable. Without it, quiet sounds are invisible.

**Tabular data and tree-based models** are the exception. XGBoost and random forests split on thresholds. They do not care about scale. You do not need to normalize for those models. For logistic regression and neural networks on tabular data, normalize.

**Missing values** need to be handled before you normalize. You cannot compute a mean or standard deviation over NaN values. Fill missing values first. Use median for skewed distributions. Use mean for roughly normal distributions. For missingness that carries signal, fill with 0 and add a binary "was_missing" flag feature alongside it.

**The critical rule:** fit your normalization statistics on the training set only. Compute the mean and standard deviation from training data. Then apply those exact values to your validation and test sets. Never peek at val or test to compute statistics. That is data leakage. See `03-data/02-data-leakage.md`.

## Real example

In SickNote, I normalized each mel spectrogram to [0, 1] individually, scaling by that spectrogram's own min and max. It seemed reasonable. Each spectrogram had consistent contrast.

It was wrong.

Per-spectrogram normalization destroys amplitude information across recordings. A loud cough and a quiet cough end up with the same normalized range, so the model cannot use absolute energy level as a feature. Switching to global normalization across the training set, using training-set mean and std applied consistently to val and test, improved val AUC by 0.02. It also forced a pipeline restructure: the normalization statistics now had to be computed once, saved, and loaded at inference time. That was the right design anyway.

## Key intuitions

- Normalize. Always. The only exception is tree-based models (XGBoost, random forests) on tabular data.
- Fit normalization on training data only. Apply those statistics to everything else.
- Per-sample normalization and global normalization are not the same thing. Know which one you are doing and why.
- Pretrained CNNs require ImageNet normalization. It is not optional.
- Log compression on spectrograms is a normalization step. If you skip it, your model will struggle to learn anything from quiet signals.

## Common mistakes

- Don't compute normalization statistics on val or test data because you introduce leakage and your reported metrics will be optimistic. The model has seen information about the test distribution during preprocessing.
- Don't skip normalization before a neural network or logistic regression because the optimizer will struggle with mismatched feature scales and training will be slow or unstable.
- Don't use ImageNet normalization values when you are training a CNN from scratch because those constants are only meaningful when the weights were pretrained on ImageNet. Your from-scratch model needs statistics computed from your own dataset.
- Don't normalize before imputing missing values because NaNs will propagate through your statistics and corrupt the entire feature column.

## Links

- [sklearn preprocessing docs](https://scikit-learn.org/stable/modules/preprocessing.html)
- [PyTorch transforms docs](https://pytorch.org/vision/stable/transforms.html)
- [Librosa mel spectrogram](https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html)
- [CS231n: Data Preprocessing](https://cs231n.github.io/neural-networks-2/#datapre)
