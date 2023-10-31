part of 'garden_task_cubit.dart';

class GardenTaskState extends Equatable {
  List<TaskEntity>? taskList;
  LoadStatus? taskStatus;
  LoadStatus? deleteTaskStatus;

  GardenTaskState({
    this.taskList,
    this.taskStatus,
    this.deleteTaskStatus,
  });

  GardenTaskState copyWith({
    List<TaskEntity>? taskList,
    LoadStatus? taskStatus,
    LoadStatus? deleteTaskStatus,
  }) {
    return GardenTaskState(
      taskList: taskList ?? this.taskList,
      taskStatus: taskStatus ?? this.taskStatus,
      deleteTaskStatus: deleteTaskStatus ?? this.deleteTaskStatus,
    );
  }

  @override
  List<dynamic> get props =>
      [this.taskList, this.taskStatus, this.deleteTaskStatus];
}
