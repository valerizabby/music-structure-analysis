import matplotlib.pyplot as plt
import librosa
import numpy as np
from IPython.display import Audio, display

import ruptures as rpt


def fig_ax(figsize=(15, 5), dpi=150):
    """Return a (matplotlib) figure and ax objects with given size."""
    return plt.subplots(figsize=figsize, dpi=dpi)


def get_sum_of_cost(algo, n_bkps):
        """Return the sum of costs for the change points `bkps`"""
        bkps = algo.predict(n_bkps=n_bkps)
        return algo.cost.sum_of_costs(bkps)


def plot_decision_graph(algo, array_of_n_bkps):
    fig, ax = fig_ax((7, 4))
    ax.plot(
        array_of_n_bkps,
        [get_sum_of_cost(algo=algo, n_bkps=n_bkps) for n_bkps in array_of_n_bkps],
        "-*",
        alpha=0.5,
    )
    ax.set_xticks(array_of_n_bkps)
    ax.set_xlabel("Number of change points")
    ax.set_title("Sum of costs")
    ax.grid(axis="x")
    ax.set_xlim(0, n_bkps_max + 1)
    fig.savefig('foo.png')
    print("Pic saved to 'foo.png'")


def compute_tempogram(sampling_rate, oenv, hop_length_tempo):
    # Compute the tempogram
    tempogram = librosa.feature.tempogram(
        onset_envelope=oenv,
        sr=sampling_rate,
        hop_length=hop_length_tempo,
    )
    # Display the tempogram
    fig, ax = fig_ax()
    _ = librosa.display.specshow(
        tempogram,
        ax=ax,
        hop_length=hop_length_tempo,
        sr=sampling_rate,
        x_axis="s",
        y_axis="tempo",
    )
    fig.savefig("tempo.png")
    print("Tempogram saved")
    return tempogram


if __name__ == "__main__":
    duration = 213  # in seconds
    #print(librosa.ex("nutcracker"))
    filename = '/Users/21415968/Desktop/Nirvana-Smells-like-teen-spirit.ogg'
    signal, sampling_rate = librosa.load(filename, duration=duration)
    #signal, sampling_rate = librosa.load(librosa.ex("nutcracker"), duration=duration)

    # listen to the music
    # display(Audio(data=signal, rate=sampling_rate))

    # look at the envelope
    fig, ax = fig_ax()
    ax.plot(np.arange(signal.size) / sampling_rate, signal)
    ax.set_xlim(0, signal.size / sampling_rate)
    ax.set_xlabel("Time (s)")
    _ = ax.set(title="Sound envelope")

    # Compute the onset strength
    hop_length_tempo = 256
    oenv = librosa.onset.onset_strength(
        y=signal, sr=sampling_rate, hop_length=hop_length_tempo
    )

    tempogram = compute_tempogram(sampling_rate, oenv, hop_length_tempo)
    # Choose detection method
    algo = rpt.KernelCPD(kernel="linear").fit(tempogram.T)

    # Choose the number of changes (elbow heuristic)
    n_bkps_max = 20  # K_max
    # Start by computing the segmentation with most changes.
    # After start, all segmentations with 1, 2,..., K_max-1 changes are also available for free.
    _ = algo.predict(n_bkps_max)

    array_of_n_bkps = np.arange(1, n_bkps_max + 1)

    plot_decision_graph(algo, array_of_n_bkps)

    # Visually we choose n_bkps=5 (highlighted in red on the elbow plot)
    n_bkps = 6
    _ = ax.scatter([5], [get_sum_of_cost(algo=algo, n_bkps=5)], color="r", s=100)


    # Segmentation
    bkps = algo.predict(n_bkps=n_bkps)
    # Convert the estimated change points (frame counts) to actual timestamps
    bkps_times = librosa.frames_to_time(bkps, sr=sampling_rate, hop_length=hop_length_tempo)

    # Displaying results
    fig, ax = fig_ax()
    _ = librosa.display.specshow(tempogram,ax=ax,x_axis="s",y_axis="tempo",hop_length=hop_length_tempo,sr=sampling_rate,)
    fig.savefig("result.png")
    print("Result file saved")

    for b in bkps_times[:-1]:
        ax.axvline(b, ls="--", color="white", lw=4)


    # Compute change points corresponding indexes in original signal
    bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()

    for segment_number, (start, end) in enumerate(
        rpt.utils.pairwise([0] + bkps_time_indexes), start=1
    ):
        segment = signal[start:end]
        # ВРЕМЯ В СЕКУНДАХ
        print("Start", round(start/sampling_rate, 3), "end", round(end/sampling_rate, 3))
        #print(f"Segment n°{segment_number} (duration: {segment.size/sampling_rate:.2f} s)")
        #display(Audio(data=segment, rate=sampling_rate))

    print(np.array(bkps_time_indexes)/sampling_rate)
