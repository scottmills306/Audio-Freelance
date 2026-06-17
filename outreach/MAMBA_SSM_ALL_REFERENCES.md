# ALL 60 MAMBA/SSM REFERENCES — Market Intelligence Scan
Generated: 2026-06-17T02:51:55.645672+00:00

─── REFERENCE #1 ───
Category: tech_trend
Source: tavily
Title: a new SSM arch. that has linear-time scaling, ultra long context, and most importantly--outperforms Transformers everywhere we've tried. : r/singularity
URL: https://www.reddit.com/r/singularity/comments/18asto2/announcing_mamba_a_new_ssm_arch_that_has
Mentions in this signal: 8
Snippet: Selective SSMs, and by extension the Mamba architecture, are fully recurrent models with key properties that make them suitable as the backbone of general foundation models operating on sequences. Mamba out-performs prior state-of-the-art models such as SaShiMi, Hyena, and Transformers on modeling audio waveforms and DNA sequences, both in pretraining quality and downstream metrics (e.g. reducing FID on a challenging speech generation dataset by more than half). With scaling laws up to 1B parameters, we show that Mamba exceeds the performance of a large range of baselines, including very strong modern Transformer training recipes based on LLaMa (Touvron et al. Many subquadratic-time architectures such as linear attention, gated convolution and recurrent models, and structured state space m

─── REFERENCE #2 ───
Category: tech_trend
Source: tavily
Title: Audio Mamba: Selective State Spaces for Self-Supervised Audio Representations
URL: https://arxiv.org/html/2406.02178v1
Mentions in this signal: 9
Snippet: # Audio Mamba: Selective State Spaces for Self-Supervised Audio Representations. This work proposes Audio Mamba, a selective state space model for learning general-purpose audio representations from randomly masked spectrogram patches through self-supervision. Empirical results on ten diverse audio recognition downstream tasks show that the proposed models, pretrained on the AudioSet dataset, consistently outperform comparable self-supervised audio spectrogram transformer (SSAST) baselines by a considerable margin and demonstrate better performance in dataset size, sequence length and model size comparisons. In this work, we propose self-supervised Audio Mamba (SSAM), an approach at the intersection of SSMs and masked predictive modelling, for learning general-purpose audio representations

─── REFERENCE #3 ───
Category: tech_trend
Source: tavily
Title: Mamba: New Selective State Space Model vs Transformer - ALLPCB
URL: https://www.allpcb.com/allelectrohub/mamba-new-selective-state-space-model-vs-transformer
Mentions in this signal: 15
Snippet: # Mamba: New Selective State Space Model vs Transformer. The Transformer architecture, dominant in large-scale AI models since its introduction in 2017, faces scalability limits as sequence lengths grow. Recent research introduces a new architecture called Mamba, based on a "selective state space model" (selective SSM). This design generalizes the earlier S4 architecture (Structured State Spaces for Sequence Modeling) by allowing the model to selectively attend to or ignore incoming inputs. According to the authors, Mamba can match or outperform Transformer models on language modeling tasks. Their Mamba-3B model is reported to outperform Transformer models of comparable size and to be competitive with Transformer models roughly twice its size on language modeling benchmarks. S4 and other s

─── REFERENCE #4 ───
Category: tech_trend
Source: tavily
Title: Mamba: Linear-Time Sequence Modeling with Selective ... - YouTube
URL: https://www.youtube.com/watch?v=9dSkvxS2EB0
Mentions in this signal: 17
Snippet: Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Paper Explained)
Yannic Kilcher
323000 subscribers
3628 likes
173514 views
24 Dec 2023
#mamba #s4 #ssm 

OUTLINE:
0:00 - Introduction
0:45 - Transformers vs RNNs vs S4
6:10 - What are state space models?
12:30 - Selective State Space Models
17:55 - The Mamba architecture
22:20 - The SSM layer and forward propagation
31:15 - Utilizing GPU memory hierarchy
34:05 - Efficient computation via prefix sums / parallel scans
36:01 - Experimental results and comments
38:00 - A brief look at the code


Paper: https://arxiv.org/abs/2312.00752

Abstract:
Foundation models, now powering most of the exciting applications in deep learning, are almost universally based on the Transformer architecture and its core attention module. Many subqu

─── REFERENCE #5 ───
Category: tech_trend
Source: tavily
Title: Mamba: Linear-Time Sequence Modeling with Selective State Spaces
URL: https://openreview.net/forum?id=AL1fq05o7H
Mentions in this signal: 11
Snippet: # Mamba: Linear-Time Sequence Modeling with Selective State Spaces | OpenReview. ## Mamba: Linear-Time Sequence Modeling with Selective State Spaces. **Code Of Ethics:**I acknowledge that I and all co-authors of this work have read and commit to adhering to the ICLR Code of Ethics. **TL;DR:**We introduce a selection mechanism into state space models, leading to state-of-the-art results on general sequence modeling including language. Many subquadratic-time architectures such as linear attention, gated convolution and recurrent models, and structured state space models (SSMs) have been developed to address Transformers' computational inefficiency on long sequences, but they have not performed as well as attention on important modalities such as language. As a general sequence model backbone

---
Total references: 5
Total mentions across all signals: 60