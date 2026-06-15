# Task Types

## What it is

A task type is the category of prediction problem your model is solving. It determines your output layer, your loss function, and your evaluation metrics. Get it wrong and nothing downstream will save you.

The main task types you will encounter:

**Binary classification**: predict one of two classes. Healthy vs. abnormal. Spam vs. not spam. Output is a single probability between 0 and 1. Loss: BCEWithLogitsLoss.

**Multi-class classification**: predict one of N mutually exclusive classes. A digit is either 0, 1, 2, or some other single digit. Output is N probabilities that sum to 1 via softmax. Loss: CrossEntropyLoss.

**Multi-label classification**: each input can belong to multiple classes at the same time. A CT scan might show both a fracture and calcification. Output is N independent binary predictions. Loss: BCEWithLogitsLoss applied per class.

**Regression**: predict a continuous number. Body mass in kilograms. House price in dollars. Output is a single scalar. Loss: MSE or MAE.

**Segmentation**: assign a class label to every pixel (or voxel) in an image. Which pixels are bone? Which are rock matrix? Output is a mask the same size as the input. Loss: Dice loss or pixel-wise CrossEntropyLoss.

**Anomaly detection**: identify inputs that do not match the training distribution. You train on normal examples and flag anything that sits far from them at inference time.

## Why it matters

Your task type is the contract between your model and the real world. If you pick binary classification when the underlying decision is continuous, you throw away information. If you pick regression when there are truly only two outcomes, you are predicting a number that has no meaning.

The task type locks in everything else. Change the task type and you change the output layer, the loss, the metrics, and sometimes the architecture. It is the first decision to get right, not the last.

## How it works (conceptually)

Every task type maps to a specific output structure.

Binary classification ends with a sigmoid. You get one number. You pick a threshold (usually 0.5) to convert it to a class label.

Multi-class classification ends with a softmax across N logits. The model produces a probability distribution. You pick the class with the highest probability.

Multi-label classification ends with N independent sigmoids. Each output fires independently. Multiple can be above threshold at the same time.

Regression ends with a linear layer and no activation. The output is unconstrained, which is what you want when predicting a real-valued quantity.

Segmentation is classification applied at every pixel. A U-Net runs an encoder to compress the image and a decoder to restore spatial resolution. Each pixel gets its own class prediction.

Anomaly detection does not require labeled anomalies. You encode normal inputs into a latent space. At inference time, you measure distance from the cluster of normal examples. Anything far away is flagged.

## Real example

In REACH, the decision was to use regression (predict a continuous reachability score) rather than binary classification (reachable vs. not reachable). That choice was deliberate. Knowing a patient scores 0.3 vs. 0.7 tells a healthcare planner exactly how much intervention is needed and where to prioritize resources. A binary yes/no collapses that gradient into a coin flip at the boundary. Regression preserved the information that made the output actionable.

In the CT segmentation project (paleo-tech), the task is segmentation, not classification. You are not asking "is this scan a fossil?" You are asking "which voxels in this scan are bone and which are rock matrix?" That pixel-level distinction requires a U-Net architecture with Dice loss, not a classifier with CrossEntropyLoss on the whole image.

## Key intuitions

- The task type determines everything downstream: output layer, loss function, evaluation metrics.
- When in doubt, start with classification. Convert to regression only if the threshold is genuinely arbitrary and the continuous value has meaning.
- Multi-label and multi-class are not the same. If your categories are mutually exclusive, use multi-class. If an input can belong to several categories at once, use multi-label.
- Segmentation is just classification applied spatially. If you understand CrossEntropyLoss on a single input, you already understand pixel-wise CrossEntropyLoss.
- Anomaly detection is often the right choice when you have plenty of normal data but rare or unlabeled failure cases.

## Common mistakes

- Don't treat ordinal categories as regression targets because the spacing between categories is not real. A pain scale of 1-10 is not continuous. Predicting 3.7 is meaningless.
- Don't use binary classification when the decision boundary is genuinely continuous because you lose the gradient that makes predictions actionable. REACH is the example.
- Don't use multi-class when inputs genuinely belong to multiple categories because the softmax forces the model to pick one winner and suppresses the others.
- Don't default to anomaly detection just because labeling is hard. If you can label even a small set of anomalies, a supervised approach will almost always outperform distance-based detection.

## Links

- [PyTorch Loss Functions overview](https://pytorch.org/docs/stable/nn.html#loss-functions)
- [U-Net paper (Ronneberger et al., 2015)](https://arxiv.org/abs/1505.04597)
- [Scikit-learn: Choosing the right estimator](https://scikit-learn.org/stable/machine_learning_map.html)
