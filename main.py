import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

plt.style.use('dark_background')
plt.ion()

roots_x = []
roots_y = []

init_x = real = 0
init_y = imag = 1
init_root_number = 2


def getRoots(real, imag, root_number):
    roots_x.clear()
    roots_y.clear()
    number = complex(real, imag)

    # Calculating r and theta
    theta = np.angle(number)
    r = np.sqrt((real ** 2 + imag ** 2))

    # Defining first root
    theta = theta / root_number
    r = np.power(r, 1 / root_number)

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    roots_x.append(x)
    roots_y.append(y)

    imag2 = y
    real2 = x

    # Defining rest of the roots
    for _ in range(root_number - 1):
        theta = theta + (2 * np.pi / root_number)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        roots_x.append(x)
        roots_y.append(y)

        imag2 = y
        real2 = x
        print(complex(real2, imag2))

    return roots_x, roots_y


def prettyShow():
    # Select length of axes and the space between tick labels
    xmin, xmax, ymin, ymax = -max(np.absolute(real), 3), max(np.absolute(real), 3), -max(np.absolute(imag), 3), max(
        np.absolute(imag), 3)
    ticks_frequency = 0.5

    # Plot points
    fig, ax = plt.subplots(figsize=(8, 8))
    start = ax.scatter(real, imag, c='white')
    roots = ax.scatter(roots_x, roots_y, c='red')

    # Set identical scales for both axes
    ax.set(xlim=(xmin - 1, xmax + 1), ylim=(ymin - 1, ymax + 1), aspect='equal')

    # Set bottom and left spines as x and y axes of coordinate system
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Create 'real' and 'imaginary' labels placed at the end of the axes
    ax.set_xlabel('real', size=14, labelpad=-24, x=1.07)
    ax.set_ylabel('imaginary', size=14, labelpad=-21, y=1.02, rotation=0)

    # Create custom major ticks to determine position of tick labels
    x_ticks = np.arange(xmin, xmax + 1, ticks_frequency)
    y_ticks = np.arange(ymin, ymax + 1, ticks_frequency)
    ax.set_xticks(x_ticks[x_ticks != 0])
    ax.set_yticks(y_ticks[y_ticks != 0])

    # Create minor ticks placed at each integer to enable drawing of minor grid lines
    ax.set_xticks(np.arange(xmin, xmax + 1), minor=True)
    ax.set_yticks(np.arange(ymin, ymax + 1), minor=True)

    # Draw major and minor grid lines
    ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

    # Draw arrows
    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
    ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.25, bottom=0.25)


    ## Sliders ##

    # Make a horizontal slider to control the x.
    ax_x = plt.axes([0.25, 0.1, 0.65, 0.03])
    x_slider = Slider(
        ax=ax_x,
        label='x',
        valmin=-10,
        valmax=10,
        valinit=init_x,
    )

    # Make a vertically oriented slider to control the y
    ax_y = plt.axes([0.1, 0.25, 0.0225, 0.63])
    y_slider = Slider(
        ax=ax_y,
        label="y",
        valmin=-10,
        valmax=10,
        valinit=init_y,
        orientation="vertical"
    )

    # Make a vertically oriented slider to control the number of roots
    ax_root_num = plt.axes([0.9, 0.25, 0.0225, 0.63])
    root_slider = Slider(
        ax=ax_root_num,
        label="Root power",
        valmin=2,
        valmax=10,
        valinit=init_root_number,
        valstep=1,
        orientation="vertical"
    )

    # The function to be called anytime a slider's value changes
    def updateStart(val):
        start.set_offsets(np.c_[x_slider.val, y_slider.val])
        roots.set_offsets(np.c_[getRoots(x_slider.val, y_slider.val, root_slider.val)])
        fig.canvas.draw_idle()


    y_slider.on_changed(updateStart)
    x_slider.on_changed(updateStart)
    root_slider.on_changed(updateStart)

    plt.show()
    plt.pause(60)


def main():
    getRoots(init_x, init_y, init_root_number)
    prettyShow()


if __name__ == "__main__":
    main()
