import os
import numpy as np
from pycfm import decompose
import soundfile as sf
import argparse
import yaml


def export(input, input_file, output_path, samplerate):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    basepath = os.path.join(
        output_path, os.path.splitext(os.path.basename(input_file))[0]
    )

    # Write out all components
    for i in range(input.shape[0]):
        sf.write(
            basepath + "_cpnt-" + str(i) + ".wav",
            input[i],
            samplerate
        )

    out_sum = np.sum(input, axis=0)
    sf.write(basepath + '_reconstruction.wav', out_sum, samplerate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Source Separation based on Common Fate Model')

    parser.add_argument('input', type=str, help='Input Audio File')

    args = parser.parse_args()

    filename = args.input

    # loading signal
    (audio, fs) = sf.read(filename, always_2d=True)

    out = decompose.process(
        audio,
        fs,
        nb_iter=100,
        nb_components=2,
        n_fft=1024,
        n_hop=512,
        cft_patch=(64, 32),
        cft_hop=(32, 16)
    )

    export(out, filename, 'output', fs)
