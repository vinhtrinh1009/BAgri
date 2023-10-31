import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/farmer/create_farmer_param.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';

part 'employee_updating_state.dart';

class EmployeeUpdatingCubit extends Cubit<EmployeeUpdatingState> {
  FarmerRepository farmerRepository;
  EmployeeUpdatingCubit({required this.farmerRepository})
      : super(EmployeeUpdatingState());

  void changeName(String value) {
    emit(state.copyWith(fullName: value));
  }

  void changeManagerId(String value) {
    emit(state.copyWith(managerId: value));
  }

  void changePhoneNumber(String value) {
    emit(state.copyWith(phoneNumber: value));
  }

  Future<void> updateFarmer(String farmerId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      CreateFarmerParam param = CreateFarmerParam(
          fullName: state.fullName,
          phone: state.phoneNumber,
          managerId: state.managerId);
      ObjectResponse<FarmerUpdateResponse> result =
          await farmerRepository.updateFarmer(farmerId: farmerId, param: param);

      emit(state.copyWith(loadStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }

  Future<void> getFarmerDetail(String farmerId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final ObjectResponse<FarmerDetailResponse> result =
          await farmerRepository.getFarmerById(farmerId);

      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS,
          farmerDetail: result.data?.farmer,
          managerId: result.data!.farmer!.manager!.id,
          fullName: result.data!.farmer!.fullname!,
          phoneNumber: result.data!.farmer!.phone!));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
