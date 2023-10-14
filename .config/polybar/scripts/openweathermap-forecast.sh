#!/bin/sh

## The base script is taken from https://github.com/polybar/polybar-scripts
## Icons are aligned to those available in Nerd Fonts

get_icon() {
    case $1 in
        # Icons for weather-icons
        # clear sky (day/night)
        01d) icon="";;
        01n) icon="";;
        # few clouds 
        02d) icon="";;
        02n) icon="";;
        # scattered clouds
        03d) icon="";;
        03n) icon="";;
        # broken clouds
        04d) icon="";;
        04n) icon="";;
        # showers
        09d) icon="";;
        09n) icon="";;
        # rain
        10d) icon="";;
        10n) icon="";;
        # thunderstorm
        11d) icon="";;
        11n) icon="";;
        # snow
        13d) icon="";;
        13n) icon="";;
        # fog/mist
        50d) icon="";;
        50n) icon="";;
        *) icon="";

    esac

    echo $icon
}

KEY="0123456"
CITY="Sofia,BG"
UNITS="metric"
SYMBOL="°"

API="https://api.openweathermap.org/data/2.5"

if [ -n "$CITY" ]; then
    if [ "$CITY" -eq "$CITY" ] 2>/dev/null; then
        CITY_PARAM="id=$CITY"
    else
        CITY_PARAM="q=$CITY"
    fi

    current=$(curl -sf "$API/weather?appid=$KEY&$CITY_PARAM&units=$UNITS")
    forecast=$(curl -sf "$API/forecast?appid=$KEY&$CITY_PARAM&units=$UNITS&cnt=1")
else
    location=$(curl -sf https://location.services.mozilla.com/v1/geolocate?key=geoclue)

    if [ -n "$location" ]; then
        location_lat="$(echo "$location" | jq '.location.lat')"
        location_lon="$(echo "$location" | jq '.location.lng')"

        current=$(curl -sf "$API/weather?appid=$KEY&lat=$location_lat&lon=$location_lon&units=$UNITS")
        forecast=$(curl -sf "$API/forecast?appid=$KEY&lat=$location_lat&lon=$location_lon&units=$UNITS&cnt=1")
    fi
fi

if [ -n "$current" ] && [ -n "$forecast" ]; then
    current_temp=$(echo "$current" | jq ".main.temp" | cut -d "." -f 1)
    current_icon=$(echo "$current" | jq -r ".weather[0].icon")

    forecast_temp=$(echo "$forecast" | jq ".list[].main.temp" | cut -d "." -f 1)
    forecast_icon=$(echo "$forecast" | jq -r ".list[].weather[0].icon")

    if [ "$current_temp" -gt "$forecast_temp" ]; then
        trend="免"
    elif [ "$forecast_temp" -gt "$current_temp" ]; then
        trend="勤"
    else
        trend="勉"
    fi

    echo "$(get_icon "$current_icon")  $current_temp$SYMBOL $trend  $(get_icon "$forecast_icon")  $forecast_temp$SYMBOL"
fi
