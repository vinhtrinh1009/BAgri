import 'package:bloc/bloc.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/process/create_process_params.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:equatable/equatable.dart';
import 'package:rxdart/rxdart.dart';
part 'add_process_state.dart';

class AddProcessCubit extends Cubit<AddProcessState> {
  ProcessRepository? processRepository;

  AddProcessCubit({
    this.processRepository,
  }) : super(AddProcessState(stages: [], actionWithStepStatus: 0));

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void addList(StageEntity value) {
    emit(state.copyWith(addProcessStatus: LoadStatus.LOADING_MORE));
    List<StageEntity> stages = state.stages!;
    stages.add(value);
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList, addProcessStatus: LoadStatus.FORMAT_EXTENSION_FILE));
  }

  void removeList(int index) {
    emit(state.copyWith(addProcessStatus: LoadStatus.LOADING_MORE));
    List<StageEntity> stages = state.stages!;
    stages.removeAt(index);
    List<StageEntity> newList = stages;
    emit(state.copyWith(
        stages: newList, addProcessStatus: LoadStatus.FORMAT_EXTENSION_FILE));
  }

  void changeName(String name) {
    emit(state.copyWith(name: name));
  }

  void changeTree(List<TreeEntity>? value) {
    emit(state.copyWith(trees: value));
  }

  void changeDuration(int index, String value) {
    // List<StageEntity> stages = state.stages!;
    // stages[index].duration = value;
    // stages[index].name = 'Giai đoạn ${index + 1}';
    // List<StageEntity> newList = stages;
    // emit(state.copyWith(stages: newList));
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

  void createProcess() async {
    emit(state.copyWith(addProcessStatus: LoadStatus.LOADING));
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
              // duration: item.duration,
              steps: steps));
        }
      }

      final param = CreateProcessParam(
        name: state.name,
        tree_ids: listTree,
        stages: listStages,
      );
      final response = await processRepository!.createProcess(param: param);

      if (response != null) {
        emit(state.copyWith(addProcessStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(addProcessStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      emit(state.copyWith(addProcessStatus: LoadStatus.FAILURE));
      showMessageController.sink.add(SnackBarMessage(
        message: S.current.error_occurred,
        type: SnackBarType.ERROR,
      ));
      return;
    }
  }
}
