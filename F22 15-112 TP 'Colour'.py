import sys
import math, copy, random
import cs112_f22_week6_linter
from cmu_112_graphics import *
import colorsys

# tp project

def appStarted(app):
    #General App Variables
    app.cx = app.width/2
    app.cy = app.height/2
    app.adjust = app.width/36.66666666666667
    app.mousePosition = [0,0]
    app.backgroundColor = rgbString(246,246,246)

    #Color Wheel Dimensions
    app.r = 250
    app.wheelX = app.cx
    app.wheelY = app.cy
    app.wheelX1 = app.wheelX-app.r
    app.wheelX2 = app.wheelX+app.r
    app.wheelY1 = app.wheelY-app.r
    app.wheelY2 = app.wheelY+app.r

    #Pages: home = 0; playColor = 1; playShape = 2; prePlayScreen = 3; accuracyScreen = 4; scoreScreen = 5
    app.page = 0  

    #Calculating Accuracy
    app.accuracy = 500
    app.accuracies = [[],[]]
    app.score = 0
    app.scoreLines = []

    #Color Interpretation
    #RGB of Target Color
    app.color = (0,0,0)
    #Points of Target Shape
    app.polygon = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #Global Target Angle
    app.angle = 0
    app.distance = 0

    #MousePressed
    app.userClick = [0,0]
    #Total clicks/guesses user makes 
    app.clicks = 0
    app.mouseClicked = [0,0]

    #Color Wheel Image Load
    app.satWheel = app.loadImage('saturationWheel.jpeg')
    app.satWheel2 = app.scaleImage(app.satWheel, 6.49/20)

    #levels
    app.levels = []
    app.currentLevel = 0
    app.currentPage = 0 # 0=ColorPlay 1=ShapePlay
    app.levelBoxes = []
    app.levelColors = ["forestgreen", "forestgreen", "forestgreen", "forestgreen", "forestgreen"]

    #Timer
    app.timerTriangles = []
    app.timerAngle = 9999999999
    app.timePassed=0
    app.drawAccuracy = False
    app.endOfTimer = False
    app.count = 0

    #Game Functions
    app.clicks = 0

    #Accuracy
    app.showAccuracy = False
    app.accuracyAverageColors = ["darkgray", "darkgray", "darkgray", "darkgray", "darkgray"]

'''''''''''''''''''''''''''''''''Drawing Functions'''''''''''''''''''''''''''

#screenshot from https://color.method.ac
def drawColorWheel(app, canvas, x, y):
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.satWheel2))

#https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def drawBackground(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,
                            fill=rgbString(246,246,246))

def drawLogo(app, canvas):
    #gray bar
    canvas.create_rectangle(0,0,app.width,38,fill ='gainsboro',
                            outline = "silver")
    #top text
    canvas.create_text(40,19, text = "colour", font = 'Helvetica 15 bold')
    canvas.create_text(147,19, text = "a colour matching game",
                       font = 'Helvetica 15')

def drawHomeButtons(app, canvas):
    (x, y, r) = (app.wheelX+2*(app.width/11), app.wheelY, 210)
    color = rgbString(246,246,246)
    #draw play button
    canvas.create_oval(x-r,y-r,x+r,y+r, fill = color, outline = color)
    canvas.create_text(x, y-20, text = "Colour", font='Helvetica 98 bold', fill = rgbString(34,33,32))
    canvas.create_text(x, y+50, text = "Press to get started", 
                       font='Helvetica 28', fill = "gray")

    (x, y, r) = (app.height/2, app.height/2, 40)
    #draw color blind assist button 
    canvas.create_rectangle(x-3*r,y-r,x+3*r,y+r,outline = "darkgray")
    canvas.create_text(x+22, y-8, text = "Color blind assist", font = 'Helvetica 18', fill = rgbString(34,33,32))
    canvas.create_text(x+22, y+10, text = "Experimental support", font = 'Helvetica 13', fill = "gray")
    canvas.create_text(x-40, y-55, text = "ADDITIONAL FEATURE", font = 'Helvetica 13 bold', fill = "gray")

    #image of eye recreated from https://color.method.ac
    (x,y) = (x-84,y)
    r = 15
    canvas.create_oval(x-r-4, y-r,x+r+4,y+r, fill = "gray", outline = "gray")
    (r,y) = (13, y+4)
    canvas.create_oval(x-r-6, y-r,x+r+6,y+r, fill = app.backgroundColor, outline = app.backgroundColor)
    (r,y) = (10, y-5)
    canvas.create_oval(x-r, y-r,x+r,y+r, fill = "gray", outline = "gray")

def getMatchColor(app, mouseX, mouseY):
    d = distance(mouseX, mouseY, app.wheelX, app.wheelY)
    a = getAngle(app, mouseX, mouseY, app.wheelX, app.wheelY)
    color = getHex(app, a, d)
    return color

def drawMatchColor(app, canvas, x, y, color):
    r = 93.7
    canvas.create_oval(x-r,y-r,x+r,y+r, fill = color, outline = color)

def drawShapes(app, canvas):
    #draw rectangle
    r = 9
    x = app.wheelX + 225
    y = app.wheelY
    canvas.create_rectangle(x-r,y-r,x+r,y+r, outline = "gray", width = 3)
    #draw circle
    r = 12
    dx = 112.5
    dy = 112.5*(math.sqrt(3))
    x = app.wheelX - dx
    y = app.wheelY - dy
    canvas.create_oval(x-r, y-r, x+r, y+r, outline = "gray", width = 3)
    #draw triangle
    dx = 225/(math.sqrt(2))
    dy = dx
    x = app.wheelX - dx
    y = app.wheelY + dy
    right = [x+r, y]
    bottom = [x - (r/2), y + ((r/2)*(math.sqrt(3)))]
    top = [bottom[0], y - (bottom[1]-y)]
    canvas.create_polygon(right[0], right[1], bottom[0], bottom[1], 
                          top[0], top[1], outline = "gray", width = 3)

'''''''''''''''''''''''''''Draw Level Start Pages'''''''''''''''''''''''''''''''''

def drawStartPage(app, canvas):
    drawHueWheel(app, canvas)
    drawLevels(app, canvas)
    drawHueMouse(app, canvas)
    # drawStartPageTimer(app, canvas)

def drawHueWheel(app, canvas):
    drawColorWheel(app, canvas, app.wheelX, app.wheelY,)
    color = rgbString(246,246,246)
    (x, y, r) = (app.wheelX, app.wheelY, 210)
    #draw white circle
    canvas.create_oval(x-r,y-r,x+r,y+r, fill = color, outline = color)
    canvas.create_text(x,y-15, text = "saturation", font = "Helvetica 65 bold", fill = rgbString(34,33,32))
    canvas.create_text(x,y+30, text = "Press to get started", font = "Helvetica 23", fill = rgbString(66,65,64))

def drawHueMouse(app, canvas):
    #mouse drawn when user plays game 
    (x, y, r) = (app.mousePosition[0], app.mousePosition[1], 1300/100)

    #mouse movement inside small circle
    if ((abs(distance(app.wheelX,app.wheelY,x,y))<=300)):
        [iX,iY] = getOutsideMouseCoors(app,x,y,r, 229.5) 
        quad = getQuadrant(app,x,y, app.wheelX, app.wheelY)
        #Quadrant 2
        if quad==2:
            d = iX-app.wheelX
            [iX,iY] = [app.wheelX-d,iY] 
        #Quadrant 3
        elif quad==3:
            dx = iX-app.wheelX
            dy = app.wheelY-iY
            [iX,iY] = [app.wheelX-dx, app.wheelY+dy]
        #Quadrant 4
        elif quad==4:
            dy = app.wheelY-iY
            [iX,iY] = [iX, app.wheelY+dy]
        #Quadrant 1
        canvas.create_oval(iX-r,iY-r,iX+r,iY+r, width = 3.5)

    #mouse movement between small and big circle
    elif (((abs(distance(app.cx,app.cy-app.adjust,x-r,y)))<=app.r) and
        ((abs(distance(app.cx,app.cy-app.adjust,x,y-r)))<=app.r) and 
        ((abs(distance(app.cx,app.cy-app.adjust,x+r,y)))<=app.r) and
        ((abs(distance(app.cx,app.cy-app.adjust,x,y+r)))<=app.r)):
        canvas.create_oval(x-r,y-r,x+r,y+r, width = 3.5)

    #mouse movement outside big circle
    else: 
        [iX,iY] = getInsideMouseCoors(app,x,y,r,244)
        quad = getQuadrant(app, x, y, app.wheelX, app.wheelY)
        #Quadrant 2
        if quad == 2:
            d = iX-app.wheelX
            [iX,iY] = [app.wheelX-d,iY] 
        #Quadrant 3
        elif quad == 3:
            dx = iX-app.wheelX
            dy = app.wheelY-iY
            [iX,iY] = [app.wheelX-dx, app.wheelY+dy]
        #Quadrant 4
        elif quad == 4:
            dy = app.wheelY-iY
            [iX,iY] = [iX, app.wheelY+dy]
        #Quadrant 1
        canvas.create_oval(iX-r,iY-r,iX+r,iY+r, width = 3.5)

'''''''''''''''''''''''''''''''''Drawing Levels'''''''''''''''''''''''''''''''''

def drawLevels(app, canvas):
    #draw bottom gray bars
    canvas.create_rectangle(0,app.height-30, app.width, app.height, 
                            fill = "gainsboro", outline = "gainsboro")
    drawAverageScoreLines(app, canvas)

    #draw saturation level
    canvas.create_rectangle(0,app.height-50, app.width/5, app.height, 
                            fill = "gainsboro", outline = "gainsboro")
    canvas.create_rectangle(0,app.height-55, app.width/5, app.height-50, 
                            fill = "black", outline = "black")
    canvas.create_text(50, app.height-35, text = "SATURATION", fill = "black", 
                        font = "Helvetica 10 bold")

def drawHomeLevels(app, canvas):
    canvas.create_rectangle(0,app.height-30, app.width, app.height, 
                            fill = "gainsboro", outline = "gainsboro")
    canvas.create_rectangle(0,app.height-35, app.width, app.height-30, 
                            fill = "darkgray", outline = "darkgray")
    # canvas.create_text(50, app.height-15, text = "SATURATION", fill = "darkgray", 
    #                     font = "Helvetica 10 bold")

def getLevelBoxes(app):
    for i in range(5):
        r = 5
        x = 23 + ((3*r)*i)
        y = app.height-18
        app.levelBoxes.append([r, x, y])

def getScoreLines(app):
    len = app.width/5
    for i in range(5):
        x = (len*(i+1))-(len/2)
        y = app.height-32.5
        r = 2.5
        app.scoreLines.append([x,y,r])

def drawAverageScoreLines(app, canvas):
    color = app.accuracyAverageColors
    for i in range(5):
        x = app.scoreLines[i][0]
        y = app.scoreLines[i][1]
        r = app.scoreLines[i][2]
        canvas.create_rectangle(x-r,y-r, x+r, y+r, 
                                fill = color[i], outline = color[i])

def drawLevelBoxes(app, canvas):
    for i in range(len(app.accuracies[app.currentLevel])):

        r = app.levelBoxes[i][0]
        x = app.levelBoxes[i][1]
        y = app.levelBoxes[i][2]        
        color = getAccuracyColor(app, app.accuracies[app.currentLevel][i])
        canvas.create_rectangle(x-r, y-r, x+r, y+r, fill = color, outline = color)

'''''''''''''''''''''''''''''''''Timer'''''''''''''''''''''''''''''''''''''''

def drawTimer(app, canvas):
    #r = 77.5
    #contains the difference in x and y for each triangle 
    triangles = app.timerTriangles

    for t in range(len(triangles)):
        # width=2 to increase opacity
        canvas.create_polygon(app.wheelX, app.wheelY, 
                        app.wheelX + triangles[t][0], app.wheelY + triangles[t][1],
                        app.wheelX + triangles[t][2], app.wheelY + triangles[t][3], 
                        fill = app.matchColor, width=2, outline = app.matchColor)


def addTriangles(app):
    #will store the difference in the x and y values, including - and +
    a = app.timerAngle

    #finds quad of angle
    if a <= 91:
        quad = 2
    elif a <= 181:
        quad = 3
    elif a <= 271:
        quad = 4
    else:
        quad = 1
    #finds differences in points based on quad
    points = findPoints(app, quad)
    
    app.timerTriangles.append([points[0], points[1], points[2], points[3]])

def findPoints(app, quad):
    #indexes into the differences and assigns - and + x and y values based on quad
    diff = findTimerDifferences()
    #index of angle in differences
    i = app.timerAngle

    # -x and -y
    if quad ==2: 
        index = diff[i-1]
        points = [-index[0], -index[1], -index[2], -index[3]]

    # -x and +y
    elif quad==3: 
        index = diff[len(diff)-(app.timerAngle)-1]
        points = [-index[0], index[1], -index[2], index[3]]

    # +x and +y
    elif quad==4:
        index = diff[i-180-1]
        points = [index[0], index[1], index[2], index[3]]

    # +x and -y
    elif quad==1:
        index = diff[len(diff)-(app.timerAngle-270)]
        points = [index[0], -index[1], index[2], -index[3]]
    return (points)    

def findTimerDifferences():
    #find differences in x and y by visualizing quadrant 2 (starting point of timer)
    #these differences will be used in rest of quadrants. 
    differences = []
    a1 = 0

    while a1<92:
        #declare other angle
        a2 = 90-a1

        #find point2
        if len(differences)==0: 
            (x2, y2) = (0,78)
        else: 
            end = differences[len(differences)-1]
            (x2, y2) = (end[2], end[3])

        #find point3
        x3 = (80*(math.cos(a2*(math.pi/180))))
        y3 = (80*(math.sin(a2*(math.pi/180))))

        a1+=1
        differences.append([x2,y2,x3,y3])
    return (differences)

'''''''''''''''''''''''''''Calculate User Accuracy'''''''''''''''''''''''''''

def getAccuracy(app, x, y):
    #get angle of userClick
    userA = getAngle(app, x, y, app.wheelX, app.wheelY)
    #get distance between userClick and center
    userD = distance(x, y, app.wheelX, app.wheelY)
    if userD>app.r:
        userD = app.r
    elif userD<93.7:
        userD = 93.7
    #get target angle and distance
    (targetA, targetD) = (app.angle, app.distance)

    #get user and target colors
    userColor = getRGB(app, userA, userD)
    (userR, userG, userB) = userColor
    targetColor = getRGB(app, targetA, targetD)
    (targetR, targetG, targetB) = targetColor

    #get percentage errors in RGB
    diffR = (abs(userR-targetR)/targetR)*100
    diffG = (abs(userG-targetG)/targetG)*100
    diffB = (abs(userB-targetB)/targetB)*100

    #get percentage accuracies in RGB
    accR = abs(diffR-100)
    accG = abs(diffG-100)
    accB = abs(diffB-100)

    totalAcc = (accR*0.33333)+(accG*0.33333)+(accB*0.33333)

    return (totalAcc)

def getAccuracyGrade(app, acc):
    if 96<=acc<=100:
        return ("perfect")
    elif 85<=acc<96:
        return ("very good")
    elif 75<=acc<85:
        return ("good")
    elif 62<=acc<75:
        return ("average")
    elif app.accuracy==500:
        return ('')
    else: 
        return ("poor")

def getAccuracyColor(app, acc):
    if 96<=acc<=100:
        return ("forestgreen")
    elif 85<=acc<96:
        return ("limegreen")
    elif 75<=acc<85:
        return ("lime")
    elif 62<=acc<75:
        return ("yellow")
    else: 
        return ("red")


def drawAccuracy(app, canvas, acc):
    accuracy = getAccuracyGrade(app, acc)
    #shadow text
    canvas.create_text(app.wheelX+0.5, app.wheelY+0.5, font = "Helvetica 19", 
                            fill = "dimgray", text = accuracy)
    #text
    canvas.create_text(app.wheelX, app.wheelY, font = "Helvetica 19", 
                            fill = "gainsboro", text = accuracy)

def getFinalScore(app):
    s = app.score
    pass

'''''''''''''''''''''''''''Shape Interpolation'''''''''''''''''''''''''''''''''

def polygonText(app, canvas):
    (x, y) = (290, 248)
    canvas.create_text(x, y, text="target", font="Helvetica 13", fill="grey")
    y = 378
    canvas.create_text(x, y, text="match", font="Helvetica 13", fill="grey")

def getRandomDistance(app):
    d = random.randint(93, app.r)
    if d==93.7:
        d = 93.7
    return d

def getRandomAngle():
    #get random angle
    a = random.randint(0,360)
    angle = a*(math.pi/180)
    if a ==360:
        angle = 6.283185307179585
    angle = a*(math.pi/180)
    return (angle)

def getTarget(app):
    (x, y, r) = (290, 305, 40)
    #get random angle
    angle = app.angle

    #gets points from random angle
    points = getPoints(app, x, y, r, angle)

    return (points)

def drawTarget(app, canvas, p, d):
    p = app.polygon
    d = app.distance
    #draws shape of random target
    canvas.create_polygon(p[0],  p[1], p[2],  p[3],  p[4],  p[5],  p[6],  p[7], 
                        p[8],  p[9], p[10], p[11], p[12], p[13], p[14], p[15], 
                        p[16], p[17], p[18], p[19], p[20], p[21], p[22], p[23], 
                        p[24], p[25], p[26], p[27], p[28], p[29], p[30], p[31],
                        outline = "dimgray", width = 10*(d/app.r),fill = rgbString(246,246,246))

def drawMatch(app, canvas, mouseX, mouseY):
    (x, y, r) = (290, 435, 40)
    #gets angle of mouse in radians
    a = getAngle(app, mouseX, mouseY, app.wheelX, app.wheelY)
    d = distance(app.wheelX,app.wheelY,mouseX,mouseY)
    if d<93.7:
        d = 93.7
    elif d>app.r:
        d = app.r
    #reassigns app.polygon
    p = getPoints(app, x, y, r, a)
    canvas.create_polygon(p[0],  p[1], p[2],  p[3],  p[4],  p[5],  p[ 6],  p[7], 
                        p[8],  p[9], p[10], p[11], p[12], p[13], p[14], p[15], 
                        p[16], p[17], p[18], p[19], p[20], p[21], p[22], p[23], 
                        p[24], p[25], p[26], p[27], p[28], p[29], p[30], p[31],
                        outline = "dimgray", width = 10*(d/app.r), 
                        fill = rgbString(246,246,246))

def getPoints(app, x, y, r, a):
    #if in between square and circle, including square:
    if a < (120*(math.pi/180)):
        return squareToCircle(a, x, y, r)

    #if in between circle and triangle, including circle:
    elif a < (225*(math.pi/180)):
        return circleToTriangle(a-(120*(math.pi/180)), x, y, r)

    #if in between triangle and square, including triangle
    #elif a < (360*(math.pi/180)):
    return triangleToSquare(a-(225*(math.pi/180)), x, y, r)

def squareToCircle(a, x, y, r):
    (sqrt2, sqrt3) = ((r/math.sqrt(2)), ((r/2)*math.sqrt(3)))
    (half, num) = (r/2, 14.289)

    #distances between circle points and square points
    d = [(abs(r-sqrt2)), 0, 
        abs(sqrt3-sqrt2), abs(half-num), 
        0, 0, 
        abs(half-num), abs(sqrt3-sqrt2), 
        0, abs(r-sqrt2), 
        abs(half-num), abs(sqrt3-sqrt2), 
        0, 0,
        abs(sqrt3-sqrt2), abs(half-num),
        abs(r-sqrt2), 0, 
        abs(sqrt3-sqrt2), abs(half-num), 
        0, 0, 
        abs(half-num), abs(sqrt3-sqrt2), 
        0, abs(r-sqrt2), 
        abs(half-num), abs(sqrt3-sqrt2), 
        0, 0,
        abs(sqrt3-sqrt2), abs(half-num)]

    #distance * angle/total angles between square & circle
    diff = []
    for i in range(len(d)):
        val = ((a / (120*(math.pi/180)))*d[i])
        diff.append(val)

    #distances from center to draw square + x or y
    polygon = [x+(r/math.sqrt(2)+diff[0]), y+diff[1],
            x+(r/math.sqrt(2)+diff[2]), y-(14.289+diff[3]),
            x+(r/math.sqrt(2)+diff[4]), y-(r/math.sqrt(2)+diff[5]), 

            x+14.289+diff[6], y-(r/math.sqrt(2)+diff[7]),
            x+diff[8], y-(r/math.sqrt(2)+diff[9]),
            x-(14.289+diff[10]), y-(r/math.sqrt(2)+diff[11]),
            x-(r/math.sqrt(2)+diff[12]), y-(r/math.sqrt(2)+diff[13]), 

            x-(r/math.sqrt(2)+diff[14]), y-(14.289+diff[15]), 
            x-(r/math.sqrt(2)+diff[16]), y+diff[17], 
            x-(r/math.sqrt(2)+diff[18]), y+14.289+diff[19], 
            x-(r/math.sqrt(2)+diff[20]), y+(r/math.sqrt(2)+diff[21]), 

            x-(14.289+diff[22]), y+(r/math.sqrt(2)+diff[23]), 
            x+diff[24], y+(r/math.sqrt(2)+diff[25]), 
            x+14.289+diff[26], y+(r/math.sqrt(2)+diff[27]), 
            x+(r/math.sqrt(2)+diff[28]), y+(r/math.sqrt(2)+diff[29]), 

            x+(r/math.sqrt(2)+diff[30]), y+14.289+diff[31]]

    return polygon

def circleToTriangle(a, x, y, r):
    (sqrt2, sqrt3) = ((r/math.sqrt(2)), ((r/2)*math.sqrt(3)))
    (half) = (r/2)

    #distances between triangle points and circle points
    d = [0, 0, 
        abs(sqrt3-17.5), abs(half-10.104), 
        abs(sqrt2-12.811), abs(sqrt2-12.811), 
        abs(half-8.75), abs(sqrt3-15.155), 
        0, abs(r-20.207), 

        0, 0, 
        abs(sqrt2-half), abs(sqrt2-17.5),
        abs(sqrt3-half), abs(half-10.104),
        abs(r-half), 0, 
        abs(sqrt3-half), abs(half-10.104), 
        abs(sqrt2-half), abs(sqrt2-17.5),

        0, 0, 
        0, abs(r-20.207), 
        abs(half-8.75), abs(sqrt3-15.155), 
        abs(sqrt2-12.811), abs(sqrt2-12.811),
        abs(sqrt3-17.5), abs(half-10.104)]

    #distance * angle/total angles between circle & triangle
    diff = []
    for i in range(len(d)):
        val = ((a / (105*(math.pi/180)))*d[i])
        diff.append(val)

    #distances from center to draw square + x or y
    polygon = [x+r-diff[0],y-diff[1], 
            x+((r/2)*math.sqrt(3)-diff[2]), y-(r/2-diff[3]), 
            x+(r/math.sqrt(2)-diff[4]), y-(r/math.sqrt(2)-diff[5]), 
            x+(r/2-diff[6]), y-((r/2)*math.sqrt(3)-diff[7]), 
            x-diff[8], y-(r-diff[9]), 

            x-(r/2-diff[10]), y-((r/2)*math.sqrt(3)-diff[11]), 
            x-(r/math.sqrt(2)-diff[12]), y-(r/math.sqrt(2)-diff[13]), 
            x-((r/2)*math.sqrt(3)-diff[14]), y-(r/2-diff[15]), 
            x-(r-diff[16]), y-diff[17], 
            
            x-((r/2)*math.sqrt(3)-diff[18]), y+(r/2)-diff[19], 
            x-(r/math.sqrt(2)-diff[20]), y+(r/math.sqrt(2)-diff[21]), 
            x-(r/2-diff[22]), y+((r/2)*math.sqrt(3)-diff[23]), 
            x-diff[24], y+r-diff[25], 
            
            x+(r/2)-diff[26], y+((r/2)*math.sqrt(3))-diff[27], 
            x+(r/math.sqrt(2))-diff[28], y+(r/math.sqrt(2))-diff[29], 
            x+((r/2)*math.sqrt(3))-diff[30], y+(r/2)-diff[31]]
    
    return polygon

def triangleToSquare(a, x, y, r):
    (sqrt2, sqrt3) = ((r/math.sqrt(2)), ((r/2)*math.sqrt(3)))
    (half) = (r/2)

    #distances between circle points and square points
    d = [(abs(r-sqrt2)), 0, 
        abs(sqrt2-17.5), abs(14.289-10.104), 
        abs(sqrt2-12.811), abs(sqrt2-12.811), 
        abs(14.289-8.75), abs(sqrt2-15.155), 
        0, abs(sqrt2-20.207), 
        abs(14.289-half), abs(sqrt3-sqrt2), 
        abs(sqrt2-half), abs(sqrt2-17.5),
        abs(sqrt2-half), abs(14.289-10.104),
        abs(half-sqrt2), 0, 
        abs(sqrt2-half), abs(14.289-10.104), 
        abs(sqrt2-half), abs(sqrt2-17.5), 
        abs(14.289-half), abs(sqrt3-sqrt2), 
        0, abs(20.207-sqrt2), 
        abs(14.289-8.75), abs(15.155-sqrt2), 
        abs(sqrt2-12.811), abs(sqrt2-12.811),
        abs(17.5-sqrt2), abs(14.289-10.104)]

    #distance * angle/total angles between triangle & square
    diff = []
    for i in range(len(d)):
        val = ((a / (135*(math.pi/180)))*d[i])
        diff.append(val)

    polygon = [x+r-diff[0], y-diff[1],
            x+17.5+diff[2], y-(10.104+diff[3]),
            x+12.811+diff[4], y-(12.811+diff[5]), 
            x+8.75+diff[6], y-(15.155+diff[7]), 
            x+diff[8], y-(20.207+diff[9]), 
            x-(r/2-diff[10]), y-((r/2)*math.sqrt(3)-diff[11]),

            x-(r/2+diff[12]), y-(17.5+diff[13]), 
            x-(r/2+diff[14]), y-(10.104+diff[15]), 
            x-(r/2+diff[16]), y+diff[17], 
            x-(r/2+diff[18]), y+10.104+diff[19], 
            x-(r/2+diff[20]), y+17.5+diff[21], 
            x-(r/2-diff[22]), y+((r/2)*math.sqrt(3))-diff[23], 

            x+diff[24], y+20.207+diff[25], 
            x+8.75+diff[26], y+15.155+diff[27], 
            x+12.811+diff[28], y+12.811+diff[29], 
            x+17.5+diff[30], y+10.104+diff[31]]

    return polygon

'''''''''''''''''''''''''''Color Interpretation'''''''''''''''''''''''''''''''''

def drawTargetColor(app, canvas, x, y, color):
    r = 77.75
    #call getRandomColor somewhere else
    canvas.create_oval(x-r,y-r,x+r,y+r, fill = color, outline = color)

def getRandomColor(app):
    #get random color by getting random mouseX and mouseY values
    a = app.angle
    d = app.distance
    if d == 93:
        d = 93.7
    color = getHex(app, a, d)
    return (color)

def getRGB(app, a, d):
    #hls: (hue, lightness, saturation) = (angle, 0.5, distance from center)
    #turn radians into degrees, then divide by 360
    angle = (a*(180/math.pi))/360

    #if mouse in color wheel
    if 93.7 <= d <= app.r:
        #convert distance to lightness percentage
        dist = (d-93.7+75)/(app.r)
    #if mouse is in color matcher region
    elif d<93.7:
        dist = 0.3
    #if mouse is outside color wheel
    elif d>93.7:
        dist = 1

    #https://docs.python.org/3/library/colorsys.html
    #https://programmingdesignsystems.com/color/color-models-and-color-spaces/index.html
    rgb = colorsys.hls_to_rgb(angle, 0.5, dist)
    r = round((rgb[0])*255)
    g = round((rgb[1])*255)
    b = round((rgb[2])*255)
    return (r,g,b)

def getHex(app, a, d):
    rgb = getRGB(app, a, d)
    (r,g,b) = (rgb[0], rgb[1], rgb[2])
    return (rgbString(r,g,b))

def getAngle(app, x, y, mouseX, mouseY):
    a = getInsideAngle(app, x, y, mouseX, mouseY)
    quad = getQuadrant(app, x, y, mouseX, mouseY)
    #Quadrant 2
    if quad == 2:
        angle = abs(a-((math.pi)/2)) + ((math.pi)/2)
    #Quadrant 3
    elif quad == 3:
        angle = a + (math.pi)
    #Quadrant 4
    elif quad == 4:
        angle = abs(a-((math.pi)/2)) + 3*((math.pi)/2)
    else: 
        angle = a
    return (angle)

'''''''''''''''''''''''''''''''''Level: Complementary'''''''''''''''''''''''''''

def drawComplementaryMouse(app, canvas):
    drawGameMouse(app, canvas, app.mousePosition[0], app.mousePosition[1])
    x = app.wheelX-(app.mousePosition[0]-app.wheelX)
    y = app.wheelY-(app.mousePosition[1]-app.wheelY)
    drawGameMouse(app, canvas, x, y)

'''''''''''''''''''''''''''''''''Level: Analogous'''''''''''''''''''''''''''

#https://uxplanet.org/how-to-use-analogous-color-scheme-in-design-bf32d18ab05c
def getAnalogousAngles(app):
    (x,y) = (app.mousePosition[0], app.mousePosition[1])
    a = getInsideAngle(app, x, y, app.wheelX, app.wheelY)
    quad = getQuadrant(app,x,y, app.wheelX, app.wheelY)
    

def drawComplementaryMouse(app, canvas):
    drawGameMouse(app, canvas, app.mousePosition[0], app.mousePosition[1])
    x = app.wheelX-(app.mousePosition[0]-app.wheelX)
    y = app.wheelY-(app.mousePosition[1]-app.wheelY)
    drawGameMouse(app, canvas, x, y)

'''''''''''''''''''''''''''Draw Background Cirlces'''''''''''''''''''''''''''

def drawBackgroundCircles(app, canvas):
    (x, y, r) = (app.wheelX+2*(app.width/11), app.wheelY, 210/6)    
    canvas.create_oval(x+r, y+r, x-r, y-r, outline = "black")
    (tx,ty, tr) = (x, y-r, app.r)
    canvas.create_oval(tx-tr,ty-tr,tx+tr,ty+tr, outline = "black")
    (lx,ly, lr) = (x-r, y, tr)
    canvas.create_oval(lx-lr,ly-lr,lx+lr,ly+lr, outline = "black")

def getOppositeAngle(app):
    wheelX = app.wheelX+2*(app.width/11)
    wheelY = app.wheelY
    angle = getAngle(app, app.mousePosition[0], app.mousePosition[1], wheelX, wheelY)
    quad = getQuadrant(app, app.mousePosition[0], app.mousePosition[1],wheelX, wheelY)
    if quad==1: 
        diff = rad(90)-angle
        return rad(90)+diff
    elif quad==2: 
        diff = angle-rad(90)
        return rad(90)-diff
    elif quad==3: 
        diff = rad(270)-angle
        return rad(270)+diff
    elif quad==4:
        diff = angle-rad(270)
        return rad(270)-diff

'''''''''''''''''''''''''''''''''Mouse Controls: Play'''''''''''''''''''''''''''
def drawGameMouse(app, canvas, x, y):
#mouse drawn when user plays game 
    r = 1300/100

    #mouse movement inside small circle
    if ((abs(distance(app.wheelX,app.wheelY,x,y))<=105.9)):
        [iX,iY] = getOutsideMouseCoors(app,x,y,r, 107.5) 
        quad = getQuadrant(app,x,y, app.wheelX, app.wheelY)
        #Quadrant 2
        if quad==2:
            d = iX-app.wheelX
            [iX,iY] = [app.wheelX-d,iY] 
        #Quadrant 3
        elif quad==3:
            dx = iX-app.wheelX
            dy = app.wheelY-iY
            [iX,iY] = [app.wheelX-dx, app.wheelY+dy]
        #Quadrant 4
        elif quad==4:
            dy = app.wheelY-iY
            [iX,iY] = [iX, app.wheelY+dy]
        #Quadrant 1
        canvas.create_oval(iX-r,iY-r,iX+r,iY+r, width = 3.5)

    #mouse movement between small and big circle
    elif (((abs(distance(app.wheelX,app.wheelY,x-r,y)))<=app.r) and
        ((abs(distance(app.wheelX,app.wheelY,x,y-r)))<=app.r) and 
        ((abs(distance(app.wheelX,app.wheelY,x+r,y)))<=app.r) and
        ((abs(distance(app.wheelX,app.wheelY,x,y+r)))<=app.r)):
        canvas.create_oval(x-r,y-r,x+r,y+r, width = 3.5)

    #mouse movement outside big circle
    else: 
        [iX,iY] = getInsideMouseCoors(app,x,y,r,app.r)
        quad = getQuadrant(app, x, y, app.wheelX, app.wheelY)
        #Quadrant 2
        if quad == 2:
            d = iX-app.wheelX
            [iX,iY] = [app.wheelX-d,iY] 
        #Quadrant 3
        elif quad == 3:
            dx = iX-app.wheelX
            dy = app.wheelY-iY
            [iX,iY] = [app.wheelX-dx, app.wheelY+dy]
        #Quadrant 4
        elif quad == 4:
            dy = app.wheelY-iY
            [iX,iY] = [iX, app.wheelY+dy]
        #Quadrant 1
        
        canvas.create_oval(iX-r,iY-r,iX+r,iY+r, width = 3.5)

def getOutsideMouseCoors(app, mouseX, mouseY, mouseR, circleR):
    angle = getInsideAngle(app, mouseX, mouseY, app.wheelX, app.wheelY)
    [oX, oY, angle2] = findOutsidePoints(app, angle, circleR)
    return [oX,oY] 

def getInsideMouseCoors(app, mouseX,mouseY,mouseR, circleR):
    angle = getInsideAngle(app, mouseX, mouseY, app.wheelX, app.wheelY)
    [oX, oY, angle2] = findOutsidePoints(app, angle, circleR)
    [iX, iY] = findInsidePoints(oX, oY, mouseR, angle, angle2)
    return [iX,iY]

def findInsidePoints(oX, oY, mouseR, angle1, angle2):
    x = mouseR*(math.cos(angle1))
    y = mouseR*(math.cos(angle2))
    iX = oX-x
    iY = oY+y
    return [iX,iY]

def findOutsidePoints(app, angle1, circleR):
    angle2 = ((math.pi/2)-angle1)
    x = circleR*(math.cos((angle1)))
    y = circleR*(math.cos(angle2))
    oX = app.wheelX+x
    oY = app.wheelY-y
    return [oX,oY, angle2]

def getInsideAngle(app, mouseX, mouseY, wheelX, wheelY):
    z = distance(mouseX, mouseY, wheelX, wheelY)
    x = abs(mouseX-wheelX)
    y = abs(mouseY-wheelY)
    if x == 0:
        return (math.pi/2)
    angle = math.asin(y/z)
    return angle

def getQuadrant(app, x, y, wheelX, wheelY):
    #Quadrant 2
    if x<=wheelX and y<=wheelY:
        return (2)    
    #Quadrant 3
    elif x<=wheelX and y>=wheelY:
        return (3)
    #Quadrant 4
    elif x>=wheelX and y>=wheelY:
        return (4)
    elif x==wheelX and y>=wheelY:
        return (4)
    return (1)

'''''''''''''''''''''''''''''''''Mouse Controls: Home'''''''''''''''''''''''''''

def drawHomeMouse(app, canvas):
    #mouse drawn when user plays game 
    (x, y, r) = (app.mousePosition[0], app.mousePosition[1], 1300/100)

    (wheelX, wheelY) = (app.wheelX+2*(app.width/11), app.wheelY)

    #mouse movement inside small circle
    if ((abs(distance(wheelX,wheelY,x,y))<=300)):
        [iX,iY] = getHomeOutsideMouseCoors(app,x,y,r, 229.5) 
        quad = getHomeQuadrant(app,x,y, wheelX, wheelY)
        #Quadrant 2
        if quad==2:
            d = iX-wheelX
            [iX,iY] = [wheelX-d,iY] 
        #Quadrant 3
        elif quad==3:
            dx = iX-wheelX
            dy = wheelY-iY
            [iX,iY] = [wheelX-dx, wheelY+dy]
        #Quadrant 4
        elif quad==4:
            dy = wheelY-iY
            [iX,iY] = [iX, wheelY+dy]
        #Quadrant 1
        canvas.create_oval(iX-r,iY-r,iX+r,iY+r, width = 3.5)

    #mouse movement outside big circle
    else: 
        [iX,iY] = getHomeInsideMouseCoors(app,x,y,r,244)
        quad = getHomeQuadrant(app, x, y, wheelX, wheelY)
        #Quadrant 2
        if quad == 2:
            d = iX-wheelX
            [iX,iY] = [wheelX-d,iY] 
        #Quadrant 3
        elif quad == 3:
            dx = iX-wheelX
            dy = wheelY-iY
            [iX,iY] = [wheelX-dx, wheelY+dy]
        #Quadrant 4
        elif quad == 4:
            dy = wheelY-iY
            [iX,iY] = [iX, wheelY+dy]
        #Quadrant 1
        canvas.create_oval(iX-r,iY-r,iX+r,iY+r, width = 3.5)

def getHomeOutsideMouseCoors(app, mouseX, mouseY, mouseR, circleR):
    angle = getHomeInsideAngle(app, mouseX, mouseY, app.wheelX+2*(app.width/11), app.wheelY)
    [oX, oY, angle2] = findHomeOutsidePoints(app, angle, circleR, app.wheelX+2*(app.width/11), app.wheelY)
    return [oX,oY] 

def getHomeInsideMouseCoors(app, mouseX,mouseY,mouseR, circleR):
    angle = getHomeInsideAngle(app, mouseX, mouseY, app.wheelX+2*(app.width/11), app.wheelY)
    [oX, oY, angle2] = findHomeOutsidePoints(app, angle, circleR, app.wheelX+2*(app.width/11), app.wheelY)
    [iX, iY] = findInsidePoints(oX, oY, mouseR, angle, angle2)
    return [iX,iY]

def findHomeOutsidePoints(app, angle1, circleR, wheelX, wheelY):
    angle2 = ((math.pi/2)-angle1)
    x = circleR*(math.cos((angle1)))
    y = circleR*(math.cos(angle2))
    oX = wheelX+x
    oY = wheelY-y
    return [oX,oY, angle2]

def getHomeAngle(app, x, y):
    a = getHomeInsideAngle(app, x, y, app.wheelX+2*(app.width/11), app.wheelY)
    quad = getHomeQuadrant(app, x, y, app.wheelX+2*(app.width/11), app.wheelY)
    #Quadrant 2
    if quad == 2:
        angle = abs(a-((math.pi)/2)) + ((math.pi)/2)
    #Quadrant 3
    elif quad == 3:
        angle = a + (math.pi)
    #Quadrant 4
    elif quad == 4:
        angle = abs(a-((math.pi)/2)) + 3*((math.pi)/2)
    else: 
        angle = a
    return (angle)

def getHomeInsideAngle(app, mouseX, mouseY, wheelX, wheelY):
    z = distance(mouseX, mouseY, wheelX, wheelY)
    x = abs(mouseX-wheelX)
    y = abs(mouseY-wheelY)
    if x == 0:
        return (math.pi/2)
    angle = math.asin(y/z)
    return angle

def getHomeQuadrant(app, x, y, wheelX, wheelY):
    #Quadrant 2
    if x<wheelX and y<wheelY:
        return (2)    
    #Quadrant 3
    elif x<wheelX and y>wheelY:
        return (3)
    #Quadrant 4
    elif x>wheelX and y>wheelY:
        return (4)
    elif x==wheelX and y>wheelY:
        return (4)
    return (1)

'''''''''''''''''''''''''''''''''User Mouse Actions'''''''''''''''''''''''''''
def mousePressed(app, event):
    app.mouseClicked = [event.x, event.y]

    #Home Screen: Color Play Button
    (x, y, r) = (app.wheelX+2*(app.width/11), app.wheelY, 210)
    if (app.page==0) and distance(event.x, event.y, x, y)<r:
        
        #generate random color
        app.color = getRandomColor(app)

        #change page
        app.page = 1
        app.currentPage = 0  

    #All Screens: Colour/"Home" Button
    elif (0<event.x<180) and (10<event.y<34):
        app.page = 0
        #resets accuracies
        app.accuracies = [[],[]]
        #reset number of clicks
        app.clicks = 0
        app.showAccuracy = False
        app.endOfTimer = False
        app.timerAngle = 9999999999
    
    #Home Screen: Color Blind Assist Button
    (x, y, dy, dx) = (app.height/2, app.height/2, 40, 120)
    if (app.page==0) and (x-dx<event.x<x+dx) and (y-dy<event.y<y+dy):

        #change page
        app.page = 2
        app.currentPage = 1

        #timer
        app.timerAngle = 999999999

    #Play Screen: User Matching Colors
    if ((app.page==1 or app.page==2) and (0<event.x<app.width) 
        and (35<event.y<app.height)):
        
        if app.page==1:
            app.currentPage=0
        elif app.page==2:
            app.currentPage=1

        #update user click
        app.userClick = [event.x, event.y]

        #update random once 
        if (app.clicks%2==0):
            getRandom(app)

        if app.polygon==None or app.distance==None:
            while (app.polygon==None) or (app.distance==None):
                getRandom(app)

        #accuracy screen
        if (app.clicks>0) or (0<app.timerAngle<361):

            app.timePassed = 0

            #updates user accuracy
            app.accuracy = getAccuracy(app, app.userClick[0], app.userClick[1])

            #updates app.accuracies
            if (len(app.accuracies)>=0):
                app.accuracies[app.currentLevel].append(app.accuracy)

            #updates app.levels
            app.accuracyMatchColor = getMatchColor(app, event.x, event.y)
            app.levels.append([app.accuracy, app.color, app.accuracyMatchColor, [app.polygon, app.distance]])
                             # [accuracy, targetColor, matchColor, matchShape]

            #updates page, timePassed, drawAccuracy
            app.page=4
            app.timePassed = 0
            app.drawAccuracy = True

        #one is added when the screen changes
        if app.clicks == 6:
            app.score = getFinalScore(app)

        #start timer
        app.timerAngle = 0
        app.timerTriangles = []

        #colors for accuracy screen
        app.accuracyMatchColor = getMatchColor(app, event.x, event.y)
        if app.page==1 or app.page==2:
            app.accuracyTargetcolor = app.color

        app.clicks+=1

def getRandom(app):
    #generate random global angle for target color and shape
    app.angle = getRandomAngle()

    #generate random global distance for target color and shape
    app.distance = getRandomDistance(app)

    #generate random color
    app.color = getRandomColor(app)

    #update target color
    app.accuracyTargetcolor = app.color

    #generate random shape
    app.polygon = getTarget(app)

    #generate random global angle for target color and shape
    app.angle = getRandomAngle()

    #generate random global distance for target color and shape
    app.distance = random.randint(93, app.r)
    if app.distance==93.7:
        app.distance = 93.7

    #generate random color
    app.color = getRandomColor(app)
    app.accuracyTargetcolor = app.color

    #generate random shape
    app.polygon = getTarget(app)

def mouseMoved(app, event):
    app.mousePosition[0] = event.x
    app.mousePosition[1] = event.y

'''''''''''''''''''''''''''''''''Timer Fired'''''''''''''''''''''''''''''''''
def timerFired(app):
    app.matchColor = getMatchColor(app, app.mousePosition[0], app.mousePosition[1])

    #update scoreLines
    getScoreLines(app)

    #Draws Timer
    app.timerDelay=2
    app.timerAngle += 1
    if app.timerAngle<361:
        addTriangles(app)

    #updates page when accuracy page ends
    if (app.page == 4) and (app.timePassed == 3000):
        app.drawAccuracy = False
        if app.currentPage==0:
            app.page = 1
        elif app.currentPage==1:
            app.page= 2

    #Shows accuracy screen once timer ends
    if app.timerAngle>360 and app.timerAngle<9999999999 and app.count == 0:

        #updates app.accuracies
        app.accuracy = getAccuracy(app, app.mousePosition[0], app.mousePosition[1])
        if len(app.accuracies)>=0:
            app.accuracies[app.currentLevel].append(app.accuracy)

        #updates app.accuracyAverages (when all levels complete)
        if (len(app.accuracies)%5==0) and (len(app.accuracies)!=0):
            app.accuracyAverageColors[app.currentLevel]=getAccuracyColor(app, (average(app.accuracies[app.currentLevel])))

        #updates app.levels + matchColor
        app.accuracyMatchColor = getMatchColor(app, app.mousePosition[0], app.mousePosition[1])
        app.levels.append([app.accuracy, app.color, app.accuracyMatchColor, 
                          [app.polygon, app.distance], app.mousePosition[0], app.mousePosition[1]])

        #Maintenance
        app.endOfTimer=True
        app.drawAccuracy=True

        #updates count
        app.count+=1

        #updates page
        app.page = 4

    #Timer for Accuracy Screen
    if app.drawAccuracy==True:
        app.timePassed+=1

        if app.timePassed == 50:
            #update random values
            getRandom(app)
            if app.polygon==None or app.distance==None:
                while (app.polygon==None) or (app.distance==None):
                    getRandom(app)

            #update variables to restart
            app.count = 0
            app.clicks = 1
            app.timePassed = 0
            app.endOfTimer = False
            app.timerAngle = 0
            app.page = app.currentPage+1
            app.timerTriangles = []
            app.drawAccuracy = False

'''''''''''''''''''''''''''''''''''''''Pages'''''''''''''''''''''''''''''''''

def drawHomePage(app, canvas):
    drawColorWheel(app, canvas, app.wheelX+2*(app.width/11), app.wheelY)
    drawHomeButtons(app, canvas)
    drawHomeLevels(app, canvas)
    drawHomeMouse(app, canvas)
    # drawComplementaryMouse(app, canvas)

def drawPlayPage(app, canvas):
    drawColorWheel(app, canvas, app.wheelX, app.wheelY)
    drawMatchColor(app, canvas, app.wheelX, app.wheelY, app.matchColor)
    drawTargetColor(app, canvas, app.wheelX, app.wheelY, app.color)
    drawHomeLevels(app, canvas)
    drawTimer(app, canvas)
    drawGameMouse(app, canvas, app.mousePosition[0], app.mousePosition[1])

def drawColorBlindAssistPage(app, canvas):
    drawColorWheel(app, canvas, app.wheelX, app.wheelY)
    drawMatchColor(app, canvas, app.wheelX, app.wheelY, app.matchColor)
    drawTargetColor(app, canvas, app.wheelX, app.wheelY, app.color)
    drawShapes(app, canvas)
    drawMatch(app, canvas, app.mousePosition[0], app.mousePosition[1])
    
    getAnalogousAngles(app)
    drawTarget(app, canvas, app.polygon, app.distance)
    polygonText(app, canvas)
    drawHomeLevels(app, canvas)
    drawTimer(app, canvas)
    drawGameMouse(app, canvas, app.mousePosition[0], app.mousePosition[1])

def drawAccuracyScreen(app, canvas):
    level = len(app.levels)-1
    drawColorWheel(app, canvas, app.wheelX, app.wheelY)
    drawMatchColor(app, canvas, app.wheelX, app.wheelY, app.levels[level][2])
    drawTargetColor(app, canvas, app.wheelX, app.wheelY, app.levels[level][1])
    drawGameMouse(app, canvas, app.mousePosition[0], app.mousePosition[1])
    drawAccuracy(app, canvas, app.levels[level][0])
    drawHomeLevels(app, canvas)

    if app.currentPage==1:
        if app.endOfTimer==True: 
            drawMatch(app, canvas, app.levels[level][4], app.levels[level][5])
        else:
            drawMatch(app, canvas, app.userClick[0], app.userClick[1])
        drawShapes(app, canvas)
        drawTarget(app, canvas, app.levels[level][3][0], app.levels[level][3][1])
        polygonText(app, canvas)

'''''''''''''''''''''''''''''''''redrawAll'''''''''''''''''''''''''''''''''

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    #home page
    drawLogo(app, canvas)
    if app.page == 0:
        drawHomePage(app, canvas)
    #color play page
    elif app.page == 1 or (app.drawAccuracy==False and app.currentPage==0):
        drawPlayPage(app, canvas)
    #shape play page
    elif app.page == 2 or (app.drawAccuracy==False and app.currentPage==1):
        drawColorBlindAssistPage(app, canvas)
    #accuracy page
    elif app.drawAccuracy==True:
        drawAccuracyScreen(app, canvas)

''''''''''''''''''''''''''''Helper Functions'''''''''''''''''''''''''''''''''
def distance(x1,y1,x2,y2):
    sum = ((x2-x1)**2) + ((y2-y1)**2)
    return (sum**(1/2))

def average(L):
    sum = 0
    for i in range(len(L)):
        sum += L[i]
    return (sum/len(L))

#turn degree into radian
def rad(a):
    return (a*(math.pi/180))

#turn radian into degree
def deg(a):
    return (a*(180/math.pi))

#https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

runApp(width = 1300, height = 790)