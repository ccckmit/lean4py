"""Tests for signal processing module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.signal_processing import (
    dft, idft, fft, ifft,
    spectrogram, compute_frequency_spectrum
)
import math


class TestDFT:
    """Tests for Discrete Fourier Transform."""
    
    def test_constant_signal(self):
        """Test DFT of constant signal."""
        x = [1.0, 1.0, 1.0, 1.0]
        X = dft(x)
        
        assert len(X) == 4
        # DC component should be 4 (sum of signal)
        assert abs(X[0].real - 4.0) < 0.01
        # Other components should be ~0
        for i in range(1, 4):
            assert abs(X[i]) < 0.01
    
    def test_sine_wave(self):
        """Test DFT of simple sine wave."""
        # 1 Hz sine wave, sampled at 4 Hz for 1 second
        x = [math.sin(2 * math.pi * 0.25 * i) for i in range(4)]
        X = dft(x)
        
        assert len(X) == 4
        # Should have non-zero components
        assert any(abs(X[i]) > 0.5 for i in range(4))
    
    def test_empty_signal(self):
        """Test DFT with empty input."""
        X = dft([])
        assert X == []


class TestIDFT:
    """Tests for Inverse DFT."""
    
    def test_roundtrip(self):
        """Test IDFT(DFT(x)) = x."""
        x = [1.0, 2.0, 3.0, 4.0]
        X = dft(x)
        x_reconstructed = idft(X)
        
        for i in range(4):
            assert abs(x[i] - x_reconstructed[i]) < 0.01
    
    def test_empty_input(self):
        """Test IDFT with empty input."""
        x = idft([])
        assert x == []


class TestFFT:
    """Tests for Fast Fourier Transform."""
    
    def test_fft_basic(self):
        """Test FFT gives same result as DFT."""
        x = [1.0, 2.0, 3.0, 4.0]
        X_dft = dft(x)
        X_fft = fft(x)
        
        assert len(X_fft) == 4  # Should be 4 (power of 2)
        for i in range(4):
            assert abs(X_dft[i] - X_fft[i]) < 0.01
    
    def test_fft_power_of_2(self):
        """Test FFT pads to power of 2."""
        x = [1.0, 2.0, 3.0]  # Length 3, should pad to 4
        X = fft(x)
        
        assert len(X) >= 3
        # Check it's a power of 2
        n = len(X)
        assert (n & (n-1)) == 0
    
    def test_ifft_roundtrip(self):
        """Test IFFT(FFT(x)) = x."""
        x = [1.0, 2.0, 3.0, 4.0]
        X = fft(x)
        x_recon = ifft(X)
        
        for i in range(4):
            assert abs(x[i] - x_recon[i]) < 0.01


class TestSpectrogram:
    """Tests for spectrogram computation."""
    
    def test_simple_spectrogram(self):
        """Test spectrogram of simple signal."""
        # Create a signal with 100 samples
        x = [math.sin(2 * math.pi * 0.1 * i) for i in range(100)]
        
        spec = spectrogram(x, window_size=32, overlap=16)
        
        assert len(spec) > 0
        # Each spectrum should have window_size//2 elements
        assert len(spec[0]) == 16
    
    def test_empty_signal(self):
        """Test spectrogram with empty signal."""
        spec = spectrogram([], window_size=32)
        assert spec == []


class TestFrequencySpectrum:
    """Tests for frequency spectrum computation."""
    
    def test_spectrum_length(self):
        """Test output lengths match."""
        x = [1.0, 2.0, 3.0, 4.0]
        freqs, mags = compute_frequency_spectrum(x, sample_rate=1.0)
        
        assert len(freqs) == len(mags)
        assert len(freqs) == 2  # n//2
    
    def test_spectrum_values(self):
        """Test spectrum has correct frequency bins."""
        x = [0.0] * 100  # Zero signal
        freqs, mags = compute_frequency_spectrum(x, sample_rate=100.0)
        
        # First frequency should be 0 Hz
        assert freqs[0] == 0.0
        # Frequency spacing should be sample_rate / n
        if len(freqs) > 1:
            assert abs(freqs[1] - 100.0/100) < 0.01
