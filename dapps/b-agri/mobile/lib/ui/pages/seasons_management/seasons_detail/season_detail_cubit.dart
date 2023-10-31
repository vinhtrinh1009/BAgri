import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/models/entities/season/qr_entity.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/models/entities/season/season_update_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/season/create_season_param.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/season_repository.dart';

part 'season_detail_state.dart';

class SeasonDetailCubit extends Cubit<SeasonDetailState> {
  SeasonRepository seasonRepository;
  SeasonDetailCubit({required this.seasonRepository})
      : super(SeasonDetailState());

  Future<void> getSeasonDetail(String seasonId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      ObjectResponse<SeasonDetailResponse> result =
          await seasonRepository.getSeasonById(seasonId);

      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS, season: result.data!.season!));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }

  Future<bool> updateSeason(String seasonId) async {
    try {
      CreateSeasonParam param = CreateSeasonParam(
        name: state.season!.name,
        garden_id: state.season!.garden!.id,
        process_id: state.season!.process!.process_id,
        tree_id: state.season!.tree!.id,
        start_date: state.season!.start_date,
        end_date: state.season!.end_date,
        status: "done",
      );
      ObjectResponse<SeasonUpdateResponse> result =
          await seasonRepository.updateSeason(seasonId, param);
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> generateQRCode(String seasonId) async {
    try {
      ObjectResponse<QREntity> result =
          await seasonRepository.generateQRCode(seasonId);
      emit(state.copyWith(
          linkQR: result.data!.qr_code_url, linkUrl: result.data!.link));
      return true;
    } catch (e) {
      return false;
    }
  }
}
