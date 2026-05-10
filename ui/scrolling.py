class ScrollManager:
    def __init__(self, window, scroll_frame):
        self.window = window
        self.scroll_frame = scroll_frame
        self.canvas = scroll_frame._parent_canvas
        self.active_textbox = None
        self.allow_main_scroll = True
        self.scroll_accumulator = 0.0

    def bind_window(self):
        self.window.bind_all("<MouseWheel>", self._check_scroll_condition)
        self.canvas.bind("<Button-1>", self._on_touch_start)
        self.canvas.bind("<B1-Motion>", self._on_touch_drag)

    def bind_textbox(self, widget):
        widget.bind("<Enter>", lambda event: self._set_scroll_target(widget))
        widget.bind("<Leave>", lambda event: self._set_scroll_target(None))

    def _set_scroll_target(self, widget):
        self.active_textbox = widget
        self.allow_main_scroll = widget is None

    def _check_scroll_condition(self, event):
        raw_delta = -1 * (event.delta / 120)
        self.scroll_accumulator += raw_delta

        if abs(self.scroll_accumulator) < 1:
            return

        move_units = int(self.scroll_accumulator)
        self.scroll_accumulator -= move_units

        if self._scroll_textbox_if_possible(event, move_units):
            return

        self._scroll_main_window(event, move_units)

    def _scroll_textbox_if_possible(self, event, move_units):
        if self.allow_main_scroll or self.active_textbox is None:
            return False

        top, bottom = self.active_textbox.yview()
        at_top = top <= 0.01
        at_bottom = bottom >= 0.99
        can_scroll_up = event.delta > 0 and not at_top
        can_scroll_down = event.delta < 0 and not at_bottom

        if can_scroll_up or can_scroll_down:
            self.active_textbox.yview_scroll(move_units, "units")
            return True

        return False

    def _scroll_main_window(self, event, move_units):
        main_top, main_bottom = self.canvas.yview()

        if event.delta > 0 and main_top <= 0:
            self.scroll_accumulator = 0
            return

        if event.delta < 0 and main_bottom >= 1.0:
            self.scroll_accumulator = 0
            return

        self.canvas.yview_scroll(move_units * 20, "units")

    def _on_touch_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _on_touch_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def update_scroll_region(self):
        self.window.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
