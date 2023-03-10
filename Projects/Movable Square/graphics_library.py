from math import pi
import sys, os.path
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget

# hint to window manager where to place graphics window
WINDOW_X = 300
WINDOW_Y = 300

# main app is global to allow things like timers to be started before/without graphics loop
app = QApplication(sys.argv)

# used for noop callbacks
def noop(*args, **kwargs):
    pass

class Image(QImage):
    def get_pixel(self, x, y):
        p = self.pixel(x, y)

        r = qRed(p) / 255.0
        g = qGreen(p) / 255.0
        b = qBlue(p) / 255.0
        a = qAlpha(p) / 255.0

        return (r, g, b, a)

    def set_pixel(self, x, y, r, g, b, a = 1.0):
        ri  = int(r * 255)
        gi  = int(g * 255)
        bi  = int(b * 255)
        ai  = int(a * 255)

        qrgba = qRgba ( ri, gi, bi, ai )
        self.setPixel(x, y, qrgba)

class Canvas(QWidget):

    def __init__(self, draw_fn, data, window_x, window_y, width, height, title, framerate,
                 mouse_press, mouse_release, mouse_move,
                 key_press, key_release):
        super(Canvas, self).__init__()

        # store callback function
        self.draw_fn = draw_fn
        self.mouse_press = mouse_press
        self.mouse_release = mouse_release
        self.mouse_move = mouse_move
        self.key_press = key_press
        self.key_release = key_release

        # data to pass to callback functions
        self.data = data

        self.window_x = window_x
        self.window_y = window_y

        self.width = width
        self.height = height
        self.title = title
        self.framerate = framerate

        # basic state setup

        self.fill_enabled = True
        self.stroke_enabled = True

        self.stroke_width = 1

        self.clear_color = (1, 1, 1, 1)
        self.pen_color = (0, 0, 0, 1)
        self.fill_color = (0, 0, 0, 1)

        # Initial font

        self.font_name = "Arial"
        self.font_size = 14
        self.font_style = QFont.Normal
        self.font_italic = False

        # initialize image just so that there is one for first redraw
        self.image = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        self.init_qt()

        # get the size right this time
        self.image = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)

        self.ipainter = QPainter(self.image)
        self.ipainter.setRenderHint(QPainter.Antialiasing, True)
        self.ipainter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.closed = False

        # store the set of currently pressed keys
        self.keys_down = set()

        self.mouse_down = False
        self.mx = -1
        self.my = -1

        #self.clear()
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        self.timer.start(1000 // self.framerate)



    def init_qt(self):

        # self.setGeometry(self.window_x, self.window_y, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(self.title)

        self.show()

        # enable tracking mouse during mouse move
        self.setMouseTracking(True)

        #self.enable_smoothing()

        self.raise_()

    def paintEvent(self, event):

        screen_painter = QPainter(self)

        screen_painter.drawImage(0, 0, self.image)

        screen_painter.end()


    def closeEvent(self, event):
        # qt unhappy if a reference to ipainter is still hanging
        #   around on close

        self.timer.stop()

        self.ipainter = None



    # used for main rendering loop
    def draw(self):
        #print("draw called")

        if self.data:
            self.draw_fn(self.data)
        else:
            self.draw_fn()

        self.update()


    def mousePressEvent(self, event):
        mx = event.x()
        my = event.y()

        self.mouse_down = True
        self.mx = mx
        self.my = my

        if self.data:
            self.mouse_press(mx, my, self.data)
        else:
            self.mouse_press(mx, my)


    def mouseReleaseEvent(self, event):
        mx = event.x()
        my = event.y()

        self.mouse_down = False
        self.mx = mx
        self.my = my

        if self.data:
            self.mouse_release(mx, my, self.data)
        else:
            self.mouse_release(mx, my)

    def mouseMoveEvent(self, event):
        mx = event.x()
        my = event.y()

        self.mx = mx
        self.my = my

        if self.data:
            self.mouse_move(mx, my, self.data)
        else:
            self.mouse_move(mx, my)

    @staticmethod
    def get_key_str(event):
        #key = event.key()
        #print("text: " + event.text())
        #if key >=65 and key <= 90:
        #    modifiers = event.modifiers()
        #    print(str(modifiers))
        #    if (modifiers & Qt.ShiftModifier) == 0:
        #        print("no shift " + chr(key))
        #        key += 32
        #
        #if key >= 0 and key <=255:
        #    return chr(key)

        #return None
        return event.text()


    def keyPressEvent(self, event):

        key_str= self.get_key_str(event)

        self.keys_down.add(key_str)
        print("key pressed " + key_str)
        if key_str:
            if self.data:
                self.key_press(key_str, self.data)
            else:
                self.key_press(key_str)

    def keyReleaseEvent(self, event):
        key_str = self.get_key_str(event)
        self.keys_down.discard(key_str)

        if key_str:
            if self.data:
                self.key_release(key_str, self.data)
            else:
                self.key_release(key_str)

    def is_key_pressed(self, key):
        return key in self.keys_down

    # Commands that affect state such as color or stroke

    # update functions that update the state of Qt based on
    #  state variables.  Call after changing relevant state variables.

    def enable_smoothing(self):
        # left in only for backwards compatibility.  antialising on by default
        pass

    def update_font(self):
        f = QFont(self.font_name, self.font_size, self.font_style, self.font_italic)
        self.ipainter.setFont(f)

    def update_pen(self):
        # set stroke color and width
        if self.stroke_enabled:
            r = int(self.pen_color[0] * 255)
            g = int(self.pen_color[1] * 255)
            b = int(self.pen_color[2] * 255)
            a = int(self.pen_color[3] * 255)
            pen = QPen(QColor(r, g, b, a))
            pen.setWidth(self.stroke_width)
            self.ipainter.setPen(pen)
        else:
            self.ipainter.setPen(Qt.NoPen)

    def update_brush(self):
        # set fill color
        if self.fill_enabled:
            r = int(self.fill_color[0] * 255)
            g = int(self.fill_color[1] * 255)
            b = int(self.fill_color[2] * 255)
            a = int(self.fill_color[3] * 255)
            self.ipainter.setBrush(QBrush(QColor(r, g, b, a)))
        else:
            self.ipainter.setBrush(Qt.NoBrush)

    def set_clear_color(self, r, g, b, alpha=1.0):
        self.clear_color = (r, g, b, alpha)

    def set_stroke_color(self, r, g, b, alpha=1.0):
        self.pen_color = (r, g, b, alpha)
        self.update_pen()

    def set_stroke_width(self, width):
        self.stroke_width = width
        self.update_pen()

    def set_fill_color(self, r, g, b, alpha=1.0):
        self.fill_color = (r, g, b, alpha)
        self.enable_fill()

    def enable_fill(self):
        self.fill_enabled = True
        self.update_brush()

    def disable_fill(self):
        self.fill_enabled = False
        self.update_brush()

    def enable_stroke(self):
        self.stroke_enabled = True
        self.update_pen()

    def disable_stroke(self):
        self.stroke_enabled = False
        self.update_pen()

    def set_font(self, font_name):
        self.font_name = font_name
        self.update_font()

    def set_font_size(self, size):
        self.font_size = size
        self.update_font()

    def set_font_normal(self):
        self.font_style = QFont.Normal
        self.font_italic = False
        self.update_font()

    def set_font_bold(self):
        self.font_style = QFont.Bold
        self.update_font()

    def set_font_italic(self):
        self.font_italic = True
        self.update_font()


    def rotate(self, angle):
        self.ipainter.rotate(angle)

    def translate(self, x, y):
        self.ipainter.translate(x, y)

    def scale(self, sx, sy):
        self.ipainter.scale(sx, sy)

    def save(self):
        self.ipainter.save()

    def restore(self):
        self.ipainter.restore()

    # Drawing command wrapper methods

    def clear(self):

        r = int(self.clear_color[0] * 255)
        g = int(self.clear_color[1] * 255)
        b = int(self.clear_color[2] * 255)
        a = int(self.clear_color[3] * 255)

        self.ipainter.setBackground(QBrush(QColor(r, g, b, a)))
        #print(self.image.rect())
        self.ipainter.eraseRect(self.image.rect());

    def draw_point(self, x, y):
        self.ipainter.drawPoint(x, y)

    def draw_line(self, x1, y1, x2, y2):
        self.ipainter.drawLine(x1, y1, x2, y2)

    def draw_rectangle(self, x, y, w, h):
        self.ipainter.drawRect(x, y, w, h)

    def draw_polygon(self, vertices):
        qpoints = []

        for vertex in vertices:
            qpoints.append(QPoint(vertex[0], vertex[1]))

        poly = QPolygonF(qpoints)
        self.ipainter.drawPolygon(poly)

    def draw_ellipse(self, x, y, rx, ry):
        self.ipainter.drawEllipse(QRectF(x - rx, y - ry, rx * 2, ry * 2))

    def draw_text(self, s, x, y):

        self.ipainter.drawText(x, y, s)


    def get_text_width(self, str):
        f = QFont(self.font_name, self.font_size, self.font_style, self.font_italic)
        fmetric = QFontMetrics(f)
        #return fmetric.boundingRect(str).width()
        return fmetric.width(str)

    def get_text_height(self):
        f = QFont(self.font_name, self.font_size, self.font_style, self.font_italic)
        fmetric = QFontMetrics(f)
        #return fmetric.boundingRect(str).height()
        return fmetric.height()


    def draw_image(self, image, x, y):
        self.ipainter.drawImage(x, y, image)




# helpful drawing commands

def is_key_pressed(key):
    return canvas.is_key_pressed(key)

def is_mouse_pressed():
    return canvas.mouse_down

def mouse_x():
    return canvas.mx

def mouse_y():
    return canvas.my

def radians_to_degrees(rad):
    return 180 * rad / pi

def enable_fill():
    canvas.enable_fill()

def disable_fill():
    canvas.disable_fill()

def set_fill_color(r, g, b, alpha=1.0):
    canvas.set_fill_color(r, g, b, alpha)

def set_clear_color(r, g, b, alpha=1.0):
    canvas.set_clear_color(r, g, b, alpha)

def enable_stroke():
    canvas.enable_stroke()

def disable_stroke():
    canvas.disable_stroke()

def set_stroke_color(r, g, b, alpha=1.0):
    canvas.set_stroke_color(r, g, b, alpha)

def set_stroke_width(width):
    canvas.set_stroke_width(width)

def set_font(font_name):
    canvas.set_font(font_name)

def set_font_size(font_size):
    canvas.set_font_size(font_size)

def set_font_normal():
    canvas.set_font_normal()

def set_font_bold():
    canvas.set_font_bold()

def set_font_italic():
    canvas.set_font_italic()

def clear():
    canvas.clear()

def draw_point(x, y):
    canvas.draw_point(x, y)

def draw_line(x1, y1, x2, y2):
    canvas.draw_line(x1, y1, x2, y2)

def draw_polygon(vertices):
    canvas.draw_polygon(vertices)

def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_polygon([(x1, y1), (x2, y2), (x3, y3)])

def draw_circle(x, y, r):
    draw_ellipse(x, y, r, r)

def draw_ellipse(x, y, rx, ry):
    if rx <= 0 or ry <= 0:
        return

    canvas.draw_ellipse(x, y, rx, ry)

def draw_rectangle(x, y, w, h):
    canvas.draw_rectangle(x, y, w, h)

def draw_text(string, x, y):
    canvas.draw_text(string, x, y)

def rotate(degrees):
    canvas.rotate(degrees)

def translate(x, y):
    canvas.translate(x, y)

# Images

def draw_image(image, x, y, cx = 0, cy = 0, theta = 0):
    canvas.save()
    translate(x - cx, y - cy)

    if theta != 0:

        translate(cx, cy)
        rotate(theta)
        translate(-cx, -cy)

    canvas.draw_image(image, 0, 0)

    canvas.restore()

def load_image(filename):
    img = Image()
    img.load(filename)
    return img

def get_text_width(string):
    return canvas.get_text_width(string)

def get_text_height():
    return canvas.get_text_height()

# enter main graphics loop
def start_graphics(draw_func=noop, frames=1, data=None, framerate=40,
                title="graphics window", width=400, height=400,
                mouse_press=noop, mouse_release = noop, mouse_move=noop,
                key_press=noop, key_release=noop):

    global canvas

    canvas = Canvas(draw_fn = draw_func, data = data, window_x=WINDOW_X, window_y=WINDOW_Y,
                       width=width, height=height, title=title, framerate=framerate,
                       mouse_press=mouse_press, mouse_release=mouse_release, mouse_move=mouse_move,
                       key_press=key_press, key_release=key_release)



    sys.exit(app.exec_())