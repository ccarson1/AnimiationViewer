import wx
import pygame
from pygame.locals import *
import os


class MenuPanel(wx.Panel):
    def __init__(self, parent, on_create_callback, on_upload_callback, on_add_callback, on_remove_callback):
        super().__init__(parent, size=(300, -1), style=wx.BORDER_SIMPLE)
        self.SetBackgroundColour(wx.Colour(240, 240, 240))

        self.on_create_callback = on_create_callback
        self.on_upload_callback = on_upload_callback
        self.on_add_callback = on_add_callback
        self.on_remove_callback = on_remove_callback

        self.image_path = None  # Store the image path

        self.init_ui()

    def init_ui(self):
        # Menu buttons
        menu_sizer = wx.BoxSizer(wx.VERTICAL)

        self.game_type = wx.StaticBox(self, label="Type")
        type_sizer = wx.StaticBoxSizer(self.game_type, wx.HORIZONTAL)

        # Radio buttons
        self.top_down = wx.RadioButton(self, label="Top Down", style=wx.RB_GROUP)
        self.platform = wx.RadioButton(self, label="Platform")

        type_sizer.Add(self.top_down, 1, wx.EXPAND | wx.ALL, 5)
        type_sizer.Add(self.platform, 1, wx.EXPAND | wx.ALL, 5)

        #Orientation
        self.orient = wx.StaticBox(self, label="Orientation")
        orient_sizer = wx.StaticBoxSizer(self.orient, wx.HORIZONTAL)

        
        self.start_left = wx.RadioButton(self, label="Left", style=wx.RB_GROUP)
        self.start_right = wx.RadioButton(self, label="Right")

        orient_sizer.Add(self.start_left, 1, wx.EXPAND | wx.ALL, 5)
        orient_sizer.Add(self.start_right, 1, wx.EXPAND | wx.ALL, 5)

        # Create button
        create_btn = wx.Button(self, label="Create")
        create_btn.Bind(wx.EVT_BUTTON, self.on_create_clicked)

        # Upload Image button
        upload_btn = wx.Button(self, label="Upload Image")
        upload_btn.Bind(wx.EVT_BUTTON, self.on_upload_image)

        # Dynamic list section
        self.list_section = wx.StaticBox(self, label="Animations")
        list_section_sizer = wx.StaticBoxSizer(self.list_section, wx.VERTICAL)

        self.list_ctrl = wx.ListBox(self, style=wx.LB_SINGLE)
        list_section_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # Add and remove buttons
        add_element_btn = wx.Button(self, label="+ Add Animation")
        add_element_btn.Bind(wx.EVT_BUTTON, self.on_add_element)
        list_section_sizer.Add(add_element_btn, 0, wx.EXPAND | wx.ALL, 5)

        remove_element_btn = wx.Button(self, label="- Remove Animation")
        remove_element_btn.Bind(wx.EVT_BUTTON, self.on_remove_element)
        list_section_sizer.Add(remove_element_btn, 0, wx.EXPAND | wx.ALL, 5)

        # Add widgets to the main menu sizer
        # menu_sizer.Add(self.top_down, 0, wx.ALL | wx.EXPAND, 10)
        # menu_sizer.Add(self.platform, 0, wx.ALL | wx.EXPAND, 10)
        menu_sizer.Add(type_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # menu_sizer.Add(self.start_left, 0, wx.ALL | wx.EXPAND, 10)
        # menu_sizer.Add(self.start_right, 0, wx.ALL | wx.EXPAND, 10)
        menu_sizer.Add(orient_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        menu_sizer.Add(upload_btn, 0, wx.ALL | wx.EXPAND, 10)
        menu_sizer.Add(list_section_sizer, 1, wx.EXPAND | wx.ALL, 10)
        menu_sizer.Add(create_btn, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(menu_sizer)

    def on_create_clicked(self, event):
        """Callback function for the Create button"""
        if self.image_path:
            self.on_create_callback(self.image_path)  # Pass the image path to the callback
        else:
            wx.MessageBox("No image uploaded. Please upload an image first.", "Error", wx.ICON_ERROR)

    def on_upload_image(self, event):
        """Callback function for uploading an image"""
        with wx.FileDialog(self, "Open Image File", wildcard="Image files (*.png;*.jpg;*.bmp)|*.png;*.jpg;*.bmp",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            self.image_path = file_dialog.GetPath()  # Store the image path
            print(f"Image selected: {self.image_path}")  # Print image path for debugging

    def on_add_element(self, event):
        self.on_add_callback()

    def on_remove_element(self, event):
        selected_index = self.list_ctrl.GetSelection()
        if selected_index != wx.NOT_FOUND:
            self.on_remove_callback(selected_index)
        else:
            wx.MessageBox("No item selected to remove.", "Error", wx.ICON_ERROR)

