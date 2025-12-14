import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading


class PoetryGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("诗歌生成器")

        # 设置长度
        self.length_var = tk.IntVar()
        self.length_var.set(5)

        # 设置布局
        ttk.Label(master, text="输入文件:").grid(row=0, column=0, sticky='w')
        self.input_entry = ttk.Entry(master, width=50)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(master, text="浏览...", command=self.load_input_file).grid(row=0, column=2, padx=5)

        ttk.Label(master, text="输出文件:").grid(row=1, column=0, sticky='w')
        self.output_entry = ttk.Entry(master, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(master, text="浏览...", command=self.save_output_file).grid(row=1, column=2, padx=5)

        ttk.Label(master, text="诗行长度:").grid(row=2, column=0, sticky='w')
        ttk.Radiobutton(master, text="五言", variable=self.length_var, value=5).grid(row=2, column=1, sticky='w')
        ttk.Radiobutton(master, text="七言", variable=self.length_var, value=7).grid(row=2, column=2, sticky='w')

        ttk.Button(master, text="生成诗歌", command=self.start_generation).grid(row=3, column=1, pady=10)

    def load_input_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def save_output_file(self):
        filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def start_generation(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        length = self.length_var.get()

        if not input_path or not output_path:
            messagebox.showerror("错误", "请指定输入和输出文件路径")
            return

        threading.Thread(target=self.generate_poems, args=(input_path, output_path, length)).start()

    def generate_poems(self, input_path, output_path, length):
        try:
            args = argparse.Namespace(inp=input_path, out=output_path, length=length, bsize=20, verbose=0, select=0)
            generate_file(args)  # 假设已经有了这个函数
            messagebox.showinfo("完成", "诗歌生成完成！")
        except Exception as e:
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PoetryGeneratorApp(root)
    root.mainloop()
