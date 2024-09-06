import imageio.v2 as imageio
import subprocess

images = []
frames = []

frames = subprocess.getoutput('find . -name "*png" | sort -k1 ')
frames = frames.split('\n')

for filename in frames:
    images.append(imageio.imread(filename))

imageio.mimsave('animation.gif', images)

