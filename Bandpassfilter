import pandas as pd
import matplotlib.pyplot as plt

def plot_bode(file1, file2):
    # Load CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Extract relevant data
    freq1 = df1["Frequency (Hz)"]
    mag1_ch1 = df1["Channel 1 Magnitude (dB)"]
    mag1_ch2 = df1["Channel 2 Magnitude (dB)"]
    phase1_ch2 = df1["Channel 2 Phase (deg)"]

    freq2 = df2["Frequency (Hz)"]
    mag2_ch1 = df2["Channel 1 Magnitude (dB)"]
    mag2_ch2 = df2["Channel 2 Magnitude (dB)"]
    phase2_ch2 = df2["Channel 2 Phase (deg)"]
    
    # Create Bode plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Magnitude plots
    axes[0, 0].semilogx(freq1, mag1_ch1, label="Channel 1", color="orange")
    axes[0, 0].semilogx(freq1, mag1_ch2, label="Channel 2", color="blue")
    axes[0, 0].set_ylabel("Magnitude (dB)")
    axes[0, 0].set_title("Bode Magnitude Plot - filter på I-kanalen")
    axes[0, 0].legend()
    axes[0, 0].grid(which="both")
    
    axes[0, 1].semilogx(freq2, mag2_ch1, label="Channel 1", color="orange")
    axes[0, 1].semilogx(freq2, mag2_ch2, label="Channel 2", color="blue")
    axes[0, 1].set_ylabel("Magnitude (dB)")
    axes[0, 1].set_title("Bode Magnitude Plot - filter på Q-kanalen")
    axes[0, 1].legend()
    axes[0, 1].grid(which="both")
    
    # Phase plots
    axes[1, 0].semilogx(freq1, phase1_ch2, color="blue")
    axes[1, 0].set_xlabel("Frequency (Hz)")
    axes[1, 0].set_ylabel("Phase (°)")
    axes[1, 0].set_title("Bode Phase Plot - filter på I-kanalen")
    axes[1, 0].grid(which="both")
    
    axes[1, 1].semilogx(freq2, phase2_ch2, color="blue")
    axes[1, 1].set_xlabel("Frequency (Hz)")
    axes[1, 1].set_ylabel("Phase (°)")
    axes[1, 1].set_title("Bode Phase Plot - filter på Q-kanalen")
    axes[1, 1].grid(which="both")
    
    plt.tight_layout()
    plt.show()

# Example usage
file1 = "bode_bandpassfilter_pin1.csv"
file2 = "bode_bandpassfilter.csv"
plot_bode(file1, file2)
