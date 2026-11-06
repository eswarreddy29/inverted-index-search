"""Module 7: frontend GUI (tkinter).

A search box, a Search button, and a read-only result area.
"""
import tkinter as tk
from tkinter import ttk

from query_processor import QueryProcessor


class SearchApp:
    def __init__(self, root: tk.Tk, processor: QueryProcessor) -> None:
        self.processor = processor
        root.title("Inverted Index Search")
        root.geometry("640x420")

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)
        self.entry = ttk.Entry(top)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.focus()
        self.entry.bind("<Return>", lambda _e: self.on_search())
        ttk.Button(top, text="Search", command=self.on_search).pack(side=tk.LEFT, padx=(8, 0))

        self.results = tk.Text(frame, state=tk.DISABLED, wrap=tk.WORD)
        self.results.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def _show(self, text: str) -> None:
        self.results.configure(state=tk.NORMAL)
        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, text)
        self.results.configure(state=tk.DISABLED)

    def on_search(self) -> None:
        query = self.entry.get().strip()
        if not query:
            self._show("Enter a query. Supports AND, OR, NOT and wildcards like mon*.")
            return
        docs = self.processor.search(query)
        if docs:
            self._show(f"{len(docs)} document(s) matched:\n\n" + "\n".join(docs))
        else:
            self._show("No documents matched.")


def run(processor: QueryProcessor) -> None:
    root = tk.Tk()
    SearchApp(root, processor)
    root.mainloop()
