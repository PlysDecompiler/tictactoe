# source for the algorithm idea:
# https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
# python2.7

def other(cc):
    if cc == 'X':
        return 'O'
    elif cc == 'O':
        return 'X'    

class TicTacToe(object):
    def new_game(self):
        self.board = ["-"]*9
        print "Welcome to Tic Tac Toe!\nDo you want to play against the computer? y/n"
        automode = ''
        while automode not in ('y','n'):
            automode = raw_input()
        self.gamemode = "auto" if automode == 'y' else "O"
        self.whostarts = True
        if self.gamemode == "auto":
            print "Do you want to make the first move against the computer? y/n"
            whostarts = ''
            while whostarts not in ('y','n'):
                whostarts = raw_input()
            self.whostarts = True if whostarts == 'y' else False
        
        self.player_on = "O" if self.whostarts else 'X'
        self.result = "open"
        
        #triples
        self.triples = [range(i,i+7,3) for i in range(3)]+[range(3*i,3*i+3) for i in range(3)]+[[0,4,8],[2,4,6]]
        
    def display(self):
        s = ""
        for i in range(3):
            for j in range (3):
                s+=self.board[3*i+j]+"\t"
            s+= "\t\t"
            s+= ' '.join([str(d) for d in range(3*i+1,3*i+4)])
            s+= "\n"
        print s
        
    def game_loop(self):
        while(True):
            self.new_game()
            #inner game loop
            while(self.result not in ['draw','X','O']):
                self.play()
            if self.result == 'X':
                print 'Player X wins'
            elif self.result == 'O':
                if self.gamemode == 'auto':
                    print 'The Computer wins'
                else:
                    print 'Player O wins'
            elif self.result == 'draw':
                print 'The Game ends in a Draw'
        
    def play(self):
        self.display()
        win = self.test_win(self.player_on)
        if win:
            self.result = self.player_on
            return
        if self.test_end():
            self.result = 'draw'
            return
        
        self.player_on = other(self.player_on)
        if self.gamemode != 'auto' or self.player_on == 'X':
            while(True):
                print 'Player '+self.player_on+', Select a Field between 1 and 9:'
                inp = raw_input()
                try:
                    inp = int(inp)
                    inp -=1
                    if int(inp) not in range(9):
                        print "Wrong input"
                        continue
                    elif self.board[inp] in ('X','O'):
                        print "field already occupied"
                        continue
                    else:
                        self.assign(inp)
                        break
                except:
                    print "try again "
                    continue
                
        else:
            print 'The Computer moves:'
            totlist = {'X': [], 'O': []}
            for trip in self.triples:
                tot = self.twoofthree([self.board[i] for i in trip])
                if tot is not None:
                    totlist[tot].append(trip)
            
            # win by filling a line that already has two 'O'
            # block if opponent has two 'X' in a row already
            for ch in ('O','X'):
                if totlist[ch]:
                    for c in totlist[ch][0]:
                        if self.board[c] == '-':
                            self.assign(c)
                            return

            possibleforks = self.possible_forks()
            for ch in ('O','X'):
                #create a fork or prevent opponent's fork
                if ch == 'X':
                    if self.board[4] == 'O' and ((self.board[0] == 'X' and self.board[8] == 'X') or (self.board[2] == 'X' and self.board[6] == 'X')):
                        if self.board[1] == '-' and self.board[7] == '-':
                            self.assign(1)
                            return
                        elif self.board[3] == '-' and self.board[5] == '-':
                            self.assign(3)
                            return
                if possibleforks[ch]:
                    for k,p in possibleforks[ch].iteritems():
                        if len(p)>=2:
                            self.assign(k)
                            return

            if self.board[4] == '-':
                self.assign(4)
                return
            
            for i in range(0,9,2):
                if self.board[i]=='X':
                    if self.board[8-i] == '-':
                        self.assign(8-i)
                        return
            for i in range(0,9,2)+range(1,8,2):
                if self.board[i] == '-':
                    self.assign(i)
                    return
               
    def assign(self,i):
        self.board[i] = self.player_on
    
    #delivers draw result if all fields are used or no more triple possible
    def test_end(self):
        if all([c!='-' for c in self.board]) \
        or all([[self.board[i] for i in trip].count('X')>=1 and [self.board[i] for i in trip].count('O')>=1 for trip in self.triples]):
            return True

    #checks if the last player has a full triple
    def test_win(self, cc):
        if any([all(field == cc for field in [self.board[i] for i in trip]) for trip in self.triples]):
            return cc
    
    #checks if a row is almost filled
    def twoofthree(self, li):
        if li.count('X')==2 and li.count('-')==1:
            return 'X'
        elif li.count('O')==2 and li.count('-')==1:
            return 'O'
        else:
            return None
    
    #get the possible forks for the computer
    def possible_forks(self):
        retdict = {'X':{}, 'O':{}}
        for trip in self.triples:
            li = [self.board[i] for i in trip]
            for ch in ('X','O'):
                if li.count(ch) == 1 and li.count('-') == 2:
                    for i in trip:
                        if self.board[i] == '-':
                            if i in retdict[ch]:
                                retdict[ch][i].append(trip)
                            else:
                                retdict[ch][i] = [trip]

        return retdict

ttt = TicTacToe()
ttt.game_loop()

