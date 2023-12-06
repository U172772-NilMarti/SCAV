import tkinter as tk
from PIL import Image, ImageTk
import Functions
from tkinter import StringVar, filedialog
from tkinter import ttk  # Importar ttk para el Combobox






def update_label():
    selected_video.set("Selected video is: " + Functions.return_path())

def update_label_output():
    selected_output.set("Selected output directory video is: " + Functions.return_output_path())




class VideoProcessingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video APP | SP3")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.add_background()
        self.create_main_menu()

    def add_background(self):
        image = Image.open("fondo2.jpg")
        photo = ImageTk.PhotoImage(image)

        background_label = tk.Label(self, image=photo)
        background_label.image = photo  # Keep a reference to the image to prevent garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_main_menu(self):
        title_label = tk.Label(self, text="Video APP | SP3", font=("Arial", 24), bg="#f0f0f0")
        title_label.pack(pady=20)

        converter_button = tk.Button(self, text="Video Converter", command=self.open_converter_menu, font=("Arial", 14), bg="#3fa9f5", fg="white")
        converter_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        comparator_button = tk.Button(self, text="Video Comparator", command=self.open_comparator_menu, font=("Arial", 14), bg="#3fa9f5", fg="white")
        comparator_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        editor_button = tk.Button(self, text="Video Editor", command=self.open_editor_menu, font=("Arial", 14), bg="#3fa9f5", fg="white")
        editor_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

    def open_converter_menu(self):
        converter_menu = tk.Toplevel(self)
        converter_menu.title("Video Converter")
        converter_menu.geometry("400x300")
        converter_menu.configure(bg="#f0f0f0")

        # Agregar fondo a la ventana del Video Converter
        converter_image = Image.open("fondoMenu.jpeg")
        converter_image = converter_image.resize((1250, 1200))

        converter_photo = ImageTk.PhotoImage(converter_image)

        converter_background_label = tk.Label(converter_menu, image=converter_photo)
        converter_background_label.image = converter_photo
        converter_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        converter_title_label = tk.Label(converter_menu, text="Video Converter", font=("Arial", 24), bg="#f0f0f0")
        converter_title_label.pack(pady=20)
        button_style = {"bg": "#3fa9f5", "fg": "white", "font": ("Arial", 12, "bold")}

        load_video_button = tk.Button(converter_menu, text="Selecciona el video que quieras convertir",
                                      command=lambda: [Functions.load_video(), update_label()],
                                      **button_style)
        #load_video_button.pack(pady=5, padx=20, ipadx=10, ipady=5)
        load_video_button.pack(pady=30, padx=20)

        global selected_video
        selected_video = StringVar()
        selected_video.set("Selected video is: " + Functions.return_path())

        label = tk.Label(converter_menu, textvariable=selected_video)
        label.pack(padx=20, pady=0)

        quality_options = ["720p", "1080p", "4K", "SD"]  # Opciones de calidad

        quality_options = ["360p", "480p", "720p", "1080p"]  # Opciones de calidad
        codec_options = ["VP8", "VP9", "h265", "AV1"]
        quality_combobox = ttk.Combobox(converter_menu, values=quality_options)
        codec_combobox = ttk.Combobox(converter_menu, values= codec_options)
        def selected_quality(event):
            selected_value = quality_combobox.get()
            print("Selected video quality:", selected_value)  # Imprimir la opción seleccionada
        def selected_codec(event):
            selected_codec = codec_combobox.get()
            print("Selected video quality:", selected_codec)  # Imprimir la opción seleccionada
        QUALITY_video_button = tk.Button(converter_menu, text="Selecciona la calidad de video", **button_style)
        QUALITY_video_button.pack(padx = 20, pady = 20)
        quality_combobox.pack(pady=5)
        quality_combobox.bind("<<ComboboxSelected>>", selected_quality)  # Función llamada al seleccionar una opción
        CODEC_video_button = tk.Button(converter_menu, text="Selecciona el codec de video", **button_style)
        CODEC_video_button.pack(padx = 30, pady = 30)
        codec_combobox.pack(pady=5)
        codec_combobox.bind("<<ComboboxSelected>>", selected_codec)  # Función llamada al seleccionar una opción
        output_video_button = tk.Button(converter_menu, text="Selecciona la ubicación donde quieras guardar el vídeo",
                                      command=lambda: [Functions.select_output_path(), update_label_output()],
                                      **button_style)
        output_video_button.pack(pady = 20)
        global selected_output
        selected_output = StringVar()
        selected_output.set("Selected output directory video is:" + Functions.return_output_path())

        label = tk.Label(converter_menu, textvariable=selected_output)
        label.pack(padx=20, pady=0)

        style = ttk.Style()
        style.configure('Circular.TButton', foreground='white', font=('Arial', 12))

        original_image = Image.open("boton.png")
        resized_image = original_image.resize((100, 100))  # Ajustar el tamaño de la imagen

        # Convertir la imagen redimensionada a un formato compatible con Tkinter
        circular_image = ImageTk.PhotoImage(resized_image)
        circular_button = ttk.Button(converter_menu, style='Circular.TButton', command = lambda: Functions.change_video_quality_codec(Functions.return_path(), Functions.return_output_path(), quality_combobox.get(), codec_combobox.get()))
        circular_button.config(image=circular_image, compound=tk.CENTER)

        circular_button.image = circular_image  # Conservar una referencia para evitar que la imagen sea eliminada por el recolector de basura
        circular_button.pack(pady=20)

        button_title_label = tk.Label(converter_menu, text="Press the button to convert!", font=("Arial", 24), bg="#f0f0f0")
        button_title_label.pack(pady = 0)

    def open_comparator_menu(self):
        comparator_menu = tk.Toplevel(self)
        comparator_menu.title("Video Comparator")
        comparator_menu.geometry("400x300")
        comparator_menu.configure(bg="#f0f0f0")

        # Agregar fondo a la ventana del Video Converter
        converter_image = Image.open("cine.jpg")
        converter_image = converter_image.resize((1250, 900))

        converter_photo = ImageTk.PhotoImage(converter_image)

        converter_background_label = tk.Label(comparator_menu, image=converter_photo)
        converter_background_label.image = converter_photo
        converter_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        converter_title_label = tk.Label(comparator_menu, text="Video Comparator", font=("Arial", 24), bg="#f0f0f0")
        converter_title_label.pack(pady=20)
        button_style = {"bg": "#3fa9f5", "fg": "white", "font": ("Arial", 12, "bold")}


        load_video1_button = tk.Button(comparator_menu, text="Cargar Video 1", command=lambda: Functions.load_video())
        load_video1_button.pack(pady=20)

        load_video2_button = tk.Button(comparator_menu, text="Cargar Video 2", command=lambda: Functions.load_video_2())
        load_video2_button.pack(pady=20)

        output_video_button = tk.Button(comparator_menu, text="Seleccionar ruta donde quieras guardar el video", command=lambda: Functions.select_output_path())
        output_video_button.pack(pady=20)

        compare_button = tk.Button(comparator_menu, text="Comparar Videos", command= lambda:Functions.combine_videos(Functions.return_path(), Functions.return_path2(), Functions.return_output_path()) )
        compare_button.pack(pady=20)







    def open_editor_menu(self):
        editor_menu = tk.Toplevel(self)
        editor_menu.title("Video Editor")
        editor_menu.geometry("400x300")
        editor_menu.configure(bg="#f0f0f0")

        editor_title_label = tk.Label(editor_menu, text="Video Editor", font=("Arial", 24), bg="#f0f0f0")
        editor_title_label.pack(pady=20)

        label = tk.Label(editor_menu, text="Coming Soon...", font=("Arial", 40))
        label.pack(pady=100)  # Ajustar el espacio alrededor del texto




        # Add more widgets and functionality for the editor menu

if __name__ == "__main__":
    app = VideoProcessingApp()
    app.mainloop()
