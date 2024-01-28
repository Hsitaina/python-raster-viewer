import rasterio
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import uuid


class GeoTIFFExplorer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataset = rasterio.open(file_path)
        self.band_indexes = self.dataset.indexes
        self.ensure_folder_exists()
        self.removeFiles()
        self.band_map = {}

    def ensure_folder_exists(self, folder_path="output"):
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except OSError as e:
                print(f"Error creating folder '{folder_path}': {e}")

    def show_bands(self, band_index):
        band_data = self.dataset.read(band_index)

        # Plot the band using Matplotlib
        plt.figure(figsize=(8, 8))
        plt.imshow(band_data, cmap='viridis')
        plt.title(f'Band {band_index}')
        plt.colorbar()
        plt.show()

    def get_band_count(self):
        return self.dataset.count

    def get_composite_image(self, band_index):
        band_data = self.dataset.read(band_index)
        pil_img = Image.fromarray(band_data)
        return pil_img

    def generateOutputPath(self, file_name, output_directory="output"):
        return os.path.abspath(os.path.join(output_directory, file_name + ".tif"))

    def apply_colormap(self, band_index, cmap=None):
        if cmap == None:
            cmap = "viridis"
        gray_image = np.array(
            self.get_composite_image(band_index).convert('L'))
        colormap = plt.get_cmap(cmap)
        colored_image = (colormap(gray_image) * 255).astype(np.uint8)

        output_directory = "output"
        os.makedirs(output_directory, exist_ok=True)

        file_name = str(uuid.uuid4())
        output_image_path = self.generateOutputPath(file_name=file_name)
        self.band_map[band_index] = file_name

        Image.fromarray(colored_image).save(output_image_path)
        return output_image_path

    def removeFiles(self, output_directory="output"):
        file_list = os.listdir(output_directory)
        for file_name in file_list:
            file_path = os.path.join(output_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def close_dataset(self):
        if self.dataset:
            self.dataset.close()
