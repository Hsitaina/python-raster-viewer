import tkinter as tk
from tkinter import ttk, filedialog
import geopandas as gpd
import matplotlib.pyplot as plt
import re


class ShapefileExplorer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Shapefile Explorer')
        self.geometry("400x400")
        # Load shapefile
        self.gdf = None  # Will be initialized on file import

        # Create GUI components
        self.attribute_var = tk.StringVar()
        self.chart_type_var = tk.StringVar(value='bar')

        # Create menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Import Shapefile',
                              command=self.import_shapefile)

        # Dropdown for selecting attribute
        self.attribute_dropdown = ttk.Combobox(
            self, values=[], textvariable=self.attribute_var)
        self.attribute_dropdown.pack()

        # Dropdown for selecting chart type
        chart_type_dropdown = ttk.Combobox(
            self, values=['bar', 'scatter', 'line'], textvariable=self.chart_type_var)
        chart_type_dropdown.pack()

        # Button to generate chart
        generate_chart_button = tk.Button(
            self, text='Generate Chart', command=self.generate_chart)
        generate_chart_button.pack()

    def import_shapefile(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Shapefiles', '*.shp')])
        if file_path:
            self.gdf = gpd.read_file(file_path)
            self.attribute_var.set(self.gdf.columns[0])
            self.attribute_dropdown['values'] = list(self.gdf.columns)

    def generate_chart(self):
        if self.gdf is None:
            tk.messagebox.showwarning(
                'Error', 'Please import a shapefile first.')
            return

        selected_attribute = self.attribute_var.get()
        chart_type = self.chart_type_var.get()
        selected_attribute = re.sub(r"[,'[\]]", "", selected_attribute).strip()
        # Generate chart based on user selection
        if chart_type == 'bar':
            plt.bar(self.gdf.index, self.gdf[selected_attribute])
        elif chart_type == 'scatter':
            plt.scatter(self.gdf.index, self.gdf[selected_attribute])
        elif chart_type == 'line':
            plt.plot(self.gdf.index, self.gdf[selected_attribute])

        plt.xlabel('Feature')
        plt.ylabel(selected_attribute)
        plt.title(f'{chart_type.capitalize()} Chart of {selected_attribute}')
        plt.show()


app = ShapefileExplorer()
app.mainloop()
