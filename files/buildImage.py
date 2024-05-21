class ImageBuilder():
    #build EM plot
    def buildImage(self, other, im):
        #self.ax.clear() # discards the old graph
        if (other._plot_ref[0] is None):
            #print("new")
            plot_refs = other.ax.imshow(other.tifArr[im], cmap='gray')
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