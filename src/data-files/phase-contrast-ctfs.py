import marimo

__generated_with = "0.9.19-dev3"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    # imports
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    from colorspacious import cspace_convert
    return AnchoredSizeBar, cspace_convert, mo, np, plt


@app.cell(hide_code=True)
def __(AnchoredSizeBar, cspace_convert, np, plt):
    # Complex Plotting Utilities
    def Complex2RGB(
        complex_data, vmin=None, vmax=None, power=None, chroma_boost=1
    ):
        """ """
        amp = np.abs(complex_data)
        phase = np.angle(complex_data)

        if power is not None:
            amp = amp**power

        if np.isclose(np.max(amp), np.min(amp)):
            if vmin is None:
                vmin = 0
            if vmax is None:
                vmax = np.max(amp)
        else:
            if vmin is None:
                vmin = 0.02
            if vmax is None:
                vmax = 0.98
            vals = np.sort(amp[~np.isnan(amp)])
            ind_vmin = np.round((vals.shape[0] - 1) * vmin).astype("int")
            ind_vmax = np.round((vals.shape[0] - 1) * vmax).astype("int")
            ind_vmin = np.max([0, ind_vmin])
            ind_vmax = np.min([len(vals) - 1, ind_vmax])
            vmin = vals[ind_vmin]
            vmax = vals[ind_vmax]

        amp = np.where(amp < vmin, vmin, amp)
        amp = np.where(amp > vmax, vmax, amp)
        amp = ((amp - vmin) / vmax).clip(1e-16, 1)

        J = amp * 61.5  # Note we restrict luminance to the monotonic chroma cutoff
        C = np.minimum(chroma_boost * 98 * J / 123, 110)
        h = np.rad2deg(phase) + 180

        JCh = np.stack((J, C, h), axis=-1)
        rgb = cspace_convert(JCh, "JCh", "sRGB1").clip(0, 1)

        return rgb


    def add_scalebar(ax, length, sampling, units, color="white"):
        """ """
        bar = AnchoredSizeBar(
            ax.transData,
            length,
            f"{sampling*length:.2f} {units}",
            "lower right",
            pad=0.5,
            color=color,
            frameon=False,
            label_top=True,
            size_vertical=1,
        )
        ax.add_artist(bar)
        return ax


    def show_complex(
        complex_data,
        figax=None,
        vmin=None,
        vmax=None,
        power=None,
        ticks=True,
        chroma_boost=1,
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

        ax.imshow(rgb, **kwargs)
        if ticks is False:
            ax.set_xticks([])
            ax.set_yticks([])
        return ax
    return Complex2RGB, add_scalebar, show_complex


@app.cell(hide_code=True)
def __():
    # parameters
    n = 48
    q_max = 2
    q_probe = 1
    sampling = 1 / q_max / 2
    reciprocal_sampling = 2 * q_max / n
    wavelength = 0.019687  # 300kV
    return n, q_max, q_probe, reciprocal_sampling, sampling, wavelength


@app.cell(hide_code=True)
def __(np):
    # probe functions
    def soft_aperture(q, q_probe, reciprocal_sampling):
        return np.sqrt(
            np.clip(
                (q_probe - q) / reciprocal_sampling + 0.5,
                0,
                1,
            ),
        )


    def aberrations(defocus, q, wavelength):
        return np.exp(-1j * np.pi * wavelength * q**2 * defocus)


    def sin_chi(defocus, q, wavelength):
        return np.sin(-1 * np.pi * wavelength * q**2 * defocus)


    def complex_probe(q, q_probe, defocus, reciprocal_sampling, wavelength):
        return soft_aperture(q, q_probe, reciprocal_sampling) * aberrations(
            defocus, q, wavelength
        )
    return aberrations, complex_probe, sin_chi, soft_aperture


@app.cell(hide_code=True)
def __(
    aberrations,
    defocus_slider,
    n,
    np,
    q_probe,
    reciprocal_sampling,
    sampling,
    soft_aperture,
    wavelength,
):
    # probes
    qx = qy = np.fft.fftfreq(n, sampling)
    q = np.sqrt(qx[:, None] ** 2 + qy[None, :] ** 2)

    probe_array_aperture = soft_aperture(q, q_probe, reciprocal_sampling)
    probe_array_aperture /= np.sqrt(np.sum(np.abs(probe_array_aperture) ** 2))

    probe_array_fourier = probe_array_aperture * aberrations(
        defocus_slider.value, q, wavelength
    )

    probe_array = np.fft.ifft2(probe_array_fourier) * n
    return probe_array, probe_array_aperture, probe_array_fourier, q, qx, qy


@app.cell(hide_code=True)
def __(complex_probe, np):
    # SSB functions

    # def ssb_ctf_single(
    #     qx, qy, kx, ky, probe, q_probe, defocus, reciprocal_sampling, wavelength
    # ):
    #     q_plus_k = np.sqrt((qx[:, None] + kx) ** 2 + (qy[None, :] + ky) ** 2)
    #     shifted_probe_plus = complex_probe(
    #         q_plus_k, q_probe, defocus, reciprocal_sampling, wavelength
    #     )

    #     q_minus_k = np.sqrt((qx[:, None] - kx) ** 2 + (qy[None, :] - ky) ** 2)
    #     shifted_probe_minus = complex_probe(
    #         q_minus_k, q_probe, defocus, reciprocal_sampling, wavelength
    #     )

    #     gamma = (
    #         probe.conj() * shifted_probe_minus - probe * shifted_probe_plus.conj()
    #     )

    #     gamma_abs = np.abs(gamma)
    #     return gamma_abs.sum() / np.abs(probe).sum()


    def ssb_ctf_vectorized(
        qx, qy, kx, ky, probe, q_probe, defocus, reciprocal_sampling, wavelength
    ):
        q_plus_k = np.sqrt(
            (qx[None, None, :, None] + kx[:, None, None, None]) ** 2
            + (qy[None, None, None, :] + ky[None, :, None, None]) ** 2
        )
        shifted_probe_plus = complex_probe(
            q_plus_k, q_probe, defocus, reciprocal_sampling, wavelength
        )

        q_minus_k = np.sqrt(
            (qx[None, None, :, None] - kx[:, None, None, None]) ** 2
            + (qy[None, None, None, :] - ky[None, :, None, None]) ** 2
        )
        shifted_probe_minus = complex_probe(
            q_minus_k, q_probe, defocus, reciprocal_sampling, wavelength
        )

        gamma = (
            probe.conj() * shifted_probe_minus - probe * shifted_probe_plus.conj()
        )

        gamma_abs = np.abs(gamma)
        return gamma_abs.sum((-1, -2)) / np.abs(probe).sum()
    return (ssb_ctf_vectorized,)


@app.cell(hide_code=True)
def __(
    defocus_slider,
    n,
    np,
    probe_array_fourier,
    q_probe,
    qx,
    qy,
    reciprocal_sampling,
    ssb_ctf_vectorized,
    wavelength,
):
    # SSB CTF
    # ssb_ctf = np.zeros((n, n))
    # for kx_index in range(n):
    #     for ky_index in range(n):
    #         kx = qx[kx_index]
    #         ky = qy[ky_index]

    #         ssb_ctf[kx_index, ky_index] = ssb_ctf_single(
    #             qx,
    #             qy,
    #             kx,
    #             ky,
    #             probe_array_fourier,
    #             q_probe,
    #             defocus_slider.value,
    #             reciprocal_sampling,
    #             wavelength,
    #         )

    ssb_ctf = np.zeros((n, n))
    ssb_ctf[: n // 2, : n // 2] = ssb_ctf_vectorized(
        qx,
        qy,
        qx[: n // 2],
        qy[: n // 2],
        probe_array_fourier,
        q_probe,
        defocus_slider.value,
        reciprocal_sampling,
        wavelength,
    )

    ssb_ctf[: n // 2, n // 2 :] = ssb_ctf_vectorized(
        qx,
        qy,
        qx[: n // 2],
        qy[n // 2 :],
        probe_array_fourier,
        q_probe,
        defocus_slider.value,
        reciprocal_sampling,
        wavelength,
    )

    ssb_ctf[n // 2 :, : n // 2] = ssb_ctf_vectorized(
        qx,
        qy,
        qx[n // 2 :],
        qy[: n // 2],
        probe_array_fourier,
        q_probe,
        defocus_slider.value,
        reciprocal_sampling,
        wavelength,
    )

    ssb_ctf[n // 2 :, n // 2 :] = ssb_ctf_vectorized(
        qx,
        qy,
        qx[n // 2 :],
        qy[n // 2 :],
        probe_array_fourier,
        q_probe,
        defocus_slider.value,
        reciprocal_sampling,
        wavelength,
    )
    return (ssb_ctf,)


@app.cell(hide_code=True)
def __(defocus_slider, np, probe_array_aperture, q, sin_chi, wavelength):
    # Parallax CTF
    parallax_ctf = np.real(
        np.fft.ifft2(np.abs(np.fft.fft2(probe_array_aperture)) ** 2)
    ) * sin_chi(defocus_slider.value, q, wavelength)
    return (parallax_ctf,)


@app.cell(hide_code=True)
def __(np, probe_array_fourier):
    # DPC CTF
    dpc_ctf = np.real(np.fft.ifft2(np.abs(np.fft.fft2(probe_array_fourier)) ** 2))
    return (dpc_ctf,)


@app.cell(hide_code=True)
def __(
    add_scalebar,
    dpc_ctf,
    n,
    np,
    parallax_ctf,
    plt,
    probe_array,
    probe_array_fourier,
    reciprocal_sampling,
    sampling,
    show_complex,
    ssb_ctf,
):
    # plots
    fig, axs = plt.subplots(2, 3, figsize=(9.5, 6))

    show_complex(np.fft.fftshift(probe_array_fourier), figax=(fig, axs[0, 0]))
    add_scalebar(axs[0, 0], n // 4, reciprocal_sampling, r"$\AA^{-1}$")
    axs[0, 0].set_title("Fourier probe")
    show_complex(np.fft.fftshift(probe_array), figax=(fig, axs[1, 0]))
    add_scalebar(axs[1, 0], n // 4, sampling, r"$\AA$")
    axs[1, 0].set_title("real-space probe")

    axs[0, 1].imshow(np.fft.fftshift(dpc_ctf), vmin=-1, vmax=1, cmap="PiYG")
    axs[0, 1].set_title("CoM CTF")
    axs[0, 2].imshow(np.fft.fftshift(parallax_ctf), vmin=-1, vmax=1, cmap="RdBu")
    axs[0, 2].set_title("Parallax CTF")
    axs[1, 1].imshow(np.fft.fftshift(ssb_ctf), vmin=0, vmax=1, cmap="magma")
    axs[1, 1].set_title("SSB CTF")

    axs[1, 2].plot(ssb_ctf[0, : n // 2 + 1], label="SSB", color="mediumvioletred")
    axs[1, 2].plot(dpc_ctf[0, : n // 2 + 1], label="CoM", color="olivedrab")
    axs[1, 2].plot(
        parallax_ctf[0, : n // 2 + 1], label="Parallax", color="cornflowerblue"
    )
    axs[1, 2].hlines(1, 0, n // 2, color="k", linestyle="--", label="Ptycho")
    axs[1, 2].set_ylim([-1, 3 / 2])
    axs[1, 2].set_title("radially-averaged CTFs")
    axs[1, 2].legend(facecolor='#dfdfd6')
    axs[1, 2].patch.set_facecolor('#dfdfd6')

    for _ax in axs.flat:
        _ax.set(xticks=[], yticks=[])
    fig.patch.set_facecolor('#dfdfd6')
    return axs, fig


@app.cell(hide_code=True)
def __(mo):
    defocus_slider = mo.ui.slider(
        start=-96,
        stop=96,
        step=4,
        value=0,
        label=r"defocus [$\AA$]",
        debounce=True,
        show_value=True,
    )
    return (defocus_slider,)


@app.cell(hide_code=True)
def __(defocus_slider, fig, mo):
    mo.vstack([mo.as_html(fig).center(), defocus_slider.center()])
    return


if __name__ == "__main__":
    app.run()
