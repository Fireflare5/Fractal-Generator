# Imports
import numpy as np
from PIL import Image
import os
from tqdm import trange
import subprocess
import time as ti

class Fractals:
    def __init__(self, n_fractals: int): # Initialization Function
        self.n_fractals = n_fractals # Number Of Fractals To Generate
        
        self.resolution = np.array([3840, 2160]) # Image Resolution
        self.depth = 250 # Level Of Detail To Render Each Fractal At (Lower Values Improve Palette Gradient)
        self.invert = True # Inverts The Color Palette
        self.Luminance_Gradient = False # Darkens The Area Outside The Fractal
        self.Luminance_Cos = False # Changes Luminance Grad Function To Cosine 

        # Correction Value For Palette Function (50% Max Color Value)
        self.a = np.array([
            0.5, 0.5, 0.5, 0.5
            ])
        # Color Scaling Value Correction Value (50% Max Color Value)
        self.b = np.array([
            0.5, 0.5, 0.5, 0.5
            ])
        # Color Shift Frequency; Changes How Fast The Colors Change (Negative Values Reverse The Palette Direction)
        self.c = np.array([
            1.0, 1.0, 1.0, 1.0
            ])
        # Color Phase
        self.d = np.array([
            0.00, 0.10, 0.20, 0.00
            ])
        # Palette Phase; Changes Where The Palette Begins
        self.s = 0.00
        
        self.h = np.linspace(0.0, np.pi * 2.0, 1200)
        
        # Runs The Core Function For Each Fractal To Be Generated
        for self.n in trange(0, self.n_fractals, ncols=100):
            self.s = self.n / self.n_fractals
            self.core()
    
    def core(self):
        
        data, tmp = os.pipe()
        os.write(tmp, bytes(f"{self.resolution[0]} {self.resolution[1]} {self.depth} {self.h[self.n]}\n", "utf-8"))
        os.close(tmp)

        out = subprocess.check_output('cd ./ && g++ -O3 -ffast-math Fractal.cpp -o Fractal && ./Fractal', stdin=data, shell=True)

        raws = np.array([_.split() for _ in [i for i in out.decode("utf-8").strip().split("\n")]], dtype=np.float32)

        img = Image.new("RGB", tuple(self.resolution))

        if self.Luminance_Gradient and self.Luminance_Cos:
            Y = 1.0 - (self.a[3] + self.b[3] * np.cos(2.0 * np.pi * (self.c[3] * raws.T / self.depth + self.d[3])))
        elif self.Luminance_Gradient:
            Y = np.maximum(np.minimum(10.0 * self.c[3] * raws.T / self.depth + self.d[3], 1.0), 0.0)
        else:
            Y = np.ones_like(raws.T)

        R = np.minimum(np.abs(255.0 * Y * (self.a[0] - self.invert + self.b[0] * np.cos(2.0 * np.pi * (self.c[0] * raws.T / self.depth + self.d[0] + self.s)))), 255.0)
        G = np.minimum(np.abs(255.0 * Y * (self.a[1] - self.invert + self.b[1] * np.cos(2.0 * np.pi * (self.c[1] * raws.T / self.depth + self.d[1] + self.s)))), 255.0)
        B = np.minimum(np.abs(255.0 * Y * (self.a[2] - self.invert + self.b[2] * np.cos(2.0 * np.pi * (self.c[2] * raws.T / self.depth + self.d[2] + self.s)))), 255.0)

        R = np.where(raws.T != 2.0 * self.depth, R, 0).astype(np.uint8)
        G = np.where(raws.T != 2.0 * self.depth, G, 0).astype(np.uint8)
        B = np.where(raws.T != 2.0 * self.depth, B, 0).astype(np.uint8)

        pixels = img.load()

        colors = np.dstack((R, G, B))

        if self.n_fractals == 1:
            for y in trange(self.resolution[1], ncols=100):
                for x in range(self.resolution[0]):
                    pixels[x, y] = tuple(colors[x, y])
        elif self.n_fractals > 1:
            for y in range(self.resolution[1]):
                for x in range(self.resolution[0]):
                    pixels[x, y] = tuple(colors[x, y])

        img.save(f'./Fractals/{self.n}.png')

if __name__ == "__main__":
    Fractals(1200)