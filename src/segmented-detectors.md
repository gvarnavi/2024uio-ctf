---
title: Segmented Detector Ptychography
style: css/custom.css
toc: false
---

```js
const segmented_img = FileAttachment("data/segmented_ptychography_comparison_wlabels.png").href;

import { return_resized_img } from "./components/ImageUtilities.js";
```

# Segmented Detector Ptychography

- Are pixelated detectors really necessary for high-resolution phase-retrieval?
  - Can we use similar phase retrieval algorithms with [segmented detectors](https://sites.curvenote.com/build/0193b1e6-6e60-7d26-9fce-9cc91236a8f8)?

<div class="card" style="background: var(--theme-foreground); margin: 0; padding: 16px 48px;">
  <div class="img-container">
    ${resize((width) =>
      return_resized_img(segmented_img, width,"auto;"),
    )}
  </div>
</div>
