import base64, json
q=chr(39)
dq=chr(34)

# ---- Code builders ----
def mk(parts): return chr(10).join(parts)

# S14-C1: FuncAnimation
c14_1 = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import matplotlib.animation as animation",
    "import numpy as np",
    "",
    "fig, ax = plt.subplots()",
    "x = np.linspace(0, 2*np.pi, 100)",
    "line, = ax.plot(x, np.sin(x))",
    "",
    "def update(frame):",
    "    line.set_ydata(np.sin(x + frame/10))",
    "    return line,",
    "",
    "ani = animation.FuncAnimation(fig, update, frames=100, interval=50)",
    "ani.save("+q+"animation.gif"+q+", writer="+q+"pillow"+q+", fps=20)",
    "print("+dq+"Animation saved"+dq+")"
])

# S14-C2: Interactive sliders
c14_2 = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import numpy as np",
    "",
    "# Simulate what a slider would produce at a=1.5, freq=2",
    "fig, ax = plt.subplots()",
    "x = np.linspace(0, 2*np.pi, 200)",
    "a, freq = 1.5, 2.0",
    "ax.plot(x, a * np.sin(freq * x))",
    "ax.set_title(f"+q+"A={a:.1f}, Freq={freq:.1f}"+q+")",
    "ax.set_xlabel("+q+"x"+q+"); ax.set_ylabel("+q+"y"+q+")",
    "fig.savefig("+q+"slider_example.png"+q+", dpi=100, bbox_inches="+q+"tight"+q+")",
    "print("+dq+"Slider simulation saved"+dq+")"
])

# S14-C3: Event handling
c14_3 = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import numpy as np",
    "",
    "fig, ax = plt.subplots()",
    "x = np.random.randn(50)",
    "y = np.random.randn(50)",
    "sc = ax.scatter(x, y, picker=True)",
    "",
    "# Simulate annotation at a clicked point",
    "ax.annotate("+q+"Clicked!"+q+", xy=(x[5], y[5]),",
    "            xytext=(x[5]+0.3, y[5]+0.3),",
    "            arrowprops=dict(arrowstyle="+q+"->"+q+"))",
    "ax.set_title("+q+"Click-to-annotate simulation"+q+")",
    "fig.savefig("+q+"event_handling.png"+q+", dpi=100, bbox_inches="+q+"tight"+q+")",
    "print("+dq+"Event handling example saved"+dq+")"
])

# S14-C4: Blitting
c14_4 = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import matplotlib.animation as animation",
    "import numpy as np",
    "",
    "fig, ax = plt.subplots()",
    "ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1.5, 1.5)",
    "line, = ax.plot([], [], lw=2)",
    "x_data, y_data = [], []",
    "",
    "def init():",
    "    line.set_data([], [])",
    "    return line,",
    "",
    "def animate(i):",
    "    x_data.append(i * 0.1)",
    "    y_data.append(np.sin(i * 0.1))",
    "    line.set_data(x_data[-50:], y_data[-50:])",
    "    return line,",
    "",
    "ani = animation.FuncAnimation(fig, animate, init_func=init,",
    "                               frames=100, blit=True)",
    "ani.save("+q+"blit_animation.gif"+q+", writer="+q+"pillow"+q+", fps=15)",
    "print("+dq+"Blit animation saved"+dq+")"
])

# S14-RW: sensor dashboard
c14_rw = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import matplotlib.animation as animation",
    "import numpy as np",
    "",
    "# Simulate streaming sensor data",
    "sensor_data = []",
    "fig, ax = plt.subplots(figsize=(10, 4))",
    "line, = ax.plot([], [], "+q+"b-"+q+", lw=2)",
    "ax.set_xlim(0, 100); ax.set_ylim(-3, 3)",
    "ax.set_title("+q+"Live Sensor Dashboard"+q+"); ax.set_xlabel("+q+"Time Step"+q+")",
    "",
    "def update(frame):",
    "    sensor_data.append(np.random.randn() * 0.5 + np.sin(frame * 0.1))",
    "    x = list(range(len(sensor_data[-100:])))",
    "    line.set_data(x, sensor_data[-100:])",
    "    return line,",
    "",
    "ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)",
    "ani.save("+q+"sensor_dashboard.gif"+q+", writer="+q+"pillow"+q+", fps=20)",
    "print("+dq+"Live sensor dashboard animation created"+dq+")"
])

# S15-C1: rcParams style
c15_1 = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import numpy as np",
    "",
    "plt.style.use("+q+"seaborn-v0_8-paper"+q+")",
    "plt.rcParams.update({",
    "    "+q+"font.size"+q+": 11,",
    "    "+q+"font.family"+q+": "+q+"serif"+q+",",
    "    "+q+"axes.linewidth"+q+": 1.2,",
    "    "+q+"xtick.major.width"+q+": 1.2,",
    "    "+q+"ytick.major.width"+q+": 1.2,",
    "})",
    "x = np.linspace(0, 4*np.pi, 200)",
    "fig, ax = plt.subplots(figsize=(5, 3.5))",
    "ax.plot(x, np.sin(x), label="+q+"sin(x)"+q+")",
    "ax.plot(x, np.cos(x), label="+q+"cos(x)"+q+")",
    "ax.legend(); ax.set_xlabel("+q+"x"+q+"); ax.set_ylabel("+q+"y"+q+")",
    "ax.set_title("+q+"Publication Style"+q+")",
    "fig.tight_layout()",
    "fig.savefig("+q+"pub_style.pdf"+q+", dpi=300, bbox_inches="+q+"tight"+q+")",
    "print("+dq+"PDF saved at 300 DPI"+dq+")"
])

# S15-C2: LaTeX labels
c15_2 = mk([
    "import matplotlib",
    "matplotlib.use("+q+"Agg"+q+")",
    "import matplotlib.pyplot as plt",
    "import numpy as np",
    "",
    "fig, ax = plt.subplots(figsize=(5, 4))",
    "x = np.linspace(0.1, 3, 200)",
    "ax.plot(x, np.exp(-x**2), label=r"+q+chr(36)+chr(101)+chr(94)+chr(123)+chr(45)+chr(120)+chr(94)+chr(50)+chr(125)+chr(36)+q+")",
    "ax.plot(x, 1/x, label=r"+q+chr(36)+chr(92)+chr(92)+chr(102)+chr(114)+chr(97)+chr(99)+chr(123)+chr(49)+chr(125)+chr(123)+chr(120)+chr(125)+chr(36)+q+")",
    "ax.set_xlabel(r"+q+chr(36)+chr(120)+chr(36)+" (parameter)"+q+", fontsize=12)",
    "ax.set_ylabel(r"+q+chr(36)+chr(102)+chr(40)+chr(120)+chr(41)+chr(36)+q+", fontsize=12)",
    "ax.set_title(r"+q+"Gaussian vs "+chr(36)+chr(49)+chr(47)+chr(120)+chr(36)+" decay"+q+", fontsize=13)",
    "ax.legend(fontsize=11)",
    "fig.tight_layout()",
    "fig.savefig("+q+"latex_labels.png"+q+", dpi=150, bbox_inches="+q+"tight"+q+")",
    "print("+dq+"LaTeX labels rendered"+dq+")"
])
