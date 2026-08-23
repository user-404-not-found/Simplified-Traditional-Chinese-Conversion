# 全自動簡繁轉換助手

一個輕量的 Windows 系統匣工具，選取文字後按下快捷鍵即可自動偵測並完成簡繁轉換，轉換結果直接原地貼回。

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 功能特色

- **自動識別模式**：自動判斷輸入為簡體或繁體，無需手動切換
- **強制模式**：可手動指定繁體→簡體或簡體→繁體（臺灣用語）
- **快捷鍵觸發**：選取文字後按 `Ctrl + Shift + Q`，轉換結果原地替換
- **系統匣常駐**：低資源佔用，右鍵選單切換模式
- **打包成單一執行檔**：免安裝 Python 環境，直接執行 `.exe`

---

## 使用方式

1. 執行 `簡繁轉換助手.exe`，系統匣會出現圖示
2. 在任意軟體中選取欲轉換的文字
3. 按下 `Ctrl + Shift + Q`
4. 文字自動轉換並原地貼回

右鍵點擊系統匣圖示可切換模式或結束程式。

---

## 轉換模式

| 模式 | 說明 |
|------|------|
| 自動識別轉換 | 自動判斷簡繁並轉換（預設） |
| 強制：繁體 → 簡體 | 使用 OpenCC `t2s` 設定 |
| 強制：簡體 → 繁體 | 使用 OpenCC `s2twp` 設定（臺灣用語） |

---

## 從原始碼執行

### 環境需求

- Python 3.10 以上
- Windows 10 / 11

### 安裝依賴

```bash
pip install pyperclip pystray pillow pynput opencc-python-reimplemented
```

### 執行

```bash
python 簡繁轉換.py
```

---

## 打包成 .exe

確保專案目錄中有 `logo.png` 與 `logo.ico`，執行以下指令：

```bash
pyinstaller --onefile --noconsole --uac-admin ^
  --add-data "logo.png;." ^
  --add-data "C:\path\to\opencc;opencc" ^
  --collect-data opencc ^
  --hidden-import opencc ^
  --hidden-import pyperclip ^
  --hidden-import pynput.keyboard._win32 ^
  --hidden-import pynput.mouse._win32 ^
  --name "簡繁轉換助手" ^
  --icon="logo.ico" ^
  簡繁轉換.py
```

> 將 `C:\path\to\opencc` 替換為你實際的 opencc 套件路徑，通常位於：  
> `你的conda環境\Lib\site-packages\opencc`

打包完成後，`dist\簡繁轉換助手.exe` 即可在無 Python 環境的電腦上直接執行。

---

## 專案結構

```
├── 簡繁轉換.py      # 主程式
├── logo.png         # 系統匣圖示（PNG）
├── logo.ico         # 打包用圖示（ICO）
└── README.md
```

---

## 已知問題與注意事項

- 轉換依賴模擬 `Ctrl+C` / `Ctrl+V`，在某些不支援快捷鍵複製貼上的輸入框中可能無效
- 部分防毒軟體可能攔截 pynput 的全域鍵盤監聽，需手動加入白名單或以系統管理員執行

---

## License

[MIT License](LICENSE)

Copyright (c) 2026
