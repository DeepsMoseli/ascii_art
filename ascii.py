import PIL
from PIL import Image, ImageFont, ImageDraw, ImageOps
import cv2
from tqdm import tqdm


class Ascii:
    """This implementation follows the kite.com tutorial on youtube. I then decided to add a
    spin to it"""
    def __init__(self, width):
        self.path = "output/" 
        self.ASCII_CHARS = ["@", "#", "$", "%", "?", "*", ",", "+",
                            ";", ".", "^", "~", "'", "-", ">", "=" ,
                            "`", "{", "}", "!", "/", "\\","|", "<"]
        self.new_width = width
        self.new_height = 1
        self.PIXEL_ON = 0  # PIL color to use for "on"
        self.PIXEL_OFF = 255  # PIL color to use for "off"

    def resize_image(self,image):
        width, height = image.size
        self.new_width = width
        self.new_height = height 
        #ratio =  (height/width)
        #self.new_height = int(self.new_width * ratio)
        resized_image = image.resize((self.new_width,self.new_height))
        return resized_image

    def gray_scale(self, image):
        gray_image = image.convert("L")
        return gray_image

    def pixels_to_ascii(self,image):
        pixels = image.getdata()
        chars = "".join([self.ASCII_CHARS[pixel//25] for pixel in pixels])
        return chars
    
    
    def text_image(self, text_path, font_path = None):
        """
        This function was taken from: https://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python
        
        Convert text file to a grayscale image with black characters on a white background.
    
        arguments:
        text_path - the content of this file will be converted to an image
        font_path - path to a font file (for example impact.ttf)
        """
        grayscale = 'L'
        # parse the file into lines
        with open(text_path) as text_file:  # can throw FileNotFoundError
            lines = tuple(l.rstrip() for l in text_file.readlines())
    
        # choose a font (you can see more detail in my library on github)
        large_font = 40  # get better resolution with larger size
        font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
        try:
            font = PIL.ImageFont.truetype(font_path, size=large_font)
        except IOError:
            font = PIL.ImageFont.load_default()
            print('Could not use chosen font. Using default.')
    
        # make the background image based on the combination of font and lines
        pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
        max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
        # max height is adjusted down because it's too large visually for spacing
        test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        max_height = pt2px(font.getsize(test_string)[1])
        max_width = pt2px(font.getsize(max_width_line)[0])
        height = max_height * len(lines)  # perfect or a little oversized
        width = int(round(max_width + 40))  # a little oversized
        image = PIL.Image.new(grayscale, (width, height), color=self.PIXEL_OFF)
        draw = PIL.ImageDraw.Draw(image)

        # draw each line of text
        vertical_position = 5
        horizontal_position = 5
        line_spacing = int(round(max_height * 0.9))  # reduced spacing seems better
        for line in lines:
            draw.text((horizontal_position, vertical_position),
                      line, fill=self.PIXEL_ON, font=font)
            vertical_position += line_spacing
        # crop the text
        c_box = PIL.ImageOps.invert(image).getbbox()
        image = image.crop(c_box)
        return image

    def main(self, filename, image, number): 
        #filename_i = "%s"%filename
        self.outputfile = 'outfile_%s.txt'%number
        #try:
        #    image = Image.open(self.path+filename)
        #except:
        #    print(filename," is not in images. include file extension!")
        
        new_image_data  = self.pixels_to_ascii(self.gray_scale(self.resize_image(image)))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+self.new_width)] for i in range(0,pixel_count,self.new_width))
        
        with open(self.outputfile,"w") as f:
            f.write(ascii_image)
        
        image_new = self.text_image(self.outputfile)
        image_new.save('%s%s.jpg'%(self.path,filename))
            

class video:
    def __init__(self):
        self.render = None
        self.done  = False
        self.path = "video/"
        self.frames = 0
        self.output_path = "output/"
        self.im_array = []
        self.aski = Ascii(200)
        
    def frameCapture(self, filename):
        vidObj = cv2.VideoCapture(self.path+filename)
        counter = 1
        success = 1
        #save imagesto disk
        
        while success:
            success, image = vidObj.read()
            try:
                image = Image.fromarray(image)
                # here goes the stuff
                
                self.aski.main(counter, image, 1)
                #image.save("%s%s.jpg"%(self.output_path,counter))
                #cv2.imwrite("%s%s.jpg"%(self.output_path,counter), image)
                counter += 1
            except Exception as e:
                print(e)
        self.done = True
        self.frames = counter-1
        print("Video to image complete")
    
    def videoCreator(self):
        h,w,c = cv2.imread(self.output_path+str(1)+".jpg").shape
        size = (w,h)
        out = cv2.VideoWriter(self.path+"video_edit.mp4",cv2.VideoWriter_fourcc(*'MP4V'),20, size)
        for k in tqdm(range(1,self.frames+1)):
            im = cv2.imread(self.output_path+str(k)+".jpg")
            out.write(im)
        out.release()
 
        print("Images to video complete")    
            
        
#aski = Ascii(200)
#aski.main("imageme.jpg", 1)

vid = video()
vid.frameCapture("Hand_Washing.mp4")
vid.videoCreator()









