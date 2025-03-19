import os
import cv2
import numpy as np
import pytesseract
import pandas as pd
from PIL import Image
from pdf2image import convert_from_path
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

class DistrictInfoPipeline:
    def __init__(self):
        self.pdf_path = os.path.join(os.path.dirname(__file__), "data/district_info.pdf")
        self.temp_image = "temp_image.png"
        self.output_dir = "output_cells"
        
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=True)
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

    def convert_pdf_to_image(self):
        pages = convert_from_path(self.pdf_path, 500)
        pages[0].save(self.temp_image, 'PNG')

    def extract_table_cells(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        img = cv2.imread(self.temp_image)
        if img is None:
            raise ValueError("Error: Could not load image. Check the image path.")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
        horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
        
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
        vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
        
        h_contours = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        h_contours = h_contours[0] if len(h_contours) == 2 else h_contours[1]
        h_lines = []
        for contour in h_contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > img.shape[1] * 0.2:
                h_lines.append(y + h // 2)
        h_lines.sort()
        
        v_contours = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        v_contours = v_contours[0] if len(v_contours) == 2 else v_contours[1]
        v_lines = []
        for contour in v_contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > img.shape[0] * 0.15:
                v_lines.append(x + w // 2)
        v_lines.sort()
        
        if len(h_lines) < 2 or len(v_lines) < 2:
            edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=30)
            h_lines, v_lines = [], []
            if lines is not None:
                for rho, theta in lines[:, 0]:
                    angle = theta * 180 / np.pi
                    if abs(angle - 90) < 15 or abs(angle - 270) < 15:
                        v_lines.append(int(rho))
                    elif abs(angle) < 15 or abs(angle - 180) < 15:
                        h_lines.append(int(rho))
            h_lines.sort()
            v_lines.sort()
            
            if len(h_lines) < 2 or len(v_lines) < 2:
                raise ValueError("Could not detect table structure")
        
        cell_count = 0
        for i in range(len(h_lines) - 1):
            for j in range(len(v_lines) - 1):
                x1 = max(0, v_lines[j] - 5)
                x2 = min(img.shape[1], v_lines[j + 1] + 5)
                y1 = max(0, h_lines[i] - 5)
                y2 = min(img.shape[0], h_lines[i + 1] + 5)
                
                cell = img[y1:y2, x1:x2]
                cv2.imwrite(f"{self.output_dir}/cell_{i}_{j}.png", cell)
                cell_count += 1
        
        print(f"Extracted {cell_count} cells.")

    def extract_text_with_pytesseract(self, image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            img = cv2.medianBlur(img, 3)
            pil_img = Image.fromarray(img)
            text = pytesseract.image_to_string(pil_img, config='--psm 6').strip()
            if not text:
                text = pytesseract.image_to_string(pil_img, config='--psm 3').strip()
            return text if text else None
        except Exception:
            return None

    def extract_text_with_trocr(self, image_path):
        try:
            image = Image.open(image_path).convert("RGB")
            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
            generated_ids = self.model.generate(pixel_values)
            text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            text = text.strip()
            return text if text else "N/A"
        except Exception:
            return "N/A"

    def extract_text_from_image(self, image_path):
        text = self.extract_text_with_pytesseract(image_path)
        return text if text else self.extract_text_with_trocr(image_path)

    def process(self):
        self.convert_pdf_to_image()
        
        self.extract_table_cells()
        
        max_row = -1
        max_col = -1
        image_files = [f for f in os.listdir(self.output_dir) if f.endswith('.png') and f.startswith('cell_')]
        
        for filename in image_files:
            parts = filename.replace('cell_', '').replace('.png', '').split('_')
            row, col = int(parts[0]), int(parts[1])
            max_row = max(max_row, row)
            max_col = max(max_col, col)
        
        grid = [[None for _ in range(max_col + 1)] for _ in range(max_row + 1)]
        
        for filename in image_files:
            row, col = map(int, filename.replace('cell_', '').replace('.png', '').split('_'))
            image_path = os.path.join(self.output_dir, filename)
            grid[row][col] = self.extract_text_from_image(image_path)
        
        df = pd.DataFrame(grid)
        
        df.columns = df.iloc[0]
        df = df.drop(0)
        
        df.iloc[:, 0] = range(1, len(df) + 1)
        
        df = df.replace(r'\n', ' ', regex=True).infer_objects(copy=False)
        
        if os.path.exists(self.temp_image):
            os.remove(self.temp_image)
        for f in image_files:
            os.remove(os.path.join(self.output_dir, f))
        if os.path.exists(self.output_dir):
            os.rmdir(self.output_dir)
        
        return df