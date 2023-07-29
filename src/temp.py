import re

def surround_second_capture_group_with_brackets(regex_pattern, input_string):
    # Compile the regex pattern
    pattern = re.compile(regex_pattern, re.IGNORECASE)

    # Find all matches in the input_string
    matches = pattern.findall(input_string)

    # Surround only the second capture group with brackets
    print(len(matches))
    for match in matches:
        new_string = pattern.sub(r'\1 [[\2]] \3', input_string, count=1)

    return new_string

if __name__ == "__main__":
    # Test the function with an example
    regex_pattern = r"(\w+) (Amplitude) (\w+)"
    input_string = """
    ---
aliases: [AM]
tags: [signalprocessing, electronics]
title: Amplitude Modulation
date created: Wednesday, July 12th 2023, 12:18:19 pm
---

# Amplitude Modulation


Amplitude Modulation (AM) is a technique used in electronic communication, most commonly for transmitting information via a radio carrier wave. It works by varying the strength or amplitude of the carrier wave in proportion to the waveform being sent. This waveform may correspond to sounds or light intensity that is to be reproduced by the receiver. AM differs from Frequency Modulation (FM) and Phase Modulation (PM), where the frequency and phase of the carrier wave are varied respectively. AM is used in many forms of communication like in broadcasting AM radio, one-way voice communication, and two-way radio communication.

Here is an example of calculating the modulation index in Amplitude Modulation.md:

$$
\begin{gather*} 
\text{Given: } V_m = 10V, V_c = 5V \\
\text{Modulation Index (m) is given by: } m = \frac{V_m}{V_c} \\
m = \frac{10}{5} \\
m = 2\\
\end{gather*}
$$

Here, $V_m$ is the peak amplitude of the message signal and $V_c$ is the peak amplitude of the carrier signal. The modulation index ($m$) in this case is 2.

    """

    new_string = surround_second_capture_group_with_brackets(regex_pattern, input_string)
    print(new_string)