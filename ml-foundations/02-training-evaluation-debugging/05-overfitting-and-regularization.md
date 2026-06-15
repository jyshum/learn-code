# Overfitting and Regularization

## What it is

Overfitting is when your model memorizes the training data instead of learning patterns that generalize. It performs great on the training set and poorly on validation or test data. The model has learned the noise and specific quirks of your examples, not the underlying signal.

Regularization is any technique that reduces overfitting. It pushes the model toward simpler, more general solutions.

## Why it matters

A model that overfits is useless in production. High training accuracy is not a success signal on its own. The only number that matters is how the model performs on data it has never seen. If you don't monitor the gap between training and validation performance, you can spend days training a model that does not actually work.

## How it works (conceptually)

Overfitting happens for a few reasons: too many parameters relative to your data, training for too many epochs, or no regularization applied. The model has enough capacity to assign a unique response to every training example, so it does.

**Dropout** randomly zeros out a fraction of neurons during each training step. No single neuron can become a crutch. The network is forced to spread its learning across multiple paths. At inference time, you turn dropout off so all neurons contribute. If you forget to call `model.eval()`, you get different outputs every time you run inference.

**L2 regularization (weight decay)** adds a penalty for large weights directly in the optimizer. Weights that grow too large get pushed back down. In PyTorch you set this with `optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)`. Small weights tend to produce smoother, more general decision boundaries.

**Early stopping** means you stop training when validation loss stops improving, not when training loss converges. Training loss almost always keeps going down. That doesn't mean the model is getting better. Watch your validation curve. Stop when it flattens or starts rising.

**Data augmentation** is regularization by expanding variety. If the model sees slightly different versions of each example every epoch, it cannot memorize the exact inputs. It has to learn the underlying pattern. See `03-data/04-data-augmentation.md` for specifics.

**Batch normalization** normalizes activations within each mini-batch. This stabilizes training and has a mild regularizing effect. Most modern architectures include it, and it reduces how much you need to rely on dropout alone.

**The bias-variance tradeoff** is the underlying tension. A model with high bias underfits. It's too simple to capture the signal. A model with high variance overfits. It's too sensitive to the specific training examples it saw. Regularization reduces variance at the cost of a small amount of bias. That trade is almost always worth it.

## Real example

In SickNote, without dropout the CNN reached 0.95 training accuracy but only 0.73 validation accuracy. That gap is a clear sign of overfitting. The model had learned to recognize individual recordings, not cough patterns.

Adding `nn.Dropout(p=0.3)` after the dense layers brought the training-val gap under 0.05. The model stopped relying on specific spectral artifacts in individual mel spectrograms and started learning generalizable cough features. That change, more than any architecture tweak, was what made the model useful.

## Key intuitions

- The first symptom of overfitting is a growing gap between train loss and val loss. Watch for it early.
- If train loss keeps dropping but val loss plateaus or rises, stop training. More epochs will not help.
- Dropout and weight decay are almost always worth trying before adding model complexity.
- Too much regularization causes underfitting. If train and val loss are both high, you've gone too far.
- Data augmentation is free regularization if you're working with images or audio. Use it.

## Common mistakes

- Don't forget to call `model.eval()` at inference because dropout stays active and your predictions become stochastic and unreliable.
- Don't wait for training loss to converge before checking val loss because by then you've already overfit and wasted compute.
- Don't apply heavy dropout everywhere because you'll underfit and the model won't learn anything useful.
- Don't tune architecture before trying early stopping and weight decay because those are cheaper fixes and often enough on their own.

## Links

- [PyTorch Dropout docs](https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html)
- [Understanding the bias-variance tradeoff (fast.ai)](https://www.fast.ai/posts/2018-07-02-adam-weight-decay.html)
- [Early stopping in practice (Papers with Code)](https://paperswithcode.com/methods/category/regularization)
- [Batch Normalization paper (Ioffe & Szegedy, 2015)](https://arxiv.org/abs/1502.03167)
