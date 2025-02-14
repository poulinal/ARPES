### 2024 Alex Poulin
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QFileDialog
from src.commonWidgets import error_dialogue_com
        
        
        
class ArrayToVideo():
    def __init__(self, data, vmin, vmax, EnergyVMomentum):
        super().__init__()

        self.data = data
        self.vmin = vmin
        self.vmax = vmax
        self.window = EnergyVMomentum
        
        self.save_video()
        
    def saveVideo(self):
        # Get dimensions of each frame (assuming all frames have the same shape)
        frame_height, frame_width, _ = self.data[0].shape
        
        # a colormap and a normalization instance
        cmap = plt.cm.jet
        norm = plt.Normalize(vmin=self.vmin, vmax=self.vmax)

        # map the normalized data to colors
        # image is now RGBA (512x512x4) 
        image = cmap(norm(self.data))

        # Define video writer parameters
        output_filename, _ = QFileDialog.getSaveFileName(self, 'Save Video', '', 'Video Files (*.avi)')
        if output_filename:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 30.0  # Frames per second
            self.video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
        else:
            return error_dialogue_com(self, "Error", "Could not save video")
        
    def save_video(self):
        # Prompt user to select a file path to save the video
        file_path, _ = QFileDialog.getSaveFileName(self.window, 'Save Video', '', 'MP4 files (*.mp4);;All Files (*)')

        if file_path:
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change codec as necessary
            fps = 30.0  # Frames per second
            height, width = self.data[0].shape[:2]
            out = cv2.VideoWriter(file_path, fourcc, fps, (width, height))

            # Write frames to video
            cmap = plt.cm.jet
            norm = plt.Normalize(vmin=self.vmin, vmax=self.vmax)
            for frame in self.data:
                #image = cmap(norm(frame))
                fig, ax = plt.subplots()
                print(frame)
                ax.imshow(frame, cmap='gray', vmin = self.vmin, vmax = self.vmax)
                ax.axis('off')  # Optional: hide axis
                fig.canvas.draw()

                # Convert matplotlib figure to numpy array
                img_np = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint32)
                img_np = img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
                
                #print(img_np)

                img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                
                out.write(img_bgr)
                cv2.imshow("output", frame) 
                
                
                plt.close(fig)

            # Release the VideoWriter and close the file
            out.release()
            print(f'Video saved to: {file_path}')