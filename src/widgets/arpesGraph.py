### 2025 Alexander Poulin
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.widgets.plottoolbar import matplotToolbar
import numpy as np

class arpesGraph(QWidget):
    def __init__(self):
        super().__init__()
        #figure vars:
        self.figure = Figure() # a figure instance to plot on
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure) # this is the Canvas Widget that displays the `figure`
        self.toolbar = matplotToolbar(self.canvas, self)
        #plot vars:
        self._plot_ref = [None, None] #first is main plot, second is line
        self.vmin = None
        self.vmax = None
        
        layout = QVBoxLayout()

        self.setLayout(layout)
        
        self.setup_graph()
        
    def setup_graph(self):
        widthPixels = 2080
        heightPixels = 810
        dpi = self.figure.get_dpi()
        widthInches = widthPixels / dpi
        heightInches = heightPixels / dpi
        self.figure.set_size_inches(widthInches, heightInches)

        self.figure.patch.set_facecolor('white')
        self.figure.patch.set_alpha(0)
        
        self.figure.tight_layout()
        self.canvas.setStyleSheet("background-color:transparent;")
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.ax.axis('off')  # Turn off axes
        self.ax.autoscale(False)
        self.figure.tight_layout()
    
    def update_graph(self, im):
        """sumary_line
        builds a plot based on the plot references (for performance)
        
        Keyword arguments:
        im - image array (should be given directly)
        Return: return_description
        """
        if (self._plot_ref[0] is None):
            new_vmin = np.min(im)
            new_vmax = np.max(im)
            plot_refs = self.ax.imshow(im, cmap='gray', vmin = new_vmin, vmax = new_vmax)
            self._plot_ref[0] = plot_refs
        else:
            self._plot_ref[0].set_data(im)
        if (self.vmax is not None and self.vmin is not None):
            self._plot_ref[0].set_clim(vmin=self.vmin, vmax=self.vmax)
        elif (self.vmin is not None):
            self._plot_ref[0].set_clim(vmin=self.vmin)
        elif (self.vmax is not None):
            self._plot_ref[0].set_clim(vmax=self.vmax)
            
        self.figure.tight_layout()
        self.canvas.draw()
        
    def change_colormap(self, text):
        self._plot_ref[0].set_cmap(text)
        self.canvas.draw()
        
        
    #resets the line
    def reset_line(self):
        self.textLineX.setText("")
        self.textLineY.setText("")
        self.textLineFinalX.setText("")
        self.textLineFinalY.setText("")
        
        
        self.lastx = None
        self.lasty = None
        self.startx = None
        self.starty = None
        
        
        #self.image_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.im)))
        self.resetButton.setStyleSheet("color : rgba(0, 0, 0, 0); background-color : rgba(0, 0, 0, 0); border : 0px solid rgba(0, 0, 0, 0);")
        self.resetButton.hide()
        
        #self.ax.cla()
        #self._plot_ref[1] = None
        self._plot_ref[1].set_xdata(0)
        self._plot_ref[1].set_ydata(0)
        ############ note this is just a bandaid fix, not really good practice ###############3
        self.canvas.draw()
        
    
    def toggleGaussian(self):
        self.gaussian = not self.gaussian
        self.imageBuilder.build_image(self, self.getImage())
        
        
     #start point on click
     
     
    def plot_mouse_click(self, e):
        self.resetButton.show()
        self.resetButton.setStyleSheet("")
        self.tracking = not self.tracking
        if e.inaxes:
            self.startx = e.xdata
            self.starty = e.ydata
            self.textLineX.setText(str(self.startx))
            self.textLineY.setText(str(self.starty))
        #print(f"startx: {self.startx}, starty: {self.starty}")
         
    def plot_mouse_move(self, e):
        if e.inaxes and self.tracking:
            #print("inaxes")
            pos = (e.xdata, e.ydata)
            self.lastx = e.xdata
            self.lasty = e.ydata
            self.make_line(pos)
            #print(f"lastx: {self.lastx}, lasty: {self.lasty}")
            
    #release stop tracking
    def plot_mouse_release(self, e):
        self.tracking = False
        
        
    def update_contrast(self, blackvalue, whitevalue):
        #print(f"black: {blackvalue}, white: {whitevalue}")
        self.vmin = blackvalue * self.maxcontrast
        self.vmax = whitevalue * self.maxcontrast
        self.label_left.setText(f"Left: {self.vmin:.2f}")
        self.label_right.setText(f"Right: {self.vmax:.2f}")
        #self.slider_right.setMinimum(value)
        #self._plot_ref[0].set_clim(vmin=self.vmin)
        self.imageBuilder.build_image(self, self.getImage())
        #self.update()
    
    def update_maxcontrast(self):
        self.maxcontrast = float(self.maxConstrastInput.text())
        self.label_right.setText(f"{self.maxcontrast:.2f}")
        
        
    #draws the line  
    def make_line(self, pos):
        if (self.startx is None or self.starty is None or self.lastx is None or self.lasty is None):
            return
        
        posExt, distance = self.extend_line(pos)
        #posExt starts from top left to whereever the line ends
        
        if self._plot_ref[1] is None:
            plot_refs = self.ax.plot(posExt[0], posExt[1], '-', color='yellow')
            self._plot_ref[1] = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref[1].set_xdata(posExt[0])
            self._plot_ref[1].set_ydata(posExt[1])
        #print(f"x_ext: {posExt[0]}, y_ext: {posExt[1]}")
        
        self.textLineFinalX.setText(str(pos[0]))
        self.textLineFinalY.setText(str(pos[1]))
        
        self.canvas.draw()
    
    def extend_line(self, pos):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim() #this is max height then the minimum

        distance = np.sqrt((pos[0] - self.startx)**2 + (pos[1] - self.starty)**2)
        
        if self.startx == pos[0]: #verticle line
            x_ext = np.full(int(ylim[0] - ylim[1]), self.startx)
            y_ext = np.linspace(ylim[1], ylim[0], int(ylim[0] - ylim[1]))
            return (x_ext, y_ext), distance 
        
        fx = np.polyfit([self.startx, pos[0]], [self.starty, pos[1]], deg=1)
        fy = np.polyfit([self.starty, pos[1]], [self.startx, pos[0]], deg=1)
        
        #here start means where xintercept is, and final means where the line would intersect with the upperbound of the box (i.e. the right side for x)
        xfinal = np.poly1d(fy)(xlim[1])
        yfinal = np.poly1d(fx)(ylim[0]) 
        xstart = np.poly1d(fy)(xlim[0])
        ystart = np.poly1d(fx)(ylim[1])
        
        xstart = np.clip(xstart, xlim[0], xlim[1]) #make sure it doesn't go out of bounds
        ystart = np.clip(ystart, ylim[1], ylim[0])
        xfinal = np.clip(xfinal, xlim[0], xlim[1])
        yfinal = np.clip(yfinal, ylim[1], ylim[0])

        if (min(xstart, xfinal) == xlim[0] and max(xstart, xfinal) == xlim[1]):
            #horizontal
            distance = np.sqrt((xlim[0] - xlim[1])**2 + (ystart - yfinal)**2)
            x_ext = np.linspace(xstart, xfinal, int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (min(ystart, yfinal) == ylim[1] and max(ystart, yfinal) == ylim[0]):
            #verticle
            distance = np.sqrt((xstart - xfinal)**2 + (ylim[1] - ylim[0])**2)
            y_ext = np.linspace(ystart, yfinal, int(distance))
            x_ext = np.poly1d(fy)(y_ext)
    
        elif (min(xstart, xfinal) == xlim[0] and min(ystart, yfinal) == ylim[1]):
            #left to top
            distance = np.sqrt((xlim[0] - max(xstart, xfinal))**2 + (max(ystart, yfinal) - ylim[1])**2)
            x_ext = np.linspace(xlim[0], max(xstart, xfinal), int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (max(xstart, xfinal) == xlim[1] and max(ystart, yfinal) == ylim[0]):
            #right to bottom
            distance = np.sqrt((xlim[1] - min(xstart, xfinal))**2 + (ylim[0] - min(ystart, yfinal))**2)
            x_ext = np.linspace(min(xstart, xfinal), xlim[1], int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (min(xstart, xfinal) == xlim[0] and max(ystart, yfinal) == ylim[0]):
            #left to bottom
            distance = np.sqrt((xlim[0] - max(xstart, xfinal))**2 + (min(ystart, yfinal) - ylim[0])**2)
            x_ext = np.linspace(xlim[0], max(xstart, xfinal), int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        elif (max(xstart, xfinal) == xlim[1] and min(ystart, yfinal) == ylim[1]):
            #right to top
            #print("right to top")
            distance = np.sqrt((xlim[1] - min(xstart, xfinal))**2 + (ylim[1] - max(ystart, yfinal))**2)
            x_ext = np.linspace(max(xstart, xfinal), xlim[0], int(distance))
            y_ext = np.poly1d(fx)(x_ext)
        else:
            #print("\n\nelse\n\n")
            #throw exception?
            #pure horizontal
            distance = xlim[1] - xlim[0]
            x_ext = np.linspace(xlim[0], xlim[1], int(distance))
            y_ext = np.linspace(ystart, ystart, int(distance))
        
        return (x_ext, y_ext), distance
        
    #interpolate the line to go across the image
    def interpl(self): 
        if (self.lastx is None or self.lasty is None or self.startx is None or self.starty is None):
            return
        posExt, distance = self.extend_line((self.lastx, self.lasty))
        #print(f"posExt: {posExt}")
        if (posExt[0] is None or posExt[1] is None):
            return #make sure there is a line to interpolate
        
        #maybe add some checks here to dumbproof
        
        #only return those points in the array which align with x_new and y_new
        #result = np.zeros(shape = (len(posExt[0]), len(posExt[1]))) #this will eventually be converted to image so should be height by width (height is number of images, width is distance of selection)
        #result = np.zeros(shape = (int(len(self.tifArr)), int(distance)))
        result = np.zeros(shape = (int(len(self.tifArr)), self.tifArr[0].shape[0])) #note shape is row, col
        imIndex = 0
        print(f"posExt: {posExt}")
        for tiffIm in self.tifArr:
            for i in range(result.shape[1] - 1):
                #data point on the exact point (note posExt[0] is x coordinates along line, posExt[1] is y coordinates along line)
                nearestXPix = int(posExt[0][i])
                nearestYPix = int(posExt[1][i])
                
                #gamma = self.distanceWeightedAverage(nearestXPix, nearestYPix, posExt[0], posExt[1], 2)
                #dataPoint = gamma * tiffIm[nearestXPix][nearestYPix]
                
                dataPoint = tiffIm[nearestXPix][nearestYPix]
                #dataPoint = self.distanceWeightedAverage(nearestXPix, nearestYPix, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix][nearestYPix]
                
                #posExt[0][i] gets the xpoint on that iteration
                
                cluster_data = 1 #amount of points we cluster --for average later
                #if (posExt[0][i] < 0 or posExt[0][i] >= 1024 or posExt[1][i] < 0 or posExt[1][i] >= 1024):
                #dataPoint += tiff_im[int(posExt[0][i])][int(posExt[1][i])]
                
                
                if (nearestXPix > 0): #can go to left for cluster
                    dataPoint += tiffIm[nearestXPix - 1][nearestYPix]
                    #dataPoint += self.distanceWeightedAverage(nearestXPix - 1, nearestYPix, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix - 1][nearestYPix]
                    cluster_data += 1
                    
                    #diagonal left up and down
                    if (nearestXPix > 0): #can go to up for cluster
                        dataPoint += tiffIm[nearestXPix - 1][nearestYPix - 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix - 1, nearestYPix - 1, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix - 1][nearestYPix - 1]
                    if (nearestXPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                        dataPoint += tiffIm[nearestXPix - 1][nearestYPix + 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix - 1, nearestYPix + 1, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix - 1][nearestYPix + 1]
                    
                if (nearestXPix < self.tifArr[0].shape[1] - 1): #can go to right for cluster
                    dataPoint += tiffIm[nearestXPix + 1][nearestYPix]
                    cluster_data += 1
                    #dataPoint += self.distanceWeightedAverage(nearestXPix + 1, nearestYPix, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix + 1][nearestYPix]
                    
                    #diagonal right up and down
                    if (nearestXPix > 0): #can go to up for cluster
                        dataPoint += tiffIm[nearestXPix + 1][nearestYPix - 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix + 1, nearestYPix - 1, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix + 1][nearestYPix - 1]
                    if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                        dataPoint += tiffIm[nearestXPix + 1][nearestYPix + 1]
                        cluster_data += 1
                        #dataPoint += self.distanceWeightedAverage(nearestXPix + 1, nearestYPix + 1, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix + 1][nearestYPix + 1]
                    
                if (nearestYPix > 0): #can go to up for cluster
                    dataPoint += tiffIm[nearestXPix][nearestYPix - 1]
                    cluster_data += 1
                    #dataPoint += self.distanceWeightedAverage(nearestXPix, nearestYPix - 1, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix][nearestYPix - 1]
                
                if (nearestYPix < self.tifArr[0].shape[0] - 1): #can go to down for cluster
                    dataPoint += tiffIm[nearestXPix][nearestYPix + 1]
                    cluster_data += 1
                    #dataPoint += self.distanceWeightedAverage(nearestXPix, nearestYPix + 1, posExt[0][i], posExt[1][i], 2) * tiffIm[nearestXPix][nearestYPix + 1]
                    
                if cluster_data > 1:
                    dataPoint = dataPoint / cluster_data
                
                
                
                if self.vmin is not None and self.vmax is not None:
                    #print(f"datapoint: {dataPoint}")
                    #dataPoint = (dataPoint - self.vmin) / (self.vmax - self.vmin)
                    dataPoint = np.clip(dataPoint, self.vmin, self.vmax)
                    #print(f"new datapoint: {dataPoint}")
                result[imIndex][i] = dataPoint
            imIndex += 1
            
        result = result.astype(float)
        #print(result)
        result = np.flip(result, axis=0)
        self.show_new_image(result)
        return
    
    
    def distanceWeightedAverage(self, x, y, x_new, y_new, p):
        ### p is the power of the distance
        ### x and y are the coordinates of the point we are trying to find the value of
        ### x_new and y_new are the coordinates of the point we are trying to find the value of
        ### returns the weighted average of the point
        gamma = 0
        for i in range(len(x_new)):
            gamma += (1 / (np.sqrt((x_new[i] - x)**2 + (y_new[i] - y)**2))**p)
        return gamma