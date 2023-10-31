import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/season_repository.dart';
import 'package:flutter_base/repositories/task_repository.dart';

part 'season_step_state.dart';

class SeasonStepCubit extends Cubit<SeasonStepState> {
  SeasonRepository? seasonRepository;

  SeasonStepCubit({
    this.seasonRepository,
  }) : super(SeasonStepState());

  @override
  Future<void> close() {
    return super.close();
  }

  Future<void> getListSeasonSteps(String seasonId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final result = await seasonRepository!.getListSeasonSteps(seasonId);

      emit(
        state.copyWith(
          loadStatus: LoadStatus.SUCCESS,
          steps: result.data!.steps,
        ),
      );
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
