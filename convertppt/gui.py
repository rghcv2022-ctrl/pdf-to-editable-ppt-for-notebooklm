import os
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from .core import (
    build_output_path,
    convert_file,
    is_supported_input,
    log_runtime_summary,
)


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ConvertPPT")
        self.root.geometry("760x560")

        self.input_path = tk.StringVar()
        self.status = tk.StringVar(value="就绪")

        self._build_widgets()
        self.log("ConvertPPT ready.")
        log_runtime_summary(self.log)

    def _build_widgets(self) -> None:
        frame_input = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="groove")
        frame_input.pack(fill="x", padx=10, pady=8)

        tk.Label(frame_input, text="输入文件", font=("Arial", 10, "bold")).pack(anchor="w")

        row = tk.Frame(frame_input)
        row.pack(fill="x", pady=6)
        tk.Label(row, text="PDF / PPT / PPTX:").pack(side="left")
        tk.Entry(row, textvariable=self.input_path, width=58).pack(side="left", padx=6)
        tk.Button(row, text="浏览...", command=self.browse_file).pack(side="left")

        frame_actions = tk.Frame(self.root, padx=10, pady=4)
        frame_actions.pack(fill="x")

        self.btn_run = tk.Button(
            frame_actions,
            text="开始转换",
            command=self.start_thread,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=16,
        )
        self.btn_run.pack()

        frame_log = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="groove")
        frame_log.pack(fill="both", expand=True, padx=10, pady=8)

        tk.Label(frame_log, text="运行日志", font=("Arial", 10, "bold")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(
            frame_log,
            height=16,
            bg="#1E1E1E",
            fg="#00FF7F",
            font=("Consolas", 10),
        )
        self.log_area.pack(fill="both", expand=True, pady=6)

        tk.Label(self.root, textvariable=self.status, relief="sunken", anchor="w").pack(
            fill="x",
            side="bottom",
        )

    def log(self, message: str) -> None:
        self.root.after(0, lambda: self._append_log(str(message)))

    def _append_log(self, message: str) -> None:
        print(message)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.status.set(message)

    def browse_file(self) -> None:
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Supported files", "*.pdf *.ppt *.pptx"),
                ("PDF files", "*.pdf"),
                ("PowerPoint files", "*.ppt *.pptx"),
            ]
        )
        if filename:
            self.input_path.set(filename)

    def start_thread(self) -> None:
        input_file = self.input_path.get().strip()
        if not input_file:
            messagebox.showwarning("提示", "请先选择一个输入文件。")
            return
        if not os.path.exists(input_file):
            messagebox.showwarning("提示", "输入文件不存在。")
            return
        if not is_supported_input(input_file):
            messagebox.showwarning("提示", "只支持 PDF、PPT 和 PPTX 文件。")
            return

        self.btn_run.config(state="disabled", text="转换中...")
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self) -> None:
        input_file = self.input_path.get().strip()
        output_file = build_output_path(input_file)

        try:
            self.log(f"Input: {input_file}")
            self.log(f"Output: {output_file}")
            convert_file(input_file, output_file, logger=self.log)
            self.root.after(
                0,
                lambda: messagebox.showinfo("完成", f"文件已保存到：\n{output_file}"),
            )
        except Exception as exc:
            error_message = str(exc)
            self.log(f"转换失败: {error_message}")
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("错误", error_message))
        finally:
            self.root.after(0, lambda: self.btn_run.config(state="normal", text="开始转换"))


def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
