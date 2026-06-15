# Transformers and LLMs

## What it is

A transformer is a neural network architecture built on self-attention: a mechanism that lets every position in a sequence directly look at every other position and decide how much to weight it. Large language models (LLMs) are transformers trained on massive text corpora to predict the next token. After enough training data, they develop general-purpose language understanding and generation capabilities.

## Why it matters

If you're using an LLM as a component in a system (like calling Qwen3 inside REACH to interpret patient narratives), you need to understand what the model is actually doing, what can go wrong, and which knobs you can turn. Without this, you're debugging a black box.

## How it works (conceptually)

**Why transformers replaced RNNs**

Before transformers, sequence modeling used recurrent neural networks (RNNs and LSTMs). RNNs process sequences token by token, left to right. Each step updates a hidden state that carries information forward. The problem: information from early in the sequence gets diluted or lost by the time it reaches later tokens. Long-range dependencies are hard to learn.

Transformers don't process sequentially. They process the entire sequence at once and use self-attention to let every token directly attend to every other token. No hidden state, no information bottleneck over long distances.

**Self-attention**

Self-attention is the core operation. For each token in the sequence, it asks: which other tokens in this sequence are most relevant to understanding this token? It then produces a weighted combination of all tokens, where the weights reflect relevance.

Think of it as: for each word, the model looks at every other word in the context, decides how relevant each one is, and builds a new representation by blending information from the most relevant ones.

A transformer stacks many self-attention layers. Early layers capture syntactic relationships (subject, verb, object). Later layers capture semantic relationships (this question is about healthcare access; the relevant context is the patient's transport situation).

**Context window**

The context window is the maximum number of tokens the model can attend to at once. Everything outside the context window is invisible to the model. Qwen3's context window is large (32k-128k tokens depending on the variant), which matters for REACH because patient records, intake notes, and conversation history can be long.

When your input exceeds the context window, the model doesn't error gracefully. It either truncates or wraps around. You need to handle this explicitly.

**Fine-tuning**

A pretrained LLM can be adapted to a specific task in several ways:

- Prompt engineering: craft the input carefully so the model applies its general knowledge to your specific task. No gradient updates. Fast, cheap, fragile.
- Few-shot prompting: include examples of the task in the prompt (input-output pairs). The model infers the pattern from examples. Still no gradient updates.
- Fine-tuning: continue training the model on task-specific examples with gradient updates. The weights change. More robust but requires labeled data and compute.
- PEFT/LoRA: fine-tune a small set of additional parameters while keeping the base model weights frozen. Reduces compute cost dramatically. Good option when you have limited task-specific data but want something more stable than prompting.

## Real example

In REACH, Qwen3 (running locally via Ollama) interprets unstructured patient intake notes to extract structured reachability signals: expressed transport barriers, appointment hesitancy, caregiver constraints. The structured output feeds into the XGBoost reachability scorer.

The context window matters here because some intake notes include prior visit history. Chunking long records before passing to Qwen3 was necessary to stay within context limits without truncating the most recent (most relevant) content.

Few-shot prompting with 5-6 examples in the prompt was enough to get consistent JSON output from Qwen3-8B without fine-tuning. When the output format became inconsistent (usually on ambiguous inputs), adding one more targeted example to the prompt fixed it faster than debugging the model.

## Key intuitions

- LLMs don't retrieve facts reliably. They generate plausible-sounding text. Use them for structure extraction and reasoning, not as a source of ground truth.
- The context window is a hard constraint, not a soft limit. Design your data pipeline to respect it explicitly.
- Prompt engineering is faster to iterate than fine-tuning. Start there and only fine-tune if you've hit a ceiling that better prompts can't clear.
- Local models (Qwen3 via Ollama) trade some capability for privacy and latency control. For structured extraction on patient data, that tradeoff is often correct.
- Self-attention is quadratic in sequence length. Long contexts are slower and more expensive. Compress inputs before sending them.

## Common mistakes

- Don't treat LLM outputs as structured data without validation. Always parse and validate the JSON or schema the model returns, and handle malformed output.
- Don't ignore temperature. Temperature=0 gives deterministic, conservative outputs. Temperature=1 gives more varied but less reliable outputs. For extraction tasks, use 0 or near-0.
- Don't assume the model knows your domain. LLMs know general language patterns. Domain-specific terms (clinical codes, local place names, field-specific jargon) may be handled poorly without examples in the prompt.
- Don't skip context window accounting. A model that silently truncates your input produces wrong outputs with no error signal.

## Links

- [Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) - best visual walkthrough of self-attention
- [Qwen3 model card and technical report](https://huggingface.co/Qwen/Qwen3-8B) - architecture details and context window specs
- [Ollama documentation](https://ollama.com/library/qwen3) - local deployment reference
- [LoRA paper (Hu et al., 2021)](https://arxiv.org/abs/2106.09685) - parameter-efficient fine-tuning if prompting isn't enough
