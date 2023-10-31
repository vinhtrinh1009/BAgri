// import 'dart:convert';
// import 'dart:async';
//
// import 'package:flutter_base/models/entities/token/login_model.dart';
// import 'package:flutter_secure_storage/flutter_secure_storage.dart';
//
// import 'share_preferences_helper.dart';
//
//
// class BagriSecureStorage {
//   static const _apiTokenKeyBagri = '_apiTokenKeyBagri';
//   static const _userInfoKey = '_userInfoKey';
//
//   final FlutterSecureStorage _storage;
//
//   BagriSecureStorage._internal(this._storage);
//
//   static final BagriSecureStorage _singleton = BagriSecureStorage._internal(FlutterSecureStorage());
//
//   factory BagriSecureStorage() {
//     return _singleton;
//   }
//
//   factory BagriSecureStorage.getInstance() {
//     return _singleton;
//   }
//
//   //Save token
//   void saveToken(LoginResponseEntity? token) async {
//     if (token == null) {
//       await _storage.delete(key: _apiTokenKeyBagri);
//       SharedPreferencesHelper.setApiTokenKey("");
//     } else {
//       await _storage.write(key: _apiTokenKeyBagri, value: jsonEncode(token.data?.token));
//       SharedPreferencesHelper.setApiTokenKey(_apiTokenKeyBagri);
//     }
//   }
//
//   //Get token
//   Future<String?> getToken() async {
//     try {
//       final key = await SharedPreferencesHelper.getApiTokenKey();
//       final tokenEncoded = await (_storage.read(key: key) as FutureOr<String>);
//       return jsonDecode(tokenEncoded);
//     } catch (e) {
//       return null;
//     }
//   }
//
// }
