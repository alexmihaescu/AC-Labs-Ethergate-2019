import tkinter
import os
import cv2 as cv
import shutil 
# import matplotlib.pyplot as plt


TAGGED = False


def load_pictures(root_folder):
    images = []

    for img_name in os.listdir(root_folder):
        image = cv.imread(f'{root_folder}/{img_name}')
        if image is not None:
            if len(image.shape) > 2:
                a = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                resize = cv.resize(a,(300,250))
                images.append(resize)
    return images


def load_classes(classes_path, tagged_path):
    if os.path.isdir(tagged_path):
        shutil.rmtree(tagged_path, ignore_errors=True)
    
    os.makedirs(tagged_path)

    classes = {}

    with open(classes_path,'r') as f:
        for line in f:
            line = line.replace('\n','')
            if line!='':
                if not os.path.isdir(f'{tagged_path}/{line}'):
                    os.makedirs(f'{tagged_path}/{line}')
                classes[line] = 0
    
    return classes

def find_faces(image):
    faceCascade = cv.CascadeClassifier(r'C:\Users\Cristina\Desktop\CoreAI\LigaACLabs2020\AC-Labs-Ethergate-2020\Sessions\Session 4\haarcascade_frontalface_default.xml')
    return faceCascade.detectMultiScale(image, 1.3, 5)

def draw_faces(image, face, faces):
    image_drawn = image.copy()
    image_drawn = cv.cvtColor(image_drawn,cv.COLOR_GRAY2BGR)

    for x,y,w,h in faces: 
        cv.rectangle(image_drawn,(x,y),(x+w,y+h), (0,120,0),2)
    
    x,y,h,w = face
    cv.rectangle(image_drawn,(x,y),(x+w,y+h), (0,255,0),4)

    return image_drawn

def butt_callback(image,coord,name, dataset_path, classes):
    x,y,w,h = coord
    global TAGGED
    try:
        # print('HIHIHI')
        crop = image[y:y+h,x:x+w]
        # print('After crop')
        crop = cv.resize(crop, (96,96))
        # print('After resize')
        cv.imwrite(f'{dataset_path}/{name}/{classes[name]:04d}.png', crop)
        # print('After imwrite')
        print(name)
        TAGGED = True
    except Exception:
        return
    TAGGED = True
    classes[name] +=1
    
def other():
    global TAGGED
    TAGGED = True

def main():
    window = tkinter.Tk()
    window.title('Tag Here')

    global TAGGED

    def closed():
        cv.waitKey(1)
        cv.destroyAllWindows()
        window.destroy()
        quit()
    
    window.protocol('WM_DELETE_WINDOW', closed)

    dataset_path = r'C:\Users\Cristina\Desktop\CoreAI\LigaACLabs2020\AC-Labs-Ethergate-2020\Sessions\dataset'
    tagged_path = r'C:\Users\Cristina\Desktop\CoreAI\LigaACLabs2020\AC-Labs-Ethergate-2020\Sessions\tagged_data'
    classes_path = r'C:\Users\Cristina\Desktop\CoreAI\LigaACLabs2020\AC-Labs-Ethergate-2020\Sessions\Session 6\classes.txt'

    images= load_pictures(dataset_path)
    classes  = load_classes(classes_path,tagged_path)
    names = classes.keys()

    print(names)
    
    buttons = {}

    image = None
    name = ''
    coord =  None

    def create_cb(name):
        def cb():
            _name = name
            butt_callback(image, coord, _name,tagged_path, classes)
        return cb

    
    for i, name in enumerate(names):
        cb  = create_cb(name)
        buttons[name] = tkinter.Button(window, text= name, bg='lightblue', command  = cb )
        buttons[name].grid(column  = 0, row = i)

    buttons['Other'] = tkinter.Button(window,text = 'Other', bg = 'lightblue', command = other)
    buttons['Other'].grid(column = 0, row =len(names))


    for img in images:
        faces  = find_faces(img)
        for face in faces:
            TAGGED = False
            image = img
            coord = face 
            image_drawn   = draw_faces(image, face, faces)
            # print(image_drawn)
            # plt.imshow(image_drawn)
            # plt.show()
            cv.imshow('Image', image_drawn)

            while not TAGGED:
                window.update()

    window.destroy()
    cv.waitKey(1)
    cv.destroyAllWindows()



if __name__ == "__main__":
    main()





