import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/season_repository.dart';

part 'season_management_state.dart';

class SeasonManagementCubit extends Cubit<SeasonManagementState> {
  SeasonRepository seasonRepository;
  SeasonManagementCubit({required this.seasonRepository})
      : super(SeasonManagementState());

  Future<void> getListSeason(String? status) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final ObjectResponse<SeasonListResponse> result =
          await seasonRepository.getListSeasonData(status ?? '');

      emit(state.copyWith(
          seasonList: result.data!.seasons, loadStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
      print(e);
    }
  }

  Future<bool> deleteSeason(String seasonId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final result = await seasonRepository.deleteSeason(seasonId);
      emit(state.copyWith(loadStatus: LoadStatus.SUCCESS));
      return true;
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
      return false;
    }
  }
}
