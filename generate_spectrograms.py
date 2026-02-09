import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

# Configuration
n_fft = 512
hop_length = 128

# Audio categories (folders under assets/audio)
audio_categories = [
    'noisy',
    'reverb',
    'bandlimit',
    'noisy_reverb',
    'noisy_reverb_bandlimit',
    'noisy_bandlimit'
]

def generate_spectrogram(audio_path, output_path):
    """Generate and save a spectrogram for a given audio file."""
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Compute STFT
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        S_dB = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        
        # Create figure
        plt.figure(figsize=(6, 3.5))
        librosa.display.specshow(S_dB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='linear')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.tight_layout()
        
        # Save figure
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"Generated: {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {audio_path}: {str(e)}")
        return False

def main():
    base_audio_dir = Path('assets/audio')
    base_img_dir = Path('assets/img/spectrograms')
    
    # Process each category
    for category in audio_categories:
        print(f"\nProcessing category: {category}")
        audio_dir = base_audio_dir / category
        img_dir = base_img_dir / category

        if not audio_dir.exists():
            print(f"Warning: Category folder not found: {audio_dir}")
            continue

        audio_files = sorted(audio_dir.glob('*.wav'))
        if not audio_files:
            print(f"Warning: No audio files found in: {audio_dir}")
            continue

        for audio_path in audio_files:
            img_filename = audio_path.with_suffix('.png').name
            output_path = img_dir / img_filename
            generate_spectrogram(str(audio_path), str(output_path))
    
    print("\n✓ All spectrograms generated successfully!")

if __name__ == "__main__":
    main()
