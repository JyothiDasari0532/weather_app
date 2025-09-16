import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# ---------------- STATE → CAPITAL MAPPING ----------------
STATE_CAPITALS = {
    "Andhra Pradesh": "Amaravati",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Dispur",
    "Bihar": "Patna",
    "Chhattisgarh": "Raipur",
    "Goa": "Panaji",
    "Gujarat": "Gandhinagar",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Odisha": "Bhubaneswar",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata",
    "Delhi": "New Delhi",
    "Jammu and Kashmir": "Srinagar",
    "Ladakh": "Leh"
}

# ---------------- WEATHER ICONS ----------------
WEATHER_ICONS = {
    0: "☀️ Clear Sky",
    1: "🌤️ Mainly Clear",
    2: "⛅ Partly Cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Fog",
    48: "🌫️ Rime Fog",
    51: "🌦️ Light Drizzle",
    61: "🌧️ Light Rain",
    63: "🌧️ Moderate Rain",
    65: "🌧️ Heavy Rain",
    71: "❄️ Snowfall",
    80: "🌦️ Rain Showers",
    95: "⛈️ Thunderstorm"
}

# ---------------- API FUNCTIONS ----------------
def get_city_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    response = requests.get(url).json()
    if "results" not in response:
        return None, None
    r = response["results"][0]
    return r["latitude"], r["longitude"]

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url).json()
    return response.get("current_weather", None)

# ---------------- GUI FUNCTIONS ----------------
def show_weather():
    state_name = city_entry.get().strip()
    if not state_name:
        messagebox.showwarning("Input Error", "Please enter a State name.")
        return

    if state_name not in STATE_CAPITALS:
        messagebox.showerror("Error", f"Only Indian States are supported!\n\nValid options:\n{', '.join(STATE_CAPITALS.keys())}")
        return

    capital = STATE_CAPITALS[state_name]
    lat, lon = get_city_coordinates(capital)
    if not lat or not lon:
        messagebox.showerror("Error", "Could not fetch location data.")
        return

    weather = get_weather(lat, lon)
    if not weather:
        messagebox.showerror("Error", "Weather data not available.")
        return

    code = weather["weathercode"]
    condition = WEATHER_ICONS.get(code, "🌍 Unknown")
    temp = weather["temperature"]
    wind = weather["windspeed"]

    result_text.set(
        f"{condition}\n\n"
        f"📍 {state_name} (Capital: {capital})\n"
        f"🌡 Temp: {temp} °C\n"
        f"💨 Wind Speed: {wind} km/h\n"
        f"⏰ Time: {weather['time']}"
    )

    search_history.insert("", "end", values=(state_name, capital, f"{temp} °C", condition, weather['time']))

def clear_weather():
    city_entry.delete(0, tk.END)
    result_text.set("")

def save_history():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["State", "Capital", "Temperature", "Condition", "Time"])
        for row in search_history.get_children():
            writer.writerow(search_history.item(row)["values"])
    messagebox.showinfo("Saved", f"Search history saved to {file_path}")

def delete_selected():
    selected = search_history.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a row to delete.")
        return
    for row in selected:
        search_history.delete(row)

def clear_history():
    for row in search_history.get_children():
        search_history.delete(row)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🌦 Smart Weather App - India Edition")
root.attributes('-fullscreen', True)
root.configure(bg="#e3f2fd")

heading = tk.Label(root, text="🌦 Smart Weather App (India States Only)",
                   font=("Arial", 32, "bold"), bg="#e3f2fd", fg="#0d47a1")
heading.pack(pady=20)

frame = tk.Frame(root, bg="#e3f2fd")
frame.pack(pady=20)

city_label = tk.Label(frame, text="Enter State Name: ",
                      font=("Arial", 20), bg="#e3f2fd", fg="#01579b")
city_label.pack(side=tk.LEFT, padx=5)

city_entry = tk.Entry(frame, font=("Arial", 20), width=25,
                      bg="#ffffff", fg="#000000")
city_entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(frame, text="Get Weather", command=show_weather,
                       font=("Arial", 16), bg="#0288d1", fg="white")
search_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(frame, text="Clear", command=clear_weather,
                      font=("Arial", 16), bg="#ff9800", fg="white")
clear_btn.pack(side=tk.LEFT, padx=5)

exit_btn = tk.Button(root, text="❌ Exit", command=root.quit,
                     font=("Arial", 16), bg="#b71c1c", fg="white")
exit_btn.pack(side=tk.BOTTOM, pady=15)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 22),
                        justify="center", bg="#e3f2fd", fg="#1a237e")
result_label.pack(pady=30)

history_label = tk.Label(root, text="📜 Search History",
                         font=("Arial", 20, "bold"),
                         bg="#e3f2fd", fg="#0d47a1")
history_label.pack()

history_frame = tk.Frame(root)
history_frame.pack(pady=10)

search_history = ttk.Treeview(history_frame,
                              columns=("State", "Capital", "Temp", "Weather", "Time"),
                              show="headings", height=6)
search_history.heading("State", text="State")
search_history.heading("Capital", text="Capital")
search_history.heading("Temp", text="Temperature")
search_history.heading("Weather", text="Condition")
search_history.heading("Time", text="Time")
search_history.column("State", width=200)
search_history.column("Capital", width=150)
search_history.column("Temp", width=150)
search_history.column("Weather", width=200)
search_history.column("Time", width=200)
search_history.pack()

# --- Buttons placed BELOW the history table ---
btn_frame = tk.Frame(root, bg="#e3f2fd")
btn_frame.pack(pady=10)

save_btn = tk.Button(btn_frame, text="💾 Save History", command=save_history,
                     font=("Arial", 16), bg="#2e7d32", fg="white")
save_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(btn_frame, text="🗑 Delete Selected", command=delete_selected,
                       font=("Arial", 16), bg="#c62828", fg="white")
delete_btn.pack(side=tk.LEFT, padx=10)

clear_hist_btn = tk.Button(btn_frame, text="🧹 Clear History", command=clear_history,
                           font=("Arial", 16), bg="#6a1b9a", fg="white")
clear_hist_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()
