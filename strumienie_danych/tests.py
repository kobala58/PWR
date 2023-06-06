import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Create a sample figure
fig, ax = plt.subplots()

# Define the positions for the buttons
x_pos = 0.9  # Adjust this value to move the buttons horizontally
y_pos = 0.9  # Adjust this value to move the buttons vertically

# Create the buttons
button1 = Button((x_pos, y_pos), "Button1" color='lightblue', hovercolor='lightgreen')
button2 = Button(ax, 'Button 2', (x_pos, y_pos - 0.1), color='lightblue', hovercolor='lightgreen')
button3 = Button(ax, 'Button 3', (x_pos, y_pos - 0.2), color='lightblue', hovercolor='lightgreen')
button4 = Button(ax, 'Button 4', (x_pos, y_pos - 0.3), color='lightblue', hovercolor='lightgreen')

# Define a button click event handler
def on_button_click(event):
    print(f'Button {event.inaxes.label.get_text()} clicked')

# Connect the button click event handler to each button
button1.on_clicked(on_button_click)
button2.on_clicked(on_button_click)
button3.on_clicked(on_button_click)
button4.on_clicked(on_button_click)

# Adjust the figure margins
fig.subplots_adjust(right=0.8)  # Increase this value if the buttons get cut off

# Display the figure
plt.show()
