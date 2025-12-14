import tkinter as tk
from tkinter import ttk, messagebox

from generator import Generator  # 确保 Generator 类已经适配于 UI 使用


class PoetryGeneratorUI:
    def __init__(self, master):
        self.master = master
        master.title("交互式诗歌生成器")

        self.generator = Generator()  # 假设 Generator 已经正确配置

        # 输入关键词
        ttk.Label(master, text="输入关键词:").grid(row=0, column=0)
        self.keyword_entry = ttk.Entry(master, width=25)
        self.keyword_entry.grid(row=0, column=1)

        # 选择诗的长度
        ttk.Label(master, text="诗的长度:").grid(row=1, column=0)
        self.length_var = tk.IntVar(value=5)
        ttk.Radiobutton(master, text="五言", variable=self.length_var, value=5).grid(row=1, column=1)
        ttk.Radiobutton(master, text="七言", variable=self.length_var, value=7).grid(row=1, column=2)

        # 输入标签
        self.labels_entries = []
        labels_descriptions = [
            "生活经历标签 (0: 军事生涯, 1: 乡村生活, 2: 其他, -1: 不指定)",
            "历史背景标签 (0: 繁荣时代, 1: 动乱时代, -1: 不指定)",
            "是否存在量词 (0: 无, 1: 有, -1: 不指定)",
            "是否存在顶针修辞 (0: 无, 1: 有, -1: 不指定)",
            "是否存在天干地支 (0: 无, 1: 有, -1: 不指定)"
        ]
        for i, label in enumerate(labels_descriptions, 2):
            ttk.Label(master, text=label).grid(row=i, column=0)
            entry = ttk.Entry(master, width=5)
            entry.grid(row=i, column=1)
            self.labels_entries.append(entry)

        # 生成按钮
        ttk.Button(master, text="生成诗歌", command=self.generate_poem).grid(row=7, column=1, pady=5)

    def generate_poem(self):
        keyword = self.keyword_entry.get()
        length = self.length_var.get()
        labels = [int(entry.get()) if entry.get().isdigit() else -1 for entry in self.labels_entries]

        if not keyword:
            messagebox.showerror("错误", "请输入关键词")
            return

        try:
            lines, info = self.generator.generate_one(keyword, length, *labels, beam_size=20, verbose=1, manu=False)
            if lines:
                messagebox.showinfo("生成的诗歌", "\n".join(lines))
            else:
                messagebox.showerror("错误", "生成失败：" + info)
        except Exception as e:
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PoetryGeneratorUI(root)
    root.mainloop()
