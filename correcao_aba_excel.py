# -*- coding: latin-1 -*-
import pyperclip as pc
import time
import pyautogui as gui


def salva_arquivo_corretamente(caminho, pausa=6):
    if caminho:
        path = caminho.replace('/', r'"\"').replace('"', r'')

        pc.copy(path)
        gui.press('winleft')
        gui.PAUSE = 0.5
        gui.hotkey('Ctrl', 'v')
        gui.press('enter')
        time.sleep(pausa)
        gui.hotkey('ctrl', 'b')
        gui.hotkey('alt', 'f4')
