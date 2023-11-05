from tkinter import Tk, Canvas, Spinbox, Frame, DoubleVar, TclError

window = Tk()
window.title("Bouncing balls")

# Global variables
balls_count = 0


class Direction:
    # [x_velocity, y_velocity]
    DOWN_RIGHT = [1, 1]
    DOWN_LEFT = [-1, 1]
    UP_RIGHT = [1, -1]
    UP_LEFT = [-1, -1]


class Ball:

    def starting_coordinates(self):
        x = 5
        y = 5
        width = 50
        height = 50

        return [x, y, width, height]

    def __init__(self, window: Tk, canvas: Canvas, speed: float, color: str):
        self.speed = DoubleVar(value=speed)
        self.direction = Direction.DOWN_RIGHT.copy()
        self.canvas = canvas
        self.coordinates = self.starting_coordinates()

        self.x_velocity = 5
        self.y_velocity = 5

        self.oval = canvas.create_oval(self.coordinates,
                                       outline=color,
                                       fill=color)

        global balls_count
        balls_count += 1

    def add_speed_spinbox(self, parent):
        spinbox = Spinbox(
            parent,
            from_=0,
            to=50,
            increment=1,
            textvariable=self.speed,
        )
        next_free_grid_row = balls_count - 1
        spinbox.grid(row=next_free_grid_row, column=0)
        #print(f"Added spinbox to row {next_free_grid_row}")

    def x_coordinate(self):
        return self.canvas.coords(self.oval)[0]

    def y_coordinate(self):
        return self.canvas.coords(self.oval)[1]

    def width(self):
        return 50  # TODO don't hardcode

    def height(self):
        return 50  # TODO don't hardcode

    def update_velocity(self):
        self.update_direction()

        try:
            speed = self.speed.get()
        except TclError as error:
            #print(f"Ignoring invalid speed: {error}")
            window.after(33, self.update_velocity)
            return

        x_direction = self.direction[0]
        y_direction = self.direction[1]
        #print(f"{self.oval}: {x_direction}, {y_direction}")

        self.x_velocity = speed * x_direction
        self.y_velocity = speed * y_direction

        # if self.x_coordinate() > x_upper_bound:
        #     self.x_velocity = -speed
        # if self.y_coordinate() < 0:
        #     self.y_velocity = speed
        # if self.y_coordinate() > y_upper_bound:
        #     self.y_velocity = -speed

        self.canvas.move(self.oval, self.x_velocity, self.y_velocity)

        window.after(33, self.update_velocity)

    def update_direction(self):
        #self.canvas.update()
        canvas_width = 600  #self.canvas.winfo_width()
        canvas_height = 300  #self.canvas.winfo_height()
        #print(canvas_width, canvas_height)
        #print("a", window.winfo_height(), window.winfo_height())

        x_upper_bound = canvas_width - self.width()
        y_upper_bound = canvas_height - self.height()
        #print("limit", x_upper_bound, y_upper_bound)

        # Bounce off the edges of the window
        if self.x_coordinate() < 0:
            # Left wall
            self.direction[0] = 1
            print(f"{self.oval}: Bouncing right")
        if self.x_coordinate() > x_upper_bound:
            # Right wall
            self.direction[0] = -1
            print(f"{self.oval}: Bouncing left")
        if self.y_coordinate() < 0:
            # Top wall
            self.direction[1] = 1
            print(f"{self.oval}: Bouncing down")
        if self.y_coordinate() > y_upper_bound:
            # Bottom wall
            self.direction[1] = -1
            print(f"{self.oval}: Bouncing up")


canvas = Canvas(window, height=300, width=600)
canvas.grid(row=0, column=0)

controls_frame = Frame(window)
controls_frame.grid(row=1, column=0)

red_ball = Ball(window, canvas, 10.0, "#ff0000")
red_ball.add_speed_spinbox(controls_frame)
red_ball.update_velocity()

blue_ball = Ball(window, canvas, 5.0, "#0000ff")
blue_ball.add_speed_spinbox(controls_frame)
blue_ball.update_velocity()

window.mainloop()
