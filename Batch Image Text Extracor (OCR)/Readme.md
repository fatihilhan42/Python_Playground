# Batch Image Text Extractor

This is a simple Flask web application that allows users to upload a zipped folder containing images, and then extracts the text from all the images in the folder using the Tesseract OCR library. The extracted text is then zipped up and made available for download.

## Prerequisites
To run this application, you'll need to have the following installed:

- Python 3.6 or higher
- Flask 2.0.1 or higher
- Tesseract OCR 4.1 or higher

You can install Flask and Tesseract OCR using pip:

```python
pip install Flask
pip install tesserocr
```

To install Tesseract OCR, you'll also need to install the Tesseract OCR engine. You can find installation instructions for various platforms on the Tesseract OCR GitHub page.

## Usage
To run the application, simply execute the **app.py** file:

```python
python app.py
```

The application will start up and you can access it by visiting http://localhost:5000/ in your web browser.

To use the application, follow these steps:

1. Click on the "Choose File" button and select the zipped folder containing the images you want to extract text from.
2. Click on the "Upload and download extracted text" button.
3. Wait for the application to extract the text from all the images in the folder. This may take some time depending on the number of images and the size of the files.
4. Once the text has been extracted, a ZIP file containing a text file for each image will be downloaded automatically. You can find the downloaded file in your web browser's downloads folder.

### License
This project is licensed under the MIT License - see the LICENSE file for details.