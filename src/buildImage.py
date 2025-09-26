### 2024 Alex Poulin
import numpy as np

class ImageRefBuilder():
    #build EM plot
    #other is the object class that is calling the function
    def build_image(self, other, im):
        """sumary_line
        builds a plot based on the other objects plot references (for performance)
        
        Keyword arguments:
        other - image object that is calling the function
        im - image array (should be given directly)
        Return: return_description
        """
        #self.ax.clear() # discards the old graph
        if (other._plot_ref[0] is None):
            #print("new")
            #print(im)
            new_vmin = np.min(im)
            new_vmax = np.max(im)
            #print(f"vmin: {new_vmin}, vmax: {new_vmax}")
            plot_refs = other.ax.imshow(im, cmap='gray', vmin = new_vmin, vmax = new_vmax)
            #print(plot_refs)
            other._plot_ref[0] = plot_refs
        else:
            #print("override")
            #plot_refs = self.ax.imshow(self.tifArr[im], cmap='gray', vmin = self.vmin, vmax = self.vmax)
            #print(self.tifArr[im])
            other._plot_ref[0].set_data(im)
        if (other.vmax is not None and other.vmin is not None):
            other._plot_ref[0].set_clim(vmin=other.vmin, vmax=other.vmax)
        elif (other.vmin is not None):
            other._plot_ref[0].set_clim(vmin=other.vmin)
        elif (other.vmax is not None):
            other._plot_ref[0].set_clim(vmax=other.vmax)
            
        #print(type(other._plot_ref[0]))
        other.figure.tight_layout()
        other.canvas.draw()