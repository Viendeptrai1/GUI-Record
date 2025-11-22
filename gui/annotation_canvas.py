import tkinter as tk
# from .app import App # Circular import removed 
# Actually better to pass callbacks or use events.

class AnnotationCanvas(tk.Canvas):
    def __init__(self, parent, textgrid, duration, width=800, height=100):
        super().__init__(parent, width=width, height=height, bg="white", bd=2, relief=tk.SUNKEN)
        self.textgrid = textgrid
        self.duration = duration
        self.width = width
        self.height = height
        
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<B1-Motion>", self.on_drag)
        
        self.selected_boundary = None
        self.draw()

    def set_textgrid(self, textgrid, duration):
        self.textgrid = textgrid
        self.duration = duration
        self.draw()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.draw()

    def time_to_x(self, time):
        if self.duration == 0: return 0
        return (time / self.duration) * self.width

    def x_to_time(self, x):
        if self.width == 0: return 0
        return (x / self.width) * self.duration

    def draw(self):
        self.delete("all")
        if not self.textgrid:
            return

        # Draw intervals
        for interval in self.textgrid.intervals:
            x1 = self.time_to_x(interval.xmin)
            x2 = self.time_to_x(interval.xmax)
            
            # Draw boundary line
            if interval.xmin > 0:
                self.create_line(x1, 0, x1, self.height, fill="blue", width=2, tags="boundary")
            
            # Draw text
            center_x = (x1 + x2) / 2
            self.create_text(center_x, self.height/2, text=interval.text, fill="black", font=("Arial", 12))

    def on_click(self, event):
        # Check if clicked near a boundary for dragging?
        time = self.x_to_time(event.x)
        # For now just store click time
        pass

    def on_double_click(self, event):
        time = self.x_to_time(event.x)
        # Check if near boundary to remove, else add
        # Simple logic: Add boundary
        self.textgrid.add_boundary(time)
        self.draw()
        
        # Or if clicked inside interval, edit text?
        # Let's use right click for edit text or a separate dialog
        # For now, double click adds boundary.
        
        # To edit text: maybe Shift+Click?
        
    def on_drag(self, event):
        # Implement boundary dragging later
        pass
        
    def edit_label(self, time):
        # Popup to edit label
        interval = self.textgrid.get_interval(time)
        if interval:
            # Create simple popup
            popup = tk.Toplevel(self)
            popup.title("Edit Label")
            popup.geometry("300x100")
            
            entry = tk.Entry(popup)
            entry.insert(0, interval.text)
            entry.pack(pady=10)
            entry.focus_set()
            
            def save():
                interval.text = entry.get()
                self.draw()
                popup.destroy()
                
            btn = tk.Button(popup, text="OK", command=save)
            btn.pack()
            
            # Allow Enter key to save
            popup.bind('<Return>', lambda e: save())
