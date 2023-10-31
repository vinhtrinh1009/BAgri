import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/season/season_task_detail_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/season_repository.dart';

part 'care_process_task_state.dart';

class CareProcessTaskCubit extends Cubit<CareProcessTaskState> {
  SeasonRepository seasonRepository;
  CareProcessTaskCubit({required this.seasonRepository})
      : super(CareProcessTaskState());

  Future<void> getTaskDetail(String taskId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));

    try {
      ObjectResponse<SeasonTaskDetailResponse> result =
          await seasonRepository.getSeasonTaskDetail(taskId);

      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS, taskDetail: result.data!.task));
    } catch (e) {
      print(e);
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
