part of 'employee_updating_cubit.dart';

class EmployeeUpdatingState extends Equatable {
  LoadStatus? loadStatus;
  String? fullName;
  String? phoneNumber;
  String? managerId;
  FarmerDetailEntity? farmerDetail;

  bool get buttonEnabled {
    if (fullName == null || phoneNumber == null || managerId == null)
      return false;
    else {
      if (fullName!.isEmpty || phoneNumber!.isEmpty)
        return false;
      else
        return true;
    }
  }

  @override
  List<dynamic> get props =>
      [fullName, phoneNumber, managerId, loadStatus, farmerDetail];

  EmployeeUpdatingState({
    this.loadStatus,
    this.fullName,
    this.phoneNumber,
    this.managerId,
    this.farmerDetail,
  });

  EmployeeUpdatingState copyWith({
    LoadStatus? loadStatus,
    String? fullName,
    String? phoneNumber,
    String? managerId,
    FarmerDetailEntity? farmerDetail,
  }) {
    return EmployeeUpdatingState(
      loadStatus: loadStatus ?? this.loadStatus,
      fullName: fullName ?? this.fullName,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      managerId: managerId ?? this.managerId,
      farmerDetail: farmerDetail ?? this.farmerDetail,
    );
  }
}
