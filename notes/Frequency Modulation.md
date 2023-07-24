---
aliases: [FM]
date created: Monday, June 26th 2023, 3:32:29 pm
tags: [signalprocessing]
title: Frequency Modulation
---
# Frequency Modulation
Modulation via sending a sine wave into a VCO

Frequency Modulation (FM) is a method of transmitting information, such as sound or data, over a carrier wave by varying its frequency. This technique is commonly used in radio broadcasting, where the frequency of the carrier wave is altered in relation to the input signal. The changes in frequency correspond to the changes in the input signal's amplitude, allowing the original information to be accurately reproduced at the receiving end. FM is known for its high fidelity and resistance to noise interference compared to other modulation methods like Amplitude Modulation (AM).

The concept of Frequency Modulation (FM) can be represented as follows:

$$
\begin{gather*} 
f(t) = A_c \cos(2\pi f_c t + \beta \sin(2\pi f_m t))
\end{gather*}
$$

Where:
- $f(t)$ is the frequency modulated signal
- $A_c$ is the amplitude of the carrier wave
- $f_c$ is the frequency of the carrier wave
- $\beta$ is the modulation index
- $f_m$ is the frequency of the modulating signal
- $t$ is time
