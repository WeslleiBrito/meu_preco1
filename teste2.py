# -*- coding: latin-1 -*-
import pyperclip as pc

import pyautogui as gui
from localiza_nota import LocalizaNotaEntrada

# gui.alert(text="Inicializando o automação", title="Automação")

caminho = str(LocalizaNotaEntrada().caminho).replace('/', r'"\"')
caminho = caminho.replace('"', '')
print(caminho)
pc.copy(caminho)
gui.press('winleft')
gui.PAUSE = 0.5
gui.hotkey('Ctrl', 'v')
gui.press('enter')
gui.hotkey('ctrl', 'b')
gui.hotkey('alt', 'f4')

