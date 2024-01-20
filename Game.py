import tkinter as tk
from dotenv import load_dotenv,find_dotenv
import os
import pprint
from login import *
from pymongo import MongoClient
import color as c
import random
load_dotenv(find_dotenv())

password=os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://mk_18:{password}@mk18cluster.3ejfo1y.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)

dbs=client.list_database_names()
database=client.AML_2048
collections=database.list_collection_names()
scorecol=database.User_Score

class Game2048(tk.Toplevel):
    def __init__(self,master,user):
        super().__init__(master)
        self.usr=user
        self.geometry("1920x1080")
        self.grid()
        self.title("2048 Game")
        self.anchor("center")
        self.grid_main = tk.Frame(
            self, bg=c.Color_grid, bd=3, width=600, height=600
        )
        self.grid_main.grid(pady=(110,0))

        self.GUI_maker()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.master.focus_set()
        self.mainloop()
    
    def GUI_maker(self):
        # Create the grid of tiles
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                frame_cells  = tk.Frame(self.grid_main, bg= c.Color_EmptyCell, width=150, height=150)
                frame_cells.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                cell_number = tk.Label(self.grid_main, bg=c.Color_EmptyCell)
                cell_data = {"frame":frame_cells , "number": cell_number}

                cell_number.grid(row=i, column=j)
                row.append(cell_data)
            self.cells.append(row)
        
        frame_score = tk.Frame(self)
        frame_score.place(relx=0.5, y=80, anchor="center")
        tk.Label(
            frame_score,
            text="Score",
            font=c.Font_ScoreLabel
        ).grid(row=0,column=0)
        self.label_score = tk.Label(frame_score, text="0", font= c.Font_Score)
        self.label_score.grid(row=1,column=0,padx=50)

        tk.Label(
            frame_score,
            text="Max Score",
            font=c.Font_ScoreLabel
        ).grid(row=0,column=2)
        scorecard=scorecol.find({"UserName": self.usr}, {"UserName":1,"Score": 1, "_id": 0})
        Scores=[]
        for doc in scorecard:
            Scores.append(int(doc["Score"]))
        max_score=max(Scores)
        self.label_max = tk.Label(frame_score, text=max_score, font= c.Font_Score)
        self.label_max.grid(row=1,column=2,padx=80)

        '''# Frame for score
        score_frame = tk.Frame(self)
        score_frame.pack(side=tk.TOP,padx=20,anchor="center")

        # Score label
        score_label = tk.Label(score_frame, text="Score: 0", font=("Helvetica", 16))
        score_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Max score label
        max_score_label = tk.Label(score_frame, text="Max Score: 0", font=("Helvetica", 16))
        max_score_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # Restart button
        restart_button = tk.Button(self, text="Restart", font=("Helvetica", 16))
        restart_button.pack(side=tk.TOP, padx=10, pady=10)'''
    
    def start_game(self):
        #create matrix of zeros
        self.matrix = [[0]*4 for _ in range(4)]
        #fill 2 random cells with 2s
        row = random.randint(0,3)
        col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.Color_Cells[2])
        self.cells[row][col]["number"].configure(
            bg=c.Color_Cells[2],
            fg=c.Color_CellNumber[2],
            font=c.Fonts_CellNumber[2],
            text="2"
        )
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.Color_Cells[2])
        self.cells[row][col]["number"].configure(
            bg=c.Color_Cells[2],
            fg=c.Color_CellNumber[2],
            font=c.Fonts_CellNumber[2],
            text="2"
        )
        self.score = 0
    
    #stack will make all the tiles with non zeros to the left and all the tiles with zeros to the right 
    def stack(self):
        Matrix_1 = [[0] * 4 for _ in range(4)]
        for i in range(4):
            position_fill = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    Matrix_1[i][position_fill] = self.matrix[i][j]
                    position_fill += 1
        self.matrix = Matrix_1

    #combine is for combining the numbers which are together having same value.
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self .matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    #reverse function is to reverse the column values of matrix. for example, in first row, column 4 element will come to column 1.
    def reverse(self):
        Matrix_1 = []
        for i in range(4):
            Matrix_1.append([])
            for j in range(4):
                Matrix_1[i].append(self.matrix[i][3-j])
        self.matrix = Matrix_1

    #transpose function is to convert the row values with column values.
    def transpose(self):
        Matrix_1 = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                Matrix_1[i][j] = self.matrix[j][i]
        self.matrix = Matrix_1
    
    #add tiles randomaly. wherever there are zero values in the matrix , only they are eligible for tile addition.
    def add_tile(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = random.choice([2,4])
    
    #updating the GUI and cell colors according to numbers combined and numbers generated.
    def GUI_update(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.Color_EmptyCell)
                    self.cells[i][j]["number"].configure(bg=c.Color_EmptyCell, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.Color_Cells[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.Color_Cells[cell_value],
                        fg=c.Color_CellNumber[cell_value],
                        font=c.Fonts_CellNumber[cell_value],
                        text=str(cell_value)
                    )
        self.label_score.configure(text=self.score)
        self.update_idletasks()
    
    #Binding utilized stepwise logic for left, right, up and down key pressing.
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_tile()
        self.GUI_update()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_tile()
        self.GUI_update()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_tile()
        self.GUI_update() 
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()       
        self.stack()
        self.reverse()
        self.transpose()
        self.add_tile()
        self.GUI_update()
        self.game_over()
    
    #function for checking the possible moves
    def Exists_horizontalMoves(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def Exists_verticalMoves(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    #validation whether the game is over or not
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            #print(self.usr)
            user_doc={
            "UserName": self.usr,
            "Score":self.score
            }
            scorecol.insert_one(user_doc)
            game_over_frame = tk.Frame(self.grid_main, borderwidth=2)
            game_over_frame.place(relx=0.5, rely= 0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text = "YOU WIN!!",
                bg=c.Winner_BG,
                fg=c.Font_Color_GameOver,
                font=c.Font_GameOver
            ).pack()
            scorecard=scorecol.find({"UserName": self.usr}, {"UserName":1,"Score": 1, "_id": 0})
            Scores=[]
            for doc in scorecard:
                Scores.append(int(doc["Score"]))
            max_score=max(Scores)
            self.label_max.configure(text=max_score)

        elif not any(0 in row for row in self. matrix) and not self.Exists_horizontalMoves() and not self.Exists_verticalMoves():
            user_doc={
            "UserName": self.usr,
            "Score":self.score
            }
            scorecol.insert_one(user_doc)
            game_over_frame = tk.Frame(self.grid_main, borderwidth=2)
            game_over_frame.place(relx=0.5, rely= 0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text = "Game Over!!",
                bg=c.Loser_BG,
                fg=c.Font_Color_GameOver,
                font=c.Font_GameOver
            ).pack()
            scorecard=scorecol.find({"UserName": self.usr}, {"UserName":1,"Score": 1, "_id": 0})
            Scores=[]
            for doc in scorecard:
                Scores.append(int(doc["Score"]))
            max_score=max(Scores)
            self.label_max.configure(text=max_score)

'''def main():
    Game2048()

if __name__ == "__main__":
    main()'''