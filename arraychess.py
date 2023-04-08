from numpy import chararray #Only importing chararray as numpy and queue both have put() functions
import time
import threading as thr
import queue as que
import struct as src

try:
    with open("chessconsoleaccts.dat", "r") as accts:
        pass
except FileNotFoundError:
    with open("chessconsoleaccts.dat", "w") as accts:
        pass

logcheck1 = 0
while logcheck1 == 0:
    user1ls = input("\nPlayer 1 (White), login or signup? ").lower()
    if user1ls == "login":
        account1 = 0
        while account1 == 0:
            print("\nPlayer 1 (White), input account details: ")
            user1 = input("Input Username (20 chars): ")
            pass1 = input("Input Password (20 chars): ")
            if (len(user1) > 20 or user1 == "") or (len(pass1) > 20 or pass1 == ""):
                print("\nLogin data invalid, returning to login or signup screen.")
                account1 = -1
                break
            with open("chessconsoleaccts.dat", "r") as accts:
                while True:
                    userpass = accts.read(55)
                    if not userpass:
                        break
                    if (user1.ljust(20).strip() == userpass[:20].strip()) and (pass1.ljust(20).strip() == userpass[20:40].strip()):
                        account1 = 1
                        break
            if account1 == 0:
                print("\nLogin data not in database, returning to login or signup screen.")
                account1 = -1
        if account1 == 1:
            logcheck1 = 1
    elif user1ls == "signup":
        account1 = 0
        while account1 == 0:
            print("\nPlayer 1 (White), input new account details: ")
            user1 = input("Input New Username (20 chars): ")
            pass1 = input("Input New Password (20 chars): ")
            if (len(user1) > 20 or user1 == "") or (len(pass1) > 20 or pass1 == ""):
                print("\nData invalid, returning to login or signup screen.")
                account1 = -1
                break
            with open("chessconsoleaccts.dat", "r") as accts:
                while True:
                    userpass = accts.read(40)
                    if not userpass:
                        account1 = 1
                        break
                    if (user1.ljust(20).strip() == userpass[:20].ljust(20).strip()):
                        account1 = 0
                        print("\nUsername already in use, please input again. ")
                        break
        if account1 == 1:
            with open("chessconsoleaccts.dat", "a") as accts:
                    accts.write(user1.ljust(20)+pass1.ljust(20)+"".ljust(15))
            logcheck1 = 1
    else:
        print("\nInvalid command. Input again.")
print("")

logcheck2 = 0
while logcheck2 == 0:
    user2ls = input("\nPlayer 2 (Black), login or signup? ").lower()
    if user2ls == "login":
        account2 = 0
        while account2 == 0:
            print("\nPlayer 2 (Black), input account details: ")
            user2 = input("Input Username (20 chars): ")
            pass2 = input("Input Password (20 chars): ")
            if (len(user2) > 20 or user2 == "") or (len(pass2) > 20 or pass2 == ""):
                print("\nLogin data invalid, returning to login or signup screen.")
                account2 = -1
                break
            with open("chessconsoleaccts.dat", "r") as accts:
                while True:
                    userpass = accts.read(55)
                    if not userpass:
                        break
                    if (user2.ljust(20).strip() == userpass[:20].strip()) and (pass2.ljust(20).strip() == userpass[20:40].strip()):
                        account2 = 1
                        break
            if account2 == 0:
                print("\nLogin data not in database, returning to login or signup screen.")
                account2 = -1
        if account2 == 1:
            logcheck2 = 1
    elif user2ls == "signup":
        account2 = 0
        while account2 == 0:
            print("\nPlayer 2 (Black), input new account details: ")
            user2 = input("Input New Username (20 chars): ")
            pass2 = input("Input New Password (20 chars): ")
            if (len(user2) > 20 or user2 == "") or (len(pass2) > 20 or pass2 == ""):
                print("\nData invalid, returning to login or signup screen.")
                account2 = -1
                break
            with open("chessconsoleaccts.dat", "r") as accts:
                while True:
                    userpass = accts.read(40)
                    if not userpass:
                        account2 = 1
                        break
                    if (user2.ljust(20).strip() == userpass[:20].ljust(20).strip()):
                        account2 = 0
                        print("\nUsername already in use, please input again. ")
                        break
        if account2 == 1:
            with open("chessconsoleaccts.dat", "a") as accts:
                    accts.write(user2.ljust(20)+pass2.ljust(20)+"".ljust(15))
            logcheck2 = 1
    else:
        print("\nInvalid command. Input again.")
print("")

print(f"\nWelcome, {user1} and {user2}!\n")

def startchess():
    
    chesslist = ["\u265C","\u265E","\u265D","\u265B","\u265A","\u265D","\u265E","\u265C", 
                 "\u265F","\u265F","\u265F","\u265F","\u265F","\u265F","\u265F","\u265F", 
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u2659","\u2659","\u2659","\u2659","\u2659","\u2659","\u2659","\u2659", 
                 "\u2656","\u2658","\u2657","\u2655","\u2654","\u2657","\u2658","\u2656"]
    notation = ["a1","a2","a3","a4","a5","a6","a7","a8","b1","b2","b3","b4","b5","b6","b7","b8",
                "c1","c2","c3","c4","c5","c6","c7","c8","d1","d2","d3","d4","d5","d6","d7","d8",
                "e1","e2","e3","e4","e5","e6","e7","e8","f1","f2","f3","f4","f5","f6","f7","f8",
                "g1","g2","g3","g4","g5","g6","g7","g8","h1","h2","h3","h4","h5","h6","h7","h8",
                "draw","resign"]
    chessdict = {"sus" : "bam"}
    
    chesstimew = 600
    chesstimeb = 600
    
    print("Possible moves: \n", notation)
    time.sleep(1)
    
    while True:
        count = 1 #move count
        
        #White's move
        if count%2 == 1:
            print(f"\n{user1}'s Turn (White)")
            print(board(chesslist))
            imove, fmove = " ", " "
            while imove not in notation or fmove not in notation:
                chesstime = chesstimew
                move = thr.Event()
                remtime = que.Queue()
                result = que.Queue()
                timerthread = thr.Thread(target = timer, args = (remtime, chesstime, move))
                movethread = thr.Thread(target = moveinput, args = (result, move,))

                timerthread.start()
                movethread.start()

                movethread.join()
                timerthread.join()

                moves = result.get()
                chesstimew = remtime.get()
                imove = moves[0].lower()
                fmove = moves[1].lower()
                if imove == "resign" or fmove == "resign":
                    return "\nBlack wins!"
                if imove == "draw" or fmove == "draw":
                    confirmw = input("Does White confirm the draw? (Y or N) ").lower()
                    confirmb = input("Does Black confirm the draw? (Y or N) ").lower()
                    if confirmw == "y" and confirmb == "y":
                        return "\nDraw!"
                    else:
                        print("Continuing game...")
                        imove, fmove = " ", " "
                if imove == None and fmove == None:
                    print("Input move")
                elif imove not in notation or fmove not in notation:
                    print("Input not a valid move")
                elif chessmovew(imove, fmove, board(chesslist)) == 1:
                    chesslist[listcheck(fmove)], chesslist[listcheck(imove)] = chesslist[listcheck(imove)], "\u3164"
                    break
                else:
                    print("Invalid Move, input again")
                    imove, fmove = " ", " "
            print("Move",count,":",imove,"to",fmove,"(White)")
            if "\u265A" not in chesslist:
                print("\nWhite wins! (Black's King was captured)")
                break
            if chesstimew == 0:
                print("\nBlack wins! (White ran out of time)")
                break
            count = count + 1   
            
        #Black's move
        if count%2 == 0:
            print(f"\n{user2}'s Turn (Black)")
            print(board(chesslist))
            imove, fmove = " ", " "
            while imove not in notation or fmove not in notation:
                chesstime = chesstimeb
                move = thr.Event()
                remtime = que.Queue()
                result = que.Queue()
                timerthread = thr.Thread(target = timer, args = (remtime, chesstime, move))
                movethread = thr.Thread(target = moveinput, args = (result, move,))

                timerthread.start()
                movethread.start()

                movethread.join()
                timerthread.join()

                moves = result.get()
                chesstimeb = remtime.get()
                imove = moves[0].lower()
                fmove = moves[1].lower()
                if imove == "resign" or fmove == "resign":
                    return "\nWhite wins!"
                if imove == "draw" or fmove == "draw":
                    confirmb = input("Does Black confirm the draw? (Y or N) ").lower()
                    confirmw = input("Does White confirm the draw? (Y or N) ").lower()
                    if confirmb == "y" and confirmw == "y":
                        return "\nDraw!"
                    else:
                        print("Continuing game...")
                        imove, fmove = " ", " "
                if imove == None and fmove == None:
                    print("Input move")
                elif imove not in notation or fmove not in notation:
                    print("Input not a valid move")
                elif chessmoveb(imove, fmove, board(chesslist)) == 1:
                    chesslist[listcheck(fmove)], chesslist[listcheck(imove)] = chesslist[listcheck(imove)], "\u3164"
                    break
                else:
                    print("Invalid Move, input again")
                    imove, fmove = " ", " "
            print("Move",count,":",imove,"to",fmove,"(Black)")
            if "\u2654" not in chesslist:
                print("\nBlack wins! (White's King was captured)")
                break
            if chesstimeb == 0:
                print("\nWhite wins! (Black ran out of time)")
                break
            count = count + 1 
            
    print("")
    return board(chesslist)
            
def chessmovew(initial, final, lst):
    white = ["\u2656","\u2658","\u2657","\u2655","\u2654","\u2659"]
    cbt = lst
    intloc = location(initial)
    finloc = location(final)
    movelist = []
    if cbt[intloc[0],intloc[1]] == "\u3164":
        print("Initial location does not contain chesspiece")
        return 0
    if cbt[intloc[0],intloc[1]] not in white:
        print("Initial location contains enemy piece")
        return 0
    if initial == final:
        print("Cannot move to same locations")
        return 0
    if cbt[finloc[0],finloc[1]] in white:
        print("Move attacks own piece")
        return 0
    if cbt[intloc[0],intloc[1]] == "\u2656":
        for xy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    movelist.append(location((x,y)))
                elif cbt[x,y] not in white:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u2658":
        for xy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in white:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u2657":
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    movelist.append(location((x,y)))
                elif cbt[x,y] not in white:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u2655":
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    movelist.append(location((x,y)))
                elif cbt[x,y] not in white:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u2654":
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in white:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u2659":
        x = intloc[0]
        y = intloc[1]
        if (cbt[x-1,y] == "\u3164") and (0<=(x-1)<=7 and 1<=y<=8):
            movelist.append(location((x-1,y)))
        if (cbt[x-1,y-1] not in white+["\u3164"]) and (0<=(x-1)<=7 and 1<=(y-1)<=8):
            movelist.append(location((x-1,y-1)))
        if (cbt[x-1,y+1] not in white+["\u3164"]) and (0<=(x-1)<=7 and 1<=(y+1)<=8):
            movelist.append(location((x-1,y+1)))
    if final in movelist:
        return 1
    else:
        return 0

def chessmoveb(initial, final, lst):
    black = ["\u265C","\u265E","\u265D","\u265B","\u265A","\u265F"]
    cbt = lst
    intloc = location(initial)
    finloc = location(final)
    movelist = []
    if cbt[intloc[0],intloc[1]] == "\u3164":
        print("Initial location does not contain chesspiece")
        return 0
    if cbt[intloc[0],intloc[1]] not in black:
        print("Initial location contains enemy piece")
        return 0
    if initial == final:
        print("Cannot move to same locations")
        return 0
    if cbt[finloc[0],finloc[1]] in black:
        print("Move attacks own piece")
        return 0
    if cbt[intloc[0],intloc[1]] == "\u265C":
        for xy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    movelist.append(location((x,y)))
                elif cbt[x,y] not in black:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u265E":
        for xy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in black:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u265D":
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    movelist.append(location((x,y)))
                elif cbt[x,y] not in black:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u265B":
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    movelist.append(location((x,y)))
                elif cbt[x,y] not in black:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u265A":
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
            x = intloc[0]
            y = intloc[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in black:
                    movelist.append(location((x,y)))
                    break
                else:
                    break
    if cbt[intloc[0],intloc[1]] == "\u265F":
        x = intloc[0]
        y = intloc[1]
        if (cbt[x+1,y] == "\u3164") and (0<=(x+1)<=7 and 1<=y<=8):
            movelist.append(location((x+1,y)))
        if (cbt[x+1,y-1] not in black+["\u3164"]) and (0<=(x+1)<=7 and 1<=(y-1)<=8):
            movelist.append(location((x+1,y-1)))
        if (cbt[x+1,y+1] not in black+["\u3164"]) and (0<=(x+1)<=7 and 1<=(y+1)<=8):
            movelist.append(location((x+1,y+1)))
    if final in movelist:
        return 1
    else:
        return 0
    
def location(moveinput):
    notationboard = ["a8","b8","c8","d8","e8","f8","g8","h8",
                     "a7","b7","c7","d7","e7","f7","g7","h7",
                     "a6","b6","c6","d6","e6","f6","g6","h6",
                     "a5","b5","c5","d5","e5","f5","g5","h5",
                     "a4","b4","c4","d4","e4","f4","g4","h4",
                     "a3","b3","c3","d3","e3","f3","g3","h3",
                     "a2","b2","c2","d2","e2","f2","g2","h2",
                     "a1","b1","c1","d1","e1","f1","g1","h1"]
    notationarray = chararray((9,9), itemsize=2, unicode=True)
    notationarray[:8,0] = ["8","7","6","5","4","3","2","1"]
    notationarray[0,1:] = notationboard[0:8]
    notationarray[1,1:] = notationboard[8:16]
    notationarray[2,1:] = notationboard[16:24]
    notationarray[3,1:] = notationboard[24:32]
    notationarray[4,1:] = notationboard[32:40]
    notationarray[5,1:] = notationboard[40:48]
    notationarray[6,1:] = notationboard[48:56]
    notationarray[7,1:] = notationboard[56:64]
    notationarray[8,:] = ["-","a"," b"," c"," d"," e"," f"," g","h "]

    if type(moveinput) is str:
        x = 0
        while x<9:
            y = 0
            while y<9:
                if notationarray[x,y] == moveinput:
                     return (x, y)
                y+=1
            x+=1
    if type(moveinput) is tuple:
        return notationarray[moveinput[0], moveinput[1]]
        
def listcheck(move):
    notationboard = ["a8","b8","c8","d8","e8","f8","g8","h8",
                     "a7","b7","c7","d7","e7","f7","g7","h7",
                     "a6","b6","c6","d6","e6","f6","g6","h6",
                     "a5","b5","c5","d5","e5","f5","g5","h5",
                     "a4","b4","c4","d4","e4","f4","g4","h4",
                     "a3","b3","c3","d3","e3","f3","g3","h3",
                     "a2","b2","c2","d2","e2","f2","g2","h2",
                     "a1","b1","c1","d1","e1","f1","g1","h1"]
    for x in range(len(notationboard)):
        if move == notationboard[x]:
            return x
    return
    
def timer(remtime, chesstime, move):
    mins, secs = divmod(chesstime, 60)
    clock = "{:02d}:{:02d}".format(mins, secs)
    print(clock, end="\r")
    time.sleep(5)
    while chesstime>0 and not move.is_set():
        mins, secs = divmod(chesstime, 60)
        clock = "{:02d}:{:02d}".format(mins, secs)
        print(clock, end="\r")
        time.sleep(1)
        chesstime-=1
    mins, secs = divmod(chesstime, 60)
    clock = "{:02d}:{:02d}".format(mins, secs)
    print(clock)
    remtime.put(int(chesstime))
    return

def moveinput(result, move):
    move1 = input("Input location of piece you want to move: ").lower()
    move2 = input("Input location of where you want your piece to move: ").lower()
    move.set()
    result.put(tuple([move1, move2]))
    return

def board(clist):
    chessboard = chararray((9,9), itemsize=2, unicode=True)
    chessboard[:8,0] = ["8","7","6","5","4","3","2","1"]
    chessboard[0,1:] = clist[0:8]
    chessboard[1,1:] = clist[8:16]
    chessboard[2,1:] = clist[16:24]
    chessboard[3,1:] = clist[24:32]
    chessboard[4,1:] = clist[32:40]
    chessboard[5,1:] = clist[40:48]
    chessboard[6,1:] = clist[48:56]
    chessboard[7,1:] = clist[56:64]
    chessboard[8,:] = ["-","a"," b"," c"," d"," e"," f"," g","h "]
    return chessboard
    
print(startchess())
