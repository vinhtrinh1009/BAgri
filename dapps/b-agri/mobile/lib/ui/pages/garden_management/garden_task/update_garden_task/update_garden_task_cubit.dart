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
import 'package:flutter_base/utils/logger.dart';

part 'update_garden_task_state.dart';

class UpdateGardenTaskCubit extends Cubit<UpdateGardenTaskState> {
  TaskRepository? taskRepository;
  UploadRepository? uploadRepo;
  UpdateGardenTaskCubit({
    this.taskRepository,
    this.uploadRepo,
  }) : super(UpdateGardenTaskState());

  @override
  Future<void> close() {
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

  void changeStartTime(String startTime) {
    emit(state.copyWith(start_time: startTime));
  }

  void changeEndTime(String endTime) {
    emit(state.copyWith(end_time: endTime));
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

  void updateTask(String? taskId) async {
    emit(state.copyWith(updateGardenTaskStatus: LoadStatus.LOADING));
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
      final response =
          await taskRepository!.updateTask(taskId: taskId, param: param);

      if (response != null) {
        emit(state.copyWith(updateGardenTaskStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(updateGardenTaskStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      logger.e(e);
      emit(state.copyWith(updateGardenTaskStatus: LoadStatus.FAILURE));
      return;
    }
  }

  Future<void> getTaskDetail(String taskId) async {
    emit(state.copyWith(loadDetailStatus: LoadStatus.LOADING));
    try {
      final result = await taskRepository!.getTaskById(taskId);

      print(result.data!.task!.start_time!.split(' ')[1].split(':')[0]);
      emit(
        state.copyWith(
          loadDetailStatus: LoadStatus.SUCCESS,
          name: result.data!.task!.step!.name,
          season_id: result.data!.task!.season_id,
          step: result.data!.task!.step,
          date: result.data!.task!.date,
          result: result.data!.task!.result,
          manager_id: result.data!.task!.manager_id,
          description: result.data!.task!.description,
          farmers: result.data!.task!.farmers,
          start_time: result.data!.task!.start_time,
          end_time: result.data!.task!.end_time,
          startHour: result.data!.task!.start_time!.split(' ')[1].split(':')[0],
          startMinute:
              result.data!.task!.start_time!.split(' ')[1].split(':')[1],
          endHour: result.data!.task!.end_time!.split(' ')[1].split(':')[0],
          endMinute: result.data!.task!.end_time!.split(' ')[1].split(':')[1],
          items: result.data!.task!.items,
        ),
      );
    } catch (e) {
      emit(state.copyWith(loadDetailStatus: LoadStatus.FAILURE));
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
