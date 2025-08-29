# CLI Weather Dashboard

A minimal Python CLI for real-time weather data using OpenWeatherMap API and SQLAlchemy.

## Features

- 🌤️ Current weather data
- 📅 5-day forecasts  
- 📊 Search history
- 🎯 Command-line and interactive modes

## Installation

1. Install dependencies: `pip install requests sqlalchemy`
2. Get API key from [OpenWeatherMap](https://openweathermap.org/api)
3. Replace API key in `lib/weather_api.py`

## Usage

### Interactive Mode
```bash
python lib/cli.py
```

### Command Line Mode
```bash
python lib/cli.py London
python lib/cli.py --city "New York" --unit F --forecast
```

## Functions

### `main_menu()`
- Displays menu options using tuples
- Validates user input (1-5)
- Routes to weather functions

### `weather_menu()`
- Gets current weather with city validation
- Uses tuple for temperature units: `("C", "F")`
- Saves search data as tuple to database
- Returns dictionary from API

### `forecast_menu()`
- Gets 5-day forecast with validation
- Processes list of forecast data
- Displays formatted results

### `view_searches()`
- Creates list of tuples from database: `[(id, city, temp, date)]`
- Displays search history

### `delete_search()`
- Validates search ID input
- Removes search from database

### `handle_command_line()`
- Parses command arguments using tuples
- Supports `--city`, `--unit`, `--forecast` flags
- Uses `sys.argv` list for arguments

## Data Structures

- **Lists**: Forecast data, search history, command arguments
- **Tuples**: Menu options, validation sets, database records  
- **Dictionaries**: API responses, weather data

## Architecture

- **weather_api.py**: API calls and formatting
- **models.py**: Database ORM classes
- **validators.py**: Input validation functions
- **cli.py**: Main interface and menu system