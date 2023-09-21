from pynput.mouse import Listener
from PIL import Image, ImageGrab
import tkinter as tk
import cv2
import pytesseract
from libretranslatepy import LibreTranslateAPI

root = tk.Tk()


ix = None
iy = None

#Get the current screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


#Get and print coordinates
def on_move(x, y):
    print('Pointer moved to {0}'.format( (x, y) ))

#Start and End mouse position

def on_click(x, y, button, pressed):
    global ix, iy

    if button == button.left:

        # Left button pressed then continue
        if pressed:
            ix = x
            iy = y
            print('left button pressed at {0}'.format((x, y)))
        else:
            print('left button released at {0}'.format((x, y)))
            root.wm_attributes('-alpha', 0)
            img = ImageGrab.grab(bbox=(ix, iy, x, y))  # Take the screenshot
            root.quit()  # Remove tkinter window
            img.save('screenshot_area.png')  # Save the screenshot

    if not pressed:
        # Stop listener
        return False


print(screen_width, screen_height)


root_geometry = str(screen_width) + 'x' + str(screen_height)
root.geometry(root_geometry)

root.overrideredirect(True)
root.wait_visibility(root)
root.wm_attributes("-alpha", 0.3)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)#Crate canvas
canvas.config(cursor="cross")#Change mouse pointer to cross

canvas.pack()

# Collect events until released
with Listener(on_move=on_move, on_click=on_click) as listener:
    root.mainloop()#Start tkinter window
    listener.join()

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\\tesseract.exe'
img = cv2.imread('screenshot_area.png')
text = pytesseract.image_to_string(img, lang="eng")
print(text)
f = open('text.txt', 'a', encoding='utf-8')
f.write(text + '\n')
f.close()


lt = LibreTranslateAPI("https://translate.argosopentech.com/")
text2 = lt.translate(f"{text}", "en", "ru")

# translator = Translator(from_lang="en", to_lang="ru")
# translation = translator.translate(text)
# print(translation)


# Create a root window for the GUI
root = tk.Tk()
root.title("Translation")
# window title




# Add a label widget to display the translated text
label = tk.Label(root, text=text2, font="Arial 12 bold", anchor="center")
label.pack(fill="both", expand=True)


# Get the required width and height of the label widget
label_width = label.winfo_reqwidth()
label_height = label.winfo_reqheight()

# Set the geometry of the root window to fit the label widget
root.geometry(f"{label_width}x{label_height}")
title_bar = tk.Frame(root, bg='blue', relief='raised', bd=2) # enter your colour here



root.bind("<Destroy>", lambda _: quit())
# Run the main loop of the GUI
root.mainloop()

