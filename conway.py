import sys, os, time, getch, copy, time

print("\u001b[44m\x1b[?25l")

board, tBoard, toDraw, base = [], [], [], []
selectedX, selectedY = 0, 0
moves, speed = 0, 0.5

directory = os.path.dirname(os.path.realpath(__file__))

recentlySaved = True

f = open(directory+"/default_var.txt","r")
lang, defLang = f.read().replace("\n",""), f.read().replace("\n","")
f.close()

f = open(directory+"/default_width.txt","r")
width = int(f.read())
f.close()

f = open(directory+"/default_height.txt","r")
height = int(f.read())
f.close()

f = open(directory+"/variants.txt", "r")
variants = []
for row in f:
    variants.append(str(row.replace("\n","")))
f.close()

f = open(directory+"/born.txt", "r")
born = []
for row in f:
    born.append(str(row.replace("\n","")))
f.close()

f = open(directory+"/survive.txt", "r")
survive = []
for row in f:
    survive.append(str(row.replace("\n","")))
f.close()

indent, name = str(" "*((os.get_terminal_size()[0] - (width+42))//2)), ""

menuToDraw = []

alphabet = ["1","2","3","4","5","6","7","8","9","0","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m","."," ",]

def bar():
    print("\u001b[46m\u001b[4mF\u001b[0m\u001b[46mile  \u001b[4mG\u001b[0m\u001b[46mo  \u001b[4mA\u001b[0m\u001b[46mpp  \u001b[46m\u001b[4mV\u001b[0m\u001b[46mariants  \u001b[46m\u001b[4mS\u001b[0m\u001b[46mettings"+" "*(os.get_terminal_size()[0]-33)+"\u001b[0m\u001b[44m")

def saveas():
    name = getImp("File name:")
    f = open(directory+"/Files/"+name+".txt","w")
    f.close()
    f = open(directory+"/Files/"+name+".txt","r+")
    f.write(lang)
    for i in range(len(base)): f.write((f.read())+"\n"+"".join(base[i]))
    f.close()

def clamp(a, min, max):
    if a < min+1: a = (min)
    elif a > max-1: a = (max)
    return a 

def drawBoard():
    time.sleep(0.03)
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height+5, cols=(width*2)+34))
    print("\u001b[44m\x1b[?25l")
    side = [
    "┌─────────────────────────┐",
    "│ X:"+str(selectedX+1)+" Y:"+str(height-selectedY)+(" "*(4-(len(str(selectedX+1))+len(str(height-selectedY)))))+"               │",
    "│ WIDTH "+str(width)+" HEIGHT "+str(height)+(" "*(10-(len(str(width))+len(str(height)))))+"│",
    "│ STEPS: "+str(moves)+(" "*(4-len(str(moves))))+"             │",
    "│ SPEED: "+str(round(10-speed,2))+(" "*(4-len(str(round(10-speed,2)))))+"             │",
    "└─────────────────────────┘",
    "┌─────────────────────────┐",
    "│ \u001b[1mARROWS\u001b[0m\u001b[44m                  │",
    "│ MOVE CURSOR             │",
    "│                         │",
    "│ \u001b[1mSPACE\u001b[0m\u001b[44m                   │",
    "│ PLACE TILE              │",
    "│                         │",
    "│ \u001b[1mR\u001b[0m\u001b[44m                       │",
    "│ NEXT SCENE              │",
    "│                         │",
    "│ \u001b[1mC\u001b[0m\u001b[44m                       │",
    "│ CLEAR                   │",
    "│                         │",
    "│ \u001b[1mP\u001b[0m\u001b[44m                       │",
    "│ RUN SIMULATION          │",
    "│                         │",
    "│ \u001b[1m^C\u001b[0m\u001b[44m                      │",
    "│ STOP SIMULATION         │",
    "│                         │",
    "│ \u001b[1m+\u001b[0m\u001b[44m\u001b[1m-\u001b[0m\u001b[44m                      │",
    "│ CHANGE SIM SPEED        │",
    "└─────────────────────────┘",
    "┌─────────────────────────┐",
    "│ © RONAN UNDERWOOD 2020  │",
    "└─────────────────────────┘"
    ]
    os.system("clear")
    bar()
    global toDraw
    toDraw = []
    for i in range(0, ((os.get_terminal_size()[1]-height)//2)-2):
        toDraw.append("")
    for y in range(len(base)):
        for x in range(len(base[y])):
            try:
                if selectedX == x and selectedY == y and not base[y][x] == "▓▓": board[y][x] = "▒▒"
                elif not base[y][x] == "▓▓": board[y][x] = "░░"
                else: board[y][x] = "▓▓"
            except: pass
    toDraw.append("┌"+str("──"*(int(width)+1))+"┐  "+side[0])
    for i in range(len(board)):
        try: toDraw.append("│ "+"".join(board[i])+" │  " + side[i+1])
        except: toDraw.append("│ "+"".join(board[i])+" │  ")
    toDraw.append("└"+str("──"*(int(width)+1))+"┘ ")
    print("\n".join(toDraw))
    return toDraw

def multiLang(grow, survive, count):
    if count in grow: return 1
    elif not count in survive: return 0
    else: return "none"

def update():
    tBoard = copy.deepcopy(base)
    for y in range(len(base)):
        for x in range(len(base[y])):
            if base[y][x] == "\u001b[34;1m░░\u001b[0m": base[y][x] = "░░"
            count = 0
            for radary in range(y-1, y+2):
                row = []
                for radarx in range(x-1, x+2):
                    try:
                        if base[radary][radarx] == "▓▓": count += 1
                        if radary == y and radarx == x: row.append("O")
                        else: row.append(base[radary][radarx])
                    except: pass
                # print(*row)
            if base[y][x] == "▓▓": 
                count -= 1
                # print(count)
            # print(count)
            bornMulti = [int(x) for x in str(born[variants.index(lang)])] 
            surviveMulti = [int(x) for x in str(survive[variants.index(lang)])] 
            num = multiLang(bornMulti, surviveMulti, count)
            if num == 1: tBoard[y][x] = "▓▓"
            elif num == 0: tBoard[y][x] = "░░"
    for i in range(len(base)):
        for j in range(len(base[i])):
            base[i][j] = tBoard[i][j]

def init(var):
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append("░░")
        var.append(list(row))
    return var

def drawBox(text, optionsBase):
    selected = 0
    for i in range(len(text)):
        if len(text[i]) % 2 != 0: text[i] = text[i]+" "
    if len(str(optionsBase)) % 2 == 0: add = " "
    else: add = ""
    while True:
        options = optionsBase.copy()
        for i in range(len(options)):
            if i == selected: options[i] = "\u001b[46m "+options[i]+" \u001b[0m\u001b[44m"
            else: options[i] = str(options[i]).replace("\u001b[46m ","").replace(" u001b[0m\u001b[44m","")
        os.system("clear")
        for i in range(0, ((os.get_terminal_size()[1]-len(text))//2)-2): print()
        print("┌────────────────────────────────────┐".center(os.get_terminal_size()[0]))
        for i in range(len(text)):
            print(str("│"+(" "*(((36)-len(text[i]))//2))+text[i]+" "*(((36)-len(text[i]))//2)+"│").center(os.get_terminal_size()[0]))
        print("│                                    │".center(os.get_terminal_size()[0]))
        print(str("               │"+(" "*(((33)-len("  ".join(optionsBase)))//2))+"  ".join(options)+" "*(((33)-len("  ".join(optionsBase)))//2)+add+" │").center(os.get_terminal_size()[0]))
        print("└────────────────────────────────────┘".center(os.get_terminal_size()[0]))
        while True:
            key = getch.getch()
            if key == "C":
                selected += 1
                break
            elif key == "D": 
                selected -= 1
                break
            elif key == "x":
                return "keyout"
            elif key == " ": return options[selected].replace("\u001b[46m ","").replace(" u001b[0m\u001b[44m","").strip()
        if selected >= len(options): selected = 0
        elif selected <= -1: selected = len(options)-1
        time.sleep(0.01)

def drawMenu(trigger, optionsBase, indent):
    selected = 0
    while True:
        menuToDraw = []
        options = optionsBase.copy()
        for i in range(len(options)):
            if i == selected:
                options[i] = "\u001b[46m "+options[i]+" \u001b[0m\u001b[44m"
            else:
                options[i] = str(options[i]).replace("\u001b[46m ","").replace(" u001b[0m\u001b[44m","")
        toDraw = drawBoard()
        os.system("clear")
        bar()

        menuToDraw.append(indent+"┌─▲────────────────────────┐")
        for i in range(len(options)):
            if i == selected: menuToDraw.append(indent+str("│ "+options[i]+str(" "*(23-len(optionsBase[i])))+"│"))
            else: menuToDraw.append(indent+str("│ "+options[i]+str(" "*(25-len(optionsBase[i])))+"│"))
        menuToDraw.append(indent+"└──────────────────────────┘")

        for i in range(len(toDraw)):
            for j in range(len(toDraw[i])):
                try:
                    if i <= len(menuToDraw) and j <= len(menuToDraw[i]) and j >= len(indent):
                        toDraw[i] = list(toDraw[i])
                        menuToDraw[i] = list(menuToDraw[i])
                        try:
                            toDraw[i][j] = menuToDraw[i][j]
                        except:
                            toDraw[i][j] = toDraw[i][j]
                        toDraw[i] = str("".join(toDraw[i]))
                except: pass
        toDraw[selected+1] = str(toDraw[selected+1].replace(" │  │","░░░░░░░░░░░░░░ │  │"))
        toDraw[selected+1] = str(toDraw[selected+1].replace(" │  └","░░░░░░░░░░░░░░ │  └"))
        toDraw[selected+1] = str(toDraw[selected+1].replace(" │  ┌","░░░░░░░░░░░░░░ │  ┌"))
        toDraw2 = toDraw.copy()
        print("\n".join(toDraw2))
        while True:
            key = getch.getch()
            if key == "B":
                selected += 1
                break
            elif key == "A": 
                selected -= 1
                break
            elif key == " ": return options[selected].replace("\u001b[46m ","").replace(" u001b[0m\u001b[44m","").strip()
            elif key == trigger: return "keyout"
        if selected >= len(options): selected = 0
        elif selected <= -1: selected = len(options)-1
        time.sleep(0.01)

def terminate():
    quitTrue = drawBox(["Are you sure you","want to quit? "],["<yes>","<no>"])
    print(quitTrue)
    if "<yes>" in quitTrue:
        os.system("clear")
        quit()

def bootup(): drawBox(["Automata","Version 0.9","Created by Ronan Underwood","","Created","in memory of John Conway"],["<close>"])

def contact(): drawBox(["Contact us at","ronan.underwood@icloud.com","for bug and issue reports"],["okay"])

def raiseError(): drawBox(["An error ocurred"],["okay"])

def getImp(prompt):
    imp = []
    while True:
        try:
            os.system("clear")
            bar()
            if len(imp) % 2 != 0: add = " "
            else: add = ""
            for _ in range(0, ((os.get_terminal_size()[1]-3)//2)-2): print()
            print("┌────────────────────────────────────┐".center(os.get_terminal_size()[0]))
            print(str("│"+(" "*(((36)-len(prompt))//2))+prompt+" "*(((36)-len(prompt))//2)+"│").center(os.get_terminal_size()[0]))
            print(str("│"+(" "*(((36)-len("".join(imp)+add))//2))+"".join(imp)+add+" "*(((36)-len("".join(imp)+add))//2)+"│").center(os.get_terminal_size()[0]))
            print("│                                    │".center(os.get_terminal_size()[0]))
            print("└────────────────────────────────────┘".center(os.get_terminal_size()[0]))
            key = getch.getch()
            if key == "C": return str("".join(imp))
            elif key == "D":
                try: imp.pop()
                except: pass
            elif key.lower() in alphabet: imp.append(key)
            imp = imp[:36]
            time.sleep(0.01)
        except:
            raiseError()
            imp = []

def savedPrompt():
    if recentlySaved == False:
        ans = drawBox(["Save file"],["<no>","<yes>"])
        if "<yes>" in ans: saveas()

init(base)
board = copy.deepcopy(base)

bootup()

toDraw = drawBoard()

while True:
    selectedX = clamp(selectedX, 0, width-1)
    selectedY = clamp(selectedY, 0, height-1)
    toDraw = drawBoard()
    key = getch.getch()
    if   key == "A": selectedY -= 1
    elif key == "B": selectedY += 1
    elif key == "C": selectedX += 1
    elif key == "D": selectedX -= 1
    elif key == " ":
        if base[selectedY][selectedX] == "▓▓": base[selectedY][selectedX] = "░░"
        else: base[selectedY][selectedX] = "▓▓"
        moves = 0
        recentlySaved = False
    elif key == "r":
        update()
        moves += 1
        recentlySaved = False
    elif key == "c":
        savedPrompt()
        base = []
        init(base)
        moves = 0
        recentlySaved = True
    elif key == "p":
        while True:
            try:
                t0 = time.time()
                update()
                toDraw = drawBoard()
                moves += 1
                t1 = time.time()
                time.sleep(speed-(t1-t0))
            except:
                break
        recentlySaved = False
    elif key == "=":
        speed = round(speed-0.1,2)
        if speed < 0: speed = 0
    elif key == "-":
        speed = round(speed+0.1,2)
        if speed > 9.9: speed = 9.9
    elif key == "q":
        savedPrompt()
        terminate()
    elif key == "a":
        selection = drawMenu(str(key),["ABOUT","CONTACT","QUIT"],"        ")
        if "ABOUT" in selection: bootup()
        elif "CONTACT" in selection: contact()
        elif "QUIT" in selection: 
            savedPrompt()
            terminate()
        elif not "keyout" in selection: raiseError()
    elif key == "g":
        selection = drawMenu(str(key),["PLACE TILE","NEXT SCENE","CLEAR","RUN","INCREASE SPEED","DECREASE SPEED"],"    ")
        if "PLACE TILE" in selection: 
            if base[selectedY][selectedX] == "▓▓": base[selectedY][selectedX] = "░░"
            else: base[selectedY][selectedX] = "▓▓"
            moves = 0
            recentlySaved = False
        elif "NEXT SCENE" in selection:
            update()
            moves += 1
            recentlySaved = False
        elif "CLEAR" in selection:
            savedPrompt()
            base = []
            init(base)
            moves = 0
            recentlySaved = True
        elif "RUN" in selection:
            while True:
                try:
                    t0 = time.time()
                    update()
                    toDraw = drawBoard()
                    moves += 1
                    t1 = time.time()
                    time.sleep(speed-(t1-t0))
                except:
                    break
            recentlySaved = False
        elif "INCREASE SPEED" in selection:
            speed = round(speed-0.1,2)
            if speed < 0: speed = 0
        elif "DECREASE SPEED" in selection:
            speed = round(speed+0.1,2)
            if speed > 9.9: speed = 9.9
        # elif not "keyout" in selection: raiseError()
    elif key == "f":
        selection = drawMenu(str(key),["NEW","SAVE FILE","LOAD","DUPLICATE","DELETE"],"")
        if "NEW" in selection:
            savedPrompt()
            output = drawMenu("f",["30x30","40x40","50x50","70x70","100x100"],"")
            if not output == "keyout":
                tLang = drawMenu("f",variants,"").replace(" \x1b[0m\x1b[44m","")
                if not tLang == "keyout":
                    lang = tLang
                    width = int(output.split("x")[0].replace(" \x1b[0m\x1b[44m",""))
                    height = int(output.split("x")[1].replace(" \x1b[0m\x1b[44m",""))
                    base, board, tBoard = [], [], []
                    base = init(base)
                    board = init(board)
                    tBoard = init(tBoard)
                    moves = 0
                    recentlySaved = False
                    bar()
                    toDraw = drawBoard()
        if "SAVE FILE" in selection: 
            saveas()
            recentlySaved = True
        elif "DUPLICATE" in selection:
            savedPrompt()
            name = getImp("File name:")
            f = open(directory+"/Files/"+name+".txt","w")
            f.close()
            f = open(directory+"/Files/"+name+".txt","r+")
            for i in range(len(base)): f.write((f.read())+"\n"+"".join(base[i]))
            f.close()
            recentlySaved = True
        elif "DELETE" in selection:
            inp = drawBox(["Delete file?"],["<no>","<yes>"])
            if "<yes>" in inp:
                try:
                    recentlySaved = False
                    os.remove(directory+"/Files/"+name+".txt")
                except:
                    drawBox(["You have no file open"],["<okay>"])
        elif "LOAD" in selection:
            savedPrompt()
            name = getImp("File name:")
            try:
                base, base2 = [], []
                moves = 0
                with open(directory+"/Files/"+name+".txt","r") as f: 
                    for line in f: base2.append(line.replace("\n",""))
                lang = base2[0].strip()
                del base2[0]
                for i in range(len(base2)):
                    row = []
                    for j in range(len(base2[i])//2):
                        strBase = ""
                        for k in range(0, 2):
                            strBase = strBase+base2[i][(j*2)+k]
                        row.append(strBase)
                    base.append(list(row))
                height, width = len(base)-1, (len(base[0]))
                board = copy.deepcopy(base)
                tBoard = copy.deepcopy(base)
                recentlySaved = True
                toDraw = drawBoard()
            except FileNotFoundError:
                drawBox(["File not found"],["<okay>"])
    elif key == "v":
        outputVariants = variants.copy()
        outputVariants.append("ADD")
        selection = str(drawMenu(str(key),outputVariants,"             ")).strip()
        if "ADD" in selection:
            vName = getImp("Variant name: ")
            vBorn = getImp("Born numbers :")
            vSurvive = getImp("Survive numbers:")

            f = open(directory+"/variants.txt", "w")
            variants.append(vName)
            f.write("\n".join(variants))
            f.close()

            f = open(directory+"/born.txt", "w")
            born.append(vBorn)
            f.write("\n".join(born))
            f.close()

            f = open(directory+"/survive.txt", "w")
            survive.append(vSurvive)
            f.write("\n".join(survive))
            f.close()

        elif not "keyout" in selection:
            result = drawBox(["Delete variant?"],["<no>","<yes>"])
            if "<yes>" in result:
                for i in range(len(variants)):
                    if variants[i] in selection: selection = variants[i]

                if lang == selection: 
                    savedPrompt()
                    base = []
                    init(base)
                    moves = 0
                    recentlySaved = True

                del born[variants.index(selection)]
                del survive[variants.index(selection)]
                del variants[variants.index(selection)]

                f = open(directory+"/variants.txt", "w")
                f.write("\n".join(variants))
                f.close()

                f = open(directory+"/born.txt", "w")
                f.write("\n".join(born))
                f.close()

                f = open(directory+"/survive.txt", "w")
                f.write("\n".join(survive))
                f.close()

    elif key == "s":
        selection = str(drawMenu(str(key),["DEFAULT SPEED","DEFAULT SIZE","DEFAULT VARIANT"],"                       ")).strip()

        if "DEFAULT VARIANT" in selection:
            dfv = drawMenu(str(key),variants,"                       ").replace(" \x1b[0m\x1b[44m","")
            f = open(directory+"/default_var.txt","w")
            f.write(dfv)
            f.close()
            lang, defLang = dfv, dfv
            f.close()

        elif "DEFAULT SPEED" in selection:
            nds = getImp("New default speed:")
            if (nds.replace(".","")).isnumeric():
                speed = 10 - float(nds)
                if speed > 9.9 or speed < 0: drawBox(["Please enter a value","from 0 to 9.9"],["<okay>"])
                else:
                    f = open(directory+"/default_speed.txt","w")
                    f.write(str(speed))
                    f.close()
            else: drawBox(["Please enter a number"],["<okay>"])

        elif "DEFAULT SIZE" in selection:
            output = drawMenu("[none]",["30x30","40x40","50x50","70x70","100x100"],"                       ")
            width = int(output.split("x")[0].replace(" \x1b[0m\x1b[44m",""))
            height = int(output.split("x")[1].replace(" \x1b[0m\x1b[44m",""))
            f = open(directory+"/default_width.txt","w")
            f.write(str(width))
            f.close()
            f = open(directory+"/default_height.txt","w")
            f.write(str(height))
            f.close()
