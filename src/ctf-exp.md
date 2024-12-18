---
title: Experimental SNR Observations
style: css/custom.css
toc: false
---

```js
const bio_fft_img = FileAttachment("data/biological_crystals-recon.png").href;

import { return_resized_img } from "./components/ImageUtilities.js";
```

# Experimental SNR Observations

- Different phase retrieval methods &rarr; different transfer of information
  - Purple membrane sample (bacteria crystal)[^1]

<div class="card" style="background: var(--theme-foreground);">
  <div class="img-container">
    ${resize((width) =>
      return_resized_img(bio_fft_img, width,"auto;"),
    )}
  </div>
</div>

[^1]: Low-dose cryo-electron ptychography of proteins at sub-nanometer resolution, [bioRxiv:2024.02.12.579607](https://www.biorxiv.org/content/10.1101/2024.02.12.579607v2)
