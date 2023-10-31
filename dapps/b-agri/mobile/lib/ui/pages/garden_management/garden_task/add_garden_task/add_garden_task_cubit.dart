import 'dart:io';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/entities/file/file_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/task/create_task_params.dart';
import 'package:flutter_base/repositories/task_repository.dart';
import 'package:flutter_base/repositories/upload_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:flutter_base/utils/logger.dart';
import 'package:rxdart/rxdart.dart';

part 'add_garden_task_state.dart';

class AddGardenTaskCubit extends Cubit<AddGardenTaskState> {
  TaskRepository? taskRepository;
  UploadRepository? uploadRepo;
  AddGardenTaskCubit({
    this.taskRepository,
    this.uploadRepo,
  }) : super(AddGardenTaskState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void changeSeason(String? seasonId) {
    emit(state.copyWith(season_id: seasonId));
  }

  void changeStep(StepEntity? step) {
    emit(state.copyWith(step: step));
  }

  void changeDate(String date) {
    emit(state.copyWith(date: date));
  }

  void changeStartHour(String startHour) {
    emit(state.copyWith(startHour: startHour));
  }

  void changeStartMinute(String startMinute) {
    emit(state.copyWith(startMinute: startMinute));
  }

  void changeEndHour(String endHour) {
    emit(state.copyWith(endHour: endHour));
  }

  void changeEndMinute(String endMinute) {
    emit(state.copyWith(endMinute: endMinute));
  }

  void changeManager(String? manager_id) {
    emit(state.copyWith(manager_id: manager_id));
  }

  void changeDescription(String description) {
    emit(state.copyWith(description: description));
  }

  void changeItems(String items) {
    emit(state.copyWith(items: items));
  }

  void changeFarmer(List<FarmerEntity>? value) {
    emit(state.copyWith(farmers: value));
  }

  void createTask() async {
    emit(state.copyWith(addGardenTaskStatus: LoadStatus.LOADING));
    try {
      List<String> listFarmer = [];
      if (state.farmers != null) {
        state.farmers!.forEach((element) {
          listFarmer.add(element.farmerId!);
        });
      }

      final param = CreateTaskParam(
        step_id: state.step!.step_id,
        name: state.step!.name,
        farmer_ids: listFarmer,
        manager_id: state.manager_id,
        description: state.description,
        season_id: state.season_id,
        date: state.date,
        start_time: '${state.date} ${state.startHour}:${state.startMinute}',
        end_time: '${state.date} ${state.endHour}:${state.endMinute}',
        result: state.result,
        items: state.items,
      );
      final response = await taskRepository!.createTask(param: param);

      if (response != null) {
        emit(state.copyWith(addGardenTaskStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(addGardenTaskStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      logger.e(e);
      emit(state.copyWith(addGardenTaskStatus: LoadStatus.FAILURE));
      return;
    }
  }

  void uploadFile(File? file) async {
    emit(state.copyWith(uploadFileStatus: LoadStatus.LOADING));

    try {
      final response = await uploadRepo!.uploadFile(file);
      if (response != null) {
        final results = state.result ?? [];
        results.add(response.data!.file_path!);
        Future.delayed(const Duration(seconds: 3), () {
          emit(
            state.copyWith(
              uploadFileStatus: LoadStatus.SUCCESS,
              result: results,
            ),
          );
        });
      } else {
        emit(
          state.copyWith(uploadFileStatus: LoadStatus.FAILURE),
        );
      }
    } catch (e) {
      emit(state.copyWith(uploadFileStatus: LoadStatus.FAILURE));
      return;
    }
  }

  void removeFileAtIndex(int index) {
    emit(state.copyWith(removeFileStatus: LoadStatus.LOADING));
    final result = state.result!;
    result.removeAt(index);
    emit(state.copyWith(removeFileStatus: LoadStatus.SUCCESS, result: result));
  }
}
