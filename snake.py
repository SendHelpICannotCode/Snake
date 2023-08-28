import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.geometry("525x400")  # Setze die Anfangsgröße des Fensters

        # Deaktiviere das Ändern der Fenstergröße
        self.root.resizable(False, False)

        # Canvas zur Anzeige des Spiels
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack(side=tk.LEFT)

        # Container für Knopf und Label
        button_label_frame = tk.Frame(root)
        button_label_frame.pack(side=tk.RIGHT, padx=20)

        # Anzeige für die Anzahl der gefutterten Äpfel
        self.score_label = tk.Label(button_label_frame, text="Äpfel: 0", font=("Helvetica", 16))
        self.score_label.pack()

        # Neustart-Knopf
        self.restart_button = tk.Button(button_label_frame, text="Neustart", command=self.restart_game)
        self.restart_button.config(state=tk.DISABLED)
        self.restart_button.pack(pady=10)

        # Initialisierung der Schlange, Richtung, Futter und Event-Bindungen
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.spawn_food()
        self.root.bind("<KeyPress>", self.change_direction)

        # Initialisierung von Spielvariablen
        self.score = 0
        self.update_score()
        self.game_over = False

        # Starte die Spielschleife
        self.game_loop()

    def start_game_loop(self):
        # Starte die Spielschleife und speichere die ID des Aufrufs
        self.game_loop_id = self.root.after(100, self.game_loop)

    def restart_game(self):
        if self.game_over:
            # Neustart des Spiels
            self.canvas.delete("all")  # Lösche das aktuelle Spielbrett
            self.restart_button.config(state=tk.DISABLED) # Deaktiviere den Neustartknopf
            self.snake = [(100, 100), (90, 100), (80, 100)]
            self.direction = "Right"
            self.food = self.spawn_food()
            self.score = 0
            self.update_score()
            self.game_over = False

            # Starte die Spielschleife erneut
            self.start_game_loop()

    def spawn_food(self):
        # Zufällige Position für das Futter
        x, y = self.random_coords()
        self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red")
        return x, y

    def change_direction(self, event):
        # Ändere die Richtung basierend auf Tastendruck
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"

    def update_score(self):
        # Aktualisiere die Punktzahl-Anzeige
        self.score_label.config(text=f"Äpfel: {self.score}")

    def check_collision(self, x, y):
        # Überprüfe auf Kollisionen (Rand des Canvas oder sich selbst)
        if x < 0 or x >= 400 or y < 0 or y >= 400 or (x, y) in self.snake:
            self.game_over = True
    
    def random_coords(self):
        while True:
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10

            # Überprüfe, ob das Futter nicht in der Schlange liegt
            if x >= 110 and x < 390 and y >= 110 and y < 390 and (x, y) not in self.snake:
                return x, y

    def game_loop(self):
        if not self.game_over:
            head_x, head_y = self.snake[0]

            # Bewegung der Schlange basierend auf der Richtung
            if self.direction == "Up":
                head_y -= 10
            elif self.direction == "Down":
                head_y += 10
            elif self.direction == "Left":
                head_x -= 10
            elif self.direction == "Right":
                head_x += 10

            # Überprüfe auf Kollisionen
            self.check_collision(head_x, head_y)

            if not self.game_over:
                self.snake.insert(0, (head_x, head_y))
                self.canvas.create_rectangle(head_x, head_y, head_x + 10, head_y + 10, fill="green")

                if (head_x, head_y) == self.food:
                    self.score += 1
                    self.update_score()
                    self.food = self.spawn_food()
                else:
                    tail_x, tail_y = self.snake.pop()
                    self.canvas.create_rectangle(tail_x, tail_y, tail_x + 10, tail_y + 10, fill="black")

                # Rufe die Spielschleife erneut nach einer Verzögerung auf
                self.root.after(100, self.game_loop)
            else:
                # Zeige "Game Over" auf dem Canvas an
                self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 24), fill="white")

                # Aktiviere den Neustart-Knopf erst nach Game Over
                self.restart_button.config(state=tk.ACTIVE)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
