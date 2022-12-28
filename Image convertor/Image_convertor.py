import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageConverter:
    def __init__(self, root):
        # Create the main window
        self.root = root
        self.root.title("Image Converter")
         # Set the window size and configure the grid layout
        self.root.geometry("1280x720")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

         # Load the background image and create a label to display it
        self.bg_image = ImageTk.PhotoImage(Image.open("D:/G-PYTHON/Basic_Python_Projects/Image convertor/bg.jpg"))
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(anchor="nw", relwidth=1, relheight=1)

       # Create the input label and text box
        self.input_label = tk.Label(self.root, text="Input Image:")
        self.input_label.grid(row=1, column=0, padx=20, pady=20)
        self.input_text = tk.Text(self.root, height=1, width=50)
        self.input_text.grid(row=2, column=0, padx=20, pady=10)

        ## Create the browse button
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_input)
        self.browse_button.grid(row=2, column=1, padx=20, pady=10)

        # Create the output label and dropdown
        self.output_label = tk.Label(self.root, text="Output Format:")
        self.output_label.grid(row=4, column=0, padx=20, pady=20)
        self.output_var = tk.StringVar(self.root)
        self.output_var.set("JPEG")
        self.output_dropdown = tk.OptionMenu(self.root, self.output_var, "JPEG", "PNG", "BMP", "GIF", "WEBP")
        self.output_dropdown.grid(row=6, column=0, padx=20, pady=10)

        # Create the convert button
        self.convert_button = tk.Button(self.root, text="Convert and save", command=self.convert)
        self.convert_button.grid(row=4, column=1, padx=20, pady=10)

    def browse_input(self):
        # Open a file dialog and update the input text box with the selected file
        filepath = filedialog.askopenfilename()
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", filepath)

        # Display the input image and the file name
        self.input_image = Image.open(filepath)
        self.input_image.thumbnail((200, 200))  # Resize the image to a maximum of 200x200 pixels
        self.input_image_tk = ImageTk.PhotoImage(self.input_image)
        self.input_image_label = tk.Label(self.root, image=self.input_image_tk)
        self.input_image_label.grid(row=3, column=0, padx=20, pady=20)
        self.input_name_label = tk.Label(self.root, text=filepath)
        self.input_name_label.grid(row=4, column=0, padx=20, pady=20)

            # Create the change button
        self.change_button = tk.Button(self.root, text="Change", command=self.change)
        self.change_button.grid(row=3, column=1, padx=20, pady=10)

    def change(self):
        # Clear the input text box and image label
        self.input_text.delete("1.0", tk.END)
        self.input_image_label.configure(image="")
        self.input_name_label.configure(text="")

        # Call the browse_input method to allow the user to select a new image
        self.browse_input()



    def convert(self):
        # Read the input image and convert it to the desired output format
        input_file = self.input_text.get("1.0", tk.END).strip()
        output_format = self.output_var.get()
        try:
            image = Image.open(input_file)
            output_file = filedialog.asksaveasfilename(defaultextension=output_format.lower())
            image.save(output_file)
            messagebox.showinfo("Success", "Image converted and saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", "Failed to convert and save image: " + str(e))


# Create the main window and start the application
root = tk.Tk()
app = ImageConverter(root)
root.mainloop()
