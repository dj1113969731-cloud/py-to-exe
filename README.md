# Python Distribution Suite (Python 分发大师) v10.2 Master Build

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**Python Distribution Suite** 是一款工业级的 Python 脚本转可执行文件 (EXE) 解决方案，专为追求安全、稳定与跨平台兼容性的开发者设计。

---

## 🌟 版本对比 (Editions)

| 功能 (Feature) | 标准版 (Standard) | 专业版 (Professional) |
| :--- | :---: | :---: |
| GUI 可视化管理 | ✅ | ✅ |
| PyInstaller / Nuitka 引擎 | ✅ | ✅ |
| 一键环境清理 (Cleanup) | ✅ | ✅ |
| GitHub 资产自动生成 | ✅ | ✅ |
| **CVE 实时漏洞扫描** | ❌ | ✅ |
| **完整性保护与自修复** | ❌ | ✅ |
| **幽灵运行 (内存解密)** | ❌ | ✅ |
| **双向多架构支持** | ❌ (基础) | ✅ (高级) |

## 🚀 快速开始 (Getting Started)

### 1. 环境准备 (Prerequisites)
建议安装常用构建引擎：
```bash
pip install pyinstaller nuitka
```

### 2. 安装 (Installation)
克隆项目并安装依赖：
```bash
git clone https://github.com/YourName/python-distribution-suite.git
cd python-distribution-suite
pip install -r requirements.txt
```

### 3. 使用 (Usage)
启动主启动器选择版本：
```bash
python src/main.py
```
或直接运行特定版本：
- **标准版**: `python src/py转exe_std.py`
- **专业版**: `python src/py转exe_pro.py`

## 🛠️ 项目结构 (Repo Structure)
- `src/`: 核心源码 (Standard & Pro)
- `docs/`: 使用手册与技术文档
- `plugins/`: 扩展钩子
- `.github/`: CI/CD 自动化构建流程

## 📄 开源协议 (License)
本项目采用 [MIT License](LICENSE) 协议。
