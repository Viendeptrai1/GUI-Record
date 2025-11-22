import tkinter as tk

class Toolbar(tk.Frame):
    def __init__(self, parent, callbacks):
        super().__init__(parent, bd=1, relief=tk.RAISED)
        self.callbacks = callbacks
        
        self.btn_record = tk.Button(self, text="Record", command=self.callbacks['record'])
        self.btn_record.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_stop = tk.Button(self, text="Stop", command=self.callbacks['stop'], state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_play = tk.Button(self, text="Play", command=self.callbacks['play'], state=tk.DISABLED)
        self.btn_play.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_save = tk.Button(self, text="Save", command=self.callbacks['save'], state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT, padx=2, pady=2)

    def set_state(self, state):
        """
        Update button states based on app state.
        state: 'idle', 'recording', 'has_data'
        """
        if state == 'idle':
            self.btn_record.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.btn_play.config(state=tk.DISABLED)
            self.btn_save.config(state=tk.DISABLED)
        elif state == 'recording':
            self.btn_record.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_play.config(state=tk.DISABLED)
            self.btn_save.config(state=tk.DISABLED)
        elif state == 'has_data':
            self.btn_record.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.btn_play.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.NORMAL)
