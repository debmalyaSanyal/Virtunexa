import os
import sys
import requests
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Frame, messagebox, PhotoImage, Canvas, StringVar, OptionMenu
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Helper function to find resources in a bundled application
def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller builds."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to fetch weather data and forecast
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
            lon, lat = data['coord']['lon'], data['coord']['lat']

            # Display the result
            weather_icon = resource_path(f"icons/{description.lower().replace(' ', '_')}.png")
            try:
                icon = PhotoImage(file=weather_icon)
                icon_label.config(image=icon)
                icon_label.image = icon
            except:
                icon_label.config(image="")

            result = (f"🌍 City: {city.capitalize()}\n"
                      f"🌡️ Temperature: {temperature}°C\n"
                      f"💧 Humidity: {humidity}%\n"
                      f"🍃 Wind Speed: {wind_speed} m/s\n"
                      f"🌥️ Description: {description}")
            result_label.config(text=result)

            # Fetch forecast data
            fetch_forecast(lat, lon)
        else:
            error_message = data.get("message", "Unable to fetch weather data.").capitalize()
            messagebox.showerror("Error", f"API Error: {error_message}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

# Fetch and plot forecast data
def fetch_forecast(lat, lon):
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    api_key = "b63f710f8ae6e917cb702e045be148d7"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(forecast_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract hourly data
            times = []
            temps = []
            for forecast in data['list'][:8]:  # Get next 8 time slots (24 hours)
                time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                temp = forecast['main']['temp']
                times.append(time)
                temps.append(temp)

            # Plot the data
            plot_forecast(times, temps)
        else:
            messagebox.showerror("Error", "Unable to fetch forecast data.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

# Plot forecast data
def plot_forecast(times, temps):
    # Clear previous graph
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.plot(times, temps, marker='o', color='blue', label='Temperature')
    ax.set_title('24-Hour Temperature Forecast', fontsize=14, color="darkgreen")
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.legend()
    ax.grid(True)

    # Embed the graph in the Tkinter app
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Clear the weather data
def clear_weather():
    city_entry.delete(0, 'end')
    result_label.config(text="")
    icon_label.config(image="")
    for widget in graph_frame.winfo_children():
        widget.destroy()

# Create the GUI application
app = Tk()
app.title("Exciting Weather App 🌟")
app.geometry("800x800")
app.resizable(False, False)

# Background Setup
background_color = "#f0f4c3"
app.configure(bg=background_color)

# Add Background Image
canvas = Canvas(app, width=1000, height=900, bg=background_color)
canvas.pack(fill="both", expand=True)

# Header Frame
header_frame = Frame(app, bg="#8bc34a", height=60)
header_frame.place(relx=0.5, rely=0.1, anchor="center")
header_label = Label(header_frame, text="🌦️ Exciting Weather App", font=("Helvetica", 20, "bold"), fg="white", bg="#8bc34a")
header_label.pack(pady=10)

# Input Frame
input_frame = Frame(app, bg=background_color)
input_frame.place(relx=0.5, rely=0.3, anchor="center")

city_label = Label(input_frame, text="Enter City:", font=("Helvetica", 14), bg=background_color)
city_label.grid(row=0, column=0, padx=10, pady=5)

city_entry = Entry(input_frame, font=("Helvetica", 14), width=25, relief="solid", borderwidth=2)
city_entry.grid(row=0, column=1, padx=10, pady=5)

# Icon Label
icon_label = Label(app, bg=background_color)
icon_label.place(relx=0.5, rely=0.4, anchor="center")

# Result Frame
result_frame = Frame(app, bg=background_color)
result_frame.place(relx=0.5, rely=0.5, anchor="center")
result_label = Label(result_frame, text="", font=("Helvetica", 14), justify="left", anchor="nw", bg="white", fg="black", width=50, height=5, relief="groove", padx=10, pady=10)
result_label.pack()

# Graph Frame
graph_frame = Frame(app, bg=background_color)
graph_frame.place(relx=0.5, rely=0.8, anchor="center")

# Footer Frame
footer_frame = Frame(app, bg="#8bc34a", height=30)
footer_frame.place(relx=0.5, rely=0.95, anchor="center")
footer_label = Label(footer_frame, text="Powered by OpenWeatherMap 🌍", font=("Helvetica", 10), fg="white", bg="#8bc34a")
footer_label.pack()

# Buttons
button_frame = Frame(app, bg=background_color)
button_frame.place(relx=0.5, rely=0.6, anchor="center")

fetch_button = Button(button_frame, text="Get Weather 🎯", font=("Helvetica", 14), bg="#4caf50", fg="white", relief="raised", command=get_weather)
fetch_button.grid(row=0, column=0, padx=10)

clear_button = Button(button_frame, text="Clear 🗑️", font=("Helvetica", 14), bg="#f44336", fg="white", relief="raised", command=clear_weather)
clear_button.grid(row=0, column=1, padx=10)

# Run the application
app.mainloop()
