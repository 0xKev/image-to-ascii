# image to ascii generator
from PIL import Image, ImageOps


OUTPUT_DIR = "output\\"
SIZE = (100, 100)
INPUT_DIR = "images\\" 

def save_ascii_text(ascii_output: list) -> None:
    """
    Save the ASCII output to a text file.

    Args:
        ascii_output (list): The ASCII output to be saved.

    Returns:
        None
    """
    with open(f"{OUTPUT_DIR}ascii_output.txt", "w") as txt_file:
        for line in ascii_output:
            txt_file.writelines(line + "\n")

def pixels_to_ascii(pixels: list, rows: int) -> None:
    """
    Translates the pixel grayscale value to ascii characters.

    Args:
        pixels (list): The list of pixel grayscale values
        rows (int): The number of rows in pixels list
    
    Returns:
        None
    """
    ascii_shading_list = ['W', 'M', 'X', 'O', '@', '#', '=', '*', '°',
                        '|', '+', '-', '~', '/', '\\', '_', "'", ';', ':', ',', '.'] # from harsh to light, total 21 characters

    ascii_row = ''
    output = []
    counter = 0 # to stay within rows length
    value_scaling = 255 / len(ascii_shading_list) # to translate 0 - 255 to 0 - 20 for indexing

    for pixel in pixels:
        if counter == rows:
            output.append(ascii_row)
            ascii_row = ''
            counter = 0

        ascii_index = int(pixel / value_scaling) - 1

        char = ascii_shading_list[ascii_index]
        ascii_row += char
        counter += 1
    
    return output

def get_pixel_data(file_name: str) -> tuple[list[int], int]:
    """
    Returns the grayscale value of each pixel and number of pixel rows.

    Args:
        file_name (str): The file name of the image.

    Returns:
        A tuple of a list of pixels grayscale value and number of pixel runs.
    """
    try:
        with Image.open(f"{INPUT_DIR}{file_name}") as im:
            im = ImageOps.cover(im, SIZE)
            im_bw = im.convert(mode = "L") # GRAYSCALE SINGLE NUMBER NOT RGB from 0 t0 255
            im_bw.save(f"{OUTPUT_DIR}out_{file_name}") # no need to save, just saved to check if working
            
            pixels = im_bw.getdata()
            rows = im_bw.size[0]

            print(f"min: {min(pixels)}") # debug
            print(f"max: {max(pixels)}") # debug

            return pixels, rows
        
    except (FileNotFoundError, TypeError):
        print("Image not found. Make sure file exists and include the extension.")


    
if __name__ == "__main__":
    file_name = "mona-lisa.jpg" # no need for path, only file name with extension assuming image in images/
    pixels, n_rows = get_pixel_data(file_name)

    ascii_output = pixels_to_ascii(pixels, n_rows)
    save_ascii_text(ascii_output) # saves to "ascii_output.txt" in output/

    print(ascii_output)

    print("---Main function run completed---")

