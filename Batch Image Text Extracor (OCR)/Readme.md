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

To install Tesseract OCR, you'll also need to install the Tesseract OCR engine. You can find installation instructions for various platforms on the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract).

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

![Ekran görüntüsü 2023-03-07 233026](https://user-images.githubusercontent.com/63750425/223665300-3741a12e-4c88-49db-a3db-678d640edf8e.png)
API view

![Ekran görüntüsü 2023-03-08 113749](https://user-images.githubusercontent.com/63750425/223665513-db850bfd-d890-4cef-9473-075ce77e61a1.png)
Zip file of extracted texts

![Ekran görüntüsü 2023-03-08 112905](https://user-images.githubusercontent.com/63750425/223665593-d8e6f69a-e6d7-4619-8115-bd964f646dfa.png)
![Ekran görüntüsü 2023-03-08 112848](https://user-images.githubusercontent.com/63750425/223665605-cc480535-aa1b-453d-ae61-bfdd4788dded.png)
Sample extracted texts

![Ekran görüntüsü 2023-03-08 112927](https://user-images.githubusercontent.com/63750425/223665825-801647ed-c8f3-47c3-979a-1feba934a1c4.png)
![Ekran görüntüsü 2023-03-08 112945](https://user-images.githubusercontent.com/63750425/223665817-54f40b98-4db8-4f8b-9ce0-16656ff83fac.png)

Images and texts are saved under the same name.
