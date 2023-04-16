from numpy import chararray #Only importing chararray as numpy and queue both have put() functions
import time
import threading as thr
import queue as que
import getpass as gp

def startchess():
    
    user1, user2 = login()
    
    startinput = ""
    startcommands = ["start", "end", "leaderboard"]
    print("Commands: \n", startcommands)
    while True:
        while startinput not in startcommands:
            startinput = input("\nInput Command: ").lower()
            print("")
            if startinput not in startcommands:
                print("Invalid command, input again")
        if startinput == "start":
            break
        if startinput == "leaderboard":
            updateleaderboard(user1, 0, 0, 0, user2, 0, 0, 0)
            startinput = ""
        if startinput == "end":
            print("\n")
            return "-END-"
    
    chesslist = ["\u265C","\u265E","\u265D","\u265B","\u265A","\u265D","\u265E","\u265C", 
                 "\u265F","\u265F","\u265F","\u265F","\u265F","\u265F","\u265F","\u265F", 
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164","\u3164",
                 "\u2659","\u2659","\u2659","\u2659","\u2659","\u2659","\u2659","\u2659", 
                 "\u2656","\u2658","\u2657","\u2655","\u2654","\u2657","\u2658","\u2656"]
    chesslistlegacy = chesslist
    notation = ["a1","a2","a3","a4","a5","a6","a7","a8","b1","b2","b3","b4","b5","b6","b7","b8",
                "c1","c2","c3","c4","c5","c6","c7","c8","d1","d2","d3","d4","d5","d6","d7","d8",
                "e1","e2","e3","e4","e5","e6","e7","e8","f1","f2","f3","f4","f5","f6","f7","f8",
                "g1","g2","g3","g4","g5","g6","g7","g8","h1","h2","h3","h4","h5","h6","h7","h8",
                "shortcastlewhite","longcastlewhite","shortcastleblack","longcastleblack",
                "draw","resign"]

    chessmoves = {}
    for x in range(64):
        chessmoves[notation[x]] = 0
    
    chesstimew = 600
    chesstimeb = 600
    count = 1    #move count
    print("Possible moves: \n", notation)
    print("\n*PS: For moves using normal chess notation (e.g. e2 to e4), please type them in the format 'move1,move2' (e.g. e2,e4).")
    time.sleep(1)
    
    while True:        
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
                if "," in moves:
                    moves = moves.split(",")
                    moves = tuple([moves[0], moves[1]])
                else:
                    moves = tuple([moves, moves])
                imove = moves[0].lower()
                fmove = moves[1].lower()
                
                if matecheck(chesslist, board(chesslist), color="white")[2] == 0:
                    validinitial = notation
                    validfinal = notation
                if matecheck(chesslist, board(chesslist), color="white")[2] == 1:
                    validinitial = notation[:64]+notation[-2:] 
                    validfinal = notation[:64]+notation[-2:]  
                if imove == None and fmove == None:
                    print("Input move")
                elif imove not in validinitial or fmove not in validfinal:
                    print("Invalid, input again")
                    imove, fmove = " ", " "
                elif imove == "resign" and fmove == "resign":
                    print("\nBlack wins! (White has resigned)")
                    updateleaderboard(user1, 0, 1, 0, user2, 1, 0, 0)
                    print("\nFinal Board:\n")
                    print(board(chesslist))
                    print("\n")
                    return "-END-"
                elif imove == "draw" and fmove == "draw":
                    confirmw = input("Does White confirm the draw (Y or N)?  ").lower()
                    confirmb = input("Does Black confirm the draw (Y or N)?  ").lower()
                    if confirmw == "y" and confirmb == "y":
                        print("\nDraw!")
                        updateleaderboard(user1, 0, 0, 1, user2, 0, 0, 1)
                        print("\nFinal Board:\n")
                        print(board(chesslist))
                        print("\n")
                        return "-END-"
                    else:
                        print("Continuing game...")
                        imove, fmove = " ", " "
                elif castling(imove, fmove, chesslist, chessmoves, color="white")[1] == 1:
                    chesslist = castling(imove, fmove, chesslist, chessmoves, color="white")[0]
                    if matecheck(chesslist, board(chesslist), color="white")[2] != 0:
                        print("Move leads to being checked, input again")
                        chesslist = chesslistlegacy
                        imove, fmove = " ", " "
                    else:
                        chessmoves["e1"]+=1
                        if imove not in notation[64:68]:
                            imove = fmove
                        if fmove not in notation[64:68]:
                            fmove = imove
                        if imove == "shortcastlewhite" or fmove == "shortcastlewhite":
                            chessmoves["h1"]+=1
                        elif imove == "longcastlewhite" or fmove == "longcastlewhite":
                            chessmoves["a1"]+=1  
                        chesslistlegacy = chesslist
                        break   
                elif chessmovew(imove, fmove, board(chesslist), chessmoves) == 1:
                    chesslist[listcheck(fmove)], chesslist[listcheck(imove)] = chesslist[listcheck(imove)], "\u3164"
                    if matecheck(chesslist, board(chesslist), color="white")[2] != 0:
                        print("Move leads to being checked, input again")
                        chesslist = chesslistlegacy
                        imove, fmove = " ", " "
                    else:
                        chessmoves[imove]+=1
                        chessmoves[fmove]+=1
                        chesslistlegacy = chesslist
                        break
                else:
                    print("Invalid move, input again")
                    imove, fmove = " ", " "
            chesslist = promotion(chesslist)
            if imove in notation[:64] and fmove in notation[:64]:
                print("Move",count,":",imove,"to",fmove,"(White)")
            elif imove == "shortcastlewhite" or fmove == "shortcastlewhite":
                print("Move",count,": short castle (White)")
            elif imove == "longcastlewhite" or fmove == "longcastlewhite":
                print("Move",count,": long castle (White)")
            if matecheck(chesslist, board(chesslist), color="black")[2] == -1: 
                print("\nWhite wins! (Black's King was checkmated)")
                updateleaderboard(user1, 1, 0, 0, user2, 0, 1, 0)
                break
            if chesstimew == 0:
                print("\nBlack wins! (White ran out of time)")
                updateleaderboard(user1, 0, 1, 0, user2, 1, 0, 0)
                break
            if "\u265A" not in chesslist:
                print("\nWhite wins! (Black's King was captured)")
                updateleaderboard(user1, 1, 0, 0, user2, 0, 1, 0)
                break 
            count+=1   
            
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
                chesstimew = remtime.get()
                if "," in moves:
                    moves = moves.split(",")
                    moves = tuple([moves[0], moves[1]])
                else:
                    moves = tuple([moves, moves])
                imove = moves[0].lower()
                fmove = moves[1].lower()
                
                if matecheck(chesslist, board(chesslist), color="black")[2] == 0:
                    validinitial = notation
                    validfinal = notation
                if matecheck(chesslist, board(chesslist), color="black")[2] == 1:
                    validinitial = notation[:64]+notation[-2:] 
                    validfinal = notation[:64]+notation[-2:] 
                if imove == None and fmove == None:
                    print("Input move")
                elif imove not in validinitial or fmove not in validfinal:
                    print("Invalid, input again")
                    imove, fmove = " ", " "
                elif imove == "resign" or fmove == "resign":
                    print("\nWhite wins! (Black has resigned)\n")
                    updateleaderboard(user1, 1, 0, 0, user2, 0, 1, 0)
                    print("\nFinal Board:\n")
                    print(board(chesslist))
                    print("\n")
                    return "-END-"
                elif imove == "draw" or fmove == "draw":
                    confirmb = input("Does Black confirm the draw (Y or N)?  ").lower()
                    confirmw = input("Does White confirm the draw (Y or N)?  ").lower()
                    if confirmb == "y" and confirmw == "y":
                        print("\nDraw!")
                        updateleaderboard(user1, 0, 0, 1, user2, 0, 0, 1)
                        print("\nFinal Board:\n")
                        print(board(chesslist))
                        print("\n")
                        return "-END-"
                    else:
                        print("Continuing game...")
                        imove, fmove = " ", " "
                elif castling(imove, fmove, chesslist, chessmoves, color="black")[1] == 1:
                    chesslist = castling(imove, fmove, chesslist, chessmoves, color="black")[0]
                    if matecheck(chesslist, board(chesslist), color="black")[2] != 0:
                        print("Move leads to being checked, input again")
                        chesslist = chesslistlegacy
                        imove, fmove = " ", " "
                    else:
                        chessmoves["e8"]+=1
                        if imove not in notation[64:68]:
                            imove = fmove
                        if fmove not in notation[64:68]:
                            fmove = imove
                        if imove == "shortcastleblack" or fmove == "shortcastleblack":
                            chessmoves["h8"]+=1
                        elif imove == "longcastleblack" or fmove == "longcastleblack":
                            chessmoves["a8"]+=1
                        chesslistlegacy = chesslist  
                        break
                elif chessmoveb(imove, fmove, board(chesslist), chessmoves) == 1:
                    chesslist[listcheck(fmove)], chesslist[listcheck(imove)] = chesslist[listcheck(imove)], "\u3164"
                    if matecheck(chesslist, board(chesslist), color="black")[2] != 0:
                        print("Move leads to being checked, input again")
                        chesslist = chesslistlegacy
                        imove, fmove = " ", " "
                    else:
                        chessmoves[imove]+=1
                        chessmoves[fmove]+=1
                        chesslistlegacy = chesslist  
                        break
                else:
                    print("Invalid move, input again")
                    imove, fmove = " ", " "
            chesslist = promotion(chesslist)
            if imove in notation[:64] and fmove in notation[:64]:
                print("Move",count,":",imove,"to",fmove,"(Black)")
            elif imove == "shortcastleblack" or fmove == "shortcastleblack":
                print("Move",count,": short castle (Black)")
            elif imove == "longcastleblack" or fmove == "longcastleblack":
                print("Move",count,": long castle (Black)")
            if matecheck(chesslist, board(chesslist), color="white")[2] == -1: 
                print("\nBlack wins! (White's King was checkmated)")
                updateleaderboard(user1, 0, 1, 0, user2, 1, 0, 0)
                break
            if chesstimeb == 0:
                print("\nWhite wins! (Black ran out of time)")
                updateleaderboard(user1, 1, 0, 0, user2, 0, 1, 0)
                break
            if "\u2654" not in chesslist:
                print("\nBlack wins! (White's King was captured)")
                updateleaderboard(user1, 0, 1, 0, user2, 1, 0, 0)
                break
            count+=1 
            
    print("\nFinal Board:\n")
    print(board(chesslist))
    print("\n")
    return "-END-"
            
def chessmovew(initial, final, cbt, dct):
    white = ["\u2656","\u2658","\u2657","\u2655","\u2654","\u2659"]
    chessnotation = ["a1","a2","a3","a4","a5","a6","a7","a8","b1","b2","b3","b4","b5","b6","b7","b8",
                     "c1","c2","c3","c4","c5","c6","c7","c8","d1","d2","d3","d4","d5","d6","d7","d8",
                     "e1","e2","e3","e4","e5","e6","e7","e8","f1","f2","f3","f4","f5","f6","f7","f8",
                     "g1","g2","g3","g4","g5","g6","g7","g8","h1","h2","h3","h4","h5","h6","h7","h8"]
    intloc = location(initial)
    finloc = location(final)
    movelist = []
    if initial not in chessnotation or final not in chessnotation:
        return 0
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
        if (0<=(x-1)<=7 and 1<=y<=8) and (cbt[x-1,y] == "\u3164"):
            movelist.append(location((x-1,y)))
        if (0<=(x-1)<=7 and 1<=(y-1)<=8) and (cbt[x-1,y-1] not in white+["\u3164"]):
            movelist.append(location((x-1,y-1)))
        if (0<=(x-1)<=7 and 1<=(y+1)<=8) and (cbt[x-1,y+1] not in white+["\u3164"]):
            movelist.append(location((x-1,y+1)))
        if (0<=(x-2)<=7 and 1<=y<=8) and (dct[initial] == 0) and (cbt[x-2,y] == "\u3164"):
            movelist.append(location((x-2,y)))
    if final in movelist:
        return 1
    else:
        return 0

def chessmoveb(initial, final, cbt, dct):
    black = ["\u265C","\u265E","\u265D","\u265B","\u265A","\u265F"]
    chessnotation = ["a1","a2","a3","a4","a5","a6","a7","a8","b1","b2","b3","b4","b5","b6","b7","b8",
                     "c1","c2","c3","c4","c5","c6","c7","c8","d1","d2","d3","d4","d5","d6","d7","d8",
                     "e1","e2","e3","e4","e5","e6","e7","e8","f1","f2","f3","f4","f5","f6","f7","f8",
                     "g1","g2","g3","g4","g5","g6","g7","g8","h1","h2","h3","h4","h5","h6","h7","h8"]
    intloc = location(initial)
    finloc = location(final)
    movelist = []
    if initial not in chessnotation or final not in chessnotation:
        return 0
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
        if (0<=(x+1)<=7 and 1<=y<=8) and (cbt[x+1,y] == "\u3164"):
            movelist.append(location((x+1,y)))
        if (0<=(x+1)<=7 and 1<=(y-1)<=8) and (cbt[x+1,y-1] not in black+["\u3164"]):
            movelist.append(location((x+1,y-1)))
        if (0<=(x+1)<=7 and 1<=(y+1)<=8) and (cbt[x+1,y+1] not in black+["\u3164"]):
            movelist.append(location((x+1,y+1)))
        if (0<=(x+2)<=7 and 1<=y<=8) and (cbt[x+2,y] == "\u3164") and (dct[initial] == 0):
            movelist.append(location((x+2,y)))
    if final in movelist:
        return 1
    else:
        return 0

def castling(initial, final, clt, dct, color):
    casclt = clt
    castlelist = ["shortcastlewhite","longcastlewhite","shortcastleblack","longcastleblack"]
    if initial not in castlelist and final not in castlelist:
        return casclt, 0
    if color == "white":
        if (initial == "shortcastlewhite" and final == "longcastlewhite") or (initial == "longcastlewhite" and final == "shortcastlewhite"):
            print("Invalid move, input only one type of castle move")
            return casclt, 0
        elif (initial == "shortcastlewhite" or final == "shortcastlewhite") and (dct["e1"] == 0) and (dct["h1"] == 0) and (casclt[listcheck("f1")] == "\u3164") and (casclt[listcheck("g1")] == "\u3164"):
            casclt[listcheck("e1")], casclt[listcheck("f1")], casclt[listcheck("g1")], casclt[listcheck("h1")] = casclt[listcheck("f1")], casclt[listcheck("h1")], casclt[listcheck("e1")], casclt[listcheck("g1")]
            return casclt, 1
        elif (initial == "longcastlewhite" or final == "longcastlewhite") and (dct["e1"] == 0) and (dct["a1"] == 0) and (casclt[listcheck("b1")] == "\u3164") and (casclt[listcheck("c1")] == "\u3164") and (casclt[listcheck("d1")] == "\u3164"):
            casclt[listcheck("a1")], casclt[listcheck("b1")], casclt[listcheck("c1")], casclt[listcheck("d1")], casclt[listcheck("e1")] = casclt[listcheck("d1")], casclt[listcheck("b1")], casclt[listcheck("e1")], casclt[listcheck("a1")], casclt[listcheck("c1")]
            return casclt, 1
        else:
            return casclt, 0
    if color == "black":
        if (initial == "shortcastleblack" and final == "longcastleblack") or (initial == "longcastleblack" and final == "shortcastleblack"):
            print("Invalid move, input only one type of castle move")
            return casclt, 0
        elif (initial == "shortcastleblack" or final == "shortcastleblack") and dct["e8"] == 0 and dct["h8"] == 0 and casclt[listcheck("f8")] == "\u3164" and casclt[listcheck("g8")] == "\u3164":
            casclt[listcheck("e8")], casclt[listcheck("f8")], casclt[listcheck("g8")], casclt[listcheck("h8")] = casclt[listcheck("f8")], casclt[listcheck("h8")], casclt[listcheck("e8")], casclt[listcheck("g8")]
            return casclt, 1
        elif (initial == "longcastleblack" or final == "longcastleblack") and dct["e8"] == 0 and dct["a8"] == 0 and casclt[listcheck("b8")] == "\u3164" and casclt[listcheck("c8")] == "\u3164" and casclt[listcheck("d8")] == "\u3164":
            casclt[listcheck("a8")], casclt[listcheck("b8")], casclt[listcheck("c8")], casclt[listcheck("d8")], casclt[listcheck("e8")] = casclt[listcheck("d8")], casclt[listcheck("b8")], casclt[listcheck("e8")], casclt[listcheck("a8")], casclt[listcheck("c8")]
            return casclt, 1
        else:
            return casclt, 0           
    
def promotion(clt):
    proclt = clt
    prolist = ["queen", "rook", "bishop", "knight"]
    whitepawnpro = ["a8","b8","c8","d8","e8","f8","g8","h8"]
    blackpawnpro = ["a1","b1","c1","d1","e1","f1","g1","h1"]
    promotion = ""
    for i in whitepawnpro:
        if proclt[listcheck(i)] == "\u2659":
            print("Can promote pawn to one of the following ['queen', 'rook', 'knight', 'bishop']")
            while promotion not in prolist:
                promotion = input("Input what you want your pawn to promote to: ").lower()
            if promotion == "queen":
                proclt[listcheck(i)] = "\u2655"
            if promotion == "rook":
                proclt[listcheck(i)] = "\u2656"
            if promotion == "bishop":
                proclt[listcheck(i)] = "\u2657"
            if promotion == "knight":
                proclt[listcheck(i)] = "\u2658"
    for i in blackpawnpro:
        if proclt[listcheck(i)] == "\u265F":
            print("Can promote pawn to one of the following ['queen', 'rook', 'knight', 'bishop']")
            while promotion not in prolist:
                promotion = input("Input what you want your pawn to promote to: ").lower()
            if promotion == "queen":
                proclt[listcheck(i)] = "\u265B"
            if promotion == "rook":
                proclt[listcheck(i)] = "\u265C"
            if promotion == "bishop":
                proclt[listcheck(i)] = "\u265D"
            if promotion == "knight":
                proclt[listcheck(i)] = "\u265E"
    return proclt

def matecheck(clt, cbt, color):
    white = ["\u2656","\u2658","\u2657","\u2655","\u2654","\u2659"]
    black = ["\u265C","\u265E","\u265D","\u265B","\u265A","\u265F"]
    if color == "white":
        for i in range(len(clt)):
            if clt[i] == "\u2654":
                king = i
                break
        kingstart = listcheck(king)
        king = location(kingstart)
        movelist = [(king[0],king[1])]
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
            x = king[0]
            y = king[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in white:
                    movelist.append((x,y))
                    break
                else:
                    break
        checkcount = 0
        for xy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    pass
                elif cbt[x,y] not in white:
                    if (cbt[x,y] == "\u265C") or (cbt[x,y] == "\u265B"):
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    pass
                elif cbt[x,y] not in white:
                    if (cbt[x,y] == "\u265D") or (cbt[x,y] == "\u265B"):
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        for xy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in white:
                    if cbt[x,y] == "\u265E":
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        for xy in [(-1,1),(-1,-1)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in white:
                    if cbt[x,y] == "\u265F":
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        escapelist = []
        if len(movelist) > 1:
            for intloc in movelist[1:]:
                matecount = 0
                for xy in [(0,1),(1,0),(0,-1),(-1,0)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] == "\u3164":
                            pass
                        elif cbt[x,y] not in white:
                            if (cbt[x,y] == "\u265C") or (cbt[x,y] == "\u265B"):
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] == "\u3164":
                            pass
                        elif cbt[x,y] not in white:
                            if (cbt[x,y] == "\u265D") or (cbt[x,y] == "\u265B"):
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] not in white:
                            if cbt[x,y] == "\u265E":
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(-1,1),(-1,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] not in white:
                            if cbt[x,y] == "\u265F":
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] not in white:
                            if cbt[x,y] == "\u265A":
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                if matecount == 0:
                    escapelist.append(location((intloc[0],intloc[1])))
    if color == "black":
        for i in range(len(clt)):
            if clt[i] == "\u265A":
                king = i
                break
        kingstart = listcheck(king)
        king = location(kingstart)
        movelist = [(king[0],king[1])]
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
            x = king[0]
            y = king[1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in black:
                    movelist.append((x,y))
                    break
                else:
                    break
        checkcount = 0
        for xy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    pass
                elif cbt[x,y] not in black:
                    if (cbt[x,y] == "\u2656") or (cbt[x,y] == "\u2655"):
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        for xy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] == "\u3164":
                    pass
                elif cbt[x,y] not in black:
                    if (cbt[x,y] == "\u2657") or (cbt[x,y] == "\u2655"):
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        for xy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in black:
                    if cbt[x,y] == "\u2658":
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        for xy in [(1,1),(1,-1)]:
            x = movelist[0][0]
            y = movelist[0][1]
            while True:
                x += xy[0]
                y += xy[1]
                if not (0<=x<=7 and 1<=y<=8):
                    break
                if cbt[x,y] not in black:
                    if cbt[x,y] == "\u2659":
                        checkcount+=1
                        break
                    else:
                        break
                else:
                    break
        escapelist = []
        if len(movelist) > 1:
            for intloc in movelist[1:]:
                matecount = 0
                for xy in [(0,1),(1,0),(0,-1),(-1,0)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] == "\u3164":
                            pass
                        elif cbt[x,y] not in black:
                            if (cbt[x,y] == "\u2656") or (cbt[x,y] == "\u2655"):
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(1,1),(-1,1),(1,-1),(-1,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] == "\u3164":
                            pass
                        elif cbt[x,y] not in black:
                            if (cbt[x,y] == "\u2657") or (cbt[x,y] == "\u2655"):
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] not in black:
                            if cbt[x,y] == "\u2658":
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(1,1),(1,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] not in black:
                            if cbt[x,y] == "\u2659":
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                for xy in [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:
                    x = intloc[0]
                    y = intloc[1]
                    while True:
                        x += xy[0]
                        y += xy[1]
                        if not (0<=x<=7 and 1<=y<=8):
                            break
                        if cbt[x,y] not in black:
                            if cbt[x,y] == "\u2654":
                                matecount+=1
                                break
                            else:
                                break
                        else:
                            break
                if matecount == 0:
                    escapelist.append(location((intloc[0],intloc[1])))
    if checkcount == 0:
        return kingstart, escapelist, 0 
    elif (checkcount != 0) and (escapelist != []):
        return kingstart, escapelist, 1
    else:
        return kingstart, escapelist, -1
    
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
    return
        
def listcheck(move):
    notationboard = ["a8","b8","c8","d8","e8","f8","g8","h8",
                     "a7","b7","c7","d7","e7","f7","g7","h7",
                     "a6","b6","c6","d6","e6","f6","g6","h6",
                     "a5","b5","c5","d5","e5","f5","g5","h5",
                     "a4","b4","c4","d4","e4","f4","g4","h4",
                     "a3","b3","c3","d3","e3","f3","g3","h3",
                     "a2","b2","c2","d2","e2","f2","g2","h2",
                     "a1","b1","c1","d1","e1","f1","g1","h1"]
    if type(move) is str:
        for x in range(len(notationboard)):
            if move == notationboard[x]:
                return x
    if type(move) is int:
        return notationboard[move]
    return
    
def timer(remtime, chesstime, move):
    mins, secs = divmod(chesstime, 60)
    clock = "{:02d}:{:02d}".format(mins, secs)
    print(clock, end="\r")
    time.sleep(5)
    while chesstime>0 and not move.is_set():
        mins, secs = divmod(chesstime, 60)
        clock = "{:02d}:{:02d}".format(mins,secs)
        print(clock, end="\r")
        time.sleep(1)
        chesstime-=1
    mins, secs = divmod(chesstime, 60)
    clock = "{:02d}:{:02d}".format(mins, secs)
    print(clock)
    remtime.put(int(chesstime))
    return

def moveinput(result, move):
    moveinput = input("Input move: ").lower()
    move.set()
    result.put(moveinput)
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

def login():
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
                pass1 = gp.getpass(str("Input Password (20 chars): "))
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
                pass1 = gp.getpass(str("Input New Password (20 chars): "))
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
                        accts.write(user1.ljust(20)+pass1.ljust(20)+"0".ljust(5)+"0".ljust(5)+"0".ljust(5))
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
                pass2 = gp.getpass(str("Input Password (20 chars): "))
                if (len(user2) > 20 or user2 == "") or (len(pass2) > 20 or pass2 == "") or (user2.ljust(20).strip() == user1.ljust(20).strip()):
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
                pass2 = gp.getpass(str("Input New Password (20 chars): "))
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
                        accts.write(user2.ljust(20)+pass2.ljust(20)+"0".ljust(5)+"0".ljust(5)+"0".ljust(5))
                logcheck2 = 1
        else:
            print("\nInvalid command. Input again.")
    print("")

    print(f"\nWelcome, {user1} and {user2}!\n")
    return user1, user2

def updateleaderboard(p1n, p1w, p1l, p1d, p2n, p2w, p2l, p2d):
    newdata = ""
    unsortedboard = {}
    with open("chessconsoleaccts.dat", "r") as accts:
        while True:
            data = accts.read(55)
            if not data:
                break
            if (p1n.ljust(20).strip() == data[:20].ljust(20).strip()):
                data = data[:20].ljust(20)+data[20:40].ljust(20)+str(int(data[40:45])+p1w).ljust(5)+str(int(data[45:50])+p1l).ljust(5)+str(int(data[50:55])+p1d).ljust(5)
            if (p2n.ljust(20).strip() == data[:20].ljust(20).strip()):
                data = data[:20].ljust(20)+data[20:40].ljust(20)+str(int(data[40:45])+p2w).ljust(5)+str(int(data[45:50])+p2l).ljust(5)+str(int(data[50:55])+p2d).ljust(5)
            unsortedboard[data[:20].ljust(20).strip()] = 1*int(data[40:45]) + 0.5*int(data[50:55])
            newdata = newdata + data
    with open("chessconsoleaccts.dat", "w") as accts:
        accts.write(newdata)
    leaderboard = dict(sorted(unsortedboard.items(), key=lambda value: -value[1]))
    leaderboardlist = list(leaderboard.items())
    print("\n\n\nLeaderboard: ")
    for i in range(5):
        placement = leaderboardlist[i] if i<len(leaderboardlist) else ("---", "---")
        print(f"\n{i+1}. {placement[0].ljust(22)}     | Point Rating: {placement[1]}")
    print("\n")
    return
    
print(startchess())
