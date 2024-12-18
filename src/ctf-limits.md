---
title: Ultimate Dose Efficiency Limits
toc: false
style: css/custom.css
---

```js
import { raster_plot } from "./components/rasterPlot.js";
const reconstructions = new Float64Array(
  await FileAttachment(
    "./data/scaled_reconstructions_2x3x256x256.npy",
  ).arrayBuffer(),
);
const n = 256 ** 2;
```

<style>

  .img-container {
    text-align: center;
  }

  .img-container img,
    svg {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
  }

</style>

# Ultimate Dose Efficiency Limits?

- Recent studies[^1][^2] &rarr; investigated dose efficiency limits in STEM vs HRTEM
  - In the ideal case, found STEM to be 50% as efficient as HRTEM
  - This is really a consequence of the phase-problem

<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="img-container" style="min-height:200px;">
    ground truth potential
    ${resize((width,height)=> raster_plot(reconstructions.slice(0 * n, 1 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    Zernike phase plate
    ${resize((width,height)=> raster_plot(reconstructions.slice(1 * n, 2 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    "complex" ptychography
    ${resize((width,height)=> raster_plot(reconstructions.slice(2 * n, 3 * n ),Math.min(width,height-26), null, false))}
  </div>
</div>

<details>
<summary> What about realistic detectors? </summary>
<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="img-container" style="min-height:200px;">
    tilt-corrected BF-STEM
    ${resize((width,height)=> raster_plot(reconstructions.slice(3 * n, 4 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    regular ptychography
    ${resize((width,height)=> raster_plot(reconstructions.slice(4 * n, 5 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    STEM-H ptychography
    ${resize((width,height)=> raster_plot(reconstructions.slice(5 * n, 6 * n ),Math.min(width,height-26), null, false))}
  </div>
</div>

</details>

[^1]: Quantum and classical Fisher information in four-dimensional scanning transmission electron microscopy, [Phys. Rev. B 110, 024110](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.110.024110)

[^2]: Retrieval of phase information from low-dose electron microscopy experiments: are we at the limit yet? [ arXiv:2408.10590](https://arxiv.org/abs/2408.10590)
