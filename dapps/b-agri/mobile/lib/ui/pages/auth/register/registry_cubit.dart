import 'package:bloc/bloc.dart';
import 'package:dio/dio.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/role/role_entity.dart';

import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/utils/logger.dart';
part 'registry_state.dart';

class RegistryCubit extends Cubit<RegistryState> {
  AuthRepository? repository;

  RegistryCubit({this.repository})
      : super(
            RegistryState(phone: '', username: '', password: '', fullName: ''));

  @override
  Future<void> close() {
    return super.close();
  }

  void registry(String username, String password, String fullname, String phone,
      String role) async {
    emit(state.copyWith(RegisterStatus: LoadStatus.LOADING));
    try {
      final response = await repository!
          .authRegistty(username, password, fullname, phone, role);
      if (response != null) {
        emit(state.copyWith(RegisterStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(RegisterStatus: LoadStatus.FAILURE));
      }
    } catch (error) {
      if (error is DioError) {
        logger.e(error.response!.data['error']['message']);
        emit(state.copyWith(
            messageError: error.response!.data['error']['message'],
            RegisterStatus: LoadStatus.FAILURE));
      }
    }
  }

  void usernameChange(String? username) {
    emit(state.copyWith(username: username));
  }

  void passChange(String? pass) {
    emit(state.copyWith(password: pass));
  }

  void changePhone(String? phone) {
    emit(state.copyWith(phone: phone));
  }

  void changeFullName(String? fullName) {
    emit(state.copyWith(fullName: fullName));
  }

  void changeRole(RoleEntity? value) {
    emit(state.copyWith(role: value));
  }
}
