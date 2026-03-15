import time
import threading
import pyperclip
import pystray
from PIL import Image, ImageDraw
from pynput import keyboard
from opencc import OpenCC
import sys
import os


cc_s2twp = OpenCC('s2twp') 
cc_t2s = OpenCC('t2s')    

class QuickConverter:
    def __init__(self):
        
        self.mode = 'auto'
        self.kb_controller = keyboard.Controller()

    def convert_logic(self):
        
        try:
            
            time.sleep(0.3)
            
           
            with self.kb_controller.pressed(keyboard.Key.ctrl):
                self.kb_controller.tap('c')
            
            
            time.sleep(0.2)
            selected_text = pyperclip.paste()
            
            if not selected_text or not selected_text.strip():
                return

            final_text = None
            
            
            if self.mode == 'auto':
                
                as_simplified = cc_t2s.convert(selected_text)
                as_traditional = cc_s2twp.convert(selected_text)

                
                if selected_text != as_simplified:
                    final_text = as_simplified
                    print("自動識別：繁體 ➔ 簡體")
                
                elif selected_text != as_traditional:
                    final_text = as_traditional
                    print("自動識別：簡體 ➔ 繁體")
                else:
                    print("未偵測到需要轉換的內容")
                    return
            
            
            elif self.mode == 't2s':
                final_text = cc_t2s.convert(selected_text)
            elif self.mode == 's2twp':
                final_text = cc_s2twp.convert(selected_text)

            
            if final_text:
                pyperclip.copy(final_text)
                time.sleep(0.1)
                with self.kb_controller.pressed(keyboard.Key.ctrl):
                    self.kb_controller.tap('v')
                print(f"轉換完成")

        except Exception as e:
            print(f"轉換過程出錯: {e}")

    def on_activate(self):
        threading.Thread(target=self.convert_logic, daemon=True).start()

    def set_mode(self, mode):
        def inner(icon, item):
            self.mode = mode
            print(f"模式切換為: {mode}")
        return inner

    def create_image(self):
        """讀取外部圖示 logo.png"""
        icon_name = "logo.png"
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(base_path, icon_name)

        try:
            image = Image.open(icon_path)
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
            return image
        except Exception as e:
            
            image = Image.new('RGB', (64, 64), (46, 204, 113))
            dc = ImageDraw.Draw(image)
            dc.text((22, 20), "Auto", fill=(255, 255, 255))
            return image

    def run_tray(self):
        
        menu = pystray.Menu(
            pystray.MenuItem("自動識別轉換", self.set_mode('auto'), checked=lambda item: self.mode == 'auto'),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("強制：繁體 ➔ 簡體", self.set_mode('t2s'), checked=lambda item: self.mode == 't2s'),
            pystray.MenuItem("強制：簡體 ➔ 繁體", self.set_mode('s2twp'), checked=lambda item: self.mode == 's2twp'),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("結束", lambda icon: (icon.stop(), sys.exit()))
        )
        icon = pystray.Icon("Converter", self.create_image(), "全自動簡繁助手 (Ctrl+Shift+Q)", menu)
        icon.run()

    def run_hotkey(self):
        with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+q': self.on_activate
        }) as h:
            h.join()

if __name__ == "__main__":
    app = QuickConverter()
    threading.Thread(target=app.run_hotkey, daemon=True).start()
    app.run_tray()