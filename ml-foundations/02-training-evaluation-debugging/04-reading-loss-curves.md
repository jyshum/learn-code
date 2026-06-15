# Reading Loss Curves

## What it is

A loss curve is a plot of your loss value over training steps or epochs. You always plot two lines: training loss and validation loss. The gap between them is the actual story. One line without the other tells you almost nothing useful.

## Why it matters

Your loss curve is the real-time diagnostic for your training run. It tells you whether your model is learning, memorizing, or stuck. Without reading it actively, you are flying blind. You might run 50 epochs and walk away with a model that peaked at epoch 12.

## How it works (conceptually)

At each epoch, your model sees the training set and updates its weights. You record the average training loss. Then you run inference on the validation set (no weight updates) and record the validation loss.

Healthy training looks like both losses decreasing together. They do not need to be identical, but they should track each other and converge toward a low value.

**Overfitting** is when training loss keeps dropping but validation loss plateaus or climbs. The model is memorizing the training data. It has stopped generalizing. The growing gap between the two lines is your signal.

**Underfitting** is when both losses are high and plateau together. The model is not expressive enough for the problem, or it needs more training, or the learning rate is too low.

**Loss spikes** are sudden jumps in the curve. A bad batch, a learning rate that is too high, or NaN gradients can all cause them. If you only log per epoch, you miss these.

**Oscillating loss** means your learning rate is too high. The optimizer is overshooting the minimum repeatedly. Drop the LR.

**Validation loss lower than training loss** is not a bug. It happens when dropout is active during training and off during eval. It can also happen if your validation set is easier than your training set.

Log per batch when you need to diagnose instability. Log per epoch when you want to see the trend. Use TensorBoard or wandb so you can actually see the curves instead of reading numbers from a terminal.

```python
writer.add_scalars("Loss", {"train": train_loss, "val": val_loss}, epoch)
```

## Real example

In SickNote, training loss dropped smoothly from epoch 1 onward. Validation loss tracked it for the first seven epochs. At epoch 8, val loss flatlined while train loss kept falling. That divergence was the signal.

I triggered a learning rate reduction there, halving the LR with `ReduceLROnPlateau`. After the reduction, val loss dropped another 4% over the next few epochs before stabilizing. Without watching the curve, I would have either stopped too early or kept training past the point of diminishing returns. The curve told me the model still had room to improve with a smaller step size.

## Key intuitions

- The gap between training loss and validation loss is your overfitting gauge. A small gap is good. A growing gap means add regularization or get more data.
- Validation loss is the number you actually care about. Training loss just tells you if the optimizer is working.
- A loss spike mid-training is almost always the learning rate or a corrupted batch. Check your data pipeline first.
- If both losses plateau early and high, changing hyperparameters alone will not save you. The architecture or the data is the problem.
- Smoothing your loss curve in wandb or TensorBoard helps you see trends. Raw per-batch loss is noisy on purpose.

## Common mistakes

- Don't only log per epoch because you will miss spikes and instability that live inside the epoch. You need per-batch logging to diagnose those.
- Don't ignore validation loss because you cannot see overfitting without it. Training loss going down means nothing on its own.
- Don't compare absolute loss values across models that use different loss functions. A BCE loss of 0.3 and a cross-entropy loss of 0.3 are not the same thing and do not indicate equal performance.
- Don't stop training the moment val loss ticks up once. One uptick is noise. A sustained upward trend over several epochs is the real signal.

## Links

- [TensorBoard with PyTorch](https://pytorch.org/tutorials/intermediate/tensorboard_tutorial.html)
- [Weights and Biases quickstart](https://docs.wandb.ai/quickstart)
- [Understanding the bias-variance tradeoff (fast.ai)](https://www.fast.ai/posts/2018-07-12-auto-augment.html)
- [PyTorch ReduceLROnPlateau docs](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html)
