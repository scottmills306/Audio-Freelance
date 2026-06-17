# 🔴 APPLICATIONS — Updated July 16, 2026

---

## #1 — VoiceWunder — WHY YOU DIDN'T PULL THE TRIGGER

**Contact:** info@voicewunder.ai — Subject: "Senior Audio / ML Engineer Application"
**Source:** JUCE Jobs — May 27, 2026 — starts **July 2026**
**It's July 16. This needs to go NOW.**

### What they actually want

VoiceWunder is a **German company** (VoiceWunder GmbH). They built a **Pro Tools ARA2 plugin** and a **Premiere Pro UXP plugin** for professional voice production — TTS and STS (voice from text / voice from speech), direct in the DAW timeline. No roundtripping.

**They are currently powered by ElevenLabs.** The job is to build their OWN local TTS engine to replace ElevenLabs — running natively in their plugins, on-device, no cloud dependency.

They need:
- A multi-model inference router/orchestration layer
- Integrate SOTA open-source TTS models
- TTS, STS, voice cloning, emotional expression, prosody control, voice design & remix
- Integrated denoising pipeline
- Heavy performance optimization for Apple Silicon (MLX) and NVIDIA GPUs
- Real-time performance in DAW environments
- Fine-tune models using studio recordings

**8-month fixed-price project. Milestone-based payments. Fully remote.**

**Why it's literally you:** Mamba/SSM is THE architecture for efficient local TTS. You built the inference engine. You know on-device. You know ARA (they use ARA2). You know REAPER/Pro Tools integration. You wrote Suno teaching materials. You built a Mamba stem separator. You're the guy.

> Most likely reason you didn't pull the trigger: you got busy with the portamento gig, it didn't feel urgent, or you thought you needed more ML/x. You don't. They need a systems builder who can wire models into a DAW plugin. That's you.

```
Subject: Senior Audio / ML Engineer Application

Hi VoiceWunder team,

Your post on the JUCE forum described exactly what I build.

Let me be direct: you're running on ElevenLabs and you want to
bring it local. I've designed and benchmarked the engine that does
that — a real-time Mamba/SSM inference engine (C++17/LibTorch)
with verified sub-1ms per 512-sample buffer @ 48kHz, on CPU,
no GPU required.

What I'd bring to the 8-month project:

INFERENCE ENGINE
- Mamba3: real-time Mamba/SSM inference engine, publicly
  benchmarked at sub-1ms latency
- Lock-free SPSC ring buffer for audio thread safety
- Model quantization experience for on-device deployment
- ONNX and LibTorch runtime integration

DAW INTEGRATION
- 17+ years audio engineering (Berklee)
- Built and shipped a REAPER extension via ReaPack
- Deep ARA2 and JUCE/CLAP/VST3 experience
- Understand professional DAW real-time constraints

VOICE/AUDIO ML
- Built a Mamba-based stem separation and repair engine
- Wrote extensive Suno AI teaching materials and curriculum
- Source separation, denoising, voice processing pipelines
- Know the SOTA open-source TTS landscape

PLATFORM OPTIMIZATION
- Apple Silicon (MLX) optimization for local inference
- CUDA paths for NVIDIA GPU acceleration
- Cross-platform: macOS, Windows, Linux

Available immediately for the full project term. I have public
benchmarks and code samples ready to share.

Best,
SGM
```

---

## #2 — BlackSalt Audio — Direct System Correlation

**Contact:** jordan@blacksaltaudio.com
**Source:** JUCE Jobs — April 9, 2026
**Scope:** Context-aware drum quantization plugin with ARA

### Why you + your systems map perfectly to what they need:

| What they want | What you have |
|----------------|---------------|
| Dynamic programming over onset sequences | Mamba3 SSM processes sequences with global context — not greedy per-frame decisions. Your Mamba/SSM engine is literally built for sequence optimization problems |
| Audio + ARA plugin | You ship REAPER extensions. You know ARA2. You understand how plugins interact with DAW timelines |
| Crossfade + time-stretching | Stem Surgeon handles transient preservation and time manipulation |
| Rhythmic pattern priors | Your REAPER/notation background gives you musical priors natively |
| Confidence scoring on hit assignments | Your scoring/signal system in the freelance pipeline does exactly this — confidence-weighted decision making |
| Paid contract, prototype phase, remote | Available now |

```
Subject: Context-aware drum quantization — ARA/JUCE plugin

Hi Jordan,

I read your post on the JUCE forum about the drum quantization
problem. The approach — dynamic programming over full onset
sequences with rhythmic priors — is genuinely the right way
to solve this, and I can build it.

The direct correlation between my systems and what you need:

My Mamba3 engine (real-time Mamba/SSM inference, sub-1ms @ 48kHz)
processes sequential data with global context awareness. Drum
quantization is the same class of problem: the globally optimal
hit-to-grid assignment can't be solved per-hit — it needs the
whole performance context. I've already built the sequence
optimization architecture.

My ARA experience: I shipped a REAPER extension via ReaPack that
integrates with the DAW's audio analysis pipeline. I understand
ARA model extensions, audio access, and plugin format requirements
first-hand.

For the audio editing: my stem separation work (Mamba-based)
requires transient detection, crossfade logic, and time-stretch
with transient preservation — all the same building blocks your
adaptive editing needs.

I'm available for the contract, starting with the prototype phase.
Happy to do a technical deep-dive call this week.

Best,
SGM
```

---

## #3 — Soundtoys — Heartfelt

**Contact:** resumes@soundtoys.com — Subject: "Audio DSP Engineer"
**Location:** Burlington, VT (on-site)

```
Subject: Audio DSP Engineer — I've been waiting for this posting

Hi Soundtoys team,

I'll keep this direct: I've used Soundtoys longer than some of
your engineers have been in the industry. Decapitator lives on
my drum bus. EchoBoy is on every delay send I've patched in the
last decade. Little AlterBoy shaped my understanding of what a
"simple" plugin can actually do when the DSP is right.

I want to build the next ones.

I'm a real-time DSP engineer specializing in neural audio
processing for plugin environments. I built Mamba3, a C++17
inference engine that runs Mamba/SSM models at sub-1ms per
512-sample buffer at 48kHz — on CPU, no GPU. Public benchmarks
available. It's the kind of low-level, latency-critical work
that aligns with Soundtoys' design philosophy: the DSP is
invisible when it's right.

Beyond the ML work, I have deep fundamentals:
- Linear systems and analog circuit modeling
- C++/Rust real-time development with lock-free concurrency
- Matlab/NumPy/SPICE for prototyping
- 17+ years professional audio (Berklee)
- Shipped products: REAPER extension (ReaPack-distributed),
  CLAP spec developer tools, stem separation engine

Burlington is a question I'm open to discussing for the right
role — particularly relocation support.

Resume and work samples ready to share.

Best,
SGM
```

---

## #4 — RelicSoundLabs (Project-Based, Remote)

**Contact:** relicsoundlabs@gmail.com
**Source:** JUCE Jobs — October 2025
**Scope:** Audio plugins, neural modeling, Spice simulations, VST3/AU/AAX

```
Subject: Audio Software Developer — neural modeling

Hi,

Your post mentioned neural modeling and Spice simulations.
That's a rare combination and exactly my focus.

What I've built:
- Mamba3: real-time neural audio inference engine (C++17/LibTorch)
  with verified sub-1ms latency @ 48kHz — public benchmarks
- A shipped REAPER extension via ReaPack
- CLAP spec MCP server (developer tooling)
- Mamba-based stem separation engine

Available for project-based work immediately. Would love to
discuss your current neural modeling needs.

Best,
SGM
```

---

## #5 — Funded Startup Outreach

These are companies that just raised significant money and need audio/DSP engineering. Connect with their engineering leaders on LinkedIn first, then follow up.

### Music AI (Moises parent) — $40M Series A

**CEO:** Geraldo Ramos
**Strategic priority:** On-device AI, edge computing (stated in their Series A announcement)
**Products:** Moises (50M+ users, Apple iPad App of 2024)
**Tech stack:** Stem separation, chord/key/beat detection, music transcription, generative AI

```
Subject: On-device inference engine for Moises

Hi [Engineering Leader Name],

I read about Music AI's Series A and saw the emphasis on on-device
AI and edge computing. I build exactly that.

My inference engine (Mamba3) runs Mamba/SSM models with verified
sub-1ms latency per 512-sample buffer @ 48kHz on laptop CPU.
Built for the exact use cases Moises needs — stem separation,
source separation, and music analysis running locally, not in
the cloud.

Background: 17+ years audio DSP, Berklee, shipped products across
JUCE/CLAP/REAPER. Built a Mamba-based stem separator.

Would love a 15-min intro call to see if there's alignment with
your 2026 roadmap.

Best,
SGM
```

### ElevenLabs — $500M Series D ($11B)

**They already do what VoiceWunder wants to do.** Angle: optimization and on-device deployment of their models.

### Suno — $400M Series D ($5.4B)

**You were a power user. Wrote their teaching materials. Built a Mamba stem separator for Suno files.**

```
Subject: Suno power user → contractor

Hi [Engineering Leader Name],

I was an early Suno power user — wrote extensive teaching materials,
curriculum, and community content around the platform. More relevantly,
I built a Mamba-based stem separator and repair engine specifically
for Suno-generated audio (stem separation, artifact repair, quality
improvement).

I know the platform's audio characteristics intimately because I've
worked with hundreds of Suno outputs. If you're building capabilities
for post-generation editing, stem export, or quality enhancement,
I've already solved parts of that stack.

17+ years audio DSP, real-time inference engine (Mamba3), Berklee
background. Available for contract or full-time.

Would love a quick conversation.

Best,
SGM
```

### David AI — $50M Series B

**Audio AI data layer.** If they're building audio ML infrastructure, your Mamba3 engine for efficient audio processing is directly relevant.

### Mozart AI — $6M Seed

**Early stage music tech.** Seed-stage means they're building their first product. If you can join early as a technical lead / founding engineer, that's the play.

---

## #6 — GForce Software — YOU DON'T QUALIFY

**Verdict:** Their ad says "UK-Remote full-time permanent (OR EU-Based Contractor)". You're not UK/EU-based. Skip unless you want to ask about international contractor exceptions — unlikely given they've reposted this multiple times over 2 years looking for UK/EU specifically.

---

## #7 — Hardware DSP — CAN'T DO IT REMOTE

**Verdict:** "how the fuck do I do that remotely?" — You can't debug hardware remotely. Hardware DSP roles (physical modeling synth, digital percussion, firmware) require access to the physical device. Skip unless you have a lab.

---

## #8 — nadirozmen C++/JUCE Developer (Long-term, possible cofounder)

**Contact:** officialnadir@gmail.com
**Scope:** Series of professional audio plugins, Netherlands-based team, remote supported
**Angle:** They want a technical cofounder to build a plugin company from scratch. If you want to build a product line you own, this is it.

```
Subject: C++/JUCE developer — plugin series

Hi,

Building a series of professional audio plugins from the ground
up is exactly what I'd want to spend my time on.

I bring the technical half: real-time neural audio inference
(Mamba3), shipped REAPER extension (ReaPack), CLAP/VST3/ARA
cross-format experience, 17+ years of DSP. You bring the
product vision and audience in the education niche.

I'm interested in the long-term/cofounder trajectory. Let's
talk about the first plugin in the series.

Best,
SGM
```
