import 'package:bloc/bloc.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/process/process_detail.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/process/create_process_params.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:equatable/equatable.dart';
import 'package:rxdart/rxdart.dart';

part 'process_season_state.dart';

class ProcessSeasonCubit extends Cubit<ProcessSeasonState> {
  ProcessRepository? processRepository;

  ProcessSeasonCubit({
    this.processRepository,
  }) : super(ProcessSeasonState(stages: [], actionWithStepStatus: 0));

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void addList(StageEntity value) {
    emit(state.copyWith(updateProcessSeasonStatus: LoadStatus.LOADING_MORE));
    List<StageEntity> stages = state.stages!;
    stages.add(value);
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList,
        updateProcessSeasonStatus: LoadStatus.FORMAT_EXTENSION_FILE));
  }

  void removeList(int index) {
    emit(state.copyWith(updateProcessSeasonStatus: LoadStatus.LOADING_MORE));
    List<StageEntity> stages = state.stages!;
    stages.removeAt(index);
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList,
        updateProcessSeasonStatus: LoadStatus.FORMAT_EXTENSION_FILE));
  }

  void changeName(String name) {
    emit(state.copyWith(name: name));
  }

  void changeTree(List<TreeEntity>? value) {
    emit(state.copyWith(trees: value));
  }

  void editSteps(int index, int indexStages, StepEntity value) {
    List<StageEntity> stages = state.stages!;
    stages[indexStages].steps![index] = value;
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList, actionWithStepStatus: state.actionWithStepStatus++));
  }

  void createStep(int index, StepEntity value) {
    List<StageEntity> stages = state.stages!;
    if (stages[index].steps == null) {
      stages[index].steps = [];
    }
    stages[index].steps!.add(value);
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList, actionWithStepStatus: state.actionWithStepStatus++));
  }

  void removeStep(int index, int indexStages) {
    List<StageEntity> stages = state.stages!;
    stages[indexStages].steps?.removeAt(index);
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList, actionWithStepStatus: state.actionWithStepStatus++));
  }

  void updateProcess(String? processId) async {
    emit(state.copyWith(updateProcessSeasonStatus: LoadStatus.LOADING));
    try {
      List<String> listTree = [];
      if (state.trees != null) {
        state.trees!.forEach((element) {
          listTree.add(element.tree_id!);
        });
      }

      List<StagesParamsEntity> listStages = [];
      if (state.stages != null) {
        for (int i = 0; i < state.stages!.length; i++) {
          List<StepEntity> steps = [];
          state.stages![i].steps!.forEach((ele) {
            steps.add(ele);
          });
          listStages.add(StagesParamsEntity(
              name: 'Giai đoạn ${i + 1}',
              stage_id: state.stages![i].stage_id,
              steps: steps));
        }
      }

      final param = CreateProcessParam(
        name: state.name,
        tree_ids: listTree,
        stages: listStages,
      );

      final response = await processRepository!
          .updateProcess(processId: processId, param: param);

      if (response != null) {
        emit(state.copyWith(updateProcessSeasonStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(updateProcessSeasonStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      emit(state.copyWith(updateProcessSeasonStatus: LoadStatus.FAILURE));
      return;
    }
  }

  Future<void> getProcessDetail(String processId) async {
    emit(state.copyWith(loadDetailStatus: LoadStatus.LOADING));
    try {
      final ObjectResponse<ProcessDetailResponse> result =
          await processRepository!.getProcessById(processId);

      emit(state.copyWith(
          loadDetailStatus: LoadStatus.SUCCESS,
          name: result.data?.process?.name!,
          trees: result.data?.process?.trees!,
          stages: result.data?.process?.stages!));
    } catch (e) {
      emit(state.copyWith(loadDetailStatus: LoadStatus.FAILURE));
    }
  }
}
