import tkinter as tk
from tkinter import font as tkfont

from constants import (
    BG, SURFACE, CARD, BORDER, FG, MUTED, ACCENT,
    SCORE_COLORS, SCORE_LABELS,
)
from analyser import analyse


class PasswordCheckerApp(tk.Tk):
    """Main application window for the Password Strength Checker."""

    def __init__(self):
        super().__init__()
        self.title("Password Strength Checker")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._init_fonts()
        self._show_pw = False
        self._build_ui()
        self._update()

    # ── Fonts ──────────────────────────────────────────────────────────────────
    def _init_fonts(self):
        self.f_title = tkfont.Font(family="Courier New", size=18, weight="bold")
        self.f_label = tkfont.Font(family="Courier New", size=10)
        self.f_small = tkfont.Font(family="Courier New", size=9)
        self.f_entry = tkfont.Font(family="Courier New", size=13)
        self.f_score = tkfont.Font(family="Courier New", size=13, weight="bold")
        self.f_mono  = tkfont.Font(family="Courier New", size=9)

    # ── Build UI ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self, bg=BG, padx=28, pady=24)
        outer.pack()

        self._build_header(outer)
        self._build_entry_card(outer)
        self._build_strength_bar(outer)
        self._build_entropy_row(outer)
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=14)
        self._build_checklist(outer)
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=14)
        self._build_suggestions(outer)
        self._build_clear_btn(outer)

    def _build_header(self, parent):
        tk.Label(parent, text="PASSWORD CHECKER", font=self.f_title,
                 bg=BG, fg=ACCENT).pack(anchor="w")
        tk.Label(parent, text="Analyse your password strength in real time.",
                 font=self.f_small, bg=BG, fg=MUTED).pack(anchor="w", pady=(2, 18))

    def _build_entry_card(self, parent):
        card = tk.Frame(parent, bg=CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x", ipady=4)

        pw_row = tk.Frame(card, bg=CARD)
        pw_row.pack(fill="x", padx=12, pady=8)

        self.pw_var = tk.StringVar()
        self.pw_var.trace_add("write", lambda *_: self._update())

        self.entry = tk.Entry(
            pw_row, textvariable=self.pw_var,
            show="*", font=self.f_entry,
            bg=CARD, fg=FG, insertbackground=ACCENT,
            relief="flat", bd=0, width=30,
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus()

        self.toggle_btn = tk.Label(pw_row, text="SHOW", font=self.f_small,
                                   bg=CARD, fg=ACCENT, cursor="hand2")
        self.toggle_btn.pack(side="right", padx=(8, 0))
        self.toggle_btn.bind("<Button-1>", self._toggle_show)

        self.char_lbl = tk.Label(card, text="0 characters",
                                 font=self.f_mono, bg=CARD, fg=MUTED, anchor="e")
        self.char_lbl.pack(fill="x", padx=12, pady=(0, 6))

    def _build_strength_bar(self, parent):
        bar_frame = tk.Frame(parent, bg=BG)
        bar_frame.pack(fill="x", pady=(14, 0))

        bar_top = tk.Frame(bar_frame, bg=BG)
        bar_top.pack(fill="x")
        tk.Label(bar_top, text="STRENGTH", font=self.f_small,
                 bg=BG, fg=MUTED).pack(side="left")
        self.score_lbl = tk.Label(bar_top, text="--", font=self.f_score,
                                  bg=BG, fg=MUTED)
        self.score_lbl.pack(side="right")

        self.bar_canvas = tk.Canvas(bar_frame, height=6, bg=SURFACE,
                                    highlightthickness=0, bd=0, width=380)
        self.bar_canvas.pack(fill="x", pady=(6, 0))

    def _build_entropy_row(self, parent):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(10, 0))
        tk.Label(row, text="ENTROPY", font=self.f_small,
                 bg=BG, fg=MUTED).pack(side="left")
        self.entropy_lbl = tk.Label(row, text="-- bits",
                                    font=self.f_small, bg=BG, fg=FG)
        self.entropy_lbl.pack(side="right")

    def _build_checklist(self, parent):
        tk.Label(parent, text="REQUIREMENTS", font=self.f_small,
                 bg=BG, fg=MUTED).pack(anchor="w", pady=(0, 8))

        grid = tk.Frame(parent, bg=BG)
        grid.pack(fill="x")
        self.check_labels = []

        labels = [
            "8+ characters", "12+ characters",
            "Uppercase (A-Z)", "Lowercase (a-z)",
            "Numbers (0-9)", "Symbols (!@#...)",
        ]
        for i, text in enumerate(labels):
            row = tk.Frame(grid, bg=BG)
            row.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 24), pady=2)
            dot = tk.Label(row, text="o", font=self.f_label, bg=BG, fg=MUTED, width=2)
            dot.pack(side="left")
            lbl = tk.Label(row, text=text, font=self.f_small, bg=BG, fg=MUTED)
            lbl.pack(side="left")
            self.check_labels.append((dot, lbl))

    def _build_suggestions(self, parent):
        tk.Label(parent, text="SUGGESTIONS", font=self.f_small,
                 bg=BG, fg=MUTED).pack(anchor="w", pady=(0, 6))
        self.tips_lbl = tk.Label(
            parent, text="Start typing to check your password...",
            font=self.f_small, bg=BG, fg=MUTED,
            justify="left", anchor="w", wraplength=380,
        )
        self.tips_lbl.pack(anchor="w")

    def _build_clear_btn(self, parent):
        tk.Frame(parent, bg=BG, height=10).pack()
        btn = tk.Label(parent, text="[ CLEAR ]", font=self.f_small,
                       bg=BG, fg=MUTED, cursor="hand2")
        btn.pack(anchor="e")
        btn.bind("<Button-1>", lambda _: self.pw_var.set(""))

    # ── Actions ────────────────────────────────────────────────────────────────
    def _toggle_show(self, _=None):
        self._show_pw = not self._show_pw
        self.entry.config(show="" if self._show_pw else "*")
        self.toggle_btn.config(text="HIDE" if self._show_pw else "SHOW")

    # ── Live update ────────────────────────────────────────────────────────────
    def _update(self):
        pw  = self.pw_var.get()
        res = analyse(pw)
        sc  = res["score"]
        col = SCORE_COLORS[sc - 1] if sc > 0 else MUTED

        # Character counter
        n = res["length"]
        self.char_lbl.config(text=f"{n} character{'s' if n != 1 else ''}")

        # Score label
        self.score_lbl.config(
            text=SCORE_LABELS[sc - 1] if sc > 0 else "--",
            fg=col if sc > 0 else MUTED,
        )

        # Strength bar
        self.bar_canvas.update_idletasks()
        W = self.bar_canvas.winfo_width() or 380
        fill_w = int(W * (sc / 5)) if sc > 0 else 0
        self.bar_canvas.delete("all")
        self.bar_canvas.create_rectangle(0, 0, W, 6, fill=SURFACE, outline="")
        if fill_w:
            self.bar_canvas.create_rectangle(0, 0, fill_w, 6, fill=col, outline="")

        # Entropy
        self.entropy_lbl.config(
            text=f"{res['entropy']} bits" if res["entropy"] else "-- bits"
        )

        # Checklist
        for i, (_, passed) in enumerate(res["checks"]):
            dot, lbl = self.check_labels[i]
            if passed:
                dot.config(text="*", fg="#4dd68c")
                lbl.config(fg=FG)
            else:
                dot.config(text="o", fg=MUTED)
                lbl.config(fg=MUTED)

        # Tips
        self.tips_lbl.config(
            text="\n".join(f"-> {t}" for t in res["tips"]),
            fg=col if sc > 0 else MUTED,
        )
