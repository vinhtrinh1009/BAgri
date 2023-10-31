// import 'dart:io';
//
// import 'package:dio/dio.dart';
// import 'package:flutter_base/models/entities/index.dart';
// import 'package:flutter_base/models/params/avatar_param.dart';
// import 'package:flutter_base/network/api_client.dart';
//
// abstract class UploadRepository {
//   Future<List<FileEntity>> uploadImage(File? file);
//
//   Future<List<FileEntity>> uploadFile(File? file);
//
//   Future<dynamic> uploadAvatar(AvatarParam avatar);
// }
//
// class UploadRepositoryImpl extends UploadRepository {
//   ApiClient? _apiClient;
//
//   UploadRepositoryImpl(ApiClient? client) {
//     _apiClient = client;
//   }
//
//   @override
//   Future<List<FileEntity>> uploadImage(File? file) async {
//     FormData formData = FormData.fromMap({
//       "files": await MultipartFile.fromFile(
//         file?.path ?? "",
//       ),
//     });
//     return await _apiClient!.uploadImage(formData);
//   }
//
//   @override
//   Future<List<FileEntity>> uploadFile(File? file) async {
//     FormData formData = FormData.fromMap({
//       "files": await MultipartFile.fromFile(
//         file?.path ?? "",
//       ),
//     });
//     return await _apiClient!.uploadFile(formData);
//   }
//
//   @override
//   Future<dynamic> uploadAvatar(AvatarParam avatar) async {
//     return await _apiClient!.uploadAvatar(avatar);
//   }
// }
