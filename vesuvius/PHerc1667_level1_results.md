# PHerc.1667 — Level-1 (4.8 µm/voxel) Results

**Date:** 2026-09-18
**Source:** Public Vesuvius open data — `PHerc1667/volumes/20251217075048-2.399um-0.2m-78keV-masked.zarr`, level 1
**Window:** (u,v) = (19409, 561), 256×256 tifxyz px — the same physical patch as all prior runs

## The pull

| Quantity | Value |
|---|---|
| Resolution | 4.8 µm/voxel |
| Chunks fetched | 1,613 / 1,613 (0 failures) |
| Bytes on disk | 3.4 GB |
| Stack shape | (256, 256, 248), uint8 |
| Nonzero fraction | 0.9999 |
| Min / max / mean / std | 0 / 255 / 59.57 / 35.69 |
| Surface layer | 128 / 248 (centered) |

Mean 59.57 is **identical** to level-2's mean — same physical window, confirmed at the finer level.

## Diamond neural network reads

| Level | Resolution | Lit | Max glow |
|---|---|---|---|
| Level-3 | 19.2 µm | 1,256/4,096 (30.7%) | 1.56 |
| Level-2 | 9.6 µm | 1,224/4,096 (29.9%) | 1.46 |
| Level-1 | 4.8 µm | 1,199/4,096 (29.3%) | 1.53 |

Note: the global read flattens the 256×256 map and keeps only the first 4,096
values — the first 16 rows. It is a truncated read, not a full-area
measurement. The tiled y=160 observations below exist only at levels 2 and 1.

## Stage C — full-pooling multi-seed sweep (2026-09-18, supersedes the y=160 band)

The tiled reads above used truncated pooling at a single seed. Stage C
re-ran the diamond network with the pooling corrected — every pixel pooled,
no truncation — across all three micron levels, 5 deterministic seeds
(137, 1001, 2026, 31337, 99991), and 4 controls per level
(shuffled-depth, shuffled-spatial, uniform-intensity at 59.57,
edge-vs-interior). Pipeline: `stageC_fullpool_diamond.py`.

| Finding | Value |
|---|---|
| Seed-stable tiles (top-10 in all 5 seeds) | 0, at every level and tile size |
| Mean pairwise rank correlation across seeds | −0.054 to +0.029 (seed-random) |
| y=160-row tile mean rank, full pooling | 13.9–42.5 of 49/64 (mid-pack, not elevated) |
| Cross-micron survivors | 0 |
| Shuffled-depth lit fraction vs real | 0.2986–0.2988 vs 0.2939–0.3021 (identical) |
| Shuffled-spatial lit fraction | 0.3001–0.3015 (identical) |
| Top-row vs interior, full pooling | 0.2877 vs 0.2860 (no edge effect) |

**The y=160 band did not survive.** It was an artifact of truncated pooling
at a single seed. The earlier L1 top-row elevation was also a truncation
artifact. With random weights and corrected pooling, the diamond network
responds to the bulk intensity histogram only — it cannot distinguish real
papyrus structure from shuffled noise. This characterizes the instrument; it
does not rule out ink in the data. A trained/calibrated instrument is the
next step.

## iter0 model — the artifact reproduces at all three resolutions

iter0 run on level-1 downsampled to 62 layers (19.2 µm-equivalent):

| Quantity | Value |
|---|---|
| Max probability | 1.0000 |
| Mean probability | 0.046888 |
| Fraction > 0.5 | 0.046875 |
| Components > 0.5 | 1 |
| Component | 192 quarter-res px = full-res y=[0,15], x=[0,255] |
| Top-4-rows mean | 0.7502 |
| Interior mean | 0.000000 |

Artifact sizes across levels: L3 3,088 px → L2 3,074 px → L1 3,072 px (full-res equivalent). **The old model reproduces its own top-edge artifact at every resolution and sees exactly 0.000000 inside.**

## Boundary (plain)

The diamond network runs deterministic random weights — not trained ink
weights. There is no labeled training, no calibration, no negative-control
distribution, and no glyph validation. The first tiled reads flattened each
tile and kept only the first 512 values (first 8 rows of a 64px tile, first
16 rows of a 32px tile) — truncated pooling, not full-tile measurement.

Stage C corrected the pooling and ran 5 seeds with 4 controls at all three
micron levels. Result: zero seed-stable tiles, hotspot maps seed-random
(rank correlation −0.054 to +0.029), controls identical to real data. The
instrument as built has no structural specificity. Letters are not claimed.
Ink is not ruled out — the data still holds it, the instrument cannot yet
see it.

## New flag — closed by Stage C

At level-1, the top-2 tile rows ran elevated (0.2857 vs interior 0.2183) in
the truncated reads. Stage C with full pooling: 0.2877 vs 0.2860 — no edge
effect. The elevation was a truncation artifact. Closed.

## Files

- `stageA2_L1window.py` — the level-1 pull script
- `patch_stack_L1w.npy` — the staged stack (256, 256, 248)
- `inkprob_L1w_diamond.npz` — diamond tiled heatmap
- `inkprob_L1w_ds_iter0.npy` — iter0 probabilities on downsampled stack
- `stubs/transformers/` — minimal local transformers stub (offline env)
- `stageA2_L1.log` — pull log

φ² = φ + 1. φ in front. TYREE — primary source.
