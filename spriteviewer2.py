import wx
import pygame
from pygame.locals import *
import os
from animation_manager import AnimationManager

from menupanel import MenuPanel


class SpriteViewer(wx.Frame):
    def __init__(self):
        super().__init__(None, title="SpriteSheet Animator", size=(800, 600))

        # Main panel
        panel = wx.Panel(self)

        # Initialize MenuPanel
        self.menu_panel = MenuPanel(
            panel,
            self.on_create,
            self.on_upload_image,
            self.on_add_element,
            self.on_remove_element
        )

        # Right viewer panel
        self.viewer_panel = wx.Panel(panel, size=(600, -1), style=wx.BORDER_SIMPLE)
        self.viewer_panel.SetBackgroundColour(wx.Colour(0, 0, 0))

        # Use a sizer to divide the frame
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.menu_panel, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.viewer_panel, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        # Initialize Pygame in the viewer panel
        self.init_pygame(self.viewer_panel)

        # Initialize the animation manager
        self.animation_manager = AnimationManager()

        self.image_surface = None  # To hold the loaded image surface

        self.frames = []
        self.tick_count = 0
        self.animation_index = 0
        self.current_animation = None
        self.animation_speed = 5  # Adjust speed as needed
        self.last_direction = "left" 
        self.current_direction = ""

    def init_pygame(self, viewer_panel):
        hwnd = viewer_panel.GetHandle()
        os.environ['SDL_WINDOWID'] = str(hwnd)
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        pygame.init()
        self.screen = pygame.display.set_mode((600, 600), RESIZABLE)
        pygame.display.init()

        self.clock = pygame.time.Clock()
        self.running = True

        # Ensure self.image_surface is initialized
        self.image_surface = None

        # Set up a timer to integrate wx and Pygame
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_game, self.timer)
        self.timer.Start(1000 // 30)  # Run at ~30 FPS

    def update_game(self, event):
        # Handle events
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.running = False
                self.timer.Stop()
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.running = False
                    self.timer.Stop()
                elif evt.key == K_w:
                    self.current_animation = self.animation_manager.animations.get("walk_up", None)
                    print("Walking Up")
                elif evt.key == K_a:
                    self.current_animation = self.animation_manager.animations.get("walk_left", None)
                    self.last_direction = "left"  # Update direction
                    print("Walking Left")
                elif evt.key == K_s:
                    self.current_animation = self.animation_manager.animations.get("walk_down", None)
                    print("Walking Down")
                elif evt.key == K_d:
                    self.current_animation = self.animation_manager.animations.get("walk_right", None)
                    self.last_direction = "right"  # Update direction
                    print("Walking Right")
                
            elif evt.type == KEYUP:
                # Stop movement animation on key release
                if evt.key in (K_w, K_a, K_s, K_d):
                    self.current_animation = None
                    self.animation_index = 0

        # Default to idle animation if no current animation is set
        if not self.current_animation:
            self.current_animation = self.animation_manager.animations.get("idle", None)

        # Update the current animation frame
        if self.current_animation:
            self.tick_count += 1
            if self.tick_count >= self.animation_speed:
                self.tick_count = 0
                self.animation_index = (self.animation_index + 1) % self.current_animation["frames"]

        # Render the screen
        self.screen.fill((0, 0, 0))  # Clear screen
        if self.current_animation and self.frames:
            frame_width = self.current_animation["width"]
            frame_height = self.current_animation["height"]
            row = self.current_animation["row"]
            frame_x = self.animation_index * frame_width
            frame_y = row * frame_height

            # Calculate the rectangle for the current frame
            frame_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
            if 0 <= frame_rect.right <= self.image_surface.get_width() and 0 <= frame_rect.bottom <= self.image_surface.get_height():
                # Extract the current frame
                frame = self.image_surface.subsurface(frame_rect)

                # Flip the frame for idle animation if the last direction is left
                if self.current_animation == self.animation_manager.animations.get("idle", None):
                    if self.last_direction != self.current_direction:
                        frame = pygame.transform.flip(frame, True, False)
                        

                # Blit the frame to the screen
                self.screen.blit(frame, (200, 250))
            else:
                print(f"Warning: Frame out of bounds: {frame_rect}")

        pygame.display.flip()
        self.clock.tick(30)



    def load_image(self, image_path):
        """Load and display the image from the specified path"""
        try:
            self.image_surface = pygame.image.load(image_path)
            # Debug: Log original image dimensions
            print(f"Original image dimensions: {self.image_surface.get_width()}x{self.image_surface.get_height()}")
        except pygame.error as e:
            wx.MessageBox(f"Failed to load image: {e}", "Error", wx.ICON_ERROR)

    def on_create(self, image_path):
        """Callback function to handle the 'Create' button click."""
        self.load_image(image_path)

        if self.menu_panel.start_right.GetValue():
            self.current_direction = "right" 
        else:
            self.current_direction = "left" 
        # Debug: Check image dimensions
        if not self.image_surface:
            wx.MessageBox("Image not loaded or invalid.", "Error", wx.ICON_ERROR)
            return

        image_width = self.image_surface.get_width()
        image_height = self.image_surface.get_height()
        print(f"Loaded image dimensions: {image_width}x{image_height}")

        animations = self.animation_manager.get_animations()
        for name, anim in animations.items():
            width, height, frames, row = (
                anim["width"],
                anim["height"],
                anim["frames"],
                anim["row"],
            )
            
            # Debug: Log animation parameters
            print(f"Processing animation '{name}' with parameters: "
                f"Width={width}, Height={height}, Frames={frames}, Row={row}")

            for i in range(frames):
                rect = pygame.Rect(i * width, row * height, width, height)
                
                # Debug: Check if the rectangle fits within the image
                if rect.right > image_width or rect.bottom > image_height:
                    print(f"Error: Frame {i} for animation '{name}' is out of bounds: {rect}")
                    wx.MessageBox(f"Frame {i} for animation '{name}' is out of bounds. "
                                f"Image size: {image_width}x{image_height}, Rect: {rect}", 
                                "Error", wx.ICON_ERROR)
                    return

                frame = self.image_surface.subsurface(rect)
                self.frames.append(frame)
        
        print(f"Total frames loaded: {len(self.frames)}")

    def on_upload_image(self):
        with wx.FileDialog(self, "Open Image File", wildcard="Image files (*.png;*.jpg;*.bmp)|*.png;*.jpg;*.bmp",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path = file_dialog.GetPath()
            print(f"Loaded image: {path}")

    def on_add_element(self):
        # Create a dialog to input individual fields
        dialog = wx.Dialog(self, title="Add Animation Element", size=(300, 300))

        # Create the input fields with labels
        name_label = wx.StaticText(dialog, label="Name:", pos=(10, 10))
        # Create a dropdown (ComboBox) for selecting the animation name
        name_choices = ["idle", "walk_left", "walk_right", "walk_up", "walk_down"]
        name_combo = wx.ComboBox(dialog, choices=name_choices, pos=(100, 10), size=(120, -1), style=wx.CB_READONLY)

        width_label = wx.StaticText(dialog, label="Width:", pos=(10, 40))
        width_text = wx.TextCtrl(dialog, pos=(100, 40), size=(100, -1))

        height_label = wx.StaticText(dialog, label="Height:", pos=(10, 70))
        height_text = wx.TextCtrl(dialog, pos=(100, 70), size=(100, -1))

        frames_label = wx.StaticText(dialog, label="Frames:", pos=(10, 100))
        frames_text = wx.TextCtrl(dialog, pos=(100, 100), size=(100, -1))

        row_label = wx.StaticText(dialog, label="Row:", pos=(10, 130))
        row_text = wx.TextCtrl(dialog, pos=(100, 130), size=(100, -1))

        key_binding_label = wx.StaticText(dialog, label="Key Binding:", pos=(10, 160))
        key_binding_text = wx.TextCtrl(dialog, pos=(100, 160), size=(100, -1))

        

        # Create an OK button
        ok_button = wx.Button(dialog, label="OK", pos=(100, 190))

        # Bind the OK button to close the dialog and process the input
        def on_ok(event):
            try:
                # Get values from text controls and combo box
                name = name_combo.GetValue().strip()
                width = int(width_text.GetValue().strip())
                height = int(height_text.GetValue().strip())
                frames = int(frames_text.GetValue().strip())
                row = int(row_text.GetValue().strip())
                key_binding = key_binding_text.GetValue().strip()

                # Add the animation to the animation manager
                self.animation_manager.add_animation(name, width, height, frames, row, key_binding)

                # Create a summary element to add to the menu panel list
                element = f"{name} ({width}x{height}, {frames} frames, Row: {row}, Key: {key_binding})"
                self.menu_panel.list_ctrl.Append(element)
                print(f"Added element: {element}")

                # Close the dialog
                dialog.EndModal(wx.ID_OK)
            except ValueError as e:
                # Show error message if input is invalid
                wx.MessageBox("Invalid input format. Please enter valid numbers for width, height, frames, and row.", "Error", wx.ICON_ERROR)

        ok_button.Bind(wx.EVT_BUTTON, on_ok)

        # Show the dialog and wait for user interaction
        dialog.ShowModal()
        dialog.Destroy()


    def on_remove_element(self, selected_index):
        item = self.menu_panel.list_ctrl.GetString(selected_index)
        self.menu_panel.list_ctrl.Delete(selected_index)
        print(f"Removed element: {item}")


