part of 'care_process_day_cubit.dart';

class CareProcessDayState extends Equatable {
  LoadStatus? loadStatus;
  List<SeasonTaskEntity>? taskList;
  @override
  List<Object?> get props => [loadStatus, taskList];

  CareProcessDayState({
    this.loadStatus,
    this.taskList,
  });

  CareProcessDayState copyWith({
    LoadStatus? loadStatus,
    List<SeasonTaskEntity>? taskList,
  }) {
    return CareProcessDayState(
      loadStatus: loadStatus ?? this.loadStatus,
      taskList: taskList ?? this.taskList,
    );
  }
}
