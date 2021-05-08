# image-scalar-quantizer

The whole compression process only consist of a single quantization stage: no transform or predictor, nor entropy encoding, just a quantizer. Obviously the compression process is lossy.
The objective is to the get the lowest Mean Squared Error (MSE) possible between the original and the reconstructed image. Since there are more than one image, the objective is to minimize the average MSE when encoding and decoding all of them.


# Quantizer
This is a scalar quantizer that generate compresseds `.bin` files with rate of (at most) 3 bps.
The encoder implements the Lloyd's algorithm to  get a representative value for each subgroup of values and will iterate until there is no changes between iteration and iteration. 


# Usage
```bash
python3 scalar_cat_encoder.py cat_image.png quantized_image.bin
python3 scalar_cat_decoder.py quantized_image.bin recovered_cat_image.png
```

# Results
After endcode and decode 193 images, the final average Mean Squared Error (MSE) is 52.761987462. 
