---
toc: false
style: css/custom.css
---

```js
// IMAGES
const img_src_image = FileAttachment("./data/demo_image_small.gif").href;
const img_src_movie = FileAttachment("./data/demo_movie_smaller.gif").href;
const img_src_volume = FileAttachment("./data/demo_3d_small.gif").href;

import { return_resized_img } from "./components/ImageUtilities.js";
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

  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: var(--sans-serif);
    font-size: 18px;
    text-align: center;
  }

</style>

:::hero
# Elemental Microscopy Demo

[elementalmicroscopy.org](https://www.elementalmicroscopy.org/)  
New interactive journal, currently inviting author submissions -- contact us if you're interested!
:::

<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="img-container" style="min-height:300px;">
    Interactive Images
    ${resize((width)=> return_resized_img(img_src_image,width,"auto;"))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Interactive Movies
    ${resize((width)=> return_resized_img(img_src_movie,width,"auto;"))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Interactive Volumes
    ${resize((width)=> return_resized_img(img_src_volume,width,"auto;"))}
  </div>
</div>
