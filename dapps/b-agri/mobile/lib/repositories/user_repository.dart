import 'package:flutter_base/models/entities/manager/manager_entity.dart';
import 'package:flutter_base/models/entities/user/user_entity.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class UserRepository {
  Future<ObjectResponse<UserEntity>> getProfile();

  Future<ObjectResponse<ManagerListResponse>> getListManager();
}

class UserRepositoryImpl extends UserRepository {
  ApiClient? _apiClient;

  UserRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  @override
  Future<ObjectResponse<UserEntity>> getProfile() {
    return _apiClient!.getProfile();
  }

  @override
  Future<ObjectResponse<ManagerListResponse>> getListManager() async {
    return _apiClient!.getListManager();
  }
}
