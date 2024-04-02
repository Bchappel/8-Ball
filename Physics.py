import phylib
import sqlite3
import os
import random
import math

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
 "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
 xmlns="http://www.w3.org/2000/svg" 
 xmlns:xlink="http://www.w3.org/1999/xlink">
 <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

FRAME_INTERVAL = 0.01;
DRAG = 150;
EPSILON = 0.01;

################################################################################
# the standard colours of pool balls

BALL_COLOURS = [ 
    "WHITE", #Cue Ball
    "#FFD700", #Yellow Ball (Solid) 1
    "#0000FF", #Blue Ball (Solid) 2
    "#FF0000", #Red  Ball (Solid) 3
    "#800080", #Purple Ball (Solid) 4 
    "#FF8C00", #Orange Ball (Solid) 5
    "#14461A", #Green Ball (Solid) 6
    "#422A1B", #Brown Ball (Solid) 7
    "BLACK", # 8 Ball
    "#FFD700", #Yellow Ball (Dotted) 9
    "#0000FF", #Blue Ball (Dotted) 10 
    "#FF0000", #Red  Ball (Dotted) 11
    "#800080", #Purple Ball (Dotted) 12
    "#FF8C00", #Orange Ball (Dotted) 13
    "#14461A", #Green Ball (Dotted) 14
    "#422A1B", #Brown Ball (Dotted) 15
    ];

class Coordinate(phylib.phylib_coord):
    pass; # This creates a Coordinate subclass, that adds nothing new, but looks more like a nice Python class.

class StillBall(phylib.phylib_object):
    # Python StillBall class.
    def __init__(self, number, pos):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_STILL_BALL, number, pos, None, None, 0.0, 0.0)
        self.__class__ = StillBall
        self.number = number  # Assigning the number attribute here

    def svg(self):

        # Initialize SVG markup with the main circle
        svg_markup = """ <circle cx="%d" cy="%d" r="%d" fill="%s"/>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
    
        if 9 <= self.obj.still_ball.number <= 15:
            # Calculate coordinates for the smaller circle
            small_circle_radius = BALL_RADIUS / 2
            small_circle_cx = self.obj.still_ball.pos.x
            small_circle_cy = self.obj.still_ball.pos.y

            # Add smaller circle to the SVG markup for the dotted balls
            svg_markup += """ <circle cx="%d" cy="%d" r="%d" fill="white"/>\n""" % (small_circle_cx, small_circle_cy, small_circle_radius)
        if self.obj.still_ball.number == 8:
            text_x = self.obj.still_ball.pos.x - BALL_RADIUS / 4
            text_y = self.obj.still_ball.pos.y + BALL_RADIUS / 4
            svg_markup += """<text x="%d" y="%d" font-size="%d" font-family="Arial" fill="WHITE">8</text>\n""" % (text_x-1, text_y + 3, 28)
            
        return svg_markup
  
class RollingBall(phylib.phylib_object):
#     # Python RollingBall class.
    def __init__(self, number, pos, vel, acc):
       phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0)
       self.__class__ = RollingBall

    def svg(self):

        # Initialize SVG markup with the main circle
        svg_markup = """ <circle cx="%d" cy="%d" r="%d" fill="%s"/>\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

        if 9 <= self.obj.rolling_ball.number <= 15:
            small_circle_radius = BALL_RADIUS / 2
            small_circle_cx = self.obj.rolling_ball.pos.x
            small_circle_cy = self.obj.rolling_ball.pos.y

            # Add smaller circle to the SVG markup
            svg_markup += """ <circle cx="%d" cy="%d" r="%d" fill="white"/>\n""" % (small_circle_cx, small_circle_cy, small_circle_radius)

        if self.obj.rolling_ball.number == 8:
            text_x = self.obj.rolling_ball.pos.x - BALL_RADIUS / 4
            text_y = self.obj.rolling_ball.pos.y + BALL_RADIUS / 4
            svg_markup += """<text x="%d" y="%d" font-size="%d" font-family="Arial" fill="WHITE">8</text>\n""" % (text_x-1, text_y + 3, 28)

        return svg_markup

class Hole(phylib.phylib_object):
    # Python Hole class.
    def __init__(self, pos):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0)
        self.__class__ = Hole
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="#99796C" />\n"""  % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

class HCushion(phylib.phylib_object):
    # Python HCushion class.
    def __init__(self, y):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y)
        self.__class__ = HCushion
    def svg(self):        
        if(self.obj.hcushion.y == 0):
            return """ <rect width = "1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        return """ <rect width = "1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (self.obj.hcushion.y)
        
class VCushion(phylib.phylib_object):
    # Python VCushion class.
    def __init__(self, x):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0) 
        self.__class__ = VCushion
    def svg(self):
        if(self.obj.vcushion.x == 0):
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (self.obj.vcushion.x)
               
class Table(phylib.phylib_table):
          
    def __init__(self):
        #Table constructor method.
        #This method call the phylib_table constructor and sets the current object index to -1.
        phylib.phylib_table.__init__(self);
        self.current = -1;

    def __iadd__(self, other):
        #+= operator overloading method.
        #This method allows you to write "table+=object" to add another object to the table.
        self.add_object(other);
        return self;

    def __iter__(self):
        #This method adds iterator support for the table.
        #This allows you to write "for object in table:" to loop over all the objects in the table.
        return self;

    def __next__(self):
        #This provides the next object from the table in a loop.
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS: # check if there are no more objects
            return self[self.current]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__(self, index):
        
        #This method adds item retreivel support using square brackets [ ] .
        #It calls get_object (see phylib.i) to retreive a generic phylib_object
        #and then sets the __class__ attribute to make the class match the object type.
        result = self.get_object(index);
        
        if result == None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__(self):
        
        #Returns a string representation of the table that matches
        #the phylib_print_table function from A1Test1.c.
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i, obj);  # append object description
        return result;  # return the string

    def segment(self):
        
        #Calls the segment method from phylib.i (which calls the phylib_segment
        #functions in phylib.c.
        #Sets the __class__ of the returned phylib_table object to Table
        #to make it a Table object.
        result = phylib.phylib_table.segment(self);
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg(self):
        # Creates SVG representation of the table.        
        svg_representation = HEADER  # start with the header
        for obj in self:
            if obj is not None:  # Check if the object is not None
                svg_representation += obj.svg()  # add SVG representation of each object
        svg_representation += FOOTER  # add the footer
        return svg_representation
    
    def roll(self, t):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                new_ball = RollingBall(ball.obj.rolling_ball.number, Coordinate(0, 0), Coordinate(0, 0), Coordinate(0, 0)) # Create a new ball with the same number as the old ball 
                phylib.phylib_roll(new_ball, ball, t) # Compute where it rolls to 
                new += new_ball # Add ball to table

            if isinstance(ball, StillBall):
                new_ball = StillBall(ball.obj.still_ball.number, Coordinate(ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)) # Create a new ball with the same number and pos as the old ball 
                new += new_ball # Add ball to table 
                
        return new # Return table 
    
    def cueBall(self, table, xvel, yvel):

        for ball in self:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:        
                #ball attributes                
                xpos = ball.obj.still_ball.pos.x;
                ypos = ball.obj.still_ball.pos.y;
                ball.type = phylib.PHYLIB_ROLLING_BALL;

                ball.obj.rolling_ball.number = 0;

                ball.obj.rolling_ball.pos.x = xpos;
                ball.obj.rolling_ball.pos.y = ypos;
                
                ball.obj.rolling_ball.vel.x = xvel;
                ball.obj.rolling_ball.vel.y = yvel;

                #acceleration caculation
                speed = (xvel * xvel + yvel * yvel)
                speed = math.sqrt(speed)

                if speed > VEL_EPSILON:
                    acc_x = -xvel / speed * DRAG
                    acc_y = -yvel / speed * DRAG
                else:
                    acc_x = 0
                    acc_y = 0
                
                ball.obj.rolling_ball.acc.x = acc_x;
                ball.obj.rolling_ball.acc.y = acc_y;
                
class Database:

    def __init__(self, reset = False):
        self.db_name = "phylib.db" # Define the name of the database
        if reset and os.path.exists(self.db_name):
            os.remove(self.db_name) # Remove the database if it exists and reset = True
        self.conn = sqlite3.connect(self.db_name)
    
    def createDB(self):
        
        c = self.conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS Ball(
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT NOT NULL,
            YVEL FLOAT NOT NULL)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS TTable(
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            TIME FLOAT NOT NULL
            )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS BallTable(
            BALLID INTEGER NOT NULL,
            TABLEID INTEGER NOT NULL,
            FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
            )''')
           
        c.execute(''' CREATE TABLE IF NOT EXISTS Shot(
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
            )''')
        
        c.execute(''' CREATE TABLE IF NOT EXISTS TableShot(
            TABLEID INTEGER NOT NULL,
            SHOTID INTEGER NOT NULL, 
            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID), 
            FOREIGN KEY (SHOTID)  REFERENCES Shot(SHOTID)
            )''')
        
        c.execute(''' CREATE TABLE IF NOT EXISTS Game(
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMENAME VARCHAR(64) NOT NULL     
            )''')
        
        c.execute(''' CREATE TABLE IF NOT EXISTS Player(
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
            )''')
        
        self.conn.commit() # Commit the connection
        c.close() # Close cursor
        
    def readTable(self, tableID):
        
        tableID += 1 # Table id is one larger the inital method argument

        c = self.conn.cursor()
        c.execute('''SELECT 
                    Ball.BALLNO, 
                    Ball.XPOS, 
                    Ball.YPOS, 
                    Ball.XVEL, 
                    Ball.YVEL,
                    TTable.TIME
                    FROM Ball 
                    INNER JOIN 
                    BallTable ON Ball.BALLID = BALLTABLE.BALLID 
                    INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID WHERE TTable.TABLEID = ?''', (tableID,))
        rows = c.fetchall()        
        c.close()

        if not rows:
            return None

        table = Table() # Instantiate the table object with standard holes and cushions

        for row in rows:
            ball_no, xpos, ypos, xvel, yvel, time = row
            table.time = time

            if xvel == 0 and yvel == 0:
                ball = StillBall(ball_no, Coordinate(xpos, ypos))
            else:             
                speed = (xvel * xvel + yvel * yvel)
                speed = math.sqrt(speed)

                if(speed > EPSILON):
                    acc_x = (-xvel / speed * DRAG)
                    acc_y = (-yvel / speed * DRAG)
                else:
                    acc_x = 0
                    acc_y = 0
                ball = RollingBall(ball_no, Coordinate(xpos, ypos), Coordinate(xvel, yvel), Coordinate(acc_x, acc_y))

            table += ball

        self.conn.commit()
        return table

    def writeTable(self, table):
        
        c = self.conn.cursor()
        
        c.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = c.lastrowid
        table_id - 1 # Reduce the tableID by one
        
        for ball in table:
            if isinstance(ball, StillBall):
                c.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y, 0, 0))
                ball_id = c.lastrowid
                c.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))
            elif isinstance(ball, RollingBall):
                c.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                ball_id = c.lastrowid
                c.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))

        self.conn.commit()
        c.close()        
        return table_id # Return the autoincremented
        
    def recordTableShot(self,tableID,shotID):
        c = self.conn.cursor();
        c.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)""", (tableID, shotID));
        self.conn.commit();
        c.close();
    
    def setGame(self, gameName, player1Name, player2Name):
        c = self.conn.cursor()
        c.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = c.lastrowid
        
        c.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
        player1ID = c.lastrowid
        
        c.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))
        player2ID = c.lastrowid
        
        self.conn.commit()
        c.close()
        return gameID 
        
    def getGame(self, gameID):
        c = self.conn.cursor()
        # Join the Game table with the Player table twice to retrieve gameName, player1Name, and player2Name
        c.execute('''SELECT g.GAMENAME, p.PLAYERNAME
                    FROM Game g
                    JOIN Player p ON g.GAMEID = p.GAMEID
                    WHERE g.GAMEID = ?
                    ORDER BY p.PLAYERID
                    LIMIT 2''', (gameID,))

        rows = c.fetchall()
        c.close()

        if rows:
            gameName, player1Name = rows[0]
            if len(rows) > 1:
                player2Name = rows[1][1]
            else:
                player2Name = None
            return gameID, gameName, player1Name, player2Name
        else:
            return None
  
    def newShot(self, playerName, gameID):
        c = self.conn.cursor()
        c.execute('''INSERT INTO Shot (PLAYERID, GAMEID) 
                    SELECT PLAYERID, ? FROM Player 
                    WHERE PLAYERNAME = ? AND GAMEID = ?''', (gameID, playerName, gameID))
        shotID = c.lastrowid
        self.conn.commit()
        c.close()
        return shotID # Returns the shotID
    
    def close(self):
        self.conn.commit() # Commit the connection
        self.conn.close() # Close the connection
            
class Game:
    
    HighLowDecider = False
    cueBall = Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - TABLE_WIDTH / 2.0)

    
    def __init__(self, gameID = None, gameName = None, player1Name = None, player2Name = None):
                
        self.gameID = gameID
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.db = Database()
               
        # Constructor 1: Retrive Game from database    
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            gameID += 1 # Increment the gameID
            result = self.db.getGame(gameID) # Retrive the game from the database
            if result is not None:
                self.gameID, self.gameName, self.player1Name, self.player2Name = result
        
        # Constructor 2: Add a new game to the database   
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.gameID = self.db.setGame(gameName, player1Name, player2Name) # Add a new game with all parameters to the database
        else:
            raise TypeError("Invilid Combination: class Game: __init__ function");
               
    def shoot(self, gameName, playerName, table, xvel, yvel):

        #shotID = self.db.newShot(playerName, self.gameID) # New entry to shot table
        table.cueBall(table, xvel, yvel) # Find the cue ball and sets the accelleration
                
        copy = table # Create copy of table to track time between segments 
        copy = copy.segment() # Segment the copy
        start_segment = table.time  # Initalize the start time
        
        svg_content_list = [] #list of svg content

        # Repeatedly segment the table
        while copy:
            segment_length = copy.time - start_segment
            totalFrames = int(segment_length / FRAME_INTERVAL)

            # Loop over the number of frames 
            for frame in range(totalFrames):
                frameTime = frame * FRAME_INTERVAL # Integer multiplied by the FRAME_INTERVAL 
                nextTable = table.roll(frameTime) # Roll the ball to create next table 
                nextTable.time = start_segment + frameTime # Update table time 
                #tableID = self.db.writeTable(nextTable) # Save to database         
                #self.db.recordTableShot(tableID, shotID) # Record the shot
                svg_content_list.append(nextTable.svg())
    
            table = table.segment() # Segment tables and save time 
            start_segment = table.time
            copy = copy.segment() # Segment the copy again
                
        #tableID = self.db.writeTable(table)
        svg_content_list.append(table.svg())
        return svg_content_list, table
            
    def initTable(self, database):

        table = Table()

        # Creates the cue ball on the table
        pos = Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - TABLE_WIDTH / 2.0)
        sb  = StillBall(0, pos)
        table += sb

        #Creating pool balls
        ball_id = 1 # Start with ball_id = 1
        rows = 5  # for a standard set of 15 pool balls

        #places the poolballs on the table
        for i in range(rows):
            for j in range(i + 1):
                x = TABLE_WIDTH/2.0 + (2 * j - i) * (BALL_DIAMETER + 10.0) / 2.0
                y = TABLE_WIDTH/2.0 + (rows - i) * math.sqrt(3.0) / 2.0  * (BALL_DIAMETER + 10.0)
                pos = Coordinate(x, y)
                sb = StillBall(ball_id, pos)
                table += sb
                ball_id += 1
                
        svg_content = table.svg() # create the intial SVG sting of the table
        database.writeTable(table) # Write the inital table table to the database
                
        return table, svg_content  
    
    def gameManager(self, table):
        
        solidCount = 0
        dottedCount = 0
        
             
        for i in range(11,18):
            if table[i] == None:
                solidCount +=1
            
    
        for i in range(19, 26):
            if table[i] == None:
                dottedCount +=1
                    
        # check if the cue ball is none and reset it if it is
        if table[10] is None:
            sb = StillBall(0, self.cueBall) # create a new still ball
            table += sb # add the cue ball back to the table
            newSVG = table.svg() # create the new table svg
            return table, newSVG, False, solidCount, dottedCount # return the new table and svg with the cue ball replaced
            
        # check if the 8 ball is none'
        if solidCount or dottedCount != 7:
            if table[18] is None:
                return table, None, True, solidCount, dottedCount
        
        return table, None, False, solidCount, dottedCount
    
    
    
    

        
            # if self.HighLowDecider == False:
            
            # if currentPlayer == 1:
            #     for i in range(11,26):
            #         if table[i] == None:
            #             if i in range(11, 18):
            #                 print("\t[Game Event] Player 1 gets solid balls and player 2 gets dotted")                    
            #                 #assign player one solid balls (1 - 7)
            #                 self.HighLowDecider = True
                            
            #             elif i in range(19, 26):
            #                 print("\t[Game Event] Player 1 gets dotted balls player to gets solid")
            
            #                 #assign player one dotted balls (9 - 15)
            #                 self.HighLowDecider = True
                            
            # elif currentPlayer == 2:
            #     for i in range(11,26):
            #         if table[i] == None:
            #             print("Ball is none at index: ", i)
            #             if i in range(11, 18):
            #                 print("\t[Game Event] Player 2 gets solid balls and player 1 gets dotted")
                            
            #                 #assign player two solid balls (1 - 7)
                            
            #                 self.HighLowDecider = True
                            
            #             elif i in range(19, 26):
            #                 print("\t[Game Event] Player 2 gets dotted balls and player 1 gets solid")
                            
            #                 #assign two one dotted balls (9 - 15)
                            
            #                 self.HighLowDecider = True