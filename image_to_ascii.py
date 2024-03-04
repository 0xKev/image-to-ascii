# image to ascii generator
from PIL import Image, ImageOps
import sys, os


OUTPUT_DIR = "output\\"
SIZE = (100, 100)
INPUT_DIR = "images\\" 

def save_ascii_text(ascii_output: list, name: str) -> None:
    """
    Save the ASCII output to a text file. Increments filename if file exists.

    Args:
        ascii_output (list): The ASCII output to be saved.

    Returns:
        None
    """
    file_index = 1
    file_name = f"{OUTPUT_DIR}{name}_ascii_output.txt" # initialized in case txt file doesn't exist

    # if txt file exists, increment the file name by one and save new txt file
    while os.path.exists(file_name):
        file_name = f"{OUTPUT_DIR}{name}_ascii_output{file_index}.txt"
        file_index += 1

    with open(file_name, "w") as txt_file:
        for line in ascii_output:
            txt_file.writelines(line + "\n")

    print(f"ascii output is saved to {file_name}")

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
            #im_bw.save(f"{OUTPUT_DIR}out_{file_name}") # no need to save, just saved to check if working
            
            pixels = im_bw.getdata() 
            rows = im_bw.size[0]

            #print(f"min: {min(pixels)}") # debug
            #print(f"max: {max(pixels)}") # debug

            return pixels, rows
        
    except (FileNotFoundError, TypeError) as err:
        print(err)
        print("--Make sure to include the extension in image name parameter--")
        sys.exit(1)
    
if __name__ == "__main__":
    if len(sys.argv) != 2 or (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Put <image_file> in images/ and run the command below")
        print("<image_file> should be file name and extension. Do not enter full path.\n")
        print("Usage: python image_to_ascii.py <image_file>\n")
        print("Example: python image_to_ascii.py simpson.png")
        sys.exit(1)
    
    else:
        file_name = sys.argv[1]
        name = file_name.split(".")[0]

        pixels, n_rows = get_pixel_data(file_name)
        ascii_output = pixels_to_ascii(pixels, n_rows)

        print(ascii_output)
        
        save_ascii_text(ascii_output, name) # saves to "ascii_output.txt" in output/

        
