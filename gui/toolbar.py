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
        
        # Separator
        tk.Label(self, text="|").pack(side=tk.LEFT, padx=5)
        
        # Zoom Controls
        self.btn_zoom_in = tk.Button(self, text="Zoom In (+)", command=self.callbacks.get('zoom_in'), state=tk.DISABLED)
        self.btn_zoom_in.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_zoom_out = tk.Button(self, text="Zoom Out (-)", command=self.callbacks.get('zoom_out'), state=tk.DISABLED)
        self.btn_zoom_out.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_reset = tk.Button(self, text="Reset", command=self.callbacks.get('reset_view'), state=tk.DISABLED)
        self.btn_reset.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Pan Controls
        self.btn_pan_left = tk.Button(self, text="<", command=self.callbacks.get('pan_left'), state=tk.DISABLED)
        self.btn_pan_left.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_pan_right = tk.Button(self, text=">", command=self.callbacks.get('pan_right'), state=tk.DISABLED)
        self.btn_pan_right.pack(side=tk.LEFT, padx=2, pady=2)

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
            self._set_zoom_state(tk.DISABLED)
        elif state == 'recording':
            self.btn_record.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_play.config(state=tk.DISABLED)
            self.btn_save.config(state=tk.DISABLED)
            self._set_zoom_state(tk.DISABLED)
        elif state == 'has_data':
            self.btn_record.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.btn_play.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.NORMAL)
            self._set_zoom_state(tk.NORMAL)

    def _set_zoom_state(self, state):
        self.btn_zoom_in.config(state=state)
        self.btn_zoom_out.config(state=state)
        self.btn_reset.config(state=state)
        self.btn_pan_left.config(state=state)
        self.btn_pan_right.config(state=state)
