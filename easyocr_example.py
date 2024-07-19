import cv2
import easyocr

def go():
    file_path = 'images/ac_unit.jpg'
    image = cv2.imread(file_path)

    reader = easyocr.Reader(['en'])
    print()
    print("!!!")

    results = reader.readtext(image)
    i = 1
    for result in results:
        print(f"{i}: {result}")
        i += 1
    
    results = reader.readtext(image)
    for result in results:
        print(f"{i}: {result}")
        i += 1

if __name__ == '__main__':
    go()