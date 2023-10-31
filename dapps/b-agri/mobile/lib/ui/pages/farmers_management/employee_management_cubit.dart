import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';
import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';

part 'employee_management_state.dart';

class EmployeeManagementCubit extends Cubit<EmployeeManagementState> {
  FarmerRepository farmerRepository;
  EmployeeManagementCubit({required this.farmerRepository})
      : super(EmployeeManagementState());

  Future<void> filterListFarmer(String value) async {
    if (value == "allManager")
      emit(state.copyWith(currentFarmerList: state.farmerList));
    else {
      List<FarmerEntity> farmerList = state.farmerList!
          .where((element) => element.managerId == value)
          .toList();
      emit(state.copyWith(currentFarmerList: farmerList));
    }
  }

  Future<void> getListFarmer() async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final FarmerList result = await farmerRepository.getListFarmer();

      emit(state.copyWith(
          farmerList: result.data!.farmers, loadStatus: LoadStatus.SUCCESS));

      filterListFarmer("allManager");
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }

  Future<void> deleteFarmer(String farmerId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final result = await farmerRepository.deleteFarmer(farmerId: farmerId);
      emit(state.copyWith(loadStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
