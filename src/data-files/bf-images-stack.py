import marimo

__generated_with = "0.8.2"
app = marimo.App()


@app.cell(hide_code=True)
def __(
    defocus_slider,
    electrons_per_area_slider,
    fig,
    kx_slider,
    ky_slider,
    mo,
):
    mo.vstack(
        [
            mo.as_html(fig).center(),
            mo.hstack(
                [defocus_slider, electrons_per_area_slider],
            ).center(),
            mo.hstack([kx_slider, ky_slider]).center(),
        ]
    )
    return


@app.cell
def __(
    add_scalebar,
    alpha,
    bin_factor_xy,
    bright_field_disk,
    exit_wave,
    np,
    pixel_size,
    plt,
    projected_potential,
    show,
    tilt_kx,
    tilt_ky,
):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.5))

    kmax = alpha.max() * 1e3 / np.sqrt(2)

    show(
        projected_potential,
        figax=(fig, axs[0]),
        ticks=False,
        cbar=False,
    )

    add_scalebar(
        axs[0],
        color="white",
        sampling=pixel_size * bin_factor_xy / 10,
        length=30,
        units="nm",
    )

    axs[0].set_title(
        "ground truth projected potential",
        fontsize=14,
    )

    show(
        bright_field_disk,
        extent=[-kmax, kmax, kmax, -kmax],
        figax=(fig, axs[1]),
        ticks=False,
        cbar=False,
    )

    axs[1].scatter(tilt_ky, -tilt_kx, color="red")
    axs[1].set_title("STEM bright-field disk", fontsize=14)

    add_scalebar(
        axs[1],
        color="white",
        sampling=1,
        length=3,
        units="mrad",
        size_vertical=0.25,
        pad=0.5,
    )

    k = np.sqrt(tilt_kx**2 + tilt_ky**2)

    show(
        exit_wave,
        figax=(fig, axs[2]),
        ticks=False,
        cbar=False,
        cmap="gray" if k <= 4 else "gray_r",
    )

    add_scalebar(
        axs[2],
        color="black",
        sampling=pixel_size * bin_factor_xy / 10,
        length=30,
        units="nm",
    )

    axs[2].set_title(
        "virtual bright-field image",
        fontsize=14,
    )

    fig.patch.set_facecolor('#dfdfd6')
    fig.tight_layout()
    return axs, fig, k, kmax


@app.cell(hide_code=True)
def __(ctf, np, tilted_plane_wave):
    # Angles
    alpha, phi = tilted_plane_wave.get_scattering_angles()
    bright_field_disk = np.fft.fftshift(ctf.evaluate_aperture(alpha, phi))
    return alpha, bright_field_disk, phi


@app.cell(hide_code=True)
def __(
    CTF,
    electrons_per_area,
    np,
    potential,
    rolloff,
    semiangle,
    tilted_plane_wave,
):
    # CTF
    ctf = CTF(
        semiangle_cutoff=semiangle,
        rolloff=rolloff,
    )

    exit_wave = tilted_plane_wave.multislice(potential)
    exit_wave = np.random.poisson(
        (
            np.abs(exit_wave) ** 2
            * np.prod(potential.sampling)
            * electrons_per_area
        ).clip(0)
    )
    return ctf, exit_wave


@app.cell(hide_code=True)
def __(Waves, np, potential, tilt_kx, tilt_ky, wavelength):
    # Tilted Plane Wave
    tilted_plane_wave = Waves(
        array=np.ones(potential.gpts, dtype=np.complex64),
        sampling=potential.sampling,
        wavelength=wavelength,
        tilt=(tilt_kx, -tilt_ky),
    )
    return tilted_plane_wave,


@app.cell(hide_code=True)
def __(mo, np):
    # inputs
    defocus_slider = mo.ui.slider(
        value=0, start=-2, stop=2, step=0.05, show_value=False, label=" defocus [µm]  "
    )
    electrons_per_area_slider = mo.ui.slider(
        steps=list(np.logspace(1, 3, num=10)),
        value=1000.0,
        show_value=False,
        label=r"fluence  [e/Å$^2$]",
    )
    kx_slider = mo.ui.slider(
        value=0,
        start=-4,
        stop=4,
        step=0.125,
        show_value=False,
        label=r"tilt, k$_x$ [mrad]",
    )
    ky_slider = mo.ui.slider(
        value=0,
        start=-4,
        stop=4,
        step=0.125,
        show_value=False,
        label=r"tilt, k$_y$ [mrad]",
    )
    return defocus_slider, electrons_per_area_slider, kx_slider, ky_slider


@app.cell(hide_code=True)
def __(defocus_slider, electrons_per_area_slider, kx_slider, ky_slider):
    # values
    defocus = defocus_slider.value
    electrons_per_area = electrons_per_area_slider.value
    tilt_kx = kx_slider.value
    tilt_ky = ky_slider.value
    return defocus, electrons_per_area, tilt_kx, tilt_ky


@app.cell(hide_code=True)
def __():
    # constants
    semiangle = 4  # mrad
    wavelength = 0.0197  # A (300kV)
    sigma = 0.00065  # 1/V (300kV)
    rolloff = 0.125  # mrad
    return rolloff, semiangle, sigma, wavelength


@app.cell(hide_code=True)
def __(PotentialArray, binned_volume_zxy, defocus):
    # PotentialArray

    pixel_size = 2 / 3
    bin_factor_xy = 2
    bin_factor_z = 6

    potential = PotentialArray(
        binned_volume_zxy,
        slice_thickness=pixel_size * bin_factor_z,
        sampling=(pixel_size * bin_factor_xy, pixel_size * bin_factor_xy),
    )

    potential.slice_thickness += 1e4 * defocus / binned_volume_zxy.shape[0]
    return bin_factor_xy, bin_factor_z, pixel_size, potential


@app.cell(hide_code=True)
def __(np, sigma):
    # Classes


    class PotentialArray:
        def __init__(self, array, slice_thickness, sampling):
            self.array = array
            self.slice_thickness = slice_thickness
            self.sampling = sampling
            self.gpts = array.shape[1:]


    class CTF:
        def __init__(
            self,
            semiangle_cutoff,
            rolloff,
        ):
            self.semiangle_cutoff = semiangle_cutoff
            self.rolloff = rolloff

        def evaluate_aperture(self, alpha, phi):
            semiangle_cutoff = self.semiangle_cutoff / 1000
            if self.rolloff > 0:
                rolloff = self.rolloff / 1000
                array = 0.5 * (
                    1
                    + np.cos(
                        np.pi * (alpha - semiangle_cutoff + rolloff) / rolloff
                    )
                )
                array[alpha > semiangle_cutoff] = 0.0
                array = np.where(
                    alpha > semiangle_cutoff - rolloff,
                    array,
                    np.ones_like(alpha),
                )
            else:
                array = np.array(alpha < semiangle_cutoff)
            return array


    class FresnelPropagator:
        def __init__(self):
            return None

        def evaluate_propagator_array(self, gpts, sampling, wavelength, dz, tilt):
            kx = np.fft.fftfreq(gpts[0], sampling[0])
            ky = np.fft.fftfreq(gpts[1], sampling[1])
            k = np.sqrt(kx[:, None] ** 2 + ky[None, :] ** 2)
            f = np.exp(
                -1j * (kx[:, None] ** 2 * np.pi * wavelength * dz)
            ) * np.exp(-1j * (ky[None, :] ** 2 * np.pi * wavelength * dz))

            if tilt is not None:
                f *= np.exp(
                    -1j * (kx[:, None] * np.tan(tilt[0] / 1e3) * dz * 2 * np.pi)
                )
                f *= np.exp(
                    -1j * (ky[None, :] * np.tan(tilt[1] / 1e3) * dz * 2 * np.pi)
                )

            cutoff = 2 / 3
            taper = 0.01

            kcut = cutoff / np.max(sampling) / 2
            rolloff = taper / np.max(sampling)
            mask = 0.5 * (1 + np.cos(np.pi * (k - kcut + rolloff) / rolloff))
            mask[k > kcut] = 0.0
            mask = np.where(k > kcut - rolloff, mask, np.ones_like(k))
            return f * mask

        def propagate(
            self,
            array,
            propagator_array,
        ):
            array_fft = np.fft.fft2(array)
            return np.fft.ifft2(array_fft * propagator_array)


    class Waves:
        def __init__(self, array, sampling, wavelength, tilt):
            self.array = array
            self.sampling = sampling
            self.wavelength = wavelength
            self.tilt = tilt
            self.gpts = array.shape
            self.propagator = FresnelPropagator()

        def get_spatial_frequencies(self):
            sx, sy = self.sampling
            nx, ny = self.gpts
            kx = np.fft.fftfreq(nx, sx)
            ky = np.fft.fftfreq(ny, sy)
            return kx, ky

        def get_scattering_angles(self):
            kx, ky = self.get_spatial_frequencies()
            alpha = np.sqrt(kx[:, None] ** 2 + ky[None, :] ** 2) * self.wavelength
            phi = np.arctan2(ky[None, :], kx[:, None])
            return alpha, phi

        def multislice(self, potential):
            dz = potential.slice_thickness
            out_array = self.array.copy()
            prop = self.propagator
            prop_array = prop.evaluate_propagator_array(
                self.gpts, self.sampling, self.wavelength, dz, self.tilt
            )
            for slice in potential.array:
                out_array = out_array * np.exp(1j * sigma * slice)
                out_array = prop.propagate(out_array, prop_array)
            return out_array
    return CTF, FresnelPropagator, PotentialArray, Waves


@app.cell(hide_code=True)
def __(
    AnchoredSizeBar,
    cm,
    cspace_convert,
    make_axes_locatable,
    mcolors,
    np,
    plt,
):
    # Plotting


    def return_scaled_histogram(
        array,
        vmin=None,
        vmax=None,
    ):
        if np.isclose(np.max(array), np.min(array)):
            if vmin is None:
                vmin = 0
            if vmax is None:
                vmax = np.max(array)
        else:
            if vmin is None:
                vmin = 0.02
            if vmax is None:
                vmax = 0.98

            vals = np.sort(array[~np.isnan(array)])
            ind_vmin = np.round((vals.shape[0] - 1) * vmin).astype("int")
            ind_vmax = np.round((vals.shape[0] - 1) * vmax).astype("int")
            ind_vmin = np.max([0, ind_vmin])
            ind_vmax = np.min([len(vals) - 1, ind_vmax])
            vmin = vals[ind_vmin]
            vmax = vals[ind_vmax]

        array = np.where(array < vmin, vmin, array)
        array = np.where(array > vmax, vmax, array)

        return array, vmin, vmax


    def Complex2RGB(
        complex_data, vmin=None, vmax=None, power=None, chroma_boost=1
    ):
        """ """
        amp = np.abs(complex_data)
        phase = np.angle(complex_data)

        if power is not None:
            amp = amp**power

        amp, vmin, vmax = return_scaled_histogram(amp, vmin, vmax)
        amp = ((amp - vmin) / vmax).clip(1e-16, 1)

        J = amp * 61.5  # Note we restrict luminance to the monotonic chroma cutoff
        C = np.minimum(chroma_boost * 98 * J / 123, 110)
        h = np.rad2deg(phase) + 180

        JCh = np.stack((J, C, h), axis=-1)
        rgb = cspace_convert(JCh, "JCh", "sRGB1").clip(0, 1)

        return rgb


    def add_scalebar(
        ax, length, sampling, units, color="white", size_vertical=1, pad=0.5
    ):
        """ """
        bar = AnchoredSizeBar(
            ax.transData,
            length,
            f"{sampling*length:.2f} {units}",
            "lower right",
            pad=pad,
            color=color,
            frameon=False,
            label_top=True,
            size_vertical=size_vertical,
        )
        ax.add_artist(bar)
        return ax


    def add_colorbar_arg(cax, chroma_boost=1, c=49, j=61.5):
        """
        cax                 : axis to add cbar to
        chroma_boost (float): boosts chroma for higher-contrast (~1-2.25)
        c (float)           : constant chroma value
        j (float)           : constant luminance value
        """

        h = np.linspace(0, 360, 256, endpoint=False)
        J = np.full_like(h, j)
        C = np.full_like(h, np.minimum(c * chroma_boost, 110))
        JCh = np.stack((J, C, h), axis=-1)
        rgb_vals = cspace_convert(JCh, "JCh", "sRGB1").clip(0, 1)
        newcmp = mcolors.ListedColormap(rgb_vals)
        norm = mcolors.Normalize(vmin=-np.pi, vmax=np.pi)

        cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=newcmp), cax=cax)

        cb.set_label("arg", rotation=0, ha="center", va="bottom")
        cb.ax.yaxis.set_label_coords(0.5, 1.01)
        cb.set_ticks(np.array([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]))
        cb.set_ticklabels(
            [r"$-\pi$", r"$-\dfrac{\pi}{2}$", "$0$", r"$\dfrac{\pi}{2}$", r"$\pi$"]
        )


    def show_complex(
        complex_data,
        figax=None,
        vmin=None,
        vmax=None,
        power=None,
        ticks=True,
        chroma_boost=1,
        cbar=True,
        **kwargs,
    ):
        """ """
        rgb = Complex2RGB(
            complex_data, vmin, vmax, power=power, chroma_boost=chroma_boost
        )

        figsize = kwargs.pop("figsize", (6, 6))
        if figax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = figax

        ax.imshow(rgb, interpolation=None, **kwargs)

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            add_colorbar_arg(ax_cb, chroma_boost=chroma_boost)

        if ticks is False:
            ax.set_xticks([])
            ax.set_yticks([])

        return ax


    def show(
        array,
        figax=None,
        vmin=None,
        vmax=None,
        power=None,
        ticks=True,
        cbar=True,
        cmap="gray",
        **kwargs,
    ):
        """ """

        if power is not None:
            array = array**power

        array, vmin, vmax = return_scaled_histogram(array, vmin, vmax)

        figsize = kwargs.pop("figsize", (6, 6))
        if figax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = figax

        ax.imshow(
            array, vmin=vmin, vmax=vmax, cmap=cmap, interpolation=None, **kwargs
        )

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")

            norm = mcolors.Normalize(vmin=0, vmax=1)
            cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax_cb)

        if ticks is False:
            ax.set_xticks([])
            ax.set_yticks([])

        return ax
    return (
        Complex2RGB,
        add_colorbar_arg,
        add_scalebar,
        return_scaled_histogram,
        show,
        show_complex,
    )


@app.cell(hide_code=True)
async def __(__file__, np, os, sys):
    # data load

    # data load

    if "pyodide" in sys.modules:
        from pyodide.http import pyfetch

        async def download_remote_file(url, filename, overwrite=False):
            if not os.path.isfile(filename) or overwrite:
                # print(f"Downloading file to {filename}")
                response = await pyfetch(url)
                if response.status == 200:
                    with open(filename, "wb") as f:
                        f.write(await response.bytes())

        file_url = (
            "https://raw.githubusercontent.com/gvarnavi/py4DSTEM-lite/dev/data/"
        )
        file_name = "apoF-ice-embedded-potential-binned.npy"

        await download_remote_file(file_url + file_name, file_name)

        binned_volume_zxy = np.load(file_name)

    else:
        file_url = os.path.dirname(os.path.realpath(__file__)) + "/data/"
        file_name = "apoF-ice-embedded-potential-binned.npy"
        binned_volume_zxy = np.load(file_url + file_name)
        
    projected_potential = binned_volume_zxy.sum(0)
    return (
        binned_volume_zxy,
        download_remote_file,
        file_name,
        file_url,
        projected_potential,
        pyfetch,
    )


@app.cell(hide_code=True)
def __():
    # imports

    import marimo as mo
    import numpy as np
    import sys
    import os

    from matplotlib import cm, colors as mcolors, pyplot as plt
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from colorspacious import cspace_convert
    return (
        AnchoredSizeBar,
        cm,
        cspace_convert,
        make_axes_locatable,
        mcolors,
        mo,
        np,
        os,
        plt,
        sys,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
