import * as Plot from "npm:@observablehq/plot";

export function raster_plot(
  values,
  width,
  title,
  legend = true,
  margin = 0,
  cmap = "Greys",
) {
  return Plot.plot({
    width: width,
    height: width,
    margin: margin,
    x: { axis: null },
    y: { axis: null },
    subtitle: title,
    color: {
      scheme: cmap,
      style: { background: "none" },
      legend: legend,
      width: width,
      range: [1, 0],
    },
    marks: [
      Plot.raster(values, {
        width: 256,
        height: 256,
      }),
    ],
  });
}
