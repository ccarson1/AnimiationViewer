import wx
import pygame
from pygame.locals import *
import os

class AnimationManager:
    def __init__(self):
        self.animations = {}  # Store animation data by name
        self.key_bindings = {}
        self.current_animation = None
        self.current_frame = 0

    def add_animation(self, name, width, height, frames, row, key_binding):
        self.animations[name] = {
            "width": width,
            "height": height,
            "frames": frames,
            "row": row
        }
        self.key_bindings[key_binding] = name

    def get_animations(self):
        return self.animations

    def play_animation(self, name):
        self.current_animation = name
        self.current_frame = 0

    def handle_key_event(self, event_key):
        for animation_name, animation_data in self.animations.items():
            if animation_data["key_binding"] == event_key:
                self.play_animation(animation_name)
                break

    def update(self):
        if self.current_animation:
            animation_data = self.animations[self.current_animation]
            frames = animation_data["frames"]
            self.current_frame = (self.current_frame + 1) % len(frames)
            return frames[self.current_frame]
        return None

    def get_current_frame(self):
        if self.current_animation:
            animation_data = self.animations[self.current_animation]
            frames = animation_data["frames"]
            return frames[self.current_frame]
        return None
    
    def get_frames_by_key(self, key):
        animation_name = self.key_bindings.get(key)
        if animation_name:
            return self.animations[animation_name]["frames"]
        return None
    
    def remove_animation(self, name):
        """Remove an animation by name"""
        if name in self.animations:
            del self.animations[name]
        else:
            print(f"Animation {name} not found!")
