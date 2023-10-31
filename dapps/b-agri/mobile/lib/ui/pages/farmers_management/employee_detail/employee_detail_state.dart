part of 'employee_detail_cubit.dart';

class EmployeeDetailState extends Equatable {
  LoadStatus? loadStatus;
  FarmerDetailEntity? farmerDetail;
  int chosenMonth;

  Map<int, List<TaskEntity>?> taskMapByDay;
  @override
  List<dynamic> get props =>
      [loadStatus, farmerDetail, taskMapByDay, chosenMonth];

  EmployeeDetailState({
    this.loadStatus,
    this.farmerDetail,
    required this.taskMapByDay,
    required this.chosenMonth,
  });

  EmployeeDetailState copyWith({
    LoadStatus? loadStatus,
    FarmerDetailEntity? farmerDetail,
    Map<int, List<TaskEntity>?>? taskMapByDay,
    int? chosenMonth,
  }) {
    return EmployeeDetailState(
      loadStatus: loadStatus ?? this.loadStatus,
      farmerDetail: farmerDetail ?? this.farmerDetail,
      taskMapByDay: taskMapByDay ?? this.taskMapByDay,
      chosenMonth: chosenMonth ?? this.chosenMonth,
    );
  }
}
