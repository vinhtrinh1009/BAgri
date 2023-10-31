part of 'employee_management_cubit.dart';

class EmployeeManagementState extends Equatable {
  List<FarmerEntity>? farmerList;
  List<FarmerEntity>? currentFarmerList;
  LoadStatus? loadStatus;

  @override
  List<dynamic> get props =>
      [this.farmerList, this.loadStatus, this.currentFarmerList];

  EmployeeManagementState({
    this.farmerList,
    this.currentFarmerList,
    this.loadStatus,
  });

  EmployeeManagementState copyWith({
    List<FarmerEntity>? farmerList,
    List<FarmerEntity>? currentFarmerList,
    LoadStatus? loadStatus,
  }) {
    return EmployeeManagementState(
      farmerList: farmerList ?? this.farmerList,
      currentFarmerList: currentFarmerList ?? this.currentFarmerList,
      loadStatus: loadStatus ?? this.loadStatus,
    );
  }
}
