import os
import sys
import requests
from tkinter import Tk, Label, Entry, Button, Frame, messagebox, PhotoImage, Canvas

# Helper function to find resources in a bundled application
def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller builds."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    api_key = "b63f710f8ae6e917cb702e045be148d7"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Query parameters
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract weather data
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            description = data['weather'][0]['description'].capitalize()

            # Display the result
            result = (f"City: {city.capitalize()}\n"
                      f"Temperature: {temperature}°C\n"
                      f"Humidity: {humidity}%\n"
                      f"Wind Speed: {wind_speed} m/s\n"
                      f"Description: {description}")
            result_label.config(text=result)
        else:
            error_message = data.get("message", "Unable to fetch weather data.").capitalize()
            messagebox.showerror("Error", f"API Error: {error_message}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

# Clear the weather data
def clear_weather():
    city_entry.delete(0, 'end')
    result_label.config(text="")

# Create the GUI application
app = Tk()
app.title("Weather App")
app.geometry("800x800")
app.resizable(False, False)

# Background Setup
background_color = "#e0f7fa"
app.configure(bg=background_color)

# Add Background Image
canvas = Canvas(app, width=600, height=600, bg=background_color)
canvas.pack(fill="both", expand=True)
background_img_path = resource_path("weather.png")  # Adjust for PyInstaller packaging
try:
    background_img = PhotoImage(file=background_img_path)
    canvas.create_image(0, 0, image=background_img, anchor="nw")
except Exception as e:
    print(f"Warning: Could not load background image: {e}")

# Header Frame
header_frame = Frame(app, bg="#00796b", height=60)
header_frame.place(relx=0.5, rely=0.1, anchor="center")
header_label = Label(header_frame, text="Weather App", font=("Helvetica", 20, "bold"), fg="white", bg="#00796b")
header_label.pack(pady=10)

# Input Frame
input_frame = Frame(app, bg=background_color)
input_frame.place(relx=0.5, rely=0.3, anchor="center")

city_label = Label(input_frame, text="Enter City:", font=("Helvetica", 14), bg=background_color)
city_label.grid(row=0, column=0, padx=10, pady=5)

city_entry = Entry(input_frame, font=("Helvetica", 14), width=25, relief="solid", borderwidth=2)
city_entry.grid(row=0, column=1, padx=10, pady=5)

# Button Frame
button_frame = Frame(app, bg=background_color)
button_frame.place(relx=0.5, rely=0.4, anchor="center")

fetch_button = Button(button_frame, text="Get Weather", font=("Helvetica", 14), bg="#4caf50", fg="white", relief="raised", command=get_weather)
fetch_button.grid(row=0, column=0, padx=10)

clear_button = Button(button_frame, text="Clear", font=("Helvetica", 14), bg="#f44336", fg="white", relief="raised", command=clear_weather)
clear_button.grid(row=0, column=1, padx=10)

# Result Display Frame
result_frame = Frame(app, bg=background_color)
result_frame.place(relx=0.5, rely=0.6, anchor="center")

result_label = Label(result_frame, text="", font=("Helvetica", 14), justify="left", anchor="nw", bg="white", fg="black", width=50, height=10, relief="groove", padx=10, pady=10)
result_label.pack()

# Footer Frame
footer_frame = Frame(app, bg="#00796b", height=30)
footer_frame.place(relx=0.5, rely=0.9, anchor="center")
footer_label = Label(footer_frame, text="Powered by OpenWeatherMap", font=("Helvetica", 10), fg="white", bg="#00796b")
footer_label.pack()

# Run the application
app.mainloop()
