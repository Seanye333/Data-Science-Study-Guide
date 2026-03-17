import json
q=chr(39)
dq=chr(34)
all_sections=[]

# ===== SECTION 14 =====
s14 = {
    "title": "14. Animations & Interactive Figures",
    "rw_scenario": "You"+q+"re building a live dashboard showing sensor readings that update every second, requiring smooth animation without full plot redraws.",
    "practice": "Create an animated scatter plot where 20 random-walking particles move each frame. Color them by their distance from the origin and save as a GIF.",
    "examples": [],
    "rw_code": ""
}

# s14 example 1 - FuncAnimation
s14["examples"].append({
    "label": "FuncAnimation for animated plots",
    "code": (
        "import matplotlib
"
        "matplotlib.use("+q+"Agg"+q+")
"
        "import matplotlib.pyplot as plt
"
        "import matplotlib.animation as animation
"
        "import numpy as np
"
        "
"
        "fig, ax = plt.subplots()
"
        "x = np.linspace(0, 2*np.pi, 100)
"
        "line, = ax.plot(x, np.sin(x))
"
        "
"
        "def update(frame):
"
        "    line.set_ydata(np.sin(x + frame/10))
"
        "    return line,
"
        "
"
        "ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
"
        "ani.save("+q+"animation.gif"+q+", writer="+q+"pillow"+q+", fps=20)
"
        "print("+dq+"Animation saved"+dq+")"
    )
})

# s14 example 2 - Interactive sliders
s14["examples"].append({
    "label": "Interactive sliders with matplotlib widgets",
    "code": (
        "import matplotlib
"
        "matplotlib.use("+q+"Agg"+q+")
"
        "import matplotlib.pyplot as plt
"
        "import numpy as np
"
        "
"
        "# Simulate what a slider would produce at a=1.5, freq=2
"
        "fig, ax = plt.subplots()
"
        "x = np.linspace(0, 2*np.pi, 200)
"
        "a, freq = 1.5, 2.0
"
        "ax.plot(x, a * np.sin(freq * x))
"
        "ax.set_title(f"+q+"A={a:.1f}, Freq={freq:.1f}"+q+")
"
        "ax.set_xlabel("+q+"x"+q+"); ax.set_ylabel("+q+"y"+q+")
"
        "fig.savefig("+q+"slider_example.png"+q+", dpi=100, bbox_inches="+q+"tight"+q+")
"
        "print("+dq+"Slider simulation saved"+dq+")"
    )
})

# s14 example 3 - Event handling
s14["examples"].append({
    "label": "Event handling — click to annotate",
    "code": (
        "import matplotlib
"
        "matplotlib.use("+q+"Agg"+q+")
"
        "import matplotlib.pyplot as plt
"
        "import numpy as np
"
        "
"
        "fig, ax = plt.subplots()
"
        "x = np.random.randn(50)
"
        "y = np.random.randn(50)
"
        "sc = ax.scatter(x, y, picker=True)
"
        "
"
        "# Simulate annotation at a clicked point
"
        "ax.annotate("+q+"Clicked!"+q+", xy=(x[5], y[5]),
"
        "            xytext=(x[5]+0.3, y[5]+0.3),
"
        "            arrowprops=dict(arrowstyle="+q+"->"+q+"))
"
        "ax.set_title("+q+"Click-to-annotate simulation"+q+")
"
        "fig.savefig("+q+"event_handling.png"+q+", dpi=100, bbox_inches="+q+"tight"+q+")
"
        "print("+dq+"Event handling example saved"+dq+")"
    )
})

# s14 example 4 - Blitting
s14["examples"].append({
    "label": "Blitting for fast animation updates",
    "code": (
        "import matplotlib
"
        "matplotlib.use("+q+"Agg"+q+")
"
        "import matplotlib.pyplot as plt
"
        "import matplotlib.animation as animation
"
        "import numpy as np
"
        "
"
        "fig, ax = plt.subplots()
"
        "ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1.5, 1.5)
"
        "line, = ax.plot([], [], lw=2)
"
        "x_data, y_data = [], []
"
        "
"
        "def init():
"
        "    line.set_data([], [])
"
        "    return line,
"
        "
"
        "def animate(i):
"
        "    x_data.append(i * 0.1)
"
        "    y_data.append(np.sin(i * 0.1))
"
        "    line.set_data(x_data[-50:], y_data[-50:])
"
        "    return line,
"
        "
"
        "ani = animation.FuncAnimation(fig, animate, init_func=init,
"
        "                               frames=100, blit=True)
"
        "ani.save("+q+"blit_animation.gif"+q+", writer="+q+"pillow"+q+", fps=15)
"
        "print("+dq+"Blit animation saved"+dq+")"
    )
})

# s14 rw_code
s14["rw_code"] = (
    "import matplotlib
"
    "matplotlib.use("+q+"Agg"+q+")
"
    "import matplotlib.pyplot as plt
"
    "import matplotlib.animation as animation
"
    "import numpy as np
"
    "
"
    "# Simulate streaming sensor data
"
    "sensor_data = []
"
    "fig, ax = plt.subplots(figsize=(10, 4))
"
    "line, = ax.plot([], [], "+q+"b-"+q+", lw=2)
"
    "ax.set_xlim(0, 100); ax.set_ylim(-3, 3)
"
    "ax.set_title("+q+"Live Sensor Dashboard"+q+"); ax.set_xlabel("+q+"Time Step"+q+")
"
    "
"
    "def update(frame):
"
    "    sensor_data.append(np.random.randn() * 0.5 + np.sin(frame * 0.1))
"
    "    x = list(range(len(sensor_data[-100:])))
"
    "    line.set_data(x, sensor_data[-100:])
"
    "    return line,
"
    "
"
    "ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
"
    "ani.save("+q+"sensor_dashboard.gif"+q+", writer="+q+"pillow"+q+", fps=20)
"
    "print("+dq+"Live sensor dashboard animation created"+dq+")"
)
all_sections.append(s14)
print("s14 rw_code added, section appended")

# ===== SECTION 15 =====
s15 = {
    "title": "15. Publication-Quality Figures",
    "rw_scenario": "You"+q+"re preparing figures for a scientific journal submission that requires 300 DPI images with LaTeX-formatted axis labels and a consistent color scheme.",
    "practice": "Create a 2x2 panel figure showing different distributions (normal, exponential, uniform, Poisson). Add LaTeX labels, use the "+q+"seaborn-v0_8-paper"+q+" style, and export as PNG at 300 DPI.",
    "examples": [],
    "rw_code": ""
}

# s15 example 1
s15["examples"].append({
    "label": "Using matplotlib styles and rcParams",
    "code": (
        "import matplotlib
"
        "matplotlib.use("+q+"Agg"+q+")
"
        "import matplotlib.pyplot as plt
"
        "import numpy as np
"
        "
"
        "plt.style.use("+q+"seaborn-v0_8-paper"+q+")
"
        "plt.rcParams.update({
"
        "    "+q+"font.size"+q+": 11,
"
        "    "+q+"font.family"+q+": "+q+"serif"+q+",
"
        "    "+q+"axes.linewidth"+q+": 1.2,
"
        "    "+q+"xtick.major.width"+q+": 1.2,
"
        "    "+q+"ytick.major.width"+q+": 1.2,
"
        "})
"
        "x = np.linspace(0, 4*np.pi, 200)
"
        "fig, ax = plt.subplots(figsize=(5, 3.5))
"
        "ax.plot(x, np.sin(x), label="+q+"sin(x)"+q+")
"
        "ax.plot(x, np.cos(x), label="+q+"cos(x)"+q+")
"
        "ax.legend(); ax.set_xlabel("+q+"x"+q+"); ax.set_ylabel("+q+"y"+q+")
"
        "ax.set_title("+q+"Publication Style"+q+")
"
        "fig.tight_layout()
"
        "fig.savefig("+q+"pub_style.pdf"+q+", dpi=300, bbox_inches="+q+"tight"+q+")
"
        "print("+dq+"PDF saved at 300 DPI"+dq+")"
    )
})
