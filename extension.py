"""
Spaceship Game
Author: Joseph-Richard Kwarteng
Date: November 10,2023
Description: This program implements a simple spaceship game where the player controls a spaceship
             and avoids colliding with moving obstacles. The game keeps track of the player's score
             and displays the high score. The game ends when the player collides with an obstacle.

Instructions:
- Use 'a' to move the spaceship left and 'd' to move it right.
- Press 'q' to quit the game.

Note: Make sure the 'graphicsPlus' library is installed before running this program.
"""

# Import necessary libraries
import graphicsPlus as gr
import random
import time
import keyboard

# Define the SpaceshipGame class
class SpaceshipGame:
    def __init__(self, width, height):
        # Initialize the game window
        self.win = gr.GraphWin("Spaceship Game", width, height)
        
        # Create the spaceship
        self.spaceship = gr.Rectangle(gr.Point(width / 2 - 20, height - 40), gr.Point(width / 2 + 20, height - 20))
        self.spaceship.setFill("blue")
        self.spaceship.draw(self.win)
        
        # Initialize obstacles, score, and high score
        self.obstacles = []
        self.score = 0
        self.high_score = self.load_high_score()
        # background_image = gr.Image(gr.Point(self.win.getWidth()/2, self.win.getHeight()/2),'C:\\Users\\there\\OneDrive\\Desktop\\Project_07\\ezgif-5-aef3613bd2.gif')
        # background_image.draw(self.win)
        # self.win.getMouse()

    # Main game loop
    def draw(self):
        while True:
            # Move the spaceship based on user input
            self.move_spaceship()
            
            # Move obstacles and check for collisions
            self.move_obstacles()
            if self.check_collisions():
                break

            # Update and display the score
            self.update_score()
            self.update_high_score()

            # Pause for a short interval to control the game speed
            time.sleep(0.033)
            
            # Update the game window
            self.win.update()

            # Check for 'q' key to exit the game
            if self.win.checkKey() == 'q':
                break

        # Display "Game Over" message, save high score, and close the window
        self.show_game_over()
        self.save_high_score()
        self.win.close()

    # Move the spaceship based on 'a' and 'd' keys
    def move_spaceship(self):
        if keyboard.is_pressed('a') and self.spaceship.getP1().getX() > 0:
            self.spaceship.move(-5, 0)
        elif keyboard.is_pressed('d') and self.spaceship.getP2().getX() < self.win.getWidth():
            self.spaceship.move(5, 0)

    # Generate initial obstacles
    def generate_obstacles(self):
        for _ in range(5):
            obstacle = gr.Rectangle(gr.Point(random.randint(0, self.win.getWidth() - 20), 0),
                                     gr.Point(random.randint(20, self.win.getWidth()), 20))
            obstacle.setFill("red")
            obstacle.draw(self.win)
            self.obstacles.append(obstacle)

    # Move obstacles downward and generate new ones
    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move(0, 5)
            if obstacle.getP2().getY() > self.win.getHeight():
                obstacle.undraw()
                self.obstacles.remove(obstacle)
                new_obstacle = gr.Rectangle(gr.Point(random.randint(0, self.win.getWidth() - 20), 0),
                                            gr.Point(random.randint(20, self.win.getWidth()), 20))
                new_obstacle.setFill("red")
                new_obstacle.draw(self.win)
                self.obstacles.append(new_obstacle)

    # Check for collisions between the spaceship and obstacles
    def check_collisions(self):
        for obstacle in self.obstacles:
            if self.collision(self.spaceship, obstacle):
                return True
        return False

    # Detect collision between two shapes
    def collision(self, shape1, shape2):
        return shape1.getP1().getX() < shape2.getP2().getX() and shape1.getP2().getX() > shape2.getP1().getX() \
               and shape1.getP1().getY() < shape2.getP2().getY() and shape1.getP2().getY() > shape2.getP1().getY()

    # Display "Game Over" message
    def show_game_over(self):
        text = gr.Text(gr.Point(self.win.getWidth() / 2, self.win.getHeight() / 2), "Game Over")
        text.setSize(24)
        text.draw(self.win)
        time.sleep(2)

    # Update and display the current score
    def update_score(self):
        # Clear the previous score text
        for item in self.win.items[:]:
            if isinstance(item, gr.Text) and item.getText().startswith("Score:"):
                item.undraw()

        # Update the score
        self.score += 1
        score_text = gr.Text(gr.Point(50, 20), f"Score: {self.score}")
        score_text.setSize(16)
        score_text.draw(self.win)

    # Update and display the high score
    def update_high_score(self):
        # Clear the previous high score text
        for item in self.win.items[:]:
            if isinstance(item, gr.Text) and item.getText().startswith("High Score:"):
                item.undraw()

        # Update the high score
        if self.score > self.high_score:
            self.high_score = self.score
        high_score_text = gr.Text(gr.Point(self.win.getWidth() - 80, 20), f"High Score: {self.high_score}")
        high_score_text.setSize(16)
        high_score_text.draw(self.win)

    # Load the high score from a file
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    # Save the high score to a file
    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

# Example usage
game = SpaceshipGame(400, 600)
game.generate_obstacles()
game.draw()
