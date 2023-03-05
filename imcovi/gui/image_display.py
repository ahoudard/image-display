from tkinter import Tk, PhotoImage, Canvas, CENTER, Event
import imcovi.gui.KEY_BINDING
KEYS = imcovi.gui.KEY_BINDING.KEY_BIND

class DynamicImage(object):        

        def __init__(self, display_size, folder_path, image_path_list: list[str]):
            self.__x: int = display_size[0]//2
            self.__y: int = display_size[1]//2
            self.__zoom: int = 1
            self.__current_image: int = 0
            self.__total_images = len(image_path_list)
            self.__path_list = image_path_list
            self.__key_current = None
            self.__folder_path = folder_path

        def update(self):

            # move image
            if self.__key_current == KEYS[0]:
                self.__y = self.__y + 1

            elif self.__key_current == KEYS[1]:
                self.__y = self.__y - 1

            elif self.__key_current == KEYS[2]:
                self.__x = self.__x + 1

            elif self.__key_current == KEYS[3]:
                self.__x = self.__x - 1

            # zoom image
            if self.__key_current == KEYS[4]:
                self.__zoom = self.__zoom*2
                print("zoom")
            elif self.__key_current == KEYS[5]:
                self.__zoom = max(1,self.__zoom//2)
                print("unzoom")

            # swap between images
            if self.__key_current == KEYS[6]:
                self.__current_image = (self.__current_image + 1) % self.__total_images
                print(self.__current_image)
            elif self.__key_current == KEYS[7]:
                self.__current_image = (self.__current_image - 1) % self.__total_images
                print(self.__current_image)

        def set_key_event(self, event: Event):
            if (event.char in KEYS):
                self.__key_current = event.char
                print(self.__key_current)
                self.update()
            elif (event.keysym in KEYS):
                self.__key_current = event.keysym
                print(self.__key_current)
                self.update()

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        @property
        def zoom(self):
            return self.__zoom
            
        @property
        def current_path(self):
            return self.__folder_path +'/'+ self.__path_list[self.__current_image]

        @property
        def text(self):
            return "displaying "+self.current_path+" at "+str(self.zoom*100)+"%"

            
class ImageAPI(Tk):

    # TO DO : make this adaptative to the screen resolution....
    WIN_WIDTH = 512
    WIN_HEIGHT = 512

    COLOR_BACKGROUND = "black"
    COLOR_FONT = "white"
    FONT = "Times 20 italic bold"
    FONT_DISTANCE = 25

    TEXT_TITLE = "Image Viewer"

    
    def __init__(self, folder_path, images_list, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        Tk.__init__(self, screenName, baseName, className, useTk, sync, use)
        
        self.__image = DynamicImage(display_size=[ImageAPI.WIN_WIDTH, ImageAPI.WIN_HEIGHT], folder_path = folder_path, image_path_list=images_list)
        self.__canvas = Canvas(self, width=ImageAPI.WIN_WIDTH, height=ImageAPI.WIN_HEIGHT)
        self.__canvas.pack()
        self.__canvas.configure(background=ImageAPI.COLOR_BACKGROUND)    
        self.title(ImageAPI.TEXT_TITLE)
        self.__canvas.focus_set()

        self.display_image()
        self.bind('<KeyPress>', self.update_display)
    
    def update_display(self, *arg):
        self.__image.set_key_event(*arg)
        self.display_image()

    def display_image(self):
        self.__canvas.delete("all")
        self.img = PhotoImage(file=self.__image.current_path) 
        self.img = PhotoImage.zoom(self.img, self.__image.zoom)     
        self.__canvas.create_image(
            self.__image.x, #*self.__image.zoom
            self.__image.y,
            anchor=CENTER, 
            image=self.img
            )   
        text_x = 0
        text_y = 0  # y coordinate of screen center
        self.title(ImageAPI.TEXT_TITLE+" - "+self.__image.text)   
        print(self.__image.text)

if __name__ == "__main__":
    ImageAPI().mainloop()