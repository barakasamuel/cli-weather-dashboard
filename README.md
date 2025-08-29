# CLI Weather Dashboard

A minimal Python CLI for real-time weather data using OpenWeatherMap API and SQLAlchemy.

## Features

- Current weather data
- 5-day forecasts  
- Search history
- User management
- Favorite cities
- Command-line and interactive modes

## Installation

1. Install dependencies: `pip install requests sqlalchemy`
2. Get API key from [OpenWeatherMap](https://openweathermap.org/api)
3. Replace API key in `lib/weather_api.py`

## Usage

### Interactive Mode
```bash
python3 lib/cli.py
```

### Command Line Mode
```bash
python3 lib/cli.py London --unit F
python3 lib/cli.py "New York" --forecast
```

## CLI Workflow

### Main Menu (`main_menu()`)
- Displays welcome header with visual enhancements
- Shows 7 menu options using tuples
- Validates user input (1-7)
- Routes to appropriate functions
- Handles exit gracefully

### Weather Functions

#### `weather_menu()`
- Prompts for city name with validation (min 2 characters)
- Gets temperature unit preference: `("C", "F")`
- Fetches current weather data
- Saves search as tuple to database: `(user_id, city, temp, condition)`
- Displays formatted weather with emojis

#### `forecast_menu()`
- Gets city input with validation
- Fetches 5-day forecast data
- Processes list of forecast objects
- Displays formatted multi-day results

### History Management

#### `view_searches()`
- Retrieves list of tuples from database: `[(id, city, temp, date)]`
- Displays search history with visual formatting
- Shows "No searches found" if empty

#### `delete_search()`
- Shows current search history
- Validates search ID input (integer)
- Removes selected search from database
- Confirms deletion with success message

### User Management

#### `user_menu()`
- Create new users with name, default city, temperature unit
- View all users with search count statistics
- Navigate back to main menu
- Uses tuple for menu options: `("Create", "View", "Back")`

#### `favorites_menu()`
- Add favorite cities for specific users
- View user's favorite cities list
- Validates user ID existence
- Stores favorites as tuples: `(user_id, city_name)`

### Command Line Handler

#### `handle_command_line()`
- Processes command line arguments list
- Validates temperature units tuple: `("C", "F")`
- Returns weather or forecast data directly
- Shows usage help if no city provided

## Data Structures Used

- **Lists**: Command arguments, forecast data, search results
- **Tuples**: Menu options, validation sets, database records, temperature units
- **Dictionaries**: API responses, weather data, menu actions mapping

## File Architecture

- **cli.py**: Main interface, menu system, user interaction
- **models.py**: SQLAlchemy ORM classes (User, WeatherSearch, FavoriteCity)
- **weather_api.py**: API calls, data formatting, external service integration
- **weather.db**: SQLite database for persistent storage

## Error Handling

- Input validation for all user entries
- Graceful handling of API failures
- Database transaction safety
- Keyboard interrupt handling (Ctrl+C)
- Visual error messages with emoji indicators