#!/usr/bin/env python3
import sys
from weather_api import get_current_weather, get_forecast, format_weather, format_forecast
from models import User, WeatherSearch, FavoriteCity

def print_header():
    print("\n" + "="*70)
    print("  WELCOME TO BARRAKHITTA'S WEATHER DASHBOARD  ".center(70))
    print()
    print("Welcome to my user-friendly platform that offers real time weather".center(70))
    print("updates, forecasts and climate trends for locations around the world".center(70))
    print("="*70)

def print_menu(title, options):
    print(f"\n{'='*20} {title} {'='*20}")
    for i, option in enumerate(options, 1): print(f"  {i}. {option}")
    print("-" * (40 + len(title)))

def get_input(prompt, default=None):
    return input(f"🔹 {prompt} [{default}]: ").strip() or default if default else input(f"🔹 {prompt}: ").strip()

def show_msg(msg, success=True): print(f"✅ {msg}" if success else f"❌ {msg}")

def main_menu():
    print_header()
    while True:
        options = (" Current Weather", " 5-Day Forecast", " View History", " Delete Search", " Users", " Favorites", " Exit")
        print_menu("User Stories", options)
        choice = get_input("Choose option (1-7)")
        actions = {"1": weather_menu, "2": forecast_menu, "3": view_searches, "4": delete_search, "5": user_menu, "6": favorites_menu}
        if choice in actions: actions[choice]()
        elif choice == "7": print("\n🌟 Thank you for using CLI Weather Dashboard! 🌟"); break
        else: show_msg("Invalid option. Choose 1-7.", False)

def weather_menu():
    city = get_input("Enter city name")
    if not city or len(city) < 2: return show_msg("City name must be at least 2 characters", False)
    unit = get_input("Temperature unit (C/F)", "C").upper()
    unit = unit if unit in ("C", "F") else "C"
    print("\n⏳ Fetching weather data...")
    weather = get_current_weather(city, unit)
    print(format_weather(weather))
    if "error" not in weather:
        try: WeatherSearch.create(1, city, weather["temperature"], weather["condition"]); show_msg("Search saved to history")
        except: pass

def forecast_menu():
    city = get_input("Enter city name")
    if not city or len(city) < 2: return show_msg("City name must be at least 2 characters", False)
    unit = get_input("Temperature unit (C/F)", "C").upper()
    print("\n⏳ Fetching 5-day forecast...")
    print(format_forecast(get_forecast(city, unit)))

def view_searches():
    print_menu("SEARCH HISTORY", [])
    data = WeatherSearch.get_all_for_cli()
    if data:
        print("📋 Recent Searches:")
        [print(f"  🔸 ID: {s[0]} | {s[1]} | {s[2]} | {s[3]}") for s in data]
    else: print("📭 No searches found")

def delete_search():
    view_searches()
    try:
        search = WeatherSearch.find_by_id(int(get_input("Enter search ID to delete")))
        if search: search.delete(); show_msg(f"Deleted search for {search.city}")
        else: show_msg("Search not found", False)
    except ValueError: show_msg("Please enter a valid number", False)

def user_menu():
    while True:
        print_menu("USER MANAGEMENT", ("➕ Create User", "👀 View Users", "🔙 Back"))
        choice = get_input("Choose option (1-3)")
        if choice == "1":
            name = get_input("Enter name")
            if name:
                city, unit = get_input("Default city (optional)"), get_input("Temperature unit (C/F)", "C").upper()
                show_msg(f"Created user: {User.create(name, city or None, unit).display_name}")
            else: show_msg("Name required", False)
        elif choice == "2":
            users = User.get_all_for_cli()
            if users: print("\n👥 Users:"); [print(f"  🔸 ID: {u[0]} | {u[1]} | {u[2]} searches") for u in users]
            else: print("👤 No users found")
        elif choice == "3": break

def favorites_menu():
    while True:
        print_menu("FAVORITE CITIES", ("➕ Add Favorite", "👀 View Favorites", "🔙 Back"))
        choice = get_input("Choose option (1-3)")
        if choice == "1":
            try:
                user_id, city = int(get_input("Enter user ID")), get_input("Enter city name")
                if city and User.find_by_id(user_id): show_msg(f"Added {FavoriteCity.create(user_id, city).display_city} to favorites")
                else: show_msg("Invalid user ID or city name", False)
            except ValueError: show_msg("Please enter a valid user ID", False)
        elif choice == "2":
            try:
                favs = FavoriteCity.get_user_favorites_for_cli(int(get_input("Enter user ID")))
                if favs: print("\n⭐ Favorite Cities:"); [print(f"  🔸 ID: {f[0]} | {f[1]}") for f in favs]
                else: print("⭐ No favorites found")
            except ValueError: show_msg("Please enter a valid user ID", False)
        elif choice == "3": break

def handle_command_line():
    if len(sys.argv) < 2: return False
    city, unit, forecast = None, "C", False
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--city" and i + 1 < len(sys.argv): city = sys.argv[i + 1]
        elif arg == "--unit" and i + 1 < len(sys.argv): unit = sys.argv[i + 1].upper() if sys.argv[i + 1].upper() in ("C", "F") else "C"
        elif arg == "--forecast": forecast = True
        elif not arg.startswith("--"): city = arg
    if not city: print("Usage: python cli.py [city] [--unit C/F] [--forecast]"); return True
    print(format_forecast(get_forecast(city, unit)) if forecast else format_weather(get_current_weather(city, unit)))
    return True

if __name__ == '__main__':
    try:
        if not handle_command_line(): main_menu()
    except KeyboardInterrupt: print("\n\n🌟 Thank you for using CLI Weather Dashboard! 🌟")