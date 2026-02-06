# Audio Structure Intelligence

## Overview

Audio Structure Intelligence is a deterministic system for analyzing musical form directly from raw audio.  
Instead of focusing on waveform features or machine learned embeddings, this project extracts interpretable structures including tempo perception, meter, rhythmic hierarchy, section boundaries, and overall song form.

---

## What the system analyzes

From a single audio file, the system infers:

- Perceived tempo (with subdivision awareness)
- Meter and beats per bar
- Rhythmic hierarchy (beat, subdivisions, pulse layers)
- Section boundaries based on rhythmic and density changes
- Section labels (e.g. chorus, breakdown, post-chorus)
- High-level song structure (e.g. A → B → A)
- Structural fingerprints for comparison and clustering
- Structure archetypes describing overall form

All outputs are deterministic and explainable.

---

## Example outputs

The system generates:

- Section timelines
- Density and boundary visualizations
- Structured JSON analysis reports
- Structural fingerprints suitable for comparison across songs

See the `examples/` folder for sample outputs.

---

## How it works (high level)

1. Audio is framed and converted into energy and onset representations
2. Periodicity analysis estimates tempo candidates
3. Rhythmic consistency determines perceived tempo
4. Sliding-window analysis detects structural changes
5. Sections are labeled and aggregated into higher-level form
6. A compact structural fingerprint is generated

No machine learning models are used.

---

## How to run

```bash
python3 main.py
```
