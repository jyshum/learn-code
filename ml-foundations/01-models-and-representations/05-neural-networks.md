# Neural Networks

## What it is

A neural network is a stack of layers. Each layer applies a linear transformation to its input, then passes the result through a nonlinear activation function. The nonlinearity is what lets the network learn complex patterns. Without it, stacking layers would just be stacking matrix multiplications, which collapses into a single linear transformation.

A neuron takes a weighted sum of its inputs and applies an activation function to produce one output value. A layer is many neurons operating on the same input in parallel. Layers stack: input goes in, passes through hidden layers, and exits as a prediction.

## Why it matters

Neural networks can learn arbitrary functions from data. You do not hand-engineer features. You let the network discover what patterns are useful. This is why they work for tasks like image classification and audio analysis, where you cannot easily specify what to look for in advance.

Depth is the key lever. A shallow network can approximate simple functions. A deep network learns hierarchical representations: early layers detect simple patterns, later layers combine them into complex ones.

## How it works (conceptually)

Think of it as a pipeline of transformations.

**Layer by layer:** Each hidden layer receives the output of the previous layer, applies a weight matrix, adds a bias, then passes the result through an activation function. The network learns what weights to use during training via backpropagation.

**Activation functions** control what each neuron outputs:
- ReLU (`max(0, x)`) is the default for hidden layers. It passes positive values through and zeros out negatives. It trains fast and avoids vanishing gradients.
- Sigmoid squashes output to 0-1. Use it only at the output layer for binary classification.
- Softmax converts a vector of raw scores into probabilities that sum to 1. Use it at the output layer for multi-class classification.

**Backpropagation** is the algorithm that computes gradients layer by layer, working backward from the loss to each weight. PyTorch handles this automatically with `loss.backward()`. You do not implement it manually, but knowing it works backward from output to input explains why activation function choice matters so much in deep networks.

**Dense vs. convolutional layers:** A fully connected (dense) layer connects every neuron to every input. That works for tabular data. For images, convolutional layers share weights spatially across the input. This is more efficient and captures local structure that dense layers miss. See `06-cnns.md` for CNNs specifically.

The mental model: `input → [layer 1: detect edges, tones, simple features] → [layer 2: combine into shapes, patterns] → [layer N: combine into task-specific output]`

## Real example

SickNote's CNN is a neural network. The convolutional layers act as the hidden layers. They extract frequency patterns and temporal patterns from mel spectrograms of cough audio. Early convolutional layers detect low-level frequency energy. Later layers combine those into patterns that distinguish healthy from abnormal coughs.

At the end of the network, dense layers take the combined feature maps and collapse them into a single binary output. BCEWithLogitsLoss with pos_weight then tells the network how wrong that output is, and backpropagation adjusts every layer's weights. The specificity of 0.77 came from the dense output layer being trained to take false negatives seriously, not just from the convolutional feature extraction.

## Key intuitions

- Every layer is just a learned feature transformation. The network is composing simpler transformations into complex ones.
- Depth helps because hierarchical structure exists in most real-world data. Audio, images, and text all have low-level components that combine into high-level meaning.
- ReLU in hidden layers is almost always the right default. Sigmoid in hidden layers causes vanishing gradients, which kills learning in early layers.
- Start shallower than you think you need. Add depth only if your training loss is stuck high (underfitting). More depth is not automatically better.
- The output layer activation matches the task: sigmoid for binary, softmax for multi-class, nothing (linear) for regression.

## Common mistakes

- Don't use fully connected layers on image data because they ignore spatial structure. Every pixel connects to every neuron, so the network cannot learn that nearby pixels relate to each other. Use convolutional layers instead.
- Don't use sigmoid in hidden layers because it saturates near 0 and 1, making gradients near zero. Backpropagation cannot update early layers effectively. Use ReLU.
- Don't skip batch normalization in deep networks because activations shift and grow across layers during training. This slows convergence and makes training unstable. Add `nn.BatchNorm2d` (or `nn.BatchNorm1d`) after convolutional or dense layers.
- Don't add depth before diagnosing the problem. If your model is overfitting, adding more layers makes it worse. Diagnose with training vs. validation loss first.

## Links

- [PyTorch nn.Module documentation](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)
- [CS231n: Neural Networks Part 1 (Stanford)](https://cs231n.github.io/neural-networks-1/)
- [Andrej Karpathy: Neural Networks Zero to Hero](https://karpathy.ai/zero-to-hero.html)
