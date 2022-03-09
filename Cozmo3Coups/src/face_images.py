from PIL import Image

import cozmo

def load_cozmo_image(path, resampling_mode=Image.NEAREST):
    image = Image.open(path)
    resized_image = image.resize(cozmo.oled_face.dimensions(), resampling_mode)

    # convert the image to the format used by the oled screen
    return cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)




