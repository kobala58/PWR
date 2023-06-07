import matplotlib.pyplot as plt
import wfdb
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import matplotlib
matplotlib.use('TkAgg')

fig, axes = plt.subplots(figsize=(10, 6))

data = wfdb.rdrecord("JS00002", pn_dir="ecg-arrhythmia/WFDBRecords/01/010").p_signal[:, 0]
t = range(len(data))
x, y = [], []

x_width = 250
y_height = 1

is_animation_running = False
is_animation_changed = False

def animate(num):
    global is_animation_changed
    if is_animation_running or is_animation_changed:
        x.append(t[num])
        y.append(data[num])
        axes.cla()  # Clear the axes
        textstr = f"max:{max(y)}\nmin:{min(y)}\ndelta:{(max(y)-min(y)).__round__(3)}"
        axes.plot(x, y, scaley=True, scalex=True, color='blue')
        axes.set_xlim(num - x_width, num)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        axes.text(0.05, 0.95, textstr, transform=axes.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
        axes.set_ylim(data[num] - y_height, data[num] + y_height)
        if num >= x_width:
            x.pop(0)
            y.pop(0)
    is_animation_changed = False

def start_animation(event):
    global is_animation_running
    is_animation_running = True
    anim.event_source.start()

def stop_animation(event):
    global is_animation_running
    is_animation_running = False
    anim.event_source.stop()

def save_screenshot(event):
    fig.savefig('screenshot.png')
    display_screenshot()

def display_screenshot():
    # Create a new figure to display the screenshot
    fig_screenshot = plt.figure()
    # Load the saved screenshot image
    screenshot_image = plt.imread('screenshot.png')
    # Display the image in the new figure
    plt.imshow(screenshot_image)
    plt.axis('off')
    plt.show()

def move_left(event):
    textstr = f"max:{max(y)}\nmin:{min(y)}\ndelta:{max(y)-min(y)}"

    if not is_animation_running:
        current_frame = anim.frame_seq.__next__()
        if current_frame-25 > 0:
            for i in range(25):
                x.pop()
                y.pop()
            anim.frame_seq = iter(range(current_frame - 25, len(t)))
            global is_animation_changed
            is_animation_changed = True
        axes.cla()  # Clear the axes
        axes.plot(x, y, scaley=True, scalex=True, color='blue')
        axes.set_xlim(current_frame - 25 - x_width, current_frame - 25)
        axes.set_ylim(data[current_frame - 25] - y_height, data[current_frame - 25] + y_height)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        axes.text(0.05, 0.95, textstr, transform=axes.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

        plt.draw()


def move_right(event):
    textstr = f"max:{max(y)}\nmin:{min(y)}\ndelta:{max(y)-min(y)}"
    if not is_animation_running:
        current_frame = anim.frame_seq.__next__()
        if current_frame < len(t) - 1:
            for i in range(25):
                x.append(t[current_frame+i])
                y.append(data[current_frame+i])
            anim.frame_seq = iter(range(current_frame + 25, len(t)))
            global is_animation_changed
            is_animation_changed = True
        axes.cla()  # Clear the axes
        axes.plot(x, y, scaley=True, scalex=True, color='blue')
        axes.set_xlim(current_frame + 25 - x_width, current_frame + 25)
        axes.set_ylim(data[current_frame + 25] - y_height, data[current_frame + 25] + y_height)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        axes.text(0.05, 0.95, textstr, transform=axes.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
        plt.draw()



# Add buttons
start_button_ax = fig.add_axes([0.3, 0, 0.1, 0.05])
start_button = Button(start_button_ax, 'Start')
start_button.on_clicked(start_animation)

stop_button_ax = fig.add_axes([0.4, 0, 0.1, 0.05])
stop_button = Button(stop_button_ax, 'Stop')
stop_button.on_clicked(stop_animation)

screenshot_button_ax = fig.add_axes([0.5, 0, 0.1, 0.05])
screenshot_button = Button(screenshot_button_ax, 'Aktualny stan')
screenshot_button.on_clicked(save_screenshot)

move_left_button_ax = fig.add_axes([0.6, 0, 0.1, 0.05])
move_left_button = Button(move_left_button_ax, 'Lewo')
move_left_button.on_clicked(move_left)

move_right_button_ax = fig.add_axes([0.7, 0, 0.1, 0.05])
move_right_button = Button(move_right_button_ax, 'Prawo')
move_right_button.on_clicked(move_right)

anim = FuncAnimation(fig, animate, interval=0.2)

plt.show()
