import 'dart:math';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/farmer/create_farmer_param.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';

part 'employee_adding_state.dart';

class EmployeeAddingCubit extends Cubit<EmployeeAddingState> {
  FarmerRepository farmerRepository;
  EmployeeAddingCubit({required this.farmerRepository})
      : super(EmployeeAddingState());

  void changeName(String value) {
    emit(state.copyWith(fullName: value));
  }

  void changePhoneNumber(String value) {
    emit(state.copyWith(phoneNumber: value));
  }

  void changeManagerId(String value) {
    emit(state.copyWith(managerId: value));
  }

  Future<void> createFarmer() async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      CreateFarmerParam param = CreateFarmerParam(
          fullName: state.fullName,
          phone: state.phoneNumber,
          managerId: state.managerId);
      final result = await farmerRepository.createFarmer(param);

      emit(state.copyWith(loadStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
