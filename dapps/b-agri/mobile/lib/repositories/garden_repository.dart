import 'package:flutter_base/models/entities/garden/garden_delete.dart';
import 'package:flutter_base/models/entities/garden/garden_detail.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/params/garden/create_garden_params.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class GardenRepository {
  Future<ObjectResponse<GardenListResponse>> getGardenData();

  Future<dynamic> createGarden({CreateGardenParam? param});

  Future<GardenDetailResponse> getGardenDataById({String? gardenId});

  Future<dynamic> updateGarden({String? gardenId, CreateGardenParam? param});

  Future<GardenDeleteResponse> deleteGarden({String? gardenId});

  Future<ObjectResponse<GardenListResponse>> getGardensByManagerId(
      String managerId);
}

class GardenRepositoryImpl extends GardenRepository {
  ApiClient? _apiClientBagri;

  GardenRepositoryImpl(ApiClient? client) {
    _apiClientBagri = client;
  }

  @override
  Future<ObjectResponse<GardenListResponse>> getGardenData() async {
    return await _apiClientBagri!.getGardenData({});
  }

  Future<dynamic> createGarden({CreateGardenParam? param}) {
    final body = {
      "name": param?.name ?? "",
      "area": param?.area ?? "",
      "manager_id": param?.manager_id ?? "",
    };

    return _apiClientBagri!.createGarden(body);
  }

  Future<GardenDetailResponse> getGardenDataById({String? gardenId}) async {
    return await _apiClientBagri!.getGardenDataById(gardenId: gardenId);
  }

  Future<dynamic> updateGarden({String? gardenId, CreateGardenParam? param}) {
    final body = {
      "name": param?.name ?? "",
      "area": param?.area ?? "",
      "manager_id": param?.manager_id ?? "",
    };

    return _apiClientBagri!.updateGarden(gardenId, body);
  }

  Future<GardenDeleteResponse> deleteGarden({String? gardenId}) async {
    return await _apiClientBagri!.deleteGarden(gardenId: gardenId);
  }

  @override
  Future<ObjectResponse<GardenListResponse>> getGardensByManagerId(
      String managerId) async {
    return await _apiClientBagri!.getGardensByManagerId(managerId);
  }
}
