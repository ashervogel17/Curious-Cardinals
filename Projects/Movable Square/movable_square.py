

#Dimensions of the display window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

#Position and velocity of the ball
ball_x = WINDOW_WIDTH/2
ball_y = WINDOW_HEIGHT/2
BALL_RADIUS = 20
BALL_SPEED = 2

#Key pressed boolean values
apressed = False
wpressed = False
spressed = False
dpressed = False

#Dictates movement of the ball by key press
def my_key_press(key):
    global apressed, wpressed, spressed, dpressed
    if key == 'a':
        apressed = True
    if key == 'w':
        wpressed = True
    if key == 's':
        spressed = True
    if key == 'd':
        dpressed = True

#Dictates movement of the paddles by key release
def my_key_release(key):
    global apressed, wpressed, spressed, dpressed
    if key == 'a':
        apressed = False
    if key == 'w':
        wpressed = False
    if key == 's':
        spressed = False
    if key == 'd':
        dpressed = False

#Draws the ball
def draw_ball(x, y, r):
    enable_stroke()
    set_stroke_color(0, 0, 0)
    set_fill_color(1, 1, 1)
    draw_circle(x, y, r)
    disable_stroke()
    set_fill_color(0, 0.3, 0)
    draw_circle(x, y, r-3)

def draw():
    global ball_x, ball_y

    set_fill_color(1, 1, 1)

    #Adjust the position of the ball
    if apressed and ball_x - BALL_RADIUS > 0:
        ball_x -= BALL_SPEED
    if dpressed and ball_x + BALL_RADIUS < WINDOW_WIDTH:
        ball_x += BALL_SPEED
    if wpressed and ball_y - BALL_RADIUS > 0:
        ball_y -= BALL_SPEED
    if spressed and ball_y + BALL_RADIUS < WINDOW_HEIGHT:
        ball_y += BALL_SPEED

    #Draws the ball for each iteration of the loop
    clear()
    draw_ball(ball_x, ball_y, BALL_RADIUS)

start_graphics(draw, width=WINDOW_WIDTH, framerate=100, height=WINDOW_HEIGHT, key_press=my_key_press, \
               key_release=my_key_release)