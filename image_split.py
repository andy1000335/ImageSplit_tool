import cv2
import os
import argparse

MAX_WIDTH = 1500
MAX_HEIGHT = 1000

def onClick(event, x, y, flags, param):
    dw = int(w/2)
    dh = int(h/2)
    org_x = round(x*ratio)
    org_y = round(y*ratio)
    if event == cv2.EVENT_LBUTTONDOWN:
        if (org_x > width-dw):
            org_x = width-dw
            x = int(width/ratio) - int(dw/ratio)
        elif (org_x < dw):
            org_x = dw
            x = int(dw/ratio)
        if (org_y > height-dh):
            org_y = height-dh
            y = int(height/ratio) - int(dh/ratio)
        elif (org_y < dh):
            org_y = dh
            y =  int(dh/ratio)
        name = f'{file[:-4]}_{org_y}_{org_x}{file[-4:]}'
        cv2.rectangle(showImg, (x-int(dw/ratio), y-int(dh/ratio)), (x+int(dw/ratio), y+int(dh/ratio)), (0, 0, 255), 2)
        cv2.imwrite(os.path.join(args.save, name), image[org_y-dh:org_y+dh, org_x-dw:org_x+dw, :])
        # print(f'save image: {name}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Split")
    parser.add_argument('--image_folder', type=str, help='source folder')
    parser.add_argument('--save', type=str, help='folder to save subimages') 
    parser.add_argument('--width', type=int, default=600, help='target width')
    parser.add_argument('--height', type=int, default=600, help='target height')
    args = parser.parse_args()
    w = args.width
    h = args.height
    
    print('|---------------------|')
    print('| ESC  : Quit         |')
    print('| SPACE: Next picture |')
    print('|---------------------|')
    print()

    files = os.listdir(args.image_folder)
    for i, file in enumerate(files):
        print(f'\r{i+1}/{len(files)}', end='')
        imagePath = os.path.join(args.image_folder, file)
        image = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
        showImg = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
        height = image.shape[0]
        width = image.shape[1]

        ratio = 1
        if (width > MAX_WIDTH) or (height > MAX_HEIGHT):
            ratio = max(width/MAX_WIDTH, height/MAX_HEIGHT)
            showImg = cv2.resize(showImg, (int(width/ratio), int(height/ratio)))

        cv2.namedWindow(file)
        cv2.setMouseCallback(file, onClick)
        while(True):
            cv2.imshow(file, showImg)
            key = cv2.waitKey(1)
            if key == 32:      # Space
                break
            elif key == 27:    # Esc
                print('\nProcess ends.')
                exit()
            
        cv2.destroyAllWindows()
    print()