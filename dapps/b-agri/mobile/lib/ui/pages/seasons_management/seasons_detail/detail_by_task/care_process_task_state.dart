part of 'care_process_task_cubit.dart';

class CareProcessTaskState extends Equatable {
  LoadStatus? loadStatus;
  SeasonTaskDetailEntity? taskDetail;

  @override
  List<Object?> get props => [loadStatus, taskDetail];

  CareProcessTaskState({
    this.loadStatus,
    this.taskDetail,
  });

  CareProcessTaskState copyWith({
    LoadStatus? loadStatus,
    SeasonTaskDetailEntity? taskDetail,
  }) {
    return CareProcessTaskState(
      loadStatus: loadStatus ?? this.loadStatus,
      taskDetail: taskDetail ?? this.taskDetail,
    );
  }
}
