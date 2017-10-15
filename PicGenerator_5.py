
import copy
from PIL import Image,ImageDraw
import string
import random

## important: file size: 400 * 200

import math

# 80 * 20
height = 400
width = 200
dx = 5
dy = 10
row_num = height // dx
col_num = width // dy


def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def find_first (x1,y1,x2,y2):
        k = (y2-y1)/(x2-x1)
        b = y1 - x1*k
        return (k,b)
'''
def find_second (x1,y1,x2,y2,x3,y3):
        #solve for b
        denominator = (x1-x2)*(x1**2-x3**2)
        denominator = denominator/(x1**2 - x2**2) - (x2 - x3)
        nominator = (y1-y2)*(x2**2-x3**2)
        nominator = nominator/(x1**2 - x2**2) - (y2 - y3)
        b = nominator/denominator
        #solve for a
        a = ((y1-y2)+b*(x2-x1))/(x1**2-x2**2)
        #sovle for b
        c = y1 - a*(x1**2) - b*x1
        return (a,b,c)

def find_third (x1,y1,x2,y2,x3,y3,x4,y4):
        #solve for a and b
        tmp1 = (x2-x4)/(x3-x4)
        A = (y3-y4) * tmp1 - (y2 - y4)
        B = (x3**3 - x4**3) * tmp1 - (x2**3 - x4 ** 3)
        C = (x3**2 - x4**2) * tmp1 - (x2**2 - x4 ** 2)
        tmp2 = (x2-x4)/(x1-x4)
        D = (y1-y4) * tmp2 - (y2 - y4)
        E = (x1**3 - x4**3) * tmp2 - (x2**3 - x4 ** 3)
        F = (x1**2 - x4**2) * tmp2 - (x2**2 - x4 ** 2)
        a = (A*F/C - D) / (B*F/C - E)
        b = (A - B*a)/C
        c = (y3 - y4) - a * (x3**3 - x4**3) - b * (x3**2 - x4**2)
        d = y1 - a*(x1**3) - b*(x1**2) - c*x1
        return (a,b,c,d)
'''
def convert_num_to_rgb_10_1 (n):
    # n should be a float
    # n should be between -8000 and 8000
    m = (n+10000) * 10
    r = int(m // 10**4)
    g = int(m // 10**2 - r * 100)
    b = int(m % 100)
    return (r,g,b)

def convert_num_to_rgb_10_3 (n):
    # n should be a float
    # n should be between -499 and 499
    m = (n+500) * 1000
    r = int(m // 10**4)
    g = int(m // 10**2 - r * 100)
    b = int(m % 100)
    return (r,g,b)

def convert_initial_list(A):
    # A is a 80*20 2-D list
    k = list()
    for i in range(len(A)):
        l = list()
        for j in range(len(A[i])):
            if(0 <= j <= 9):
                l.append(convert_num_to_rgb_10_3(A[i][j]))
            else:
                l.append(convert_num_to_rgb_10_1(A[i][j]))
        k.append(l)
    return k

def get_pixel(A,x,y):
    # x: row number
    # y: col number
    # assume the pic is 400 * 360
    if ( x >= height or y >= width):
        return (0,0,0)
    x0 = (x // dx) 
    y0 = (y // dy)
    
    return A[x0][y0]

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


def draw(RGBs):
        height = 400
        width = 200
        rowHeight = 5
        colWidth = 10
        #PILdraw
        #[(min_R,range_R),(min_G,range_G),(min_B,range_B)] = findRange(RGBs,height,width,rowHeight,colWidth)
        image1 = Image.new("RGB", (width, height),'white')
        draw = ImageDraw.Draw(image1)
        #draw
        S = convert_initial_list(RGBs)
        for row in range(0,height):
                print(row)
                for col in range(0,width):
                        x1 = row
                        y1 = col
                        x2 = row + 1
                        y2 = col + 1
                        #(R,G,B) = get_pixel(RGBs,x1,y1)
                        #R = int((R - min_R)*255/range_R)
                        #G = int((G - min_G)*255/range_G)
                        #B = int((B - min_B)*255/range_B)
                        #color = (R,G,B)
                        #PILdraw
                        color = get_pixel(S,x1,y1)
                        draw.rectangle([(y1,x1),(y2,x2)],fill=color)
        name = 'pics/'+id_generator()+'.jpeg'  #need coordination
        #PIL save
        image1.save(name)

def combineData(alphaList,omegaList):
    result = list()
    for row in range(row_num):
        l = list()
        for col in range(col_num):
            temp = col_num//2
            if(col<temp):
                l.append(alphaList[row][col])
            else:
                l.append(omegaList[row][col-temp])
        result.append(l)
    return result
'''
def getListFromFile(oname,aname):
    omegaList = list()
    alphaList = list()
    omegaL = list()
    alphaL = list()
    count = 0
    with open(oname) as omegaFile:
        lines = omegaFile.read().splitlines()
        for line in lines:
            l = list()
            line = line[1:-1]
            for omega in line.split(','):
                l.append(omega)
            omegaList.append(l)
            count += 1
            if(count == 80):
                break
    count = 0
    with open(aname) as alphaFile:
        lines = alphaFile.read().splitlines()
        for line in lines:
            l = list()
            line = line[1:-1]
            for alpha in line.split(','):
                l.append(alpha)
            alphaList.append(l)
            count += 1
            if(count == 80):
                break
    for i in range(len(omegaList)):
        ol = list()
        al = list()
        for j in range(len(omegaList[0])):
            ol.append(float(omegaList[i][j]))
            al.append(float(alphaList[i][j]))
        omegaL.append(ol)
        alphaL.append(al)
    return combineData(omegaL,alphaL)

def drawFromFiles(startIndex,endIndex):
    for i in range(startIndex,endIndex):
        oname = "omega/omega%d.txt"%i
        aname = "alpha/alpha%d.txt"%i
        print("generating first picture")
        draw(getListFromFile(oname,aname))

drawFromFiles(0,297)

draw(combineData(omegaList,alphaList))
'''