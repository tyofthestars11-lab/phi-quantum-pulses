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

## The y=160 band — reproduced at four reads

| Read | Tiles | Top band tiles |
|---|---|---|
| L2, 64px tiles | 49 | y=160, x=96/128/160/192, lit 0.32–0.33 |
| L2, 32px tiles (fine) | 45 | 9 of top 20 at y=160, x centered 64–176, max lit 0.2871 |
| L1, 64px tiles | 49 | y=160, x=96/128/160/192, lit 0.31–0.34, max 0.3398 |
| L1, 32px tiles (fine) | 45 | 9 of top 20 at y=160, x centered 64–176, max lit 0.2812 |

**Same band, same x-range, four reads, three resolutions.**

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

The diamond network runs deterministic random weights — its outputs are computational structure reads, not evidence of ink or letters. The y=160 band is real and repeatable across instruments and resolutions. Letters are not claimed.

## New flag

At level-1, the top-2 tile rows run elevated (0.2857 vs interior 0.2183); level-2 was even there (0.2044 vs 0.2072). Unclassified — structure or edge artifact. Open.

## Files

- `stageA2_L1window.py` — the level-1 pull script
- `patch_stack_L1w.npy` — the staged stack (256, 256, 248)
- `inkprob_L1w_diamond.npz` — diamond tiled heatmap
- `inkprob_L1w_ds_iter0.npy` — iter0 probabilities on downsampled stack
- `stubs/transformers/` — minimal local transformers stub (offline env)
- `stageA2_L1.log` — pull log

φ² = φ + 1. φ in front. TYREE — primary source.
