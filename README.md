# Audio Structure Intelligence

## Overview

Audio Structure Intelligence is a deterministic system for analyzing musical form directly from raw audio.  
Instead of focusing on waveform features or machine-learned embeddings, this project extracts **interpretable musical structure** including tempo perception, meter, rhythmic hierarchy, section boundaries, and overall song form.

The system is designed to be **explainable, reproducible, and structure-centric**, prioritizing how music is organized over how it sounds.

---

## What the system analyzes

From a single audio file, the system infers:

- Perceived tempo (with subdivision awareness)
- Meter and beats per bar
- Rhythmic hierarchy (beat, subdivisions, pulse layers)
- Groove timing and tempo drift
- Section boundaries based on rhythmic and density changes
- Section labels (e.g. chorus, breakdown, post-chorus)
- High-level song structure (e.g. A → B → A)
- Structural fingerprints for comparison and clustering
- Structure archetypes describing overall form
- Section-level similarity between songs
- Chorus-only similarity with explanatory breakdowns

All outputs are deterministic and explainable.

---

## Structure fingerprints

Each song is summarized into a compact **structure fingerprint** containing:

- Tempo and meter
- Section sequence and durations
- Chorus count and chorus ratio
- Average energy density per section type
- Groove profile per section
- Inferred structural archetype

These fingerprints are saved as JSON and can be used for:

- song comparison
- clustering
- structural similarity search

---

## Section-level similarity

Songs can be compared **section by section**, rather than globally.

The system computes:

- distance between matching section types
- weighted overall structural similarity
- per-section similarity scores
- human-readable explanations (e.g. duration shape vs energy density)

This enables comparisons such as:

- “How similar are the choruses of these two songs?”
- “Do these songs share a similar breakdown → chorus transition?”

---

## Example outputs

The system generates:

- Section timelines
- Density and boundary visualizations
- Structured JSON analysis reports
- Structure fingerprints (`fingerprint.json`)
- Section-aware similarity scores

See the `examples/` folder for sample outputs, including:

- `analysis.json`
- `fingerprint.json`
- `structure_timeline.png`
- `density_boundaries.png`

---

## How it works (high level)

1. Audio is framed and converted into energy and onset representations
2. Periodicity analysis estimates tempo candidates
3. Rhythmic consistency determines perceived tempo
4. Sliding-window analysis detects structural change points
5. Sections are labeled and aggregated into higher-level form
6. Groove and tempo drift are measured
7. A compact structural fingerprint is generated
8. Songs are compared using section-aware distance metrics

No machine learning models are used.

---

## How to run

```bash
python3 main.py
```

## License

MIT
