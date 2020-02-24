import pygame as pg
import sys
from pygame.locals import *

'''
QUESTION:

Have the function CorrectPath(str) read the str parameter being passed, which will represent the movements made in a 5x5 grid of cells starting from the top left position.
The characters in the input string will be entirely composed of: r, l, u, d, ?.
Each of the characters stand for the direction to take within the grid, for example: r = right, l = left, u = up, d = down.
Your goal is to determine what characters the question marks should be in order for a path to be created to go from the top left of the grid all the way to the bottom right without touching previously travelled on cells in the grid.

For example: if str is "r?d?drdd" then your program should output the final correct string that will allow a path to be formed from the top left of a 5x5 grid to the bottom right. For this input, your program should therefore return the string "rrdrdrdd". There will only ever be one correct path and there will always be at least one question mark within the input string.
'''

def CorrectPath(string):
  CheckingRect = FONT.render("Checking",True,WHITE).get_rect()
  CheckingRect.center = (SW/2,SH/2)
  Display.blit(FONT.render("Checking",True,WHITE),CheckingRect)
  pg.display.update()
  qmark = "?"
  qmnum = 0
  qmloc = []
  oristring = string
  teststring = []
  resstring = []
  curpoint = [0,0]
  possi = 0
  possibin = ""
  possibinlist = []
  optionbin = ""
  optionbinlist = []

  fivefivegrid = []

  #set the grid
  for i in range(5):
      fivefivegrid.append(["x","x","x","x","x"])

  #pow(4,qmnum) = pow(2,2*qmnum)
  for alpha in oristring:
    teststring.append(alpha)

  #qm amount
  for i in range(len(string)):
    if string[i] == qmark:
      qmnum += 1
      qmloc.append(i)
  possi = pow(4,qmnum)
  possibin = "{0:b}".format(possi)
  for pos in possibin:
    possibinlist.append(pos)
  if (len(possibin)) % 2 != 0:
      possibinlist.pop(0)
  
  #replace the qm
  for i in range(possi):
    optionbin = "{0:b}".format(i)
    for binar in optionbin:
      optionbinlist.append(binar)
    if (len(optionbin) != len(possibinlist)):
      for i in range(len(possibinlist) - len(optionbin)):
        optionbinlist.insert(0,"0")

    for i in range(qmnum):
      combi = optionbinlist[0] +  optionbinlist[1] 
      if ( combi == "00" ):
        teststring[qmloc[i]] = "u"
      if ( combi == "01" ):
        teststring[qmloc[i]] = "d"
      if ( combi == "10" ):
        teststring[qmloc[i]] = "l"
      if ( combi == "11" ):
        teststring[qmloc[i]] = "r"
        
      optionbinlist.pop(0)
      optionbinlist.pop(0)

    #make the move
    fivefivegrid[curpoint[0]][curpoint[1]] = "o"
    for alpha in teststring:
      if alpha == "u":
        curpoint[0] -= 1
      if  alpha == "d":
        curpoint[0] += 1
      if  alpha == "l":
        curpoint[1] -= 1
      if  alpha == "r":
        curpoint[1] += 1
      
      if (curpoint[0] < 0 or curpoint[0] > 4 or curpoint[1] < 0 or curpoint[1] > 4 ):
        curpoint = [-1,-1]
        break
        
      if (fivefivegrid[curpoint[0]][curpoint[1]] == "o"):
        curpoint = [-1,-1]
        break
      else:
        fivefivegrid[curpoint[0]][curpoint[1]] = "o"
    
    #check endpoint
    if curpoint == [4,4]:
      resstring = teststring
      curpoint = [0,0]
      break
    
    if curpoint != [4,4]:
      curpoint = [0,0]
      teststring = []
      for alpha in oristring:
        teststring.append(alpha)
      optionbinlist = []
      fivefivegrid = []
      for i in range(5):
        fivefivegrid.append(["x","x","x","x","x"])
  return ("".join(resstring),fivefivegrid)



SW = 800
SH = 600
BW = 50
BH = 50

BLACK = (0,0,0)
WHITE = (255,255,255)

pg.font.init()
FONT = pg.font.Font(pg.font.get_default_font(),20)

pg.display.init()
Display = pg.display.set_mode((SW,SH))
pg.display.set_caption("Correct Path")

def main():

    inputstring = []
    corpath = ""

    #create the 5x5 grid
    fivefivegrid = []
    for i in range(5):
        fivefivegrid.append(["x","x","x","x","x"])
    
    ffgword = FONT.render("5 x 5 grid",True,WHITE)
    ffgwordRect = ffgword.get_rect()
    ffgwordRect.center = (SW/2,ffgword.get_rect().height*3)

    inputword = FONT.render("Input: ",True,WHITE)
    inputwordrect = inputword.get_rect()
    inputwordrect.center = (100,SH*2/3)

    corpathword = FONT.render("Correct Path: ", True,WHITE)
    corpathwordrect = corpathword.get_rect()
    corpathwordrect.center = (100,SH*2/3+inputwordrect.height*2)
    condition = True
    
    while (condition):
        Display.fill(BLACK)
        for event in pg.event.get():
            if(event.type == QUIT):
              pg.display.quit()
              sys.exit()
              condition = False
            elif (event.type == KEYDOWN):
                if (event.key == K_u or event.key == K_d or event.key == K_l or event.key == K_r or event.key == K_q):
                    if(event.key == K_q):
                        inputstring.append("?")
                    else:
                        inputstring.append(chr(event.key))
                elif(event.key == K_BACKSPACE):
                    if (len(inputstring) != 0):
                        inputstring.pop(len(inputstring)-1)
                elif(event.key == K_RETURN):
                        ans = CorrectPath("".join(inputstring))
                        corpath = ans[0]
                        fivefivegrid = ans[1]
                    
        for i in range(5):
            boxRect3 = pg.rect.Rect(SW/2 - BW/2,ffgword.get_rect().height*4 + BH*i,BW,BH)
            boxRect2 = pg.rect.Rect(boxRect3.left-BW,boxRect3.top,BW,BH)
            boxRect1 = pg.rect.Rect(boxRect3.left-2*BW,boxRect3.top,BW,BH)
            boxRect4 = pg.rect.Rect(boxRect3.left+BW,boxRect3.top,BW,BH)
            boxRect5 = pg.rect.Rect(boxRect3.left+2*BW,boxRect3.top,BW,BH)
            pg.draw.rect(Display,WHITE,boxRect3,2)
            pg.draw.rect(Display,WHITE,boxRect1,2)
            pg.draw.rect(Display,WHITE,boxRect2,2)
            pg.draw.rect(Display,WHITE,boxRect4,2)
            pg.draw.rect(Display,WHITE,boxRect5,2)

            #column3
            leRect = FONT.render(fivefivegrid[i][2],True,WHITE).get_rect()
            leRect.center = (SW/2, boxRect3.top + BH/2)
            Display.blit(FONT.render(fivefivegrid[i][2],True,WHITE),leRect)
            #column2
            leRect = FONT.render(fivefivegrid[i][1],True,WHITE).get_rect()
            leRect.center = (SW/2 - BW, boxRect3.top + BH/2)
            Display.blit(FONT.render(fivefivegrid[i][1],True,WHITE),leRect)
            #column1
            leRect = FONT.render(fivefivegrid[i][0],True,WHITE).get_rect()
            leRect.center = (SW/2 - 2*BW, boxRect3.top + BH/2)
            Display.blit(FONT.render(fivefivegrid[i][0],True,WHITE),leRect)
            #column4
            leRect = FONT.render(fivefivegrid[i][3],True,WHITE).get_rect()
            leRect.center = (SW/2 + BW, boxRect3.top + BH/2)
            Display.blit(FONT.render(fivefivegrid[i][3],True,WHITE),leRect)
            #column5
            leRect = FONT.render(fivefivegrid[i][4],True,WHITE).get_rect()
            leRect.center = (SW/2 + 2*BW, boxRect3.top + BH/2)
            Display.blit(FONT.render(fivefivegrid[i][4],True,WHITE),leRect)    
            
        Display.blit(ffgword,ffgwordRect)        
        Display.blit(inputword, inputwordrect)
        Display.blit(corpathword,corpathwordrect)
        Display.blit(FONT.render("".join(inputstring),True,WHITE),pg.Rect(inputwordrect.right,inputwordrect.top,FONT.render("".join(inputstring),True,WHITE).get_rect().width, FONT.render("".join(inputstring),True,WHITE).get_rect().height))
        Display.blit(FONT.render(corpath,True,WHITE),pg.Rect(corpathwordrect.right,corpathwordrect.top,FONT.render(corpath,True,WHITE).get_rect().width,FONT.render(corpath,True,WHITE).get_rect().height))
        pg.display.update()

main()
