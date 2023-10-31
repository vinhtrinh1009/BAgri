part of 'employee_adding_cubit.dart';

class EmployeeAddingState extends Equatable {
  LoadStatus? loadStatus;
  String? fullName;
  String? phoneNumber;
  String? managerId;

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
  List<dynamic> get props => [fullName, phoneNumber, managerId, loadStatus];

  EmployeeAddingState({
    this.loadStatus,
    this.fullName,
    this.phoneNumber,
    this.managerId,
  });

  EmployeeAddingState copyWith({
    LoadStatus? loadStatus,
    String? fullName,
    String? phoneNumber,
    String? managerId,
  }) {
    return EmployeeAddingState(
      loadStatus: loadStatus ?? this.loadStatus,
      fullName: fullName ?? this.fullName,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      managerId: managerId ?? this.managerId,
    );
  }
}
