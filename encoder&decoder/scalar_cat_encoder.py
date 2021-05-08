#!/usr/bin/env python3

import numpy as np
import imageio
import sys


def probabilities(image):  # calculem la probabilitat dels colors sobre la imatge
    probs = {}
    for x in image:
        for y in x:
            for rgb in y:
                if rgb not in probs:
                    probs[rgb] = 1
                else:
                    probs[rgb] += 1

    for (value, prob) in probs.items():
        probs[value] /= image.shape[0] + image.shape[1]
    return probs


def quantize(image):

    # calcular probabilitats de cada rg de la foto
    x = [i + 1 for i in range(-1, 255)]
    probSum = [0 for i in range(8)]
    barresBlaves = [0 for i in range(9)]
    barresBlaves[8] = 256
    iteration = 1
    barresNegresAnterior = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    repeat = False

    probs = probabilities(image)
    print("-------")
    print("quantizing the image...")
    # 1. Definir el set inicial dels nivellls representatius
    initialSet = np.array([0, 1, 2, 3, 4, 5, 6, 7])  # barres negres

    barresNegres = (initialSet / 8) * 256

    while repeat == False:

        # 2. Calcular els thresholds (Barres blaves --> mitjana per cada valor x-x+1)
        for i in range(len(barresNegres) - 1):
            barresBlaves[i + 1] = int((barresNegres[i] + barresNegres[i + 1]) / 2)

        # 3. Calcular el valor representatiu de cada conjunt (barres negres)
        for i in range(
            len(barresBlaves) - 1
        ):  # ajustem el valor representatiu de cada conjunt (barres negres)
            barresNegres[i] = 0
            probSum[i] = 0
            # print(barresBlaves[i], barresBlaves[i+1])
            for j in range(barresBlaves[i], barresBlaves[i + 1]):
                if j in probs.keys():
                    barresNegres[i] += j * probs[j]
                    probSum[i] += probs[j]
                else:
                    barresNegres[i] += j * 0
                    probSum[i] += 0

            # dividim entre el sumatori de les probabilitsts del conjunt
            if barresNegres[i] != 0:
                barresNegres[i] /= probSum[i]

        # repetir 2 i 3 fins que no es modifiqui

        if (barresNegres == barresNegresAnterior).all():
            repeat = True
        else:
            barresNegresAnterior = np.copy(barresNegres)
            iteration += 1

    # print("Punts finals ajustats (barres Negres):", barresNegres)
    # print("Extrems dels conjunts (barres Blaves):", barresBlaves)
    print("Lloyd quantizer done")
    print("Shan necesitat ", iteration, " iteracions. ")

    return barresBlaves, barresNegres


def classify_quantizer(
    value, barresBlaves
):  # metode per classificar un valor entre els diferents conjunts (barres blaves)
    for i in range(len(barresBlaves) - 1):
        if value >= barresBlaves[i] and value < barresBlaves[i + 1]:
            return i

    if value == barresBlaves[-1]:  # 256
        return len(barresBlaves) - 1


img = imageio.imread(sys.argv[1])  # not sure
img = img.astype("int64")
shape_x = img.shape[0]
shape_y = img.shape[1]
shape_rgb = img.shape[2]
barres = quantize(img)
barresBlaves = barres[0]
barresNegres = barres[1]


integer = 0


# classifiquem cada valor de la imatge
for i in range(img.shape[0]):  # x
    for j in range(img.shape[1]):  # y
        for rgb in range(img.shape[2]):  # (r,g,b)
            img[i, j, rgb] = classify_quantizer(img[i, j, rgb], barresBlaves)


# envio 8 valors ints cada 3 bytes -->
cont = 0
suma = 0
cont2 = 0

print("creant i omplint el fitxer .bin ...")
with open(sys.argv[2], "wb+") as f:

    # header:
    f.write(int(img.shape[0]).to_bytes(2, byteorder="big", signed=False))
    f.write(int(img.shape[1]).to_bytes(2, byteorder="big", signed=False))

    # guardem al header els punts de reconstruccio
    for i in range(len(barresNegres)):
        f.write(int(barresNegres[i]).to_bytes(2, byteorder="big", signed=False))

    for i in range(img.shape[0]):  # x
        for j in range(img.shape[1]):  # y
            for rgb in range(img.shape[2]):  # (r,g,b)
                suma = suma << 3
                suma |= img[i, j, rgb]
                cont += 1

                if cont == 8:
                    f.write(int(suma).to_bytes(3, byteorder="big", signed=False))
                    cont2 += 1
                    suma = 0
                    cont = 0

print(cont2, "escritures")
