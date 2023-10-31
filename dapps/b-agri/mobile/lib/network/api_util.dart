import 'package:dio/dio.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'api_client_bagri.dart';
import 'api_weather.dart';
import 'api_interceptors.dart';

class ApiUtil {
  static ApiClient? getApiClient() {
    final dio = Dio();
    dio.options.connectTimeout = 60000;
    dio.interceptors.add(ApiInterceptors());
    final apiClientBagri = ApiClient(dio, baseUrl: AppConfig.baseUrl);
    return apiClientBagri;
  }

  static ApiWeather? getApiWeather() {
    final dio = Dio();
    dio.options.connectTimeout = 60000;
    dio.interceptors.add(ApiInterceptors());
    final apiWeather = ApiWeather(dio, baseUrl: AppConfig.weatherUrl);
    return apiWeather;
  }
}
