"""Signal processing module with Fourier transforms."""

from typing import List, Tuple
import math
import cmath


def dft(x: List[float]) -> List[complex]:
    """Discrete Fourier Transform.
    
    Args:
        x: Input signal (real-valued)
        
    Returns:
        List of complex numbers representing the DFT
    """
    n = len(x)
    if n == 0:
        return []
    
    result = []
    for k in range(n):
        # Compute k-th DFT coefficient
        coeff = 0j
        for i in range(n):
            angle = -2 * math.pi * k * i / n
            coeff += x[i] * cmath.exp(complex(0, angle))
        result.append(coeff)
    
    return result


def idft(X: List[complex]) -> List[float]:
    """Inverse Discrete Fourier Transform.
    
    Args:
        X: DFT coefficients (complex-valued)
        
    Returns:
        Reconstructed signal (real-valued)
    """
    n = len(X)
    if n == 0:
        return []
    
    result = []
    for i in range(n):
        # Compute i-th time-domain sample
        value = 0j
        for k in range(n):
            angle = 2 * math.pi * k * i / n
            value += X[k] * cmath.exp(complex(0, angle))
        result.append(value.real / n)
    
    return result


def _fft_recursive(x: List[complex]) -> List[complex]:
    """Recursive Cooley-Tukey FFT algorithm."""
    n = len(x)
    if n <= 1:
        return x
    
    # Split into even and odd
    even = _fft_recursive([x[i] for i in range(0, n, 2)])
    odd = _fft_recursive([x[i] for i in range(1, n, 2)])
    
    # Combine
    result = [0j] * n
    for k in range(n // 2):
        angle = -2 * math.pi * k / n
        twiddle = cmath.exp(complex(0, angle)) * odd[k]
        result[k] = even[k] + twiddle
        result[k + n // 2] = even[k] - twiddle
    
    return result


def fft(x: List[float]) -> List[complex]:
    """Fast Fourier Transform (Cooley-Tukey algorithm).
    
    Args:
        x: Input signal (real-valued), length should be power of 2
        
    Returns:
        List of complex numbers representing the FFT
    """
    if not x:
        return []
    
    # Pad to power of 2
    n = 1
    while n < len(x):
        n *= 2
    padded = [complex(val, 0) for val in x] + [0j] * (n - len(x))
    
    return _fft_recursive(padded)


def ifft(X: List[complex]) -> List[float]:
    """Inverse Fast Fourier Transform.
    
    Args:
        X: FFT coefficients (complex-valued)
        
    Returns:
        Reconstructed signal (real-valued)
    """
    if not X:
        return []
    
    # Conjugate input
    X_conj = [x.conjugate() for x in X]
    
    # Run FFT on conjugated input
    result_complex = _fft_recursive(X_conj)
    
    # Conjugate and divide by n
    n = len(X)
    result = [x.conjugate().real / n for x in result_complex]
    
    return result


def spectrogram(
    x: List[float],
    window_size: int = 256,
    overlap: int = 128
) -> List[List[float]]:
    """Compute a simple spectrogram using STFT.
    
    Args:
        x: Input signal
        window_size: Size of each window (should be power of 2)
        overlap: Number of samples to overlap between windows
        
    Returns:
        List of power spectra (one per window)
    """
    if not x or window_size <= 0:
        return []
    
    # Create simple window (rectangular)
    window = [1.0] * window_size
    
    # Compute STFT
    step = window_size - overlap
    spectrogram_result = []
    
    for start in range(0, len(x) - window_size + 1, step):
        # Extract window
        windowed = [x[start + i] * window[i] for i in range(window_size)]
        
        # Compute FFT
        spectrum = fft(windowed)
        
        # Compute power spectrum (magnitude squared)
        power_spectrum = [abs(s)**2 for s in spectrum[:window_size//2]]
        
        spectrogram_result.append(power_spectrum)
    
    return spectrogram_result


def compute_frequency_spectrum(
    x: List[float],
    sample_rate: float = 1.0
) -> Tuple[List[float], List[float]]:
    """Compute frequency spectrum of a signal.
    
    Args:
        x: Input signal
        sample_rate: Sampling rate in Hz
        
    Returns:
        (frequencies, magnitudes) - frequencies in Hz, magnitudes as float
    """
    if not x:
        return [], []
    
    n = len(x)
    spectrum = fft(x)
    
    # Compute magnitudes
    magnitudes = [abs(s) for s in spectrum[:n//2]]
    
    # Compute frequency bins
    frequencies = [i * sample_rate / n for i in range(n//2)]
    
    return frequencies, magnitudes
