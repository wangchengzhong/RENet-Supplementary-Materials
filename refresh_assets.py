from __future__ import annotations

from pathlib import Path
import shutil
import sys


CATEGORIES = [
    # "noisy",
    # "reverb",
    # "bandlimit",
    "noisy_reverb",
    "noisy_reverb_bandlimit",
    "noisy_bandlimit",
]

COPY_RULES = [
    # ("only_noise_*.wav", "noisy"),
    # ("only_reverb_*.wav", "reverb"),
    # ("only_bandlimit_*.wav", "bandlimit"),
    ("noise_reverb_*.wav", "noisy_reverb"),
    ("noise_reverb_limit_*.wav", "noisy_reverb_bandlimit"),
    ("noise_limit_*.wav", "noisy_bandlimit"),
]


def clear_folder(folder: Path, pattern: str) -> None:
    for path in folder.glob(pattern):
        if path.is_file():
            path.unlink()


def copy_audio_files(raw_dir: Path, audio_dir: Path) -> None:
    for pattern, category in COPY_RULES:
        dest = audio_dir / category
        dest.mkdir(parents=True, exist_ok=True)
        for src in raw_dir.glob(pattern):
            # Avoid copying noise_reverb_limit into noisy_reverb
            if category == "noisy_reverb" and src.name.startswith("noise_reverb_limit_"):
                continue
            shutil.copy2(src, dest / src.name)


def main() -> int:
    root = Path(__file__).resolve().parent
    raw_dir = root / "raw_audios"
    audio_dir = root / "assets" / "audio"
    spec_dir = root / "assets" / "img" / "spectrograms"

    if not raw_dir.exists():
        print(f"Raw audio folder not found: {raw_dir}")
        return 1

    # Clear existing audio and spectrogram files for known categories
    for category in CATEGORIES:
        (audio_dir / category).mkdir(parents=True, exist_ok=True)
        (spec_dir / category).mkdir(parents=True, exist_ok=True)
        clear_folder(audio_dir / category, "*.wav")
        clear_folder(spec_dir / category, "*.png")

    copy_audio_files(raw_dir, audio_dir)

    # Generate spectrograms
    try:
        import generate_spectrograms

        generate_spectrograms.main()
    except Exception as exc:  # pragma: no cover - simple runner
        print(f"Failed to generate spectrograms: {exc}")
        return 1

    print("✓ Audio copied and spectrograms regenerated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
