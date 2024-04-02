import sys
import cgi
import Physics
import gzip
import random

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

INITIAL_VELOCITY_SCALE = -6

class MyHandler(BaseHTTPRequestHandler):
    
    latest_svg = ""
    table = None
    
    currentTurn = 0
    hasFirstBallSunk = False
    is8BallSunk = False
    bonusTurn = False
    
    whoHasDotted = None
    whoHasSolid = None

    playerOneName = "Player 1"
    playerTwoName = "Player 2"
    gameName = "Game Name"
                
    PlayerOneScore = 0
    PlayerTwoScore = 0
    
    solidNumber = 0
    dottedNumber = 0
    
    winFlag = 0
        
    def do_GET(self):
        
        parsed = urlparse(self.path)
            
        if parsed.path == '/shoot.html':
            self.serve_file('shoot.html', 'text/html') # Serve shoot.html (main page)
            
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')  # Set the content type
        self.end_headers()
                        
        self.wfile.write(self.latest_svg.encode()) # Write the latest svg as a response
    
    def calculateVelocity(startX, startY, endX, endY):
        # Calculate the difference between release position and cue ball position
        diff_x = endX - startX
        diff_y = endY - startY
        
        # Calculate initial velocity components
        initial_vel_x = diff_x * INITIAL_VELOCITY_SCALE
        initial_vel_y = diff_y * INITIAL_VELOCITY_SCALE

        # Max/Min the values
        initial_vel_x = max(-2000, min(2000, initial_vel_x))
        initial_vel_y = max(-2000, min(2000, initial_vel_y))
        
        return initial_vel_x, initial_vel_y
    
    def assignPlayers(playerOneName, playerTwoName):
        players = [playerOneName, playerTwoName]
        first_player = random.choice(players)
        if first_player == playerOneName:
            return 1
        else:
            return 2
              
    def stream_data(self, data):
        with gzip.GzipFile(fileobj=self.wfile, mode='w') as gzipped_file:
            gzipped_file.write(data.encode('utf-8'))
                      
    def do_POST(self):
        parsed = urlparse(self.path)
        # Add a new endpoint to your server
                    
        if parsed.path == '/sendPlayerNames':
            # Parse the form data
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']})
            
            # Retrieve the variables from the form data
            MyHandler.gameName = form.getvalue('gameName')
            MyHandler.playerOneName = form.getvalue('playerOne')
            MyHandler.playerTwoName = form.getvalue('playerTwo')

            print("\t[From Client] Game Name:", MyHandler.gameName)
            print("\t[From Client] Player One Name:", MyHandler.playerOneName)
            print("\t[From Client] Player Two Name:", MyHandler.playerTwoName)

            MyHandler.currentTurn = MyHandler.assignPlayers(MyHandler.playerOneName, MyHandler.playerTwoName)
    
            print("\t[SERVER] Current Player: ", MyHandler.currentTurn);


            # Send a response indicating success
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(str(MyHandler.currentTurn).encode())
            
        elif parsed.path == '/shoot.html':
            # Parse the form data
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']})
            
            print("[GAME] Current Turn is: ", MyHandler.currentTurn)
            
            
            # Retrieve the variables from the form data and convert them to floats
            startX = float(form.getvalue('startX'))
            startY = float(form.getvalue('startY'))
            endX = float(form.getvalue('endX'))
            endY = float(form.getvalue('endY'))
                        
                                    
            initial_vel_x, initial_vel_y = MyHandler.calculateVelocity(startX, startY, endX, endY) # Calculate velocity
        
            # Start the svg: the return value is the list of svgs from the animated shot.
            svg_list, updated_table = game.shoot("Game 01", "Braedan", MyHandler.table, initial_vel_x, initial_vel_y)
            MyHandler.latest_svg = svg_list[-1]; # set the last frame as the new current
                
            #check to see if the shot broke any of the rules and apply the correct rules to the score
            updated_table, newSVG, MyHandler.is8BallSunk, MyHandler.solidNumber, MyHandler.dottedNumber = game.gameManager(updated_table)
        
            if not MyHandler.hasFirstBallSunk:
                
                if MyHandler.currentTurn == 1:
                    for i in range(11,26):
                        if updated_table[i] == None:
                            if i in range(11, 18):
                                print("\t[Game Event] Player 1 gets solid balls and player 2 gets dotted")                    
                                #(1 - 7)
                                MyHandler.whoHasSolid = 1 # Player 1 assigned solid
                                MyHandler.whoHasDotted = 2 # Player 2 assigned dotted
                                MyHandler.PlayerOneScore = MyHandler.solidNumber # player one score assigned to solid balls
                                MyHandler.PlayerTwoScore = MyHandler.dottedNumber # player two score assigned to dotted balls
                                MyHandler.hasFirstBallSunk = True
                                
                            elif i in range(19, 26):
                                #(9 - 15)
                                print("\t[Game Event] Player 1 gets dotted balls player to gets solid")
                                MyHandler.whoHasDotted = 1 # Player 1 assigned dotted
                                MyHandler.whoHasSolid = 2 # Player 2 assigned solid
                                MyHandler.PlayerOneScore = MyHandler.dottedNumber # player one score assigned to dotted balls
                                MyHandler.PlayerTwoScore = MyHandler.solidNumber # player two score assigned to solid balls
                                MyHandler.hasFirstBallSunk = True
                                
                elif MyHandler.currentTurn == 2:
                    for i in range(11,26):
                        if updated_table[i] == None:
                            if i in range(11, 18):
                                #assign player two solid balls (1 - 7)
                                print("\t[Game Event] Player 2 gets solid balls and player 1 gets dotted")
                                MyHandler.whoHasDotted = 1 # Player 1 assigned dotted
                                MyHandler.whoHasSolid = 2 # Player 2 assigned solid
                                MyHandler.PlayerOneScore = MyHandler.dottedNumber # player one score assigned to dotted balls
                                MyHandler.PlayerTwoScore = MyHandler.solidNumber # player two score assigned to solid balls
                                MyHandler.hasFirstBallSunk = True
                                
                            elif i in range(19, 26):
                                #assign two one dotted balls (9 - 15) 
                                print("\t[Game Event] Player 2 gets dotted balls and player 1 gets solid")
                                MyHandler.whoHasSolid = 1 # Player one assigned solid
                                MyHandler.whoHasDotted = 2 # Player 2 assigned dotted
                                MyHandler.PlayerOneScore = MyHandler.solidNumber # Player one score assigned to solid balls
                                MyHandler.PlayerTwoScore = MyHandler.dottedNumber # player two score assigned to dotted balls
                                MyHandler.hasFirstBallSunk = True
            
            
            print("Dotted Player", MyHandler.whoHasDotted)
            print("Solid Player", MyHandler.whoHasSolid)
             
            # Variable to track if any balls have disappeared
            

            if MyHandler.is8BallSunk is not True:
            # Check for differences between the two tables
                balls_disappeared = False
                for i in range(11, 26):
                    if updated_table[i] is None and MyHandler.table[i] is not None:
                        balls_disappeared = True
                        if i in range(11, 18):
                            if MyHandler.currentTurn == 1:
                                if MyHandler.whoHasSolid == 1:
                                    print("\t[BONUS] Player one has sunk solid, turn does not change")
                                    MyHandler.currentTurn = 1
                                else:
                                    print("\t[BONUS] Player one has sunk opponent's solid, turn changes to player two")
                                    MyHandler.currentTurn = 2
                            elif MyHandler.currentTurn == 2:
                                if MyHandler.whoHasSolid == 2:
                                    print("\t[BONUS] Player two has sunk solid, turn does not change")
                                    MyHandler.currentTurn = 2
                                else:
                                    print("\t[BONUS] Player two has sunk opponent's solid, turn changes to player one")
                                    MyHandler.currentTurn = 1
                        elif i in range(19, 26):
                            if MyHandler.currentTurn == 1:
                                if MyHandler.whoHasDotted == 1:
                                    print("\t[BONUS] Player one has sunk dotted, turn does not change")
                                    MyHandler.currentTurn = 1
                                else:
                                    print("\t[BONUS] Player one has sunk opponent's dotted, turn changes to player two")
                                    MyHandler.currentTurn = 2
                            elif MyHandler.currentTurn == 2:
                                if MyHandler.whoHasDotted == 2:
                                    print("\t[BONUS] Player two has sunk dotted, turn does not change")
                                    MyHandler.currentTurn = 2
                                else:
                                    print("\t[BONUS] Player two has sunk opponent's dotted, turn changes to player one")
                                    MyHandler.currentTurn = 1
                # If no balls have disappeared, switch turns
                if not balls_disappeared:
                    print("\t[RESULT] No balls were None on shot")
                    MyHandler.currentTurn = 1 if MyHandler.currentTurn == 2 else 2 # switch turn

            if MyHandler.is8BallSunk == True:
                print("\t[Game] 8 Ball was Sunk")
                if MyHandler.currentTurn == 1:
                    print("game technically lost")
                    MyHandler.winFlag = 2
                elif MyHandler.currentTurn == 2:
                    print("game technically lost")
                    MyHandler.winFlag = 1
            
            print("Dotted ", MyHandler.dottedNumber)
            print("Solid ", MyHandler.solidNumber)
            
            if MyHandler.dottedNumber == 7:
                if MyHandler.whoHasDotted == 1:
                    print("[dotted high] player 1 sank all thier balls")
                    MyHandler.winFlag = 1
                elif MyHandler.whoHasDotted == 2:
                    print("[dotted high] player 2 sank all thier balls")
                    MyHandler.winFlag = 2

            if MyHandler.solidNumber == 7:
                if MyHandler.whoHasSolid == 1:
                    print("[solid low] player 1 sank all thier balls")
                    MyHandler.winFlag = 1
                elif MyHandler.whoHasSolid == 2:
                    print("[solid low] player 2 sank all thier balls")
                    MyHandler.winFlag = 2
                    

            if newSVG is not None:
                svg_list.append(newSVG)
                
            print("\t[Server] Number of SVGs passed to client", len(svg_list))
            
            svg_list = [svg.replace('\n', '') for svg in svg_list] # strip new line character
            MyHandler.table = updated_table # Update MyHandler.table with the new table object returned from game.shoot()            
            concatenated_list = ','.join(svg_list)
          
            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Encoding", "gzip")  # Indicate gzip compression
            self.end_headers()

            # Stream and compress the CSV data to the client
            self.stream_data(concatenated_list)
            
        elif parsed.path == '/getCurrentTurn':
            # Add additional values to be sent
            additional_values = (MyHandler.currentTurn, MyHandler.whoHasDotted, MyHandler.whoHasSolid, MyHandler.winFlag,)

            # Create a single string containing all the values
            response_str = ",".join(str(value) for value in additional_values)

            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response_str.encode())
            
        else:
            self.send_error(404, "File not found")
            
    
    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
        
    db = Physics.Database(reset = True)
    db.createDB()

    #get the playerNames and gameName
    game = Physics.Game(gameName = "Game 01", player1Name = "Braedan", player2Name = "Zach")
    MyHandler.table, MyHandler.latest_svg = game.initTable(db) #initialize the first snapshot table        
   
    port = int(sys.argv[1])
    httpd = HTTPServer(('localhost', port), MyHandler)
    print("[SERVER] Server listening on port:", port)
    httpd.serve_forever()
    