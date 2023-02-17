import customtkinter
from tkintermapview import TkinterMapView
import requests
from PIL import Image
import os

res = requests.get('https://ipinfo.io/')
data = res.json()

city = data['city']
loc = data['loc'].split(',')

lat = float(loc[0])
lon = float(loc[1])


class App(customtkinter.CTk):
    APP_NAME = "Health App"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self):
        super().__init__()
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        # Create and configure CTk frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_map = customtkinter.CTkFrame(master=self, width=780, height=320, corner_radius=15, fg_color=None)
        self.frame_map.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nesw")

        self.frame_setting = customtkinter.CTkFrame(master=self, width=380, height=140, corner_radius=15, fg_color=None)
        self.frame_setting.grid(row=1, column=0, padx=10, pady=10, sticky="nesw")

        self.frame_tracker = customtkinter.CTkFrame(master=self, width=380, height=140, corner_radius=15, fg_color=None)
        self.frame_tracker.grid(row=1, column=1, padx=10, pady=10, sticky="nesw")

        # Map Frame
        self.frame_map.grid_columnconfigure(0, weight=1)
        self.frame_map.grid_rowconfigure(0, weight=1)
        self.frame_map.grid_rowconfigure(1, weight=1)

        self.map_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "map_icon.png")),
                                                size=(740, 200))
        self.pog_image = customtkinter.CTkImage(Image.open("images/map_icon.png"), size=(740, 200))

        self.map_label = customtkinter.CTkLabel(master=self.frame_map, width=740, height=200, corner_radius=15,
                                                image=self.pog_image, text="", anchor="nw")
        self.map_label.grid(row=0, rowspan=1, column=0, padx=2, pady=2, sticky="nesw")

        self.map_button = customtkinter.CTkButton(master=self.frame_map, width=740, height=80, corner_radius=15,
                                                  text="AQI and Temperature Map", font=("Arial", 30),
                                                  fg_color="transparent", anchor="w",  hover_color=("gray70", "gray30"),
                                                  text_color=("gray10", "gray90"))
        self.map_button.grid(row=1, column=0, padx=10, pady=10, sticky="nesw")

        # Settings Frame

        self.frame_setting.grid_columnconfigure(0, weight=1)
        self.frame_setting.grid_rowconfigure(0, weight=1)

        self.setting_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "settings_icon.png")),
                                                    size=(100, 100))

        self.setting_button = customtkinter.CTkButton(master=self.frame_setting, text="Settings", width=360, height=120,
                                                      font=("Arial", 30), corner_radius=15, fg_color="transparent",
                                                      image=self.setting_image, anchor="w",
                                                      hover_color=("gray70", "gray30"), text_color=("gray10", "gray90"))
        self.setting_button.grid(padx=10, pady=10, sticky="nesw")

        # Tracker Frame

        self.frame_tracker.grid_columnconfigure(0, weight=1)
        self.frame_tracker.grid_rowconfigure(0, weight=1)

        self.tracker_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "tracker_icon.png")),
                                                    size=(100, 100))

        self.tracker_button = customtkinter.CTkButton(master=self.frame_tracker, text="Health Tracker", width=360,
                                                      height=120, font=("Arial", 30), corner_radius=15,
                                                      fg_color="transparent", image=self.tracker_image, anchor="w",
                                                      hover_color=("gray70", "gray30"), text_color=("gray10", "gray90"))
        self.tracker_button.grid(padx=10, pady=10, sticky="nesw")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.start()
