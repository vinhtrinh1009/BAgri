// import 'dart:convert';
//
// import 'package:flutter/services.dart' show rootBundle;
// import 'package:flutter_base/models/entities/address/area_json_entity.dart';
//
// class LoadJsonHelper {
//   LoadJsonHelper._privateConstructor();
//
//   static final LoadJsonHelper shared = LoadJsonHelper._privateConstructor();
//
//   List<CountryEntity>? countries;
//   List<ProvinceEntity?>? provinces;
//   List<IdentifyAddressEntity?>? identifyAddress;
//   List<DistrictEntity?>? identifyDistricty;
//
//   Future load() async {
//     try {
//       final _countries = await LoadJsonHelper.loadCountries();
//       countries = _countries;
//
//       final _provinces = await LoadJsonHelper.loadProvinces();
//       provinces = _provinces;
//
//       final _identifies = await LoadJsonHelper.loadIndentifyAddress();
//       identifyAddress = _identifies;
//
//       final _districtyfies = await LoadJsonHelper.loadIndentifyDistrict();
//       identifyDistricty = _districtyfies;
//     } catch (error) {}
//   }
//
//   static Future<List<CountryEntity>> loadCountries() async {
//     return [
//       CountryEntity('Việt Nam'),
//     ];
//   }
//
//   static Future<List<ProvinceEntity?>> loadProvinces() async {
//     try {
//       List<ProvinceEntity?> results = [];
//       final jsonString = await rootBundle.loadString('assets/area/area.json');
//       final _json = json.decode(jsonString);
//       if (_json is List) {
//         _json.forEach((json) {
//           try {
//             final province = ProvinceEntity.fromJson(json);
//             results.add(province);
//           } catch (error) {
//             print(error);
//           }
//         });
//       }
//       return results;
//     } catch (error) {
//       print(error);
//       return [];
//     }
//   }
//
//   static Future<List<IdentifyAddressEntity?>> loadIndentifyAddress() async {
//     try {
//       List<IdentifyAddressEntity?> results = [];
//       final jsonString =
//           await rootBundle.loadString('assets/area/indentify_address.json');
//       final _json = json.decode(jsonString);
//       if (_json is List) {
//         _json.forEach((json) {
//           try {
//             final address = IdentifyAddressEntity.fromJson(json);
//
//             results.add(address);
//           } catch (error) {
//             print(error);
//           }
//         });
//       }
//       return results;
//     } catch (error) {
//       print(error);
//       return [];
//     }
//   }
//
//   static Future<List<DistrictEntity?>> loadIndentifyDistrict() async {
//     try {
//       List<DistrictEntity?> results = [];
//       final jsonString = await rootBundle.loadString('assets/area/area.json');
//       final _json = json.decode(jsonString);
//       if (_json is List) {
//         _json.forEach((json) {
//           try {
//             final address = DistrictEntity.fromJson(json);
//             results.add(address);
//           } catch (error) {
//             print(error);
//           }
//         });
//       }
//       return results;
//     } catch (error) {
//       print(error);
//       return [];
//     }
//   }
// }
