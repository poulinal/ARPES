### 2025 Alexander Poulin
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.widgets.plottoolbar import CustomToolbar
import numpy as np
from src.widgets.draggableText import DraggableRotatedText

class arpesGraph(QWidget):
    mouse_graphpos_change = pyqtSignal(float, float)
    mouse_graphpos_start = pyqtSignal(float, float)
    
    ##TODO: allow for nonlinear colorramps
    
    def __init__(self, graphtype="imshow"):
        super().__init__()
        #figure vars:
        self.figure = Figure() # a figure instance to plot on
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure) # this is the Canvas Widget that displays the `figure`
        self.toolbar = CustomToolbar(self.canvas, self)
        self.toolbar.exportData.connect(self.exportData)
        self.toolbar.resetButtonClicked.connect(self.resetCuts)
        #plot vars:
        # self._plot_ref = [None, None] #first is main plot, second is line
        self._plot_ref = {}
        self.vmin = None
        self.vmax = None
        self.scaledVmin = None
        self.scaledVmax = None
        self.maxcontrast = 10000
        self.tracking = False
        self.toggledLineCutMode = False
        self.toggledSegLineCutMode = False
        self.toggledBoxCutMode = False
        self.draggableText = None
        
        self.posExtended = None ##Todo should we really keep this as class var, is it possible to send by signal or preferably return it?
        self.posExtendedDistance = None
        
        
        # Connect the mouse events
        self.canvas.mpl_connect('button_press_event', self.plot_mouse_click) ###Todo make a signal out to arpesHome
        self.canvas.mpl_connect('motion_notify_event', self.plot_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.plot_mouse_release)
        
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        
        self.setup_graph()
        if graphtype == "imshow":
            self.setup_imshow()
        else:
            self.setup_basic_plot()
            
        
    def setup_graph(self):
        widthPixels = 2080
        heightPixels = 810
        dpi = self.figure.get_dpi()
        widthInches = widthPixels / dpi
        heightInches = heightPixels / dpi
        self.figure.set_size_inches(widthInches, heightInches)

        self.figure.patch.set_facecolor('white')
        self.figure.patch.set_alpha(0)
        
        # self.figure.tight_layout(True)
        self.canvas.setStyleSheet("background-color:transparent;")
        # self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(208, 81)
        
    def setup_imshow(self):
        self.ax.axis('off')  # Turn off axes
        self.ax.autoscale(True)
        # autoScaledFigSize = self.figure.get_size_inches()
        # self.ax.autoscale(False)
        # self.figure.set_size_inches(autoScaledFigSize) ###TOdo: make this better
        
        # self.ax.autoscale(False)
        self.figure.tight_layout(pad = 0, h_pad = 0, w_pad = 0, rect = [0, 0, 1, 1]) #pad is the padding between the figure and the axes, h_pad is the padding between the top and bottom of the figure, w_pad is the padding between the left and right of the figure, rect is the rectangle to which the figure is drawn
           
    def setup_basic_plot(self):
        self.ax.clear()
        self.ax.grid(True)
        self.ax.axis('on')
        self.ax.minorticks_on()
        self.ax.tick_params(axis='both', which='both', labelsize=8, colors='white')
        self.ax.set_xlabel('X-axis', color='white')
        self.ax.set_ylabel('Y-axis', color='white')
        self.ax.set_title('Basic Plot', color='white')
        self.canvas.draw()
        
    def setup_draggableText(self):
        # Set to top left of the plot
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        sizeX = (xlim[1] - xlim[0])
        sizeY = (ylim[1] - ylim[0])
        x_init = xlim[0] + int(sizeX * 0.1)
        y_init = ylim[1] - int(sizeY * 0.1)
    
        
        # Set to center of the plot
        self.centerX = sizeX / 2
        self.centerY = sizeY / 2
        
        
        # print(f"x_init, y_init: {x_init, y_init}, center: {self.centerX, self.centerY}")
        self.draggableText = DraggableRotatedText(
            self.ax, "eV: ", 
            x_init, y_init, 
            self.centerX, self.centerY,
            fontsize=6, fontweight='bold'
        )
    
    def setup_lincut_buttons(self):
        self.toolbar.add_lincut_button()
        self.toolbar.add_seg_lincut_button()
        self.toolbar.lineCutModeToggled.connect(self.toggleLineCutMode)
        self.toolbar.segLineCutModeToggled.connect(self.toggleSegLineCutMode)
        
    def setup_boxcut_button(self):
        self.toolbar.add_boxcut_button()
        self.toolbar.boxCutModeToggled.connect(self.toggleBoxCutMode)
        
    def setLabels(self, xlabel = None, ylabel = None, title = None):
        if xlabel is not None:
            self.ax.set_xlabel(xlabel, color='white')
        if ylabel is not None:
            self.ax.set_ylabel(ylabel, color='white')
        if title is not None:
            self.ax.set_title(title, color='white')
        self.canvas.draw()
        
    def getMaxContrast(self):
        return self.maxcontrast
    
    def getCurrentVminVmax(self):
        return self.vmin, self.vmax
    
    def setPlotRef(self, refIndex, value, changeX=False, changeY=False):
        if refIndex not in self._plot_ref.keys():
            print(f"WARNING... setPlotRef: refIndex {refIndex} not in plot_ref keys")
            return
        if changeX:
            self._plot_ref[refIndex].set_xdata(value)
        if changeY:
            self._plot_ref[refIndex].set_ydata(value)
            
    def draw_graph(self):
        self.canvas.draw()
        
    def toggleLineCutMode(self, checked):
        # print(f"toggling line cut mode to {checked}")
        if checked and self.getToggledSegLineCutMode():
            print("WARNING... turning off seg line cut mode")
            self.toolbar.toggle_seg_line_cut_mode(False)
        self.toggledLineCutMode = checked
        return self.toggledLineCutMode
    
    def toggleBoxCutMode(self, checked):
        self.toggledBoxCutMode = checked
        return self.toggledBoxCutMode
    
    def getToggledBoxCutMode(self):
        return self.toggledBoxCutMode
    
    def getToggledLineCutMode(self):
        return self.toggledLineCutMode
    
    def toggleSegLineCutMode(self, checked):
        # print(f"toggling seg line cut mode to {checked}")
        if checked and self.getToggledLineCutMode():
            print("WARNING... turning off line cut mode")
            self.toolbar.toggle_line_cut_mode(False)
        self.toggledSegLineCutMode = checked
        return self.toggledSegLineCutMode
    
    def getToggledSegLineCutMode(self):
        return self.toggledSegLineCutMode
    
    def toggleEnergyText(self, checked):
        if self.draggableText == None:
            print("WARNING... draggableText is None")
            return
        self.draggableText.set_visible(checked)
        
    def setEnergyText(self, energyValue):
        if self.draggableText == None:
            print("WARNING... draggableText is None")
            return
        self.draggableText.set_text(f"eV: {energyValue:.3f}")
        
    def exportData(self):
        """Export current plot data to CSV: #TODO currently saving line but want to save data"""
        try:
            filename = "exported_plot_data.csv"  # Default filename
            with open(filename, "w") as f:
                for ax in self.canvas.figure.get_axes():
                    lines = ax.get_lines()
                    for line in lines:
                        xdata = line.get_xdata()
                        ydata = line.get_ydata()
                        f.write("x,y\n")
                        for x, y in zip(xdata, ydata):
                            f.write(f"{x},{y}\n")
            print(f"Data exported to {filename}")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def update_im(self, im: np.ndarray, set_default_clim: bool = False, extent: tuple = None):
        """sumary_line
        builds a plot based on the plot references (for performance)
        
        Keyword arguments:
        im - image array (should be given directly)
        set_default_clim - if True, autosets the vmin and vmax to the min and max of the image
        extent - the extent of the image, if None, it will be set to (0, im.shape[1], 0, im.shape[0]), otherwise it should be a tuple of (xmin, xmax, ymin, ymax); example for evm it is: (0, result.shape[1], energiesLow, energiesHigh)
        Return: return_description
        """
        # self.ax.cla()  # Clear axes
        # self.ax.axis('off')  # If you want to keep axes off
        # self.canvas.draw()
        # print(f"shape of im: {im.shape}")
        # print(f"extent: {extent}")
        if extent is None:
            extentDefault = True
            extent = (0, im.shape[1], 0, im.shape[0]) #default extent is (xmin, xmax, ymin, ymax, yvalueAtMin, yvalueAtMax)
        else:
            extentDefault = False
            if len(extent) != 4:
                raise ValueError("extent should be a tuple of (xmin, xmax, ymin, ymax, yvalueAtMin, yvalueAtMax)")
            # print(f"update_im: im: {im.shape}")
            # print(f"nonzero im: {np.count_nonzero(im)}")

        if ('mainGraph' not in self._plot_ref.keys()):
            # print(f"update_im: self.__plot_ref is None")
            new_vmin = np.min(im)
            new_vmax = np.max(im)
            self.vmin = new_vmin
            self.vmax = new_vmax
            self.scaledVmax = new_vmax * self.maxcontrast
            self.scaledVmin = new_vmin * self.maxcontrast
            plot_refs = self.ax.imshow(im, cmap='gray', vmin = self.scaledVmin, vmax = self.scaledVmax, extent=extent, interpolation='bilinear')
            # plot_refs = self.ax.imshow(im, cmap='gray')
            self._plot_ref['mainGraph'] = plot_refs
        else:
            # print(f"update_im: self.__plot_ref is Not None")
            self._plot_ref['mainGraph'].set_data(im) #set data to im
            #correct range to plot entire range of data
            self.ax.set_xlim(0, im.shape[1]) #Todo do we need this?? before we did but now it seems to be messing up EVM with the extend
            self.ax.set_ylim(im.shape[0], 0)
            
            if set_default_clim == True:
                imMax = np.max(im)
                self._plot_ref['mainGraph'].set_clim(vmin = np.min(im), vmax = imMax)
                self.update_maxcontrast(imMax)
            elif (self.scaledVmax is not None and self.scaledVmin is not None):
                # print(f"update_im: scaledVmin, scaledVmax: {self.scaledVmin, self.scaledVmax}")
                self._plot_ref['mainGraph'].set_clim(vmin=self.scaledVmin, vmax=self.scaledVmax)
            elif (self.scaledVmin is not None):
                print(f"WARNING... update_im: only scaledVmin is not None")
                self._plot_ref['mainGraph'].set_clim(vmin=self.scaledVmin)
            elif (self.scaledVmax is not None):
                print(f"WARNING... update_im: only scaledVmax is not None")
                self._plot_ref['mainGraph'].set_clim(vmax=self.scaledVmax)
        
        self.ax.set_aspect(extent[1] / (extent[3] - extent[2]), anchor='C') #if not extentDefault else None #set aspect ratio to match the image
        self.ax.set_xlim(extent[0], extent[1]) #if not extentDefault else None #set xlim to match the image
        self.ax.set_ylim(extent[2], extent[3]) #if not extentDefault else None #set ylim to match the image
        
        
            
        # print(f"update_im before draw: vmin: {self.vmin}, vmax: {self.vmax}")
        # input("press enter to continue...")
        # self.figure.tight_layout()
        self.draw_graph()
        
    def change_colormap(self, text):
        self._plot_ref['mainGraph'].set_cmap(text)
        self.canvas.draw()
        
        
        
     #start point on click
    
    def getCanvas(self):
        """Returns the canvas of the graph"""
        return self.canvas
    
    def getFigureSize(self):
        return self.figure.get_size_inches()
     
    def plot_mouse_click(self, e):
        self.tracking = not self.tracking
        if e.inaxes:
            startx = e.xdata
            starty = e.ydata
            self.mouse_graphpos_start.emit(startx, starty)
        
    def resetCuts(self):
        if 'lineCut' in self._plot_ref.keys():
            self._plot_ref['lineCut'].remove()
            # del self._plot_ref['lineCut']
            self.canvas.draw()    
        if 'rectangleTop' in self._plot_ref.keys():
            self._plot_ref['rectangleTop'].remove()
            # del self._plot_ref['rectangleTop']
            self.canvas.draw()
        if 'rectangleBottom' in self._plot_ref.keys():
            self._plot_ref['rectangleBottom'].remove()
            # del self._plot_ref['rectangleBottom']
            self.canvas.draw()
        if 'rectangleLeft' in self._plot_ref.keys():
            self._plot_ref['rectangleLeft'].remove()
            # del self._plot_ref['rectangleLeft']
            self.canvas.draw()
        if 'rectangleRight' in self._plot_ref.keys():
            self._plot_ref['rectangleRight'].remove()
            # del self._plot_ref['rectangleRight']
            self.canvas.draw()
         
    def plot_mouse_move(self, e):
        if e.inaxes and self.tracking:
            #print("inaxes")
            pos = (e.xdata, e.ydata)
            self.lastx = e.xdata
            self.lasty = e.ydata
            self.mouse_graphpos_change.emit(pos[0], pos[1]) ###Todo double check if this is value or relative x-y
            # self.make_line(self.getPos())
            #print(f"lastx: {self.lastx}, lasty: {self.lasty}")
            
    #release stop tracking
    def plot_mouse_release(self, e):
        self.tracking = False
        
        
    def update_contrast(self, blackvalue, whitevalue):
        # print(f"black: {blackvalue}, white: {whitevalue}")
        if type(blackvalue) is float:
            self.vmin = blackvalue
            self.scaledVmin = blackvalue * self.maxcontrast
        if type(whitevalue) is float:
            self.vmax = whitevalue
            self.scaledVmax = whitevalue * self.maxcontrast
        
        return self.scaledVmax, self.scaledVmin
    
    def update_maxcontrast(self, maxContrastInput):
        """Given maxContrastInput, sets the maxcontrast and updates scaled vmin and vmax
        
        Keyword arguments:
        argument -- description
        Return: self.vmin, self.vmax
        """
        
        # print(f"maxContrastInput: {maxContrastInput}")
        self.maxcontrast = float(maxContrastInput)
        if self.vmin is not None and self.vmax is not None:
            # print(f"update_maxcontrast: vvmin and vmax is not none")
            self.scaledVmin = self.vmin * self.maxcontrast
            self.scaledVmax = self.vmax * self.maxcontrast
        # self.vmax = self.maxcontrast
        ###most of the time we will want to call update_contrast after
        return self.vmin, self.vmax
        # self.label_right.setText(f"{self.maxcontrast:.2f}")
        
    def update_line(self, xpos, ypos, colorline = 'yellow', extentSpace = None):
        if 'lineCut' not in self._plot_ref.keys():
            plot_refs = self.ax.plot(xpos, ypos, '-', color=colorline)
            self._plot_ref['lineCut'] = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref['lineCut'].set_xdata(xpos)
            self._plot_ref['lineCut'].set_ydata(ypos)
            
    def updateDCLine(self, xpos, ypos, extentSpace = None, transform = "None", colorline = 'blue'):
        xpos = np.array(xpos)  # Convert to NumPy array
        ypos = np.array(ypos)  # Convert to NumPy array
    
        if 'lineCut' not in self._plot_ref.keys():
            if extentSpace is not None and transform != "None":
                if transform == "x":
                    x_transformed = np.interp(xpos, (xpos.min(), xpos.max()), (extentSpace[0][0], extentSpace[0][1]))  # Map x to range [2, 8]
                    plot_refs = self.ax.plot(x_transformed, ypos, '-', color=colorline)
                elif transform == "y":
                    y_transformed = np.interp(ypos, (ypos.min(), ypos.max()), (extentSpace[1][0], extentSpace[1][1]))  # Map y to range [-0.5, 0.5]
                    plot_refs = self.ax.plot(xpos, y_transformed, '-', color=colorline)
            else:
                plot_refs = self.ax.plot(xpos, ypos, '-', color=colorline)
            self._plot_ref['lineCut'] = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref['lineCut'].set_xdata(xpos)
            self._plot_ref['lineCut'].set_ydata(ypos)
        
        
    #draws the line  
    def make_line_across(self, startx, starty, lastx, lasty):                                         
        if (startx == "" or starty == "" or lastx == "" or lasty == ""):
            print(f"WARNING... empty string where {startx, starty, lastx, lasty}")
            return
        
        if type(startx) is str or type(starty) is str or type(lastx) is str or type(lasty) is str: #cast to float
            startx = float(startx)
            starty = float(starty)
            lastx = float(lastx)
            lasty = float(lasty)
        else:
            print(f"WARNING... non string where {startx, starty, lastx, lasty}")

            return
        
        posExt, distance = self.extend_line(startx, starty, lastx, lasty)
        #posExt starts from top left to whereever the line ends
        
        self.update_line(posExt[0], posExt[1])
        
        
    def make_line_partial(self, startx, starty, lastx, lasty):
        """Creates a line from startx, starty to lastx, lasty
        
        Keyword arguments:
        startx -- x coordinate of the start point
        starty -- y coordinate of the start point
        lastx -- x coordinate of the end point
        lasty -- y coordinate of the end point
        """
        if (startx == "" or starty == "" or lastx == "" or lasty == ""):
            print(f"WARNING... empty string where {startx, starty, lastx, lasty}")
            return
        
        if type(startx) is str or type(starty) is str or type(lastx) is str or type(lasty) is str:
            startx = float(startx)
            starty = float(starty)
            lastx = float(lastx)
            lasty = float(lasty)
            
        distance = int(np.sqrt((lastx - startx)**2 + (lasty - starty)**2))
        
        if distance < 1:
            print(f"WARNING... distance is less than 1 pixel, not drawing line")
            return
        xpos = np.linspace(startx, lastx, distance)
        ypos = np.linspace(starty, lasty, distance)
        
        self.setPosExtended(xpos, ypos)
        self.setPosExtendedDistance(distance)
        
        
        self.update_line(xpos, ypos)
        # if 'lineCut' not in self._plot_ref:
        #     plot_refs = self.ax.plot([startx, lastx], [starty, lasty], '-', color='yellow')
        #     self._plot_ref['lineCut'] = plot_refs[0]
        # else:
        #     # We have a reference, we can use it to update the data for that line.
        #     self._plot_ref['lineCut'].set_xdata([startx, lastx])
        #     self._plot_ref['lineCut'].set_ydata([starty, lasty])
        # self.textLineFinalX.setText(str(lastx))
        # self.textLineFinalY.setText(str(lasty))
        # self.canvas.draw()
    
    def extend_line(self, startx, starty, lastx, lasty):
        
        xlim = self.ax.get_xlim() #this is max height then the minimum
        ylim = self.ax.get_ylim() 
        xlim = (xlim[0], xlim[1] - 1) #for some reason, these go from 0 to 1024 but tiffs are 1024 by 1024 (0 to 1023), so we need to subtract 1
        ylim = (max(ylim[0], ylim[1]) - 1, min(ylim[0], ylim[1])) #same here, but for y axis
        # print(f"xlim: {xlim}, ylim: {ylim}")

        distance = np.sqrt((lastx - startx)**2 + (lasty - starty)**2)
        
        if startx == lastx: #verticle line
            print(f"startx: {startx}, ylim: {ylim[0], ylim[1]}")
            x_ext = np.full(int(ylim[0] - ylim[1]), abs(startx))
            y_ext = np.linspace(ylim[1], ylim[0], int(ylim[0] - ylim[1]))
            return (x_ext, y_ext), distance 
        
        # Calculate slope and intercept for y = m*x + b
        if lastx - startx != 0:
            m = (lasty - starty) / (lastx - startx)
            b = starty - m * startx
        else:
            m = None  # vertical line, handled above
            b = None

        # For x as a function of y: x = (y - b) / m
        if lasty - starty != 0:
            m_inv = (lastx - startx) / (lasty - starty)
            b_inv = startx - m_inv * starty
        else:
            m_inv = None  # horizontal line
            b_inv = None

        # Define functions for y(x) and x(y)
        def fx(x):
            return m * x + b if m is not None else np.full_like(x, starty)

        def fy(y):
            return m_inv * y + b_inv if m_inv is not None else np.full_like(y, startx)
        
        #here start means where xintercept is, and final means where the line would intersect with the upperbound of the box (i.e. the right side for x)
        xfinal = fy(xlim[1])
        yfinal = fx(ylim[0]) 
        xstart = fy(xlim[0])
        ystart = fx(ylim[1])
        
        xstart = np.clip(xstart, xlim[0], xlim[1]) #make sure it doesn't go out of bounds
        ystart = np.clip(ystart, ylim[1], ylim[0])
        xfinal = np.clip(xfinal, xlim[0], xlim[1])
        yfinal = np.clip(yfinal, ylim[1], ylim[0])

        if (min(xstart, xfinal) == xlim[0] and max(xstart, xfinal) == xlim[1]):
            #horizontal
            distance = np.sqrt((xlim[0] - xlim[1])**2 + (ystart - yfinal)**2)
            x_ext = np.linspace(xstart, xfinal, int(distance))
            y_ext = fx(x_ext)
        elif (min(ystart, yfinal) == ylim[1] and max(ystart, yfinal) == ylim[0]):
            #verticle
            distance = np.sqrt((xstart - xfinal)**2 + (ylim[1] - ylim[0])**2)
            y_ext = np.linspace(ystart, yfinal, int(distance))
            x_ext = fy(y_ext)
    
        elif (min(xstart, xfinal) == xlim[0] and min(ystart, yfinal) == ylim[1]):
            #left to top
            distance = np.sqrt((xlim[0] - max(xstart, xfinal))**2 + (max(ystart, yfinal) - ylim[1])**2)
            x_ext = np.linspace(xlim[0], max(xstart, xfinal), int(distance))
            y_ext = fx(x_ext)
        elif (max(xstart, xfinal) == xlim[1] and max(ystart, yfinal) == ylim[0]):
            #right to bottom
            distance = np.sqrt((xlim[1] - min(xstart, xfinal))**2 + (ylim[0] - min(ystart, yfinal))**2)
            x_ext = np.linspace(min(xstart, xfinal), xlim[1], int(distance))
            y_ext = fx(x_ext)
        elif (min(xstart, xfinal) == xlim[0] and max(ystart, yfinal) == ylim[0]):
            #left to bottom
            distance = np.sqrt((xlim[0] - max(xstart, xfinal))**2 + (min(ystart, yfinal) - ylim[0])**2)
            x_ext = np.linspace(xlim[0], max(xstart, xfinal), int(distance))
            y_ext = fx(x_ext)
        elif (max(xstart, xfinal) == xlim[1] and min(ystart, yfinal) == ylim[1]):
            #right to top
            #print("right to top")
            distance = np.sqrt((xlim[1] - min(xstart, xfinal))**2 + (ylim[1] - max(ystart, yfinal))**2)
            x_ext = np.linspace(max(xstart, xfinal), xlim[0], int(distance))
            y_ext = fx(x_ext)
        else:
            #print("\n\nelse\n\n")
            #throw exception?
            #pure horizontal
            distance = xlim[1] - xlim[0]
            x_ext = np.linspace(xlim[0], xlim[1], int(distance))
            y_ext = np.linspace(ystart, ystart, int(distance))
            
        self.setPosExtended(x_ext, y_ext)
        self.setPosExtendedDistance(distance)
        
        # print(f"extended line: x_ext: {x_ext[0]}, last x_ext: {x_ext[len(x_ext) - 1]}, y_ext: {y_ext[0]}, last y_ext: {y_ext[len(y_ext) - 1]}, distance: {distance}")
        
        return (x_ext, y_ext), distance
    
    def setPosExtended(self, x_ext, y_ext):
        self.posExtended = (x_ext, y_ext)
        return self.posExtended
    
    def setPosExtendedDistance(self, distance):
        self.posExtendedDistance = distance
        return self.posExtendedDistance

    def getPosExtended(self):
        return self.posExtended  
    
    def getPosExtendedDistance(self):
        return self.posExtendedDistance
    
    #integrate over y
    def integrateY(self, evmData, startx, starty, lastx, lasty, extent, energies, extentXarr, extentYarr):
        typePlot = "MDC"
        #create new window
        
        
        if(startx is None or starty is None or lastx is None or lasty is None) or (startx == '' or starty == '' or lastx == '' or lasty == ''): #if none given, integrate over entire data
            print("Not given all four coords, so user defined box... integrating over entire dataset")
            selectedBox = evmData
        else:    
            print(f"evmData shape: {evmData.shape}, extent: {extent}, energies: {energies}, starty: {starty}, lasty: {lasty}, type energies: {type(energies), type(energies[0]), type(starty), type(lasty)}, {np.where(np.array(energies) == starty)}")
            yindexstart = np.where(np.array(energies) == starty)[0][0] if starty in energies else 0
            yindexlast = np.where(np.array(energies) == lasty)[0][0] if lasty in energies else evmData.shape[0] - 1
            
            selectedBox = evmData[int(min(yindexstart, yindexlast)): int(max(yindexstart, yindexlast)), int(min(startx, lastx)): int(max(startx, lastx))]
            
        #now given box, integrate over y
        mdcResult = np.zeros(shape = (1, selectedBox.shape[0])) #length of y
        print(f"mdcResults shape: {mdcResult.shape}")
        # for row in range(selectedBox.shape[0]): #range of result height
        #     mdcResult[0] += selectedBox[row]
        
        
        # Example: If selectedBox = [[1, 2, 3], [4, 5, 6]], summing columns gives [5, 7, 9], summing rows gives [6, 15]
        # To get [6, 15], sum across columns for each row (i.e., sum each row)
        mdcResult = np.sum(selectedBox, axis=1, keepdims=True).T  # shape (1, nrows), transpose to match output
        # mdcResult = np.sum(selectedBox, axis=1, keepdims=True)  # shape (nrows, 1)
        
        #example if given selectedBox = [[1, 2, 3], [4, 5, 6]], then summing over axis 0 (columns) gives [5, 7, 9], summing over axis 1 (rows) gives [6, 15]
        # mdcResult = np.sum(selectedBox, axis=0, keepdims=True)
        
        
        # for row in range(selectedBox.shape[0]): #range of result height
        #     for col in range(len(mdcResult[0])):
        #         mdcResult[0][row] += selectedBox[row][col]
        
        
        print(f"mdcResult: {mdcResult}, mdcResult shape: {mdcResult.shape}")
        mdcResult = mdcResult.astype(float)
        y = list(range(selectedBox.shape[0]))
        mdcResult = list(zip(mdcResult[0].tolist(), y))
        mdcResult = np.array(mdcResult).astype(float)
        print(f"mdcResult shape: {mdcResult.shape}, mdcResult: {mdcResult}")
        return mdcResult, yindexstart, yindexlast
    
    #Todo double check these integrations are correct
    
    #integrate over x
    def integrateX(self, evmData, startx, starty, lastx, lasty, extent, energies, extentXarr, extentYarr):
        typePlot = "EDC"
        #create new window
        if (startx is None or starty is None or lastx is None or lasty is None) or (startx == '' or starty == '' or lastx == '' or lasty == ''): #if none given, integrate over entire data
            print("Not given all four coords, so user defined box... integrating over entire dataset")
            # self.datax = 0
            # self.datay = self.evmData.shape[0]
            # self.dataLastx = self.energiesLow
            # self.dataLasty = self.energiesHigh
            selectedBox = evmData
        else:
            print(f"evmData shape: {evmData.shape}, extent: {extent}, energies: {energies}, starty: {starty}, lasty: {lasty}, type energies: {type(energies), type(energies[0]), type(starty), type(lasty)}, {np.where(np.array(energies) == starty)}")
            yindexstart = np.where(np.array(energies) == starty)[0][0] if starty in energies else 0
            yindexlast = np.where(np.array(energies) == lasty)[0][0] if lasty in energies else evmData.shape[0] - 1
            
            selectedBox = evmData[int(min(yindexstart, yindexlast)): int(max(yindexstart, yindexlast)), int(min(startx, lastx)): int(max(startx, lastx))]
            
            
            # print(f"startx, starty, lastx, lasty: {startx, starty, lastx, lasty}")
            # selectedBox = evmData[int(min(starty, lasty)): int(max(starty, lasty)), 
            #                           int(min(startx, lastx)): int(max(startx, lastx))]
        print(f"selectedbox: {selectedBox}")
            
        #now given box, integrate over x
        edcResult = np.zeros(shape = (1, selectedBox.shape[1])) #essentially length of x
        print(f"edcResult shape: {edcResult.shape}, rowRange: {selectedBox.shape[1]}, colRange: {len(evmData[0])}, box shape: {selectedBox.shape}")
        for col in range(selectedBox.shape[1]):
            for row in range(selectedBox.shape[0]): #range of result height
                edcResult[0][col] += selectedBox[row][col]
        print(f"edcResult: {edcResult}, edcResult shape: {edcResult.shape}")
        x = list(range(selectedBox.shape[1]))
        y = edcResult[0].tolist()
        edcResult = list(zip(x, y))
        edcResult = np.array(edcResult).astype(float)
        print(edcResult.shape, edcResult)
        return edcResult, yindexstart, yindexlast
        
        
    #create the boxed area
    def create_area(self, startx, starty, lastx, lasty):
        # if x0 or y0 or xf or yf: #TOdo secure if str not float
        x0 = float(startx)
        y0 = float(starty)
        xf = float(lastx)
        yf = float(lasty)
        xLength = abs(x0 - xf)
        yLength = abs(y0 - yf)
        dataTopX = np.linspace(x0, xf, int(xLength))
        dataTopY = np.linspace(y0, y0, int(xLength))
        dataBottomX = np.linspace(x0, xf, int(xLength))
        dataBottomY = np.linspace(yf, yf, int(xLength))
        dataLeftX = np.linspace(x0, x0, int(xLength))
        dataLeftY = np.linspace(y0, yf, int(xLength))
        dataRightX = np.linspace(xf, xf, int(xLength))
        dataRightY = np.linspace(y0, yf, int(xLength))
        
        # Note: With this reference below, we no longer need to clear the axis.
        #Note: this takes more to store the references, but it is faster
        if 'rectangleTop' not in self._plot_ref or 'rectangleBottom' not in self._plot_ref or 'rectangleLeft' not in self._plot_ref is None or 'rectangleRight' not in self._plot_ref:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.ax.plot(dataTopX, dataTopY, '-', color='yellow')
            self._plot_ref['rectangleTop'] = plot_refs[0]
            plot_refs = self.ax.plot(dataBottomX, dataBottomY, '-', color='yellow')
            self._plot_ref['rectangleBottom'] = plot_refs[0]
            plot_refs = self.ax.plot(dataLeftX, dataLeftY, '-', color='yellow')
            self._plot_ref['rectangleLeft'] = plot_refs[0]
            plot_refs = self.ax.plot(dataRightX, dataRightY, '-', color='yellow')
            self._plot_ref['rectangleRight'] = plot_refs[0]
            #print(f"dataTopX: {dataTopX}, dataTopY: {dataTopY}, dataBottomX: {dataBottomX}, dataBottomY: {dataBottomY}, dataLeftX: {dataLeftX}, dataLeftY: {dataLeftY}, dataRightX: {dataRightX}, dataRightY: {dataRightY}")
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref['rectangleTop'].set_ydata(dataTopY)
            self._plot_ref['rectangleTop'].set_xdata(dataTopX)
            self._plot_ref['rectangleBottom'].set_ydata(dataBottomY)
            self._plot_ref['rectangleBottom'].set_xdata(dataBottomX)
            self._plot_ref['rectangleLeft'].set_ydata(dataLeftY)
            self._plot_ref['rectangleLeft'].set_xdata(dataLeftX)
            self._plot_ref['rectangleRight'].set_ydata(dataRightY)
            self._plot_ref['rectangleRight'].set_xdata(dataRightX)
            #'''
        # self.canvas.draw()
        self.draw_graph()
        
        
              