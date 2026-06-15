# What Is a Model

## What it is

A model is a function that maps inputs to outputs. That's it. Everything else is details about how that function is defined and how it learns.

The function has two parts: an architecture and parameters. The architecture is the structure of the function. A CNN is structured to process grids of numbers. A decision tree is structured to make binary splits. The architecture defines what kinds of patterns the function can even represent. The parameters (also called weights) are the numbers that define the specific function within that structure. Training is the process of finding good parameter values.

Before training, the weights are random. The model maps inputs to outputs, but the outputs are garbage. After training, the weights encode patterns learned from your data. The model now maps inputs to useful outputs.

## Why it matters

Every decision you make in ML flows from what you want the model to do. The architecture you choose, the data you feed it, the loss you optimize, and the evaluation metric you care about, all of these are downstream of what the model is supposed to learn.

If you don't have a clear picture of what function you're trying to approximate, you'll make bad choices at every step. A model is not a magic pattern finder. It's a function with a fixed structure that you're training to approximate some target mapping.

## How it works (conceptually)

During training, you show the model many input-output pairs. For each input, the model produces a prediction using its current weights. A loss function measures how wrong that prediction is. The optimizer then nudges the weights slightly in the direction that would reduce the loss. Repeat this millions of times and the weights gradually encode the patterns in your data.

During inference, the weights are frozen. You're just running the function forward. Input goes in, output comes out. No learning happens.

In deep learning, the function is composed of many layers stacked on top of each other. Each layer builds a higher-level representation of the input. Early layers detect low-level features like edges or frequency peaks. Middle layers combine those into shapes or patterns. Final layers detect task-specific features. The model learns these representations automatically from data, not from rules you write by hand.

The weights after training are a compressed encoding of the patterns in your training data. The model "knows" things as numerical relationships stored in tensors, not as explicit if-then logic you can read.

## Real example

In SickNote, the CNN takes a mel spectrogram as input. A mel spectrogram is a 2D array where one axis is frequency and the other is time. Each cell holds the intensity of that frequency at that moment. The model is a function that takes this 2D array and outputs a single number: the probability that the cough is abnormal.

The layers in between learn to detect frequency patterns in early layers, temporal patterns in middle layers, and cough-specific acoustic signatures in the final layers. None of those intermediate representations were hand-coded. They emerged from training on labeled COUGHVID recordings.

After training, the weights encode what distinguishes an abnormal cough from a healthy one, purely as numerical relationships across the filter banks. Grad-CAM let me visualize which parts of the spectrogram the model was responding to, which was the only way to sanity-check that it was picking up on acoustically meaningful features rather than recording artifacts.

## Key intuitions

- The architecture sets the ceiling. A linear model cannot learn non-linear patterns no matter how long you train it.
- The model does not understand anything. It finds correlations in data and encodes them as weights. Figuring out whether those correlations are meaningful is your job.
- More parameters do not mean a better model. They mean a more expressive function that can also memorize noise.
- The weights are the model. Everything else is scaffolding to find good weights.
- Inference and training are different modes. During inference you are running a fixed function. During training you are searching for a better one.

## Common mistakes

- Don't assume more parameters equals better performance, because larger models overfit on small datasets and you end up memorizing training examples instead of learning generalizable patterns.
- Don't treat the model as a black box and skip probing what it learned, because the model might be exploiting spurious correlations in your data that will collapse on new inputs.
- Don't conflate architecture choice with hyperparameter tuning, because choosing the wrong architecture for your data structure (e.g., a fully connected net on image data) is a structural problem that tuning learning rates will not fix.
- Don't forget that the model only knows what was in your training data, because if the training distribution doesn't match deployment conditions the weights will encode the wrong patterns.

## Links

- [Stanford CS229 Lecture Notes: Supervised Learning](https://cs229.stanford.edu/notes2022fall/main_notes.pdf)
- [PyTorch: What is a model (nn.Module docs)](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)
- [Andrej Karpathy: The spelled-out intro to neural networks (YouTube)](https://www.youtube.com/watch?v=VMj-3S1tku0)
- [distill.pub: Feature Visualization](https://distill.pub/2017/feature-visualization/)
