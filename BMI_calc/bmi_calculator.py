
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==================================================
# DATABASE
# ==================================================

conn = sqlite3.connect("bmi_records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()


# ==================================================
# COLORS
# ==================================================

BG = "#F5F0FF"
PURPLE = "#7653A6"
DARK = "#34264A"
MUTED = "#82758F"
WHITE = "#FFFFFF"

CATEGORY_COLORS = {
    "Underweight": "#77BDE8",
    "Normal": "#65C99A",
    "Overweight": "#F4B66A",
    "Obese": "#E98591"
}


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("460x780")
root.configure(bg=BG)
root.resizable(False, False)


# ==================================================
# HEADING
# ==================================================

tk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=PURPLE
).pack(pady=(20, 5))

tk.Label(
    root,
    text="A little step towards a healthier you",
    font=("Arial", 11),
    bg=BG,
    fg=MUTED
).pack(pady=5)


# ==================================================
# INPUT FIELDS
# ==================================================

def create_input(label_text):

    tk.Label(
        root,
        text=label_text,
        font=("Arial", 12, "bold"),
        bg=BG,
        fg=DARK
    ).pack(pady=(12, 4))

    entry = tk.Entry(
        root,
        font=("Arial", 14),
        justify="center",
        width=25,
        relief="flat",
        bd=5
    )

    entry.pack(pady=4, ipady=5)

    return entry


name_entry = create_input("Enter Your Name")
weight_entry = create_input("Enter Weight (kg)")
height_entry = create_input("Enter Height (metres)")


# ==================================================
# RESULT DISPLAY
# ==================================================

result_label = tk.Label(
    root,
    text="Your result will appear here",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=PURPLE,
    justify="center"
)

result_label.pack(pady=15)


# ==================================================
# BMI CALCULATION
# ==================================================

def calculate_bmi():

    name = name_entry.get().strip()

    if not name:
        messagebox.showerror(
            "Invalid Input",
            "Please enter your name!"
        )
        name_entry.focus()
        return

    try:

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be greater than zero!"
            )
            return

        bmi = weight / (height * height)

        if bmi < 18.5:
            category = "Underweight"

        elif bmi < 25:
            category = "Normal"

        elif bmi < 30:
            category = "Overweight"

        else:
            category = "Obese"

        result_label.config(
            text=f"Hello, {name}!\n\n"
                 f"Your BMI: {bmi:.2f}\n"
                 f"Category: {category}",
            fg=CATEGORY_COLORS[category]
        )

        cursor.execute("""
            INSERT INTO bmi_history
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "BMI record saved successfully!"
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for weight and height!"
        )


# ==================================================
# CLEAR FIELDS / NEW USER
# ==================================================

def clear_fields():

    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_label.config(
        text="Your result will appear here",
        fg=PURPLE
    )

    name_entry.focus()


# ==================================================
# DELETE ALL BMI RECORDS
# ==================================================

def delete_old_data():

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete ALL BMI records?\n\n"
        "This action cannot be undone!"
    )

    if confirm:

        cursor.execute("DELETE FROM bmi_history")

        cursor.execute("""
            DELETE FROM sqlite_sequence
            WHERE name = 'bmi_history'
        """)

        conn.commit()

        messagebox.showinfo(
            "Success",
            "All BMI records have been deleted!"
        )

        result_label.config(
            text="All old records cleared!",
            fg=PURPLE
        )


# ==================================================
# VIEW BMI HISTORY
# ==================================================

def view_history():

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("950x430")
    history_window.configure(bg=BG)

    tk.Label(
        history_window,
        text="BMI RECORD HISTORY",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=PURPLE
    ).pack(pady=15)

    columns = (
        "ID", "Name", "Weight", "Height",
        "BMI", "Category", "Date"
    )

    table = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=115, anchor="center")

    table.column("ID", width=45)
    table.column("Date", width=170)

    scrollbar = ttk.Scrollbar(
        history_window,
        orient="vertical",
        command=table.yview
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10
    )

    cursor.execute("""
        SELECT id, name, weight, height, bmi, category, date
        FROM bmi_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)

    if not records:
        messagebox.showinfo(
            "No Records",
            "No BMI records available."
        )
        history_window.destroy()


# ==================================================
# BMI GRAPH DASHBOARD
# ==================================================

def view_graphs():

    cursor.execute("""
        SELECT name, bmi, category
        FROM bmi_history
        ORDER BY id
    """)

    records = cursor.fetchall()

    if not records:
        messagebox.showinfo(
            "No Data",
            "Calculate BMI for at least one user first!"
        )
        return

    names = [
        f"{record[0]} ({i + 1})"
        for i, record in enumerate(records)
    ]

    bmi_values = [record[1] for record in records]
    categories = [record[2] for record in records]

    graph_window = tk.Toplevel(root)
    graph_window.title("BMI Analytics Dashboard")
    graph_window.geometry("1050x850")
    graph_window.configure(bg=BG)

    tk.Label(
        graph_window,
        text="BMI ANALYTICS",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=PURPLE
    ).pack(pady=(18, 3))

    tk.Label(
        graph_window,
        text="Your health data at a glance",
        font=("Arial", 11),
        bg=BG,
        fg=MUTED
    ).pack(pady=(0, 15))

    # Summary cards

    summary = tk.Frame(graph_window, bg=BG)
    summary.pack(fill="x", padx=25, pady=10)

    average_bmi = sum(bmi_values) / len(bmi_values)

    summary_items = [
        ("TOTAL RECORDS", str(len(records))),
        ("AVERAGE BMI", f"{average_bmi:.2f}"),
        ("CATEGORIES", str(len(set(categories))))
    ]

    for title, value in summary_items:

        card = tk.Frame(
            summary,
            bg=WHITE,
            padx=15,
            pady=12,
            highlightbackground="#E7DDF5",
            highlightthickness=1
        )

        card.pack(
            side="left",
            expand=True,
            fill="x",
            padx=6
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack()

        tk.Label(
            card,
            text=value,
            font=("Arial", 20, "bold"),
            bg=WHITE,
            fg=PURPLE
        ).pack(pady=5)

    # Create graphs

    figure = Figure(
        figsize=(10, 8),
        dpi=100,
        facecolor=BG
    )

    ax1 = figure.add_subplot(221)
    ax2 = figure.add_subplot(222)
    ax3 = figure.add_subplot(212)

    for ax in (ax1, ax2, ax3):

        ax.set_facecolor(WHITE)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.tick_params(
            axis="both",
            labelsize=9,
            colors=MUTED
        )

    # GRAPH 1: HORIZONTAL BMI COMPARISON

    bar_colors = [
        CATEGORY_COLORS.get(category, PURPLE)
        for category in categories
    ]

    positions = list(range(len(names)))

    bars = ax1.barh(
        positions,
        bmi_values,
        color=bar_colors,
        height=0.55
    )

    ax1.set_yticks(positions)
    ax1.set_yticklabels(
        names,
        fontsize=9,
        rotation=0,
        ha="right"
    )

    ax1.invert_yaxis()

    ax1.set_title(
        "BMI Comparison",
        fontsize=13,
        fontweight="bold",
        color=DARK,
        pad=15
    )

    ax1.set_xlabel("BMI Value", color=MUTED)

    ax1.set_xlim(
        0,
        max(35, max(bmi_values) + 6)
    )

    ax1.grid(axis="x", alpha=0.2)
    ax1.set_axisbelow(True)

    for bar, value in zip(bars, bmi_values):

        ax1.text(
            value + 0.4,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}",
            va="center",
            fontsize=9,
            fontweight="bold",
            color=DARK
        )

    # GRAPH 2: DONUT CHART

    category_counts = {}

    for category in categories:

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

    ax2.pie(
        category_counts.values(),
        labels=category_counts.keys(),
        colors=[
            CATEGORY_COLORS[category]
            for category in category_counts
        ],
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
        wedgeprops={
            "width": 0.38,
            "edgecolor": WHITE,
            "linewidth": 2
        },
        textprops={
            "fontsize": 9,
            "color": DARK
        }
    )

    ax2.set_title(
        "Category Distribution",
        fontsize=13,
        fontweight="bold",
        color=DARK,
        pad=15
    )

    # GRAPH 3: BMI REFERENCE RANGES

    reference_categories = [
        "Underweight",
        "Normal",
        "Overweight",
        "Obese"
    ]

    lower_limits = [0, 18.5, 25, 30]
    upper_limits = [18.5, 25, 30, 40]

    for i, category in enumerate(reference_categories):

        ax3.barh(
            category,
            upper_limits[i] - lower_limits[i],
            left=lower_limits[i],
            color=CATEGORY_COLORS[category],
            height=0.55
        )

    ax3.set_title(
        "Adult BMI Reference Ranges",
        fontsize=13,
        fontweight="bold",
        color=DARK,
        pad=15
    )

    ax3.set_xlabel("BMI Value", color=MUTED)
    ax3.set_xlim(0, 40)
    ax3.set_xticks([0, 10, 18.5, 25, 30, 40])
    ax3.grid(axis="x", alpha=0.2)
    ax3.set_axisbelow(True)
    ax3.invert_yaxis()

    figure.subplots_adjust(
        left=0.24,
        right=0.96,
        top=0.93,
        bottom=0.09,
        hspace=0.65,
        wspace=0.45
    )

    canvas = FigureCanvasTkAgg(
        figure,
        master=graph_window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    def close_graph():
        plt.close(figure)
        graph_window.destroy()

    graph_window.protocol(
        "WM_DELETE_WINDOW",
        close_graph
    )


# ==================================================
# BUTTONS
# ==================================================

button_style = {
    "font": ("Arial", 12, "bold"),
    "width": 24,
    "pady": 8,
    "relief": "flat",
    "cursor": "hand2"
}

tk.Button(
    root,
    text="Calculate BMI",
    bg="#A78BFA",
    fg="white",
    command=calculate_bmi,
    **button_style
).pack(pady=6)

tk.Button(
    root,
    text="New User / Clear",
    bg="#D8B4FE",
    fg=DARK,
    command=clear_fields,
    **button_style
).pack(pady=4)

tk.Button(
    root,
    text="View BMI History",
    bg="#C4B5FD",
    fg=DARK,
    command=view_history,
    **button_style
).pack(pady=4)

tk.Button(
    root,
    text="View Graphs",
    bg="#8B5CF6",
    fg="white",
    command=view_graphs,
    **button_style
).pack(pady=4)

tk.Button(
    root,
    text="Delete All Records",
    bg="#FCA5A5",
    fg="#7F1D1D",
    command=delete_old_data,
    **button_style
).pack(pady=4)


# ==================================================
# KEYBOARD NAVIGATION
# ==================================================

name_entry.bind(
    "<Return>",
    lambda event: weight_entry.focus()
)

weight_entry.bind(
    "<Return>",
    lambda event: height_entry.focus()
)

height_entry.bind(
    "<Return>",
    lambda event: calculate_bmi()
)


# ==================================================
# CLOSE APPLICATION
# ==================================================

def close_application():

    conn.close()
    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

name_entry.focus()

root.mainloop()
