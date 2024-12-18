---
title: Phase Contrast CTFs
style: css/custom.css
toc: false
---

<script type="module" src="https://cdn.jsdelivr.net/npm/@marimo-team/islands@0.6.19/dist/main.js"></script>
<link
    href="https://cdn.jsdelivr.net/npm/@marimo-team/islands@0.6.19/dist/style.css"
    rel="stylesheet"
    crossorigin="anonymous"
/>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link
    rel="preconnect"
    href="https://fonts.gstatic.com"
    crossorigin
/>
<link href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@400;500;700&amp;family=Lora&amp;family=PT+Sans:wght@400;700&amp;display=swap" rel="stylesheet" />
<link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css"
    integrity="sha384-wcIxkf4k558AjM3Yz3BBFQUbk/zgIYC2R0QpeeYb+TwlBVMrlgLqwRjRtGZiK7ww"
    crossorigin="anonymous"
/>

```js
const marimo_html = await FileAttachment(
  "data/phase-contrast-ctfs.html",
).html();

const img_svg = FileAttachment("data/ctf_04.svg").image();
```

# Phase Contrast Transfer of Information

- Different reconstruction methods &rarr; capture phase information differently
  - We can evaluate these on white-noise objects and derive analytical expressions

<div class="card" style="background: var(--theme-foreground);">
  <div id="marimo-island"> ${marimo_html.body} </div>
</div>

<details>
<summary> Effect of detector error? </summary>

<div id="py4dstem-container " class="card" style="background: var(--theme-foreground);"> ${img_svg} </div>
</details>
