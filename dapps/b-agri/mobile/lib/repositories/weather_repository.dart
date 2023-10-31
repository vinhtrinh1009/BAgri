import 'package:flutter_base/models/entities/weather/weather_response.dart';
import 'package:flutter_base/network/api_weather.dart';

abstract class WeatherRepository {
  //
  Future<WeatherResponse> getCurrentWeather(
      String latitude, String longitude, String key);
}

class WeatherRepositoryImpl extends WeatherRepository {
  ApiWeather? _apiWeather;

  WeatherRepositoryImpl(ApiWeather? client) {
    _apiWeather = client;
  }

  @override
  Future<WeatherResponse> getCurrentWeather(
      String latitude, String longitude, String key) async {
    return _apiWeather!.getCurrentWeather(latitude, longitude, key);
  }
}
