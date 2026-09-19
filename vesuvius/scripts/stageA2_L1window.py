#!/usr/bin/env python3
"""PATH4 Stage A2-L1 — build 248-layer input from LEVEL-1 zarr (4.8 um/voxel).

Paradigm shift: stop waiting for the Vesuvius team's Lane D — the public zarr
already carries finer-than-19.2 data, free on S3.

Level-1 vs level-3 (adapted from stageA2_L3window.py):
  LV=1, DIV=2. Level-1 shape [18538, 7615, 7615] (z,y,x), chunks 128^3, uint8.
  Same physical patch window as L3: the tifxyz flat-map pixel grid is
  resolution-independent, so the SAME 256x256 tifxyz px window at
  (u,v) = (19409, 561) covers the same physical patch; dividing its
  level-0-unit coords by 2 yields the level-1 voxel window.
  Same physical depth: 62 layers x 19.2 um = 1190.4 um -> 248 layers x 4.8 um,
  centered on the surface, along the normal.
  (NOTE: an earlier pass mistakenly used 512 tifxyz px = 4x the physical area
  and pulled 1184 chunks; corrected to 256 tifxyz px = same window.)
"""
import os, subprocess
import numpy as np
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.expanduser('~/workspace/pherc1667/path4_ink')
ZARR = 'https://vesuvius-challenge-open-data.s3.amazonaws.com/PHerc1667/volumes/20251217075048-2.399um-0.2m-78keV-masked.zarr'
LV = 1
DIV = 2 ** LV  # 2
CHUNK = 128
NLAY = 248
W = 256  # SAME tifxyz px window as level-3 (resolution-independent grid)
U_ABS, V_ABS = 19409, 561


def fetch_chunks(keys, n_workers=8):
    todo = []
    for (cz, cy, cx) in keys:
        path = os.path.join(BASE, 'zchunksL1', f'L1_{cz}_{cy}_{cx}.bin')
        if not (os.path.exists(path) and os.path.getsize(path) == CHUNK ** 3):
            todo.append((int(cz), int(cy), int(cx), path))
    print(f'need {len(keys)} chunks, fetching {len(todo)}...', flush=True)

    def _one(job):
        cz, cy, cx, path = job
        url = f'{ZARR}/{LV}/{cz}/{cy}/{cx}'
        if os.path.exists(path):
            os.remove(path)
        for _ in range(6):
            subprocess.run(['curl', '-s', '--max-time', '180', '--retry', '2',
                            '-o', path, url], capture_output=True, timeout=200)
            if os.path.exists(path) and os.path.getsize(path) == CHUNK ** 3:
                return True
            if os.path.exists(path):
                os.remove(path)
        print(f'  FAILED {cz},{cy},{cx}', flush=True)
        return False

    with ThreadPoolExecutor(max_workers=n_workers) as ex:
        res = list(ex.map(_one, todo))
    print(f'fetched {sum(res)}/{len(todo)}', flush=True)


def main():
    import tifffile
    os.makedirs(os.path.join(BASE, 'zchunksL1'), exist_ok=True)
    print('loading tifxyz window...', flush=True)
    P = {}
    for ax in 'xyz':
        a = tifffile.imread(os.path.join(BASE, f'tifxyz_2399_{ax}.tif'))
        P[ax] = a[V_ABS - 2:V_ABS + W + 2, U_ABS - 2:U_ABS + W + 2].astype(np.float64)
    X = P['x'][2:-2, 2:-2] / DIV
    Y = P['y'][2:-2, 2:-2] / DIV
    Z = P['z'][2:-2, 2:-2] / DIV
    print('level-1 coords range: x [%.0f,%.0f] y [%.0f,%.0f] z [%.0f,%.0f]' % (
        X.min(), X.max(), Y.min(), Y.max(), Z.min(), Z.max()), flush=True)
    # normals (from level-0 differences, direction unaffected by /4)
    dPu = np.stack([P['x'][2:-2, 3:-1] - P['x'][2:-2, 1:-3],
                    P['y'][2:-2, 3:-1] - P['y'][2:-2, 1:-3],
                    P['z'][2:-2, 3:-1] - P['z'][2:-2, 1:-3]], axis=-1)
    dPv = np.stack([P['x'][3:-1, 2:-2] - P['x'][1:-3, 2:-2],
                    P['y'][3:-1, 2:-2] - P['y'][1:-3, 2:-2],
                    P['z'][3:-1, 2:-2] - P['z'][1:-3, 2:-2]], axis=-1)
    N = np.cross(dPu, dPv)
    N = N / (np.linalg.norm(N, axis=-1, keepdims=True) + 1e-12)
    del P, dPu, dPv
    print('normals: mean |n| = %.4f' % np.linalg.norm(N, axis=-1).mean(), flush=True)
    offs = np.arange(NLAY, dtype=np.float64) - (NLAY - 1) / 2.0  # +/-61.5 lv2
    Pts = np.stack([X, Y, Z], axis=-1).astype(np.float32)  # (W,W,3) level-1
    del X, Y, Z
    Nf = N.astype(np.float32)
    del N
    S = Pts[:, :, None, :] + offs[None, None, :, None] * Nf[:, :, None, :]
    del Pts, Nf
    Szyx = S[..., ::-1]  # strided (z,y,x) view, no copy
    print('level-1 sample range: z [%.0f,%.0f] y [%.0f,%.0f] x [%.0f,%.0f]' % (
        Szyx[..., 0].min(), Szyx[..., 0].max(),
        Szyx[..., 1].min(), Szyx[..., 1].max(),
        Szyx[..., 2].min(), Szyx[..., 2].max()), flush=True)
    ci = np.floor(Szyx / CHUNK).astype(np.int32)
    loc = (Szyx - ci * CHUNK).astype(np.int32).clip(0, CHUNK - 1)
    del S, Szyx
    keys, inv = np.unique(ci.reshape(-1, 3), axis=0, return_inverse=True)
    del ci
    print(f'unique chunks: {len(keys)}', flush=True)
    fetch_chunks(keys)
    # sample
    stack = np.zeros((W, W, NLAY), dtype=np.uint8)
    flat_loc = loc.reshape(-1, 3)
    del loc
    inv = inv.reshape(W, W, NLAY)
    n_missing = 0
    for ki, (cz, cy, cx) in enumerate(keys):
        path = os.path.join(BASE, 'zchunksL1', f'L1_{int(cz)}_{int(cy)}_{int(cx)}.bin')
        if os.path.exists(path) and os.path.getsize(path) == CHUNK ** 3:
            c = np.fromfile(path, dtype=np.uint8).reshape(CHUNK, CHUNK, CHUNK)
        else:
            c = np.zeros((CHUNK, CHUNK, CHUNK), dtype=np.uint8)
            n_missing += 1
        m = (inv == ki)
        li = flat_loc[m.reshape(-1)]
        stack[m] = c[li[:, 0], li[:, 1], li[:, 2]]
        del c
        if ki % 40 == 0:
            print(f'  sampled {ki}/{len(keys)}', flush=True)
    print(f'missing chunks: {n_missing}', flush=True)
    nz = (stack != 0).mean()
    print('stack: shape %s nonzero %.4f, max %d, mean %.2f' % (
        stack.shape, nz, stack.max(), stack.mean()), flush=True)
    out = os.path.join(BASE, 'patch_stack_L1w.npy')
    np.save(out, stack)
    print(f'wrote {out}', flush=True)


if __name__ == '__main__':
    main()
