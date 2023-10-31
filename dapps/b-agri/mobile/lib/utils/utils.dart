import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_snackbar.dart';
import 'package:flutter_base/database/share_preferences_helper.dart';

import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/utils/logger.dart';
import 'package:flutter_base/utils/replacement_map.dart';
import 'package:geolocator/geolocator.dart';
import 'package:intl/intl.dart' as intl;
import 'package:url_launcher/url_launcher.dart';

class Utils {
  static Size getTextSize(String text, TextStyle style) {
    final TextPainter textPainter = TextPainter(
      text: TextSpan(text: text, style: style),
      maxLines: 1,
      textDirection: TextDirection.ltr,
    )..layout(
        minWidth: 0,
        maxWidth: double.infinity,
      );
    return textPainter.size;
  }

  static determinePosition() async {
    // bool serviceEnabled;
    // LocationPermission permission;
    //
    // // Test if location services are enabled.
    // serviceEnabled = await Geolocator.isLocationServiceEnabled();
    // if (!serviceEnabled) {
    //   return Future.error('Location services are disabled.');
    // }
    //
    // permission = await Geolocator.checkPermission();
    // if (permission == LocationPermission.denied) {
    //   permission = await Geolocator.requestPermission();
    //   if (permission == LocationPermission.denied) {
    //     return Future.error('Location permissions are denied');
    //   }
    // }
    //
    // if (permission == LocationPermission.deniedForever) {
    //   // Permissions are denied forever, handle appropriately.
    //   return Future.error(
    //       'Location permissions are permanently denied, we cannot request permissions.');
    // }

    var _locationData = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high);
    SharedPreferencesHelper.setLongitude("${_locationData.longitude}");
    SharedPreferencesHelper.setLatitude("${_locationData.latitude}");
  }
}
