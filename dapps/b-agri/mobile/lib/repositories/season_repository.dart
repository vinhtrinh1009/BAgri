import 'package:flutter_base/models/entities/season/qr_entity.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/models/entities/season/season_steps_response.dart';
import 'package:flutter_base/models/entities/season/season_task_detail_entity.dart';
import 'package:flutter_base/models/entities/season/season_task_entity.dart';
import 'package:flutter_base/models/entities/season/season_update_entity.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/entities/tree/tree_delete_response.dart';
import 'package:flutter_base/models/params/farmer/create_farmer_param.dart';
import 'package:flutter_base/models/params/season/create_season_param.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class SeasonRepository {
  Future<ObjectResponse<SeasonListResponse>> getListSeasonData(String status);

  Future<ObjectResponse<SeasonDetailResponse>> getSeasonById(String seasonId);

  Future<ObjectResponse<SeasonCreateResponse>> createSeason(
      CreateSeasonParam param);

  Future<TreeDeleteResponse> deleteSeason(String seasonId);

  Future<ObjectResponse<SeasonUpdateResponse>> updateSeason(
      String seasonId, CreateSeasonParam param);

  Future<ObjectResponse<SeasonTaskResponse>> getSeasonTaskByDay(
      String seasonId, String date);

  Future<ObjectResponse<SeasonTaskDetailResponse>> getSeasonTaskDetail(
      String taskId);

  Future<ObjectResponse<SeasonStepsResponse>> getListSeasonSteps(
      String seasonId);

  Future<ObjectResponse<QREntity>> generateQRCode(String seasonId);
}

class SeasonRepositoryImpl extends SeasonRepository {
  ApiClient? _apiClientBagri;

  SeasonRepositoryImpl(ApiClient? client) {
    _apiClientBagri = client;
  }

  @override
  Future<ObjectResponse<SeasonListResponse>> getListSeasonData(
      String status) async {
    return await _apiClientBagri!.getListSeasonData(status);
  }

  @override
  Future<ObjectResponse<SeasonDetailResponse>> getSeasonById(
      String seasonId) async {
    return await _apiClientBagri!.getSeasonById(seasonId);
  }

  @override
  Future<ObjectResponse<SeasonCreateResponse>> createSeason(
      CreateSeasonParam param) async {
    return await _apiClientBagri!.createSeason(param);
  }

  @override
  Future<TreeDeleteResponse> deleteSeason(String seasonId) async {
    return await _apiClientBagri!.deleteSeason(seasonId);
  }

  @override
  Future<ObjectResponse<SeasonUpdateResponse>> updateSeason(
      String seasonId, CreateSeasonParam param) async {
    return await _apiClientBagri!.updateSeason(seasonId, param);
  }

  @override
  Future<ObjectResponse<SeasonTaskResponse>> getSeasonTaskByDay(
      String seasonId, String date) async {
    return await _apiClientBagri!.getSeasonTaskByDay(seasonId, date);
  }

  @override
  Future<ObjectResponse<SeasonTaskDetailResponse>> getSeasonTaskDetail(
      String taskId) async {
    return await _apiClientBagri!.getSeasonTaskDetail(taskId);
  }

  @override
  Future<ObjectResponse<SeasonStepsResponse>> getListSeasonSteps(
      String seasonId) async {
    return await _apiClientBagri!.getListSeasonSteps(seasonId);
  }

  @override
  Future<ObjectResponse<QREntity>> generateQRCode(String seasonId) async {
    return await _apiClientBagri!.generateQRCode(seasonId);
  }
}
