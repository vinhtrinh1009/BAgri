import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/garden_task/task_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/task_repository.dart';

part 'garden_task_state.dart';

class GardenTaskCubit extends Cubit<GardenTaskState> {
  TaskRepository taskRepository;

  GardenTaskCubit({required this.taskRepository}) : super(GardenTaskState());

  void getGardenTask(String? seasonId, String? date) async {
    emit(state.copyWith(taskStatus: LoadStatus.LOADING));
    try {
      final result = await taskRepository.getGardenTask(seasonId, date);
      if (result != null) {
        emit(state.copyWith(
            taskList: result.data!.tasks, taskStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(taskStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      emit(state.copyWith(taskStatus: LoadStatus.FAILURE));
    }
  }

  Future<bool> deleteTask(String taskId) async {
    emit(state.copyWith(deleteTaskStatus: LoadStatus.LOADING));
    try {
      final result = await taskRepository.deleteTask(taskId);
      emit(state.copyWith(deleteTaskStatus: LoadStatus.SUCCESS));
      return true;
    } catch (e) {
      emit(state.copyWith(deleteTaskStatus: LoadStatus.FAILURE));
      return false;
    }
  }
}
