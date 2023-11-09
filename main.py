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

    def __init__(self,
                 window: Tk,
                 canvas: Canvas,
                 speed: float,
                 color: str,
                 bounds=None):
        self.canvas = canvas
        self.speed = DoubleVar(value=speed)

        self.bounds = bounds

        self.direction = [0, 0]
        self.coordinates = self.starting_coordinates()
        self.x_velocity = 0
        self.y_velocity = 0

        self.oval = canvas.create_oval(self.coordinates,
                                       outline=color,
                                       fill=color)

        global balls_count
        balls_count += 1

    def calculate_bounds(self):
        # Boundaries for the bottom-right of the object
        end_bounds = self.bounds or [
            self.canvas.winfo_width(),
            self.canvas.winfo_height()
        ]

        # Boundaries for the top-left of the object
        start_bounds = [
            end_bounds[0] - self.width(), end_bounds[1] - self.height()
        ]

        return start_bounds

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

        self.x_velocity = abs(self.x_velocity) * x_direction
        self.y_velocity = abs(self.y_velocity) * y_direction

        self.canvas.move(self.oval, self.x_velocity, self.y_velocity)

        window.after(33, self.update_velocity)

    def on_key_down(self, event):
        #print("Keydown", event.keysym)
        if event.keysym == "Up":
            self.set_direction("y", -1)  # [-1, 1]
        elif event.keysym == "Down":
            self.set_direction("y", 1)
        elif event.keysym == "Left":
            self.set_direction("x", -1)
        elif event.keysym == "Right":
            self.set_direction("x", 1)

    def on_key_up(self, event):
        #print("Down", event.keysym)
        if event.keysym == "Up":
            self.set_direction("y", 0)
        elif event.keysym == "Down":
            self.set_direction("y", 0)
        elif event.keysym == "Left":
            self.set_direction("x", 0)
        elif event.keysym == "Right":
            self.set_direction("x", 0)

    def set_direction(self, axis: str, direction: int):
        if axis == "x":
            self.x_velocity = 5 * direction
        elif axis == "y":
            self.y_velocity = 5 * direction

        print("x", self.x_velocity)
        print("y", self.y_velocity)

        self.canvas.move(self.oval, self.x_velocity, self.y_velocity)

    def update_direction(self):
        x_upper_bound = self.calculate_bounds()[0]
        y_upper_bound = self.calculate_bounds()[1]

        # Bounce off the edges of the window
        if self.x_coordinate() < 0:
            # Left wall
            self.direction[0] = 1
        if self.x_coordinate() > x_upper_bound:
            # Right wall
            self.direction[0] = -1
        if self.y_coordinate() < 0:
            # Top wall
            self.direction[1] = 1
        if self.y_coordinate() > y_upper_bound:
            # Bottom wall
            self.direction[1] = -1


def bind_to_keypress(key, function):
    pass


canvas = Canvas(window, height=300, width=600, background="white")
canvas.grid(row=0, column=0)

controls_frame = Frame(window)
controls_frame.grid(row=1, column=0, pady=5)

red_ball = Ball(window, canvas, 10.0, "#ff0000")
#red_ball.add_speed_spinbox(controls_frame)
#red_ball.update_velocity()

#blue_ball = Ball(window, canvas, 5.0, "#0000ff", bounds=[200, 300])
#blue_ball.add_speed_spinbox(controls_frame)
#blue_ball.update_velocity()

window.bind_all("<KeyPress>", red_ball.on_key_down)
window.bind_all("<KeyRelease>", red_ball.on_key_up)

window.mainloop()
