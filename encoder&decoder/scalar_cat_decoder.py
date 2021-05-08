#!/usr/bin/env python3

import numpy as np
import imageio
import sys
from PIL import Image


def classify_dequantizer(
    value, barresNegres
):  # metode per retornar el valor representatiu de cada conjunt(punts negres)
    return barresNegres[value]


# necesito el header per tenir les dimensions de la imatge
"""
shape_x = header
shape_y = header
shape_rgb = header

barres = quantize(img)
barresBlaves = barres[0]
barresNegres = barres[1]
"""

# separar 3 bytes en 8 ints

print("traduir del bin a la imatge")
with open(sys.argv[1], "rb") as f:
    vec2 = []
    cont1 = 0
    cont2 = 0
    barresNegresReconstructed = []
    read = f.read()

    # treiem header
    shape_x = int.from_bytes(read[:2], byteorder="big")
    shape_y = int.from_bytes(read[2:4], byteorder="big")
    shape_rgb = 3  # RGB

    # punts de reconstruccio
    contRead = 4
    for i in range(8):
        barresNegresReconstructed.append(
            int.from_bytes(read[contRead : contRead + 2], byteorder="big")
        )
        contRead += 2
    print(barresNegresReconstructed)
    read = read[contRead:]

    # creem nova imatge
    img2 = np.array(
        [
            [[0 for x in range(shape_rgb)] for y in range(shape_y)]
            for rgb in range(shape_x)
        ]
    )

    for i in range(shape_x):
        for j in range(shape_y):
            for rgb in range(shape_rgb):
                # print(rgb)
                # print(cont1)

                if cont1 == 0:
                    # print('estic pilland de:', cont2, cont2+3)
                    r = int.from_bytes(read[cont2 : cont2 + 3], byteorder="big")
                    # print(r)

                    for x in range(8):
                        r = bin(r)[2:]
                        if len(r[-3:]) == 3:
                            # print(r[-3:])
                            last = int(r[-3:], 2)
                            vec2.append(last)
                            r = int(r, 2)
                            r -= last
                            r = r >> 3
                        elif len(r[-3:]) == 2:
                            last = int(r[-2:], 2)
                            vec2.append(last)
                            r = int(r, 2)
                            r -= last
                            r = r >> 2
                        elif len(r[-3:]) == 1:
                            last = int(r[-1:], 2)
                            vec2.append(last)
                            r = int(r, 2)
                            r -= last
                            r = r >> 1

                        # vec2.append(int(bin(r)[-3:], 2))
                        # r -= int(bin(r)[-3:], 2)
                        # r = r >> 3

                    cont2 += 3
                # print(vec2)
                img2[i][j][rgb] = int(vec2[7 - cont1])
                # print(img[i,j,rgb])

                cont1 += 1
                # print(cont1)
                # cont2+=1

                if cont1 == 8:
                    cont1 = 0
                    vec2 = []


# reconstruim els valors de la imatge apartir dels punts de reconstruccio
for i in range(shape_x):
    for j in range(shape_y):
        for rgb in range(shape_rgb):
            img2[i][j][rgb] = classify_dequantizer(
                int(img2[i][j][rgb]), barresNegresReconstructed
            )

# guardem la imatge
img2 = img2.astype(dtype=np.uint8)
# print(img2)
imgToSave = Image.fromarray(img2, "RGB")
imgToSave.save(sys.argv[2])
print("Imatge", sys.argv[2], "creada")
