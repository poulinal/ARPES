import numpy as np
import matplotlib.pyplot as plt

class DraggableRotatedText:
    
    def __init__(self, ax, text, x, y, center_x, center_y, **text_kwargs):
        self.ax = ax
        self.center_x = center_x
        self.center_y = center_y
        self.press = None
        self.dragging = False
        
        # Create text object
        self.text_obj = self.ax.text(x, y, text, 
                                   picker=True, #pickradius=10,
                                #    bbox=dict(boxstyle="round,pad=0.3", 
                                        #    facecolor='yellow', 
                                        #    alpha=0.7),
                                        color='red',
                                        # fontname='Comic Sans MS',
                                   **text_kwargs)
        
        # Calculate and set initial rotation
        self.update_rotation()
        
        # Connect events
        self.text_obj.figure.canvas.mpl_connect('pick_event', self.on_pick)
        self.text_obj.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.text_obj.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.set_visible(False)
    
    def update_rotation(self):
        """Update text rotation to be tangential to radius from center"""
        x, y = self.text_obj.get_position()
        
        # Calculate angle from center to text position
        dx = x - self.center_x
        dy = y - self.center_y
        
        # Angle in degrees (tangent is perpendicular to radius)
        radius_angle = np.degrees(np.arctan2(dy, dx))
        tangent_angle = (radius_angle + 90)# % 360  # Perpendicular to radius

        # Mirror angle for readability and keep in [-90, 90]
        if tangent_angle > 90 and tangent_angle < 270:
            tangent_angle = ((tangent_angle + 180) % 360) - 180

        if tangent_angle > 90:
            tangent_angle -= 180
        elif tangent_angle < -90:
            tangent_angle += 180

        # print(f"Setting text angle to {tangent_angle} degrees")
        self.text_obj.set_rotation(tangent_angle)
    
    def on_pick(self, event):
        """Handle pick event - start dragging"""
        if event.artist == self.text_obj:
            self.press = (event.mouseevent.xdata, event.mouseevent.ydata)
            self.dragging = True
            
            # Highlight during drag
            # self.text_obj.set_bbox(dict(boxstyle="round,pad=0.3", 
            #                           facecolor='orange', alpha=0.8))
            self.text_obj.set_color('orange')
            self.ax.figure.canvas.draw_idle()
    
    def on_motion(self, event):
        """Handle motion event - drag text"""
        if self.dragging and self.press and event.inaxes == self.ax:
            # Calculate new position
            dx = event.xdata - self.press[0]
            dy = event.ydata - self.press[1]
            
            current_x, current_y = self.text_obj.get_position()
            new_x = current_x + dx
            new_y = current_y + dy
            
            # Update position
            self.text_obj.set_position((new_x, new_y))
            
            # Update rotation based on new position
            self.update_rotation()
            
            # Update press position for next move
            self.press = (event.xdata, event.ydata)
            
            self.ax.figure.canvas.draw_idle()
    
    def on_release(self, event):
        """Handle release event - stop dragging"""
        if self.dragging:
            self.dragging = False
            self.press = None
            
            # Remove highlight
            # self.text_obj.set_bbox(dict(boxstyle="round,pad=0.3", 
            #                           facecolor='yellow', alpha=0.7))
            self.text_obj.set_color('red')
            self.ax.figure.canvas.draw_idle()
    
    def set_text(self, text):
        """Update text content"""
        self.text_obj.set_text(text)
        self.ax.figure.canvas.draw_idle()
    
    def set_visible(self, visible):
        """Show/hide text"""
        self.text_obj.set_visible(visible)
        self.ax.figure.canvas.draw_idle()
    
    def set_center(self, center_x, center_y):
        """Update rotation center"""
        self.center_x = center_x
        self.center_y = center_y
        self.update_rotation()
        self.ax.figure.canvas.draw_idle()