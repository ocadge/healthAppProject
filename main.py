import customtkinter
from tkintermapview import TkinterMapView
import requests
from PIL import Image
import os


class App(customtkinter.CTk):
    APP_NAME = "Health App"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.marker_list = []

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        # Create and configure CTk frames
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_header = customtkinter.CTkFrame(master=self, width=780, height=50, corner_radius=15, fg_color=None)
        self.frame_header.grid(row=0, columnspan=2, padx=5, pady=5, sticky="nesw")

        self.frame_map = customtkinter.CTkFrame(master=self, width=780, height=320, corner_radius=15, fg_color=None)
        self.frame_map.grid(row=1, rowspan=2, columnspan=2, padx=5, pady=5, sticky="nesw")

        self.frame_setting = customtkinter.CTkFrame(master=self, width=380, height=140, corner_radius=15, fg_color=None)
        self.frame_setting.grid(row=3, column=0, padx=5, pady=5, sticky="nesw")

        self.frame_tracker = customtkinter.CTkFrame(master=self, width=380, height=140, corner_radius=15, fg_color=None)
        self.frame_tracker.grid(row=3, column=1, padx=5, pady=5, sticky="nesw")

        # Header Frame

        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_header, values=["OpenStreetMap", "Google normal",
                                                                                      "Google satellite"],
                                                           command=self.change_map)
        self.map_option_menu.grid(row=0, column=1, padx=5, pady=5)

        self.entry = customtkinter.CTkEntry(master=self.frame_header,
                                            placeholder_text="Enter address", width=200)
        self.entry.grid(row=0, column=0, sticky="nesw", padx=5, pady=5)
        self.entry.bind("<Return>", self.search_event)

        # Map Frame
        self.frame_map.grid_columnconfigure(0, weight=1)
        self.frame_map.grid_rowconfigure(0, weight=1)
        self.frame_map.grid_rowconfigure(1, weight=1)

        res = requests.get('https://ipinfo.io/')
        data = res.json()

        user_loc = data['loc'].split(',')

        lat = float(user_loc[0])
        lon = float(user_loc[1])

        apikey = "9026ad74768e9c727ac1337f1bf32e3f"

        # res = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=european_aqi")
        res = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apikey}")
        data = res.json()
        print(data)

        self.map_widget = TkinterMapView(self.frame_map, corner_radius=0)
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_marker(lat, lon)
        self.map_widget.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

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

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def clear_marker(self):
        for marker in self.marker_list:
            marker.delete()

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.start()
