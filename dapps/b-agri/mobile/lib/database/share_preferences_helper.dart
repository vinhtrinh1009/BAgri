import 'dart:convert';

import 'package:flutter_base/models/entities/user/user_entity.dart';
import 'package:flutter_base/utils/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SharedPreferencesHelper {
  static const _authTokenKey = '_authTokenKey';
  static const _roleKey = '_roleKey';
  static const _userInfoKey = '_userInfoKey';
  static const _longitude = '_longitude';
  static const _latitude = '_latitude';

  static void setToken(String token) async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString(_authTokenKey, token);
    } catch (e) {
      logger.e(e);
    }
  }

  static Future<String?> getToken() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(_authTokenKey) ?? null;
    } catch (e) {
      return "";
    }
  }

  static void removeToken() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.remove(_authTokenKey);
    } catch (e) {
      logger.e(e);
    }
  }

  static void setRole(String role) async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString(_roleKey, role);
    } catch (e) {
      logger.e(e);
    }
  }

  static Future<String?> getRole() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(_roleKey) ?? null;
    } catch (e) {
      return "";
    }
  }

  static void setUserInfo(UserEntity user) async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString(_userInfoKey, json.encode(user.toJson()));
    } catch (e) {
      logger.e(e);
    }
  }

  static Future<UserEntity?> getUserInfo() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      var value = prefs.getString(_userInfoKey);
      return UserEntity.fromJson(json.decode(value!));
    } catch (e) {
      return null;
    }
  }

  //Set latitude
  static void setLatitude(String latitude) async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString(_latitude, latitude);
    } catch (e) {
      logger.e(e);
    }
  }

  //Get latitude
  static Future<String?> getLatitude() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(_latitude) ?? null;
    } catch (e) {
      return "";
    }
  }

  //Set longitude
  static void setLongitude(String longitude) async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString(_longitude, longitude);
    } catch (e) {
      logger.e(e);
    }
  }

  //Get latitude
  static Future<String?> getLongitude() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(_longitude) ?? null;
    } catch (e) {
      return "";
    }
  }
}
