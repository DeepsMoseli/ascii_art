
from PIL import Image

class Ascii:
    def __init__(self, width):
        self.path = "images/" 
        self.ASCII_CHARS = ["@", "#", "$", "%", "?", "*", ",", "+",
                            ";", ".", "^", "~", "'", "-", ">", "=" ,
                            "`", "{", "}", "!", "/", "\\","|", "<"]
        self.new_width = width
        self.new_height = 1

    def resize_image(self,image):
        width, height = image.size
        ratio =  (height/width)
        self.new_height = int(self.new_width * ratio)
        resized_image = image.resize((self.new_width,self.new_height))
        return resized_image

    def gray_scale(self, image):
        gray_image = image.convert("L")
        return gray_image

    def pixels_to_ascii(self,image):
        pixels = image.getdata()
        chars = "".join([self.ASCII_CHARS[pixel//25] for pixel in pixels])
        return chars

    def main(self, filename, number): 
        filename = "%s"%filename
        self.outputfile = 'outfile_%s.txt'%number
        try:
            image = Image.open(self.path+filename)
        except:
            print(filename," is not in images. include file extension!")
        
        new_image_data  = self.pixels_to_ascii(self.gray_scale(self.resize_image(image)))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+self.new_width)] for i in range(0,pixel_count,self.new_width))
        
        print(ascii_image)

        with open(self.outputfile,"w") as f:
            f.write(ascii_image)
            
            
aski = Ascii(120)
aski.main("karabo.jpeg", 1)
