import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/season/season_task_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/season_repository.dart';

part 'care_process_day_state.dart';

class CareProcessDayCubit extends Cubit<CareProcessDayState> {
  SeasonRepository seasonRepository;
  CareProcessDayCubit({required this.seasonRepository})
      : super(CareProcessDayState());

  Future<void> getSeasonTaskByDay(
      {required String seasonId, required String date}) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));

    try {
      ObjectResponse<SeasonTaskResponse> result =
          await seasonRepository.getSeasonTaskByDay(seasonId, date);
      print('--------${result.data!.tasks?.length ?? 0}--------');

      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS, taskList: result.data!.tasks!));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
