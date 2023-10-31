import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/global/global_event.dart';

import 'package:flutter_base/utils/logger.dart';

class ApiInterceptors extends InterceptorsWrapper {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final method = options.method;
    final uri = options.uri;
    final data = options.data;
    if (GlobalData.instance.token != null) {
      options.headers['Authorization'] = 'Bearer ${GlobalData.instance.token}';
    }
    logger.log(
        "\n\n--------------------------------------------------------------------------------------------------------");
    if (method == 'GET') {
      logger.log(
          "✈️ REQUEST[$method] => PATH: $uri \n Token: ${options.headers}",
          printFullText: true);
    } else {
      try {
        logger.log(
            "✈️ REQUEST[$method] => PATH: $uri \n Token: ${GlobalData.instance.token} \n DATA: ${jsonEncode(data)}",
            printFullText: true);
      } catch (e) {
        logger.log(
            "✈️ REQUEST[$method] => PATH: $uri \n Token: ${GlobalData.instance.token} \n DATA: $data",
            printFullText: true);
      }
    }
    return super.onRequest(options, handler);
  }

  @override
  void onResponse(
    Response response,
    ResponseInterceptorHandler handler,
  ) {
    final statusCode = response.statusCode;
    final uri = response.requestOptions.uri;
    final data = jsonEncode(response.data);
    logger.log("✅ RESPONSE[$statusCode] => PATH: $uri\n DATA: $data");
    //Handle section expired
    if (response.statusCode == 401) {
      GlobalEvent.instance.onTokenExpired.add(true);
    }
    return super.onResponse(response, handler);
  }

  @override
  void onError(
    DioError err,
    ErrorInterceptorHandler handler,
  ) {
    final statusCode = err.response?.statusCode;
    final uri = err.requestOptions.path;
    var data = "";
    try {
      data = jsonEncode(err.response?.data);
    } catch (e) {}
    logger.log("⚠️ ERROR[$statusCode] => PATH: $uri\n DATA: $data");
    return super.onError(err, handler);
  }
}
