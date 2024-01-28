import tkinter as tk
from tkinter import ttk, filedialog
from components.canvas_image import CanvasImage
from components.raster_manager import GeoTIFFExplorer
import matplotlib.pyplot as plt


class MainWindow(ttk.Frame):
    def __init__(self, mainframe, path):
        if path == "":
            path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tif;*.ttf")])
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Raster Viewer')
        self.master.geometry('800x600')
        # self.master.attributes("-fullscreen", True)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.bands_explorer = GeoTIFFExplorer(path)
        path = self.bands_explorer.apply_colormap(1)

        self.canvas = CanvasImage(self.master, path)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # Create a menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Create a "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import", command=self.import_image)

        # Create a "Bands" menu
        self.bands_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bands", menu=self.bands_menu)

        # Create a "Colormaps" menu
        self.colormap_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Colormaps", menu=self.colormap_menu)
        self.selected_colormap = tk.StringVar(value="viridis")
        self.update_colormap_menu()

        # Initialize band menu items and selected band
        self.band_items = []
        self.selected_band = tk.IntVar(value=1)  # Set default band to 1
        self.update_band_menu()

    def reinitialize(self, file_path):
        self.canvas.destroy()
        self.bands_explorer = GeoTIFFExplorer(file_path)
        self.bands_explorer.removeFiles()
        self.selected_band.set(1)  # Set selected band to 1
        self.selected_colormap.set("viridis")  # Set colormap to viridis
        file_path = self.bands_explorer.apply_colormap(
            self.selected_band.get(), self.selected_colormap.get())
        self.canvas = CanvasImage(self.master, file_path)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.update_band_menu()
        self.update_colormap_menu()

    def import_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tif;*.ttf")])
        if file_path:
            self.reinitialize(file_path)

    def update_band_menu(self):
        # Clear existing band menu items
        self.band_items = []
        self.bands_menu.delete(0, "end")

        # Get band count from the canvas
        band_count = self.bands_explorer.get_band_count()

        # Create band menu items
        for band_index in range(1, band_count + 1):
            item = self.bands_menu.add_radiobutton(
                label=f"Band {band_index}", variable=self.selected_band, value=band_index, command=lambda idx=band_index: self.toggle_band(idx))
            self.band_items.append(item)

    def update_colormap_menu(self):
        # Clear existing colormap menu items
        self.colormap_menu.delete(0, "end")

        colormaps = plt.colormaps()
        top_colormaps = colormaps[:10]

        # Create colormap menu items
        for colormap in top_colormaps:
            self.colormap_menu.add_radiobutton(
                label=colormap, variable=self.selected_colormap, value=colormap, command=lambda cmap=colormap: self.on_colormap_selected(cmap))

    def on_colormap_selected(self, colormap):
        self.selected_colormap.set(colormap)
        self.canvas.destroy()
        self.bands_explorer.removeFiles()
        self.bands_explorer.band_map = {}
        file_path = self.bands_explorer.apply_colormap(
            self.selected_band.get(), self.selected_colormap.get())
        self.canvas = CanvasImage(self.master, file_path)
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def toggle_band(self, band_index):
        # Update the canvas with the selected band
        file_path = ""
        if (band_index in self.bands_explorer.band_map):
            file_name = self.bands_explorer.band_map[band_index].strip()
            file_path = self.bands_explorer.generateOutputPath(
                file_name=file_name)
        else:
            file_path = self.bands_explorer.apply_colormap(
                band_index, self.selected_colormap.get())
        self.canvas.destroy()
        self.canvas = CanvasImage(self.master, file_path)
        self.canvas.grid(row=0, column=0, sticky="nsew")


filename = 'assets/geo.tif'
app = MainWindow(tk.Tk(), path=filename)
app.mainloop()
