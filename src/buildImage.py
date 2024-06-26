import numpy as np

class ImageBuilder():
    #build EM plot
    #other is the object class that is calling the function
    def build_image(self, other, im):
        #self.ax.clear() # discards the old graph
        if (other._plot_ref[0] is None):
            #print("new")
            print(im)
            new_vmin = np.min(other.tifArr[im])
            new_vmax = np.max(other.tifArr[im])
            print(f"vmin: {new_vmin}, vmax: {new_vmax}")
            plot_refs = other.ax.imshow(other.tifArr[im], cmap='gray', vmin = new_vmin, vmax = new_vmax)
            print(plot_refs)
            other._plot_ref[0] = plot_refs
        else:
            #print("override")
            #plot_refs = self.ax.imshow(self.tifArr[im], cmap='gray', vmin = self.vmin, vmax = self.vmax)
            #print(self.tifArr[im])
            other._plot_ref[0].set_data(other.tifArr[im])
        if (other.vmax is not None and other.vmin is not None):
            other._plot_ref[0].set_clim(vmin=other.vmin, vmax=other.vmax)
        elif (other.vmin is not None):
            other._plot_ref[0].set_clim(vmin=other.vmin)
        elif (other.vmax is not None):
            other._plot_ref[0].set_clim(vmax=other.vmax)

        other.canvas.draw()