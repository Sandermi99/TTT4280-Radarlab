import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.signal as signal


def raspi_import(path, channels=5):
    """
    Import data produced using adc_sampler.c.

    Returns sample period and a (`samples`, `channels`) `float64` array of
    sampled data from all `channels` channels.

    Example (requires a recording named `foo.bin`):
    ```
    >>> from raspi_import import raspi_import
    >>> sample_period, data = raspi_import('foo.bin')
    >>> print(data.shape)
    (31250, 5)
    >>> print(sample_period)
    3.2e-05

    ```
    """

    with open(path, "r") as fid:
        sample_period = np.fromfile(fid, count=1, dtype=float)[0]
        data = np.fromfile(fid, dtype="uint16").astype("float64")
        # The "dangling" `.astype('float64')` casts data to double precision
        # Stops noisy autocorrelation due to overflow
        data = data.reshape((-1, channels))

    # sample period is given in microseconds, so this changes units to seconds
    sample_period *= 1e-6
    return sample_period, data


def plot(data, sample_period):
    """
    Plot data from `raspi_import`.

    Args:
        data (numpy.ndarray): The data array from `raspi_import`.
        sample_period (float): The sample period from `raspi_import`.
    """
    x = np.arange(data.shape[0]) * sample_period * 1000
    c = ["C0", "C1", "C2", "C3", "C4"]
    labels = ["y_1[n]", "y_2[n]", "y_3[n]", "y_4[n]", "y_5[n]"]
    # make a subplot for each channel
    fig, axs = plt.subplots(data.shape[1], 1, sharex=True)
    for i in range(data.shape[1]):
        axs[i].plot(x[1:], data[1:, i], color=c[i], label=labels[i])
        axs[i].set_title(f"ADC {i + 1}")
        axs[i].grid(True)
        axs[i].set_xlim(1000, 1200)
        axs[i].legend()
        # axs[i].set_ylim(0, 3.3)
    axs[data.shape[1] // 2].set_ylabel("Spenning (V)")
    axs[-1].set_xlabel("Tid (ms)")
    plt.tight_layout()
    # plt.savefig('plots/adc2.png')
    plt.show()


def plot_fft(data, sample_period):
    """
    Plot the FFT of data from `raspi_import`.

    Args:
        data (numpy.ndarray): The data array from `raspi_import`.
        sample_period (float): The sample period from `raspi_import`.
    """
    channel = 4  # choose your ADC channel here
    NFFT = 65536 * 8

    c = np.zeros(NFFT)
    c[: data.shape[0]] = data[:, channel] - np.mean(data[:, channel])
    cHann = np.hanning(NFFT) * c

    f = np.fft.fftfreq(NFFT, d=sample_period)
    f = np.fft.fftshift(f)

    c = np.fft.fft(c) * sample_period
    cHann = np.fft.fft(cHann) * sample_period

    c = np.fft.fftshift(c)
    cHann = np.fft.fftshift(cHann)

    c = np.abs(c)
    cHann = np.abs(cHann)

    # Find peak
    peaks = signal.find_peaks(cHann[NFFT // 2 + 10 :])
    print(peaks)
    peak = peaks[0][0] + NFFT // 2 + 10
    print(f"Peaks: {f[peak]} Hz")

    n = 10

    sum_signal = cHann[peak] ** 2
    sum_noice = (
        np.sum(cHann[NFFT // 2 + 10 : peak - n] ** 2) + np.sum(cHann[peak + n :] ** 2)
    ) / (NFFT // 2 - 2 * n)
    print(f"SNR: {10 * np.log10(sum_signal / sum_noice)}")

    # Convert to dB
    # c = 20 * np.log10(np.abs(c))
    # cHann = 20 * np.log10(np.abs(cHann))

    # Plot Normal FFT
    plt.figure()
    plt.plot(f, c)
    plt.title("FFT av digitalisert signal - Ingen vindu")
    plt.xlim(-500, 500)
    # plt.ylim(-120, 0)
    plt.xlabel("Frekvens (Hz)")
    plt.ylabel("Amplitudespektrum (dB)")
    plt.grid(True)
    plt.show()

    # Plot Hanning FFT
    plt.figure()
    plt.plot(f, cHann)
    plt.title("FFT av digitalisert signal - Hann-vindu")
    plt.xlim(-500, 500)
    # plt.ylim(-120, )
    plt.xlabel("Frekvens (Hz)")
    plt.ylabel("Amplitudespektrum (dB)")
    plt.grid(True)
    plt.show()


# Import data from bin file
if __name__ == "__main__":
    sample_period, data = raspi_import(
        sys.argv[1] if len(sys.argv) > 1 else "C:\Users\sassj\Downloads\Lab4\Lab4\Sensor_Radarlab\Lab4\bil\rygging1"
    )
    # print(data.shape)
    # print(sample_period)
    # print(data)

    for i in range(5):
        data[:, i] *= 3.3 / 4095  # Konverterer til volt, formel (3)

    plot(data, sample_period)  # plotter innsamlet data.

    plot_fft(data, sample_period)  # plotter fft og finner SNR


