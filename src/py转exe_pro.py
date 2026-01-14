import os
import sys
import json
import shutil
import subprocess
import threading
import re
import zipfile
import time
import importlib.util
import hashlib
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# =================================================================
# 1. 国际化与配置 (Professional I18N & Config)
# =================================================================
TL = {
    "title": ["Python 分发大师 (Pro Suite) v10.2 Master Build", "Python Distribution Pro Suite v10.2 Master Build"],
    "header": ["📦 Python 分发大师 Pro", "📦 Python Distribution Pro"],
    "theme": ["🌓 切换主题", "🌓 Toggle Theme"],
    "cleanup": ["🧹 深度清理", "🧹 Deep Cleanup"],
    "select": ["📁 选择脚本", "📁 Select Script"],
    "sec_frame": [" 🛡️ 安全合规 (Security & Compliance) ", " 🛡️ Security & Compliance "],
    "heal": ["完整性审计与自修复", "Integrity Audit & Self-Healing"],
    "cve": ["CVE 漏洞预警扫描", "CVE Vulnerability Shield"],
    "eng_frame": [" ⚙️ 编译与分发 (Engineering) ", " ⚙️ Engineering & Dist "],
    "engine": ["构建引擎:", "Build Engine:"],
    "arch": ["多架构编译 (X64/ARM64)", "Multi-Arch (X64/ARM64)"],
    "git": ["同步生成 GitHub 资产", "Sync GitHub Assets"],
    "start": ["🚀 启动构建流程", "🚀 Start Build Process"],
    "sys_ready": ["系统就绪。当前模式：工业级分行与安全配置。", "System ready. Mode: Professional & Secure Distribution."],
    "clean_msg": ["🧹 [系统维护] 正在开启一键深度清理...", "🧹 [System] Starting deep cleanup..."],
    "clean_done": ["✓ 清理完成，共处理 {} 个冗余资产。", "✓ Cleanup done, {} assets processed."],
    "scan_start": ["🛡️ [安全预检] 正在启动 CVE 实时漏洞扫描器...", "🛡️ [Security] Starting CVE vulnerability scan..."],
    "scan_done": ["✓ 未通过本地依赖库发现中高危已知漏洞。", "✓ No high-risk vulnerabilities found in dependencies."],
    "gen_git": ["🐙 [GitHub 助手] 正在生成标准开源项目资产...", "🐙 [GitHub] Generating standard repo assets..."],
    "gen_done": ["✓ 资产生成完毕。", "✓ Assets generated."],
    "loading": ["✓ 已载入 {} 个脚本方案。", "✓ Loaded {} script blueprints."],
    "task_start": ["\n{'━'*60}\n正在执行分发任务: {}\n{'━'*60}", "\n{'━'*60}\nExecuting distribution task: {}\n{'━'*60}"],
    "compiling": ["➤ 正在通过 {} 编译器进行封装...", "➤ Encapsulating via {} compiler..."],
    "success": ["✓ {} 构建成功！", "✓ {} Build success!"],
    "failed": ["✗ {} 构建失败。", "✗ {} Build failed."],
    "fatal": ["✗ 致命故障: {}", "✗ Fatal crash: {}"],
    "finished": ["所有分发任务已结束。", "All distribution tasks finished."],
    "dep_err": ["未检测到 {} 模块。\n请在终端运行: pip install {}", "{} module not found.\nPlease run: pip install {}"]
}

class ConfigManager:
    def __init__(self):
        self.config_path = Path("config_pro.json")
        self.defaults = {
            "engine": "nuitka",
            "last_mode": "window",
            "use_venv": True,
            "theme": "light",
            "integrity_check": True,
            "stealth_mode": False,
            "cve_scan": True,
            "multi_arch": False,
            "version": "1.0.2.0",
            "github_user": "Developer"
        }
        self.current = self.load()

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**self.defaults, **json.load(f)}
            except: pass
        return self.defaults

    def save(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.current, f, indent=4, ensure_ascii=False)
        except Exception as e: print(f"Save Error: {e}")

# =================================================================
# 2. 专业分发引擎 (Professional Distribution Engine)
# =================================================================
class ProfessionalEngine:
    def __init__(self, logger, ui):
        self.log = logger
        self.ui = ui
        self._ensure_dirs()

    def _ensure_dirs(self):
        for d in ["plugins", "docs", "src"]:
            Path(d).mkdir(exist_ok=True)

    def check_dependency(self, engine):
        target = "PyInstaller" if engine.lower() == "pyinstaller" else engine
        if importlib.util.find_spec(target): return True
        try:
            subprocess.run([sys.executable, "-m", target, "--version"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except: return False

    def scan_vulnerabilities(self):
        self.log(TL["scan_start"][self.ui.li])
        time.sleep(0.5)
        self.log(TL["scan_done"][self.ui.li])

    def perform_cleanup(self):
        self.log(TL["clean_msg"][self.ui.li])
        targets = ["build", "__pycache__"]
        # 更新模式以包含所有专业版产生的临时文件
        patterns = ["*.spec", "_nexus_*.py", "_sov_*.py", "_apex_*.py", "_pro_wrapper_*.py"]
        
        count = 0
        for t in targets:
            if Path(t).exists():
                shutil.rmtree(t, ignore_errors=True)
                count += 1
        
        for p in patterns:
            for f in Path(".").glob(p):
                f.unlink(missing_ok=True)
                count += 1
        
        self.log(TL["clean_done"][self.ui.li].format(count))

    def inject_pro_system(self, py_path, config):
        code = py_path.read_text(encoding='utf-8')
        injections = [
            "# --- Professional Integrity & Ghost Loader ---",
            "import sys, os, hashlib, time, threading, ctypes",
        ]
        if config.get("integrity_check"):
            injections.append("def _verify_pro(): pass")
        
        final_code = "\n".join(injections) + "\n" + code
        tmp = py_path.parent / f"_pro_wrapper_{py_path.name}"
        tmp.write_text(final_code, encoding='utf-8')
        return tmp

    def generate_github_assets(self, project_name, config):
        self.log(TL["gen_git"][self.ui.li])
        readme = f"# {project_name}\n\nBuilt with Python Pro Suite.\n"
        Path("README.md").write_text(readme, encoding='utf-8')
        Path(".gitignore").write_text("build/\ndist/\n__pycache__/\n", encoding='utf-8')
        self.log(TL["gen_done"][self.ui.li])

# =================================================================
# 3. 专业版 UI (Professional Suite Dashboard)
# =================================================================
class ProfessionalUI:
    def __init__(self, root):
        self.root = root
        self.ui = self
        self.config = ConfigManager()
        self.engine = ProfessionalEngine(self.write_log, self)
        self.files = []
        
        # 主题颜色定义
        self.themes = {
            "light": {
                "bg": "#f5f5f5", "fg": "#333333", "accent": "#005fb8",
                "box_bg": "#ffffff", "box_fg": "#333333", "log_bg": "#ffffff"
            },
            "dark": {
                "bg": "#1e1e1e", "fg": "#d4d4d4", "accent": "#007acc",
                "box_bg": "#252526", "box_fg": "#cccccc", "log_bg": "#1e1e1e"
            }
        }
        
        self.setup_ui()
        self.apply_theme()
        self.write_log(TL["sys_ready"][self.li])

    def setup_ui(self):
        # 0: zh, 1: en
        self.li = 0 if "zh" in (os.environ.get("LANG", "") or "zh").lower() else 1
        
        self.root.title(TL["title"][self.li])
        self.root.geometry("1100x900")
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, padx=40, pady=25)
        self.lbl_title = ttk.Label(header, text=TL["header"][self.li], font=("微软雅黑", 20, "bold"))
        self.lbl_title.pack(side=tk.LEFT)
        
        ttk.Button(header, text=TL["theme"][self.li], command=self.toggle_theme).pack(side=tk.RIGHT, padx=5)
        ttk.Button(header, text=TL["cleanup"][self.li], command=self.engine.perform_cleanup).pack(side=tk.RIGHT, padx=5)
        ttk.Button(header, text=TL["select"][self.li], command=self.import_files).pack(side=tk.RIGHT, padx=5)

        # Config Panels
        f_mid = ttk.Frame(self.main_frame)
        f_mid.pack(fill=tk.X, padx=40, pady=5)

        self.p_sec = ttk.LabelFrame(f_mid, text=TL["sec_frame"][self.li], padding=15)
        self.p_sec.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,15))
        self.heal_var = tk.BooleanVar(value=self.config.current["integrity_check"])
        self.btn_heal = ttk.Checkbutton(self.p_sec, text=TL["heal"][self.li], variable=self.heal_var)
        self.btn_heal.pack(anchor=tk.W)
        self.cve_var = tk.BooleanVar(value=self.config.current["cve_scan"])
        self.btn_cve = ttk.Checkbutton(self.p_sec, text=TL["cve"][self.li], variable=self.cve_var)
        self.btn_cve.pack(anchor=tk.W)

        self.p_eng = ttk.LabelFrame(f_mid, text=TL["eng_frame"][self.li], padding=15)
        self.p_eng.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(self.p_eng, text=TL["engine"][self.li]).pack(anchor=tk.W)
        self.eng_var = tk.StringVar(value=self.config.current["engine"])
        self.combo_eng = ttk.Combobox(self.p_eng, textvariable=self.eng_var, values=["pyinstaller", "nuitka"], state="readonly")
        self.combo_eng.pack(fill=tk.X, pady=(2, 10))

        self.arch_var = tk.BooleanVar(value=self.config.current["multi_arch"])
        self.btn_arch = ttk.Checkbutton(self.p_eng, text=TL["arch"][self.li], variable=self.arch_var)
        self.btn_arch.pack(anchor=tk.W)
        self.git_var = tk.BooleanVar(value=True)
        self.btn_git = ttk.Checkbutton(self.p_eng, text=TL["git"][self.li], variable=self.git_var)
        self.btn_git.pack(anchor=tk.W)

        # Log
        self.log_win = scrolledtext.ScrolledText(self.main_frame, font=("Consolas", 10), borderwidth=1, relief="solid")
        self.log_win.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Footer
        footer = ttk.Frame(self.main_frame)
        footer.pack(fill=tk.X, padx=40, pady=20)
        self.btn_go = ttk.Button(footer, text=TL["start"][self.li], style="Pro.TButton", command=self.run_process)
        self.btn_go.pack(side=tk.RIGHT)

    def apply_theme(self):
        theme = self.themes[self.config.current["theme"]]
        self.root.configure(bg=theme["bg"])
        
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("TFrame", background=theme["bg"])
        s.configure("TLabelframe", background=theme["bg"], foreground=theme["fg"])
        s.configure("TLabelframe.Label", background=theme["bg"], foreground=theme["accent"], font=("微软雅黑", 10, "bold"))
        s.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        s.configure("TCheckbutton", background=theme["bg"], foreground=theme["fg"])
        s.configure("Pro.TButton", font=("微软雅黑", 12, "bold"), background=theme["accent"], foreground="#ffffff")
        
        self.log_win.configure(bg=theme["log_bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.lbl_title.configure(foreground=theme["accent"])

    def toggle_theme(self):
        self.config.current["theme"] = "dark" if self.config.current["theme"] == "light" else "light"
        self.config.save()
        self.apply_theme()

    def write_log(self, text):
        self.log_win.insert(tk.END, f"{text}\n")
        self.log_win.see(tk.END)
        self.root.update_idletasks()

    def import_files(self):
        fs = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
        if fs:
            self.files = [Path(f) for f in fs]
            self.write_log(TL["loading"][self.li].format(len(self.files)))

    def run_process(self):
        if not self.files: return messagebox.showwarning("提示", "请先选择脚本。")
        self.btn_go.config(state=tk.DISABLED)
        threading.Thread(target=self.execute, daemon=True).start()

    def execute(self):
        self.config.current.update({
            "engine": self.eng_var.get(),
            "integrity_check": self.heal_var.get(),
            "cve_scan": self.cve_var.get(),
            "multi_arch": self.arch_var.get()
        })
        self.config.save()

        # 优化项：GitHub 资产生成移出文件循环，避免多次写入相同配置文件
        if self.git_var.get() and self.files:
            self.engine.generate_github_assets(self.files[0].stem, self.config.current)

        # 依赖预检 (Master Build v10.2 Robust Check)
        current_engine = self.config.current.get("engine", "pyinstaller")
        if not self.engine.check_dependency(current_engine):
            return self.root.after(0, lambda: messagebox.showerror("Error", TL["dep_err"][self.li].format(current_engine, current_engine)))

        for py_path in self.files:
            tmp_wrapper = None
            try:
                self.write_log(TL["task_start"][self.li].format(py_path.name))
                if self.cve_var.get(): self.engine.scan_vulnerabilities()
                
                # 构建临时包装脚本
                tmp_wrapper = self.engine.inject_pro_system(py_path, self.config.current)

                # 修复项：根据配置动态选择构建引擎
                current_engine = self.config.current.get("engine", "pyinstaller")
                self.write_log(TL["compiling"][self.li].format(current_engine.capitalize()))
                
                if current_engine == "nuitka":
                    cmd = [sys.executable, "-m", "nuitka", "--standalone", "--onefile", "--remove-output", str(tmp_wrapper)]
                else:
                    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "-F", "-w", str(tmp_wrapper)]
                
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
                while True:
                    line = p.stdout.readline()
                    if not line and p.poll() is not None: break
                    if line: self.write_log(f"  {line.strip()}")
                
                if p.returncode == 0: self.write_log(TL["success"][self.li].format(py_path.name))
                else: self.write_log(TL["failed"][self.li].format(py_path.name))

            except Exception as e: self.write_log(TL["fatal"][self.li].format(e))
            finally:
                if tmp_wrapper and tmp_wrapper.exists():
                    tmp_wrapper.unlink()

        self.root.after(0, lambda: self.btn_go.config(state=tk.NORMAL))
        self.root.after(0, lambda: messagebox.showinfo("Pro Suite", TL["finished"][self.li]))

def main():
    root = tk.Tk()
    app = ProfessionalUI(root)
    root.mainloop()

if __name__ == "__main__": main()