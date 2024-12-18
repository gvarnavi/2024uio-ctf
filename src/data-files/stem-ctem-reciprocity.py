import marimo

__generated_with = "0.8.2"
app = marimo.App()


@app.cell(hide_code=True)
def __(add_traces, ctem, fig, invert_source, mo, stem, tilted_beams):
    mo.vstack(
        [
            mo.as_html(fig).center(),
            mo.hstack([ctem, stem], justify="center"),
            mo.hstack([add_traces, tilted_beams, invert_source], justify="center"),
        ]
    )
    return


@app.cell
def __(mo):
    # controls
    ctem = mo.ui.checkbox(value=True, label="CTEM ray diagram")
    stem = mo.ui.checkbox(value=True, label="STEM ray diagram")
    invert_source = mo.ui.switch(value=False, label="invert STEM source")
    add_traces = mo.ui.switch(value=True, label="show ray traces")
    tilted_beams = mo.ui.switch(value=False, label="show tilted beams")
    return add_traces, ctem, invert_source, stem, tilted_beams


@app.cell(hide_code=True)
def __(temgymlite):
    # tem
    components = [
        temgymlite.Lens(name="Condenser Lens", z=1.25, f=-0.25),
        temgymlite.Sample(name="Sample", z=0.75),
        temgymlite.Lens(name="Objective Lens", z=0.5, f=-0.205),
        temgymlite.Aperture(
            name="Objective Aperture", z=0.2875, aperture_radius_inner=0.0875
        ),
    ]

    components_scattered_left = [
        temgymlite.Lens(name="Condenser Lens", z=1.25, f=-0.25),
        temgymlite.DoubleDeflector(
            name="Deflector",
            z_up=1.05,
            z_low=0.95,
            updefx=0.3,
            lowdefx=-0.6,
        ),
        temgymlite.Sample(name="Sample", z=0.75),
        temgymlite.Lens(name="Objective Lens", z=0.5, f=-0.205),
        temgymlite.Aperture(
            name="Objective Aperture", z=0.2875, aperture_radius_inner=0.0875
        ),
    ]

    components_scattered_right = [
        temgymlite.Lens(z=1.25, f=-0.25),
        temgymlite.DoubleDeflector(
            z_up=1.05,
            z_low=0.95,
            updefx=-0.3,
            lowdefx=0.6,
        ),
        temgymlite.Lens(z=0.5, f=-0.205),
    ]

    unscattered_model = temgymlite.Model(
        components,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=3,
        gun_beam_semi_angle=0.35,
    )

    scattered_model_left = temgymlite.Model(
        components_scattered_left,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=3,
        gun_beam_semi_angle=0.35,
    )

    scattered_model_right = temgymlite.Model(
        components_scattered_right,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=3,
        gun_beam_semi_angle=0.35,
    )
    return (
        components,
        components_scattered_left,
        components_scattered_right,
        scattered_model_left,
        scattered_model_right,
        unscattered_model,
    )


@app.cell(hide_code=True)
def __(temgymlite):
    # stem
    components_stem = [
        temgymlite.Aperture(
            name="Objective Aperture", z=1.5 - 0.2875, aperture_radius_inner=0.0875
        ),
        temgymlite.Lens(name="Objective Lens", z=1, f=-0.205),
        temgymlite.Sample(name="Sample", z=0.75),
    ]

    bf_stem_center = temgymlite.Model(
        components_stem,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=3,
        gun_beam_semi_angle=0.35,
    )

    bf_stem_left = temgymlite.Model(
        components_stem,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=2,
        gun_beam_semi_angle=0.2,
    )

    bf_stem_right = temgymlite.Model(
        components_stem,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=1,
        gun_beam_semi_angle=0.2,
    )

    bf_stem = temgymlite.Model(
        components_stem,
        beam_z=1.5,
        beam_type="x_axial",
        num_rays=9,
        gun_beam_semi_angle=0.35,
    )
    return (
        bf_stem,
        bf_stem_center,
        bf_stem_left,
        bf_stem_right,
        components_stem,
    )


@app.cell
def __(
    add_traces,
    bf_stem,
    bf_stem_center,
    bf_stem_left,
    bf_stem_right,
    ctem,
    invert_source,
    plt,
    scattered_model_left,
    scattered_model_right,
    stem,
    temgymlite,
    tilted_beams,
    unscattered_model,
):
    # figure

    # COLOR = 'white'
    # mpl.rcParams['text.color'] = COLOR
    # mpl.rcParams['axes.labelcolor'] = COLOR
    # mpl.rcParams['xtick.color'] = COLOR
    # mpl.rcParams['ytick.color'] = COLOR

    fig, (ax, ax_stem) = plt.subplots(1, 2, figsize=(9.5, 5))

    if ctem.value:

        if tilted_beams.value:

            fig, ax = temgymlite.show_matplotlib(
                scattered_model_left,
                figax=(fig, ax),
                label_fontsize=12,
                plot_rays=add_traces.value,
                fill_color="purple",
                ray_color="purple",
                fill_between=True,
                highlight_edges=False,
                show_labels=True,
                fill_alpha=0.5,
            )

            fig, ax = temgymlite.show_matplotlib(
                scattered_model_right,
                figax=(fig, ax),
                label_fontsize=12,
                plot_rays=add_traces.value,
                fill_color="orange",
                ray_color="orange",
                fill_between=True,
                highlight_edges=False,
                show_labels=False,
                fill_alpha=0.5,
            )

            fig, ax = temgymlite.show_matplotlib(
                unscattered_model,
                figax=(fig, ax),
                label_fontsize=12,
                plot_rays=add_traces.value,
                fill_color="green",
                ray_color="green",
                fill_between=True,
                highlight_edges=False,
                fill_alpha=0.5,
                show_labels=False,
            )
        else:
            fig, ax = temgymlite.show_matplotlib(
                unscattered_model,
                figax=(fig, ax),
                label_fontsize=12,
                plot_rays=add_traces.value,
                fill_color="green",
                ray_color="green",
                fill_between=True,
                highlight_edges=False,
                fill_alpha=0.5,
                show_labels=True,
            )

        ax.set_title("CTEM", fontsize=16)
        ax.set_xlim([-0.3, 0.3])
    else:
        ax.axis("off")

    if stem.value:
        fig, ax_stem = temgymlite.show_matplotlib(
            bf_stem,
            figax=(fig, ax_stem),
            label_fontsize=12,
            plot_rays=False,
            fill_color="gray",
            fill_between=True,
            fill_alpha=0.5,
            highlight_edges=False,
            show_labels=True,
        )

        fig, ax_stem = temgymlite.show_matplotlib(
            bf_stem_center,
            figax=(fig, ax_stem),
            label_fontsize=12,
            plot_rays=add_traces.value,
            ray_lw=1,
            ray_color="green",
            fill_between=False,
            highlight_edges=False,
            show_labels=False,
        )

        if tilted_beams.value:
            fig, ax_stem = temgymlite.show_matplotlib(
                bf_stem_left,
                figax=(fig, ax_stem),
                label_fontsize=12,
                plot_rays=add_traces.value,
                ray_lw=1,
                ray_color="orange",
                fill_between=False,
                highlight_edges=False,
                show_labels=False,
            )

            fig, ax_stem = temgymlite.show_matplotlib(
                bf_stem_right,
                figax=(fig, ax_stem),
                label_fontsize=12,
                plot_rays=add_traces.value,
                ray_lw=1,
                ray_color="purple",
                fill_between=False,
                highlight_edges=False,
                show_labels=False,
            )

        ax_stem.set_title("BF-STEM", fontsize=16)

        if invert_source.value:
            ax_stem.invert_yaxis()

        ax_stem.set_xlim([-0.3, 0.3])
    else:
        ax_stem.axis("off")

    # fig.patch.set_color((24/255, 28/255, 26/255))
    # ax.patch.set_color((24/255, 28/255, 26/255))
    # ax_stem.patch.set_color((24/255, 28/255, 26/255))
    fig.patch.set_facecolor('#dfdfd6')
    ax.patch.set_facecolor('#dfdfd6')
    ax_stem.patch.set_facecolor('#dfdfd6')
    return ax, ax_stem, fig


@app.cell(hide_code=True)
async def __():
    # imports
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import sys

    if "pyodide" in sys.modules:
        import micropip

        repo = "https://raw.githubusercontent.com/gvarnavi/TemGymLite/main/dist/"
        wheel = "temgymlite-0.6.0.0-py3-none-any.whl"
        await micropip.install(repo + wheel)

    import temgymlite
    return micropip, mo, mpl, np, plt, repo, sys, temgymlite, wheel


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
