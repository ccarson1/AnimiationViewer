import wx
import pygame
from pygame.locals import *
import os
from spriteviewer2 import SpriteViewer


class MyApp(wx.App):
    def OnInit(self):
        frame = SpriteViewer()
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()