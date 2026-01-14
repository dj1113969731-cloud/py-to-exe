def pre_build(files):
    print(f"🧩 [插件通知] 准备构建 {len(files)} 个项目...")

def on_success(file_path):
    print(f"🧩 [插件通知] 构建任务圆满成功: {file_path}")
