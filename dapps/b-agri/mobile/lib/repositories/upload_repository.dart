import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter_base/models/entities/file/file_entity.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class UploadRepository {
  Future<ObjectResponse<FileEntity>> uploadFile(File? file);
}

class UploadRepositoryImpl extends UploadRepository {
  ApiClient? _apiClient;

  UploadRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  @override
  Future<ObjectResponse<FileEntity>> uploadFile(File? file) async {
    String fileName = file!.path.split('/').last;
    FormData formData = FormData.fromMap({
      "file": await MultipartFile.fromFile(file.path, filename: fileName),
    });

    return await _apiClient!.uploadFile(formData);
  }
}
