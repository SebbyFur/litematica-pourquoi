import math
import os
import shutil
import sys

from configparser import ConfigParser
from PIL import Image

import nbtlib

from tkinter.filedialog import askopenfilename
from litemapy import *
from nbtlib.tag import Int, String

block = BlockState("minecraft:gold_block")
centre = BlockState("minecraft:diamond_block")

sgw = BlockState("minecraft:stained_glass", {"color": "white"})
sgb = BlockState("minecraft:stained_glass", {"color": "black"})

def cercle(name):
    length = int(input("length?: "))
    schem = Schematic(length, 1, length, name=name, author="Sebby", description="ftg", main_region_name=name)
    region = schem.regions[name]
    for x in range(length):
        for z in range(length):
            relx = x - (length-1)/2
            relz = z - (length-1)/2
            if (math.sqrt(relx**2+relz**2) < length/2):
                region.setblock(x, 0, z, block)
                if (x == length//2 and z == length//2):
                    region.setblock(x, 0, z, centre)
    return schem

def hexagoneIrr(name):
    length = int(input("length?: "))
    schem = Schematic(length, 1, length, name=name, author="Sebby", description="ftg", main_region_name=name)
    region = schem.regions[name]
    #Centre
    region.setblock(length//2, 0, length//2, centre)
    #Points de droite et gauche
    region.setblock(length//2, 0, 0, block)
    region.setblock(length//2, 0, length-1, block)
    #Droite diag bas
    leftoff = 1
    rightoff = length-2
    for i in range(length//2+1, length):
        region.setblock(i, 0, int(leftoff), block)
        region.setblock(i, 0, math.ceil(rightoff), block)
        leftoff += 0.5
        rightoff -= 0.5
    #Droite diag haut
    leftoff = 1
    rightoff = length-2
    for i in range(length//2-1, -1, -1):
        region.setblock(i, 0, int(leftoff), block)
        region.setblock(i, 0, math.ceil(rightoff), block)
        leftoff += 0.5
        rightoff -= 0.5
    #Droite haut et bas
    for x in range(length):
        region.setblock(0, 0, x, block)
        region.setblock(length-1, 0, x, block)
    return schem

def pngToLitematic(name):
    img = Image.open(askopenfilename())
    width, height = img.size
    px = img.load()
    schem = Schematic(width, 1, height, name=name, author="Sebby", description="ftg", main_region_name=name)
    region = schem.regions[name]
    for x in range(width):
        for z in range(height):
            if (px[x, z][3] >= 130):
                region.setblock(x, 0, z, sgb)
            else:
                region.setblock(x, 0, z, sgw)
    return schem

def save(schem, name, schem_folder):
    file_name = name + ".litematic"
    schem.save(file_name)
    onetwelve = nbtlib.load(file_name)
    onetwelve.root["Version"] = Int(4)
    onetwelve.save()
    shutil.copy(file_name, schem_folder)
    os.remove(file_name)

if __name__ == "__main__":
    name = sys.argv[1]
    config = ConfigParser()
    config.read("config.ini")
    schem_folder = config["Config"]["schematic_folder"]
    schem = pngToLitematic(name)
    save(schem, name, schem_folder)