import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/entities/garden/garden_delete.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';

import 'package:flutter_base/models/params/farmer/create_farmer_param.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class FarmerRepository {
  Future<FarmerList> getListFarmer();

  Future<FarmerList> getListFarmerByManager(String? managerId);

  Future<ObjectResponse<FarmerDetailResponse>> getFarmerById(String farmerId);

  Future<ObjectResponse<FarmerCreateResponse>> createFarmer(
      CreateFarmerParam param);

  Future<ObjectResponse<FarmerUpdateResponse>> updateFarmer(
      {required String farmerId, required CreateFarmerParam param});

  Future<dynamic> deleteFarmer({String? farmerId});
}

class FarmerRepositoryImpl extends FarmerRepository {
  ApiClient? _apiClientBagri;

  FarmerRepositoryImpl(ApiClient? client) {
    _apiClientBagri = client;
  }

  @override
  Future<FarmerList> getListFarmer() async {
    return await _apiClientBagri!.getListFarmerData();
  }

  Future<FarmerList> getListFarmerByManager(String? managerId) async {
    return await _apiClientBagri!.getListFarmerByManager(managerId!);
  }

  @override
  Future<ObjectResponse<FarmerDetailResponse>> getFarmerById(
      String farmerId) async {
    return await _apiClientBagri!.getFarmerById(farmerId);
  }

  @override
  Future<ObjectResponse<FarmerCreateResponse>> createFarmer(
      CreateFarmerParam param) async {
    return await _apiClientBagri!.createFarmer(param);
  }

  @override
  Future<dynamic> deleteFarmer({String? farmerId}) async {
    return await _apiClientBagri!.deleteFarmer(farmerId ?? "");
  }

  @override
  Future<ObjectResponse<FarmerUpdateResponse>> updateFarmer(
      {required String farmerId, required CreateFarmerParam param}) async {
    return await _apiClientBagri!.updateFarmer(farmerId, param);
  }
}
