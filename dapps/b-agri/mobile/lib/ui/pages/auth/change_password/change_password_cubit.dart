import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/utils/logger.dart';

part 'change_password_state.dart';

class ChangePasswordCubit extends Cubit<ChangePasswordState> {
  AuthRepository? repository;

  ChangePasswordCubit({this.repository}) : super(ChangePasswordState());

  @override
  Future<void> close() {
    return super.close();
  }

  void changePassword(
      String oldPass, String newPass, String confirmedPass) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final result =
          await repository!.changePassword(oldPass, newPass, confirmedPass);
      if (result != null) {
        emit(state.copyWith(loadStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
      }
    } catch (error) {
      logger.e(error);
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }

  void removeUserSection() {
    repository!.removeToken();
    GlobalData.instance.token = null;
  }
}
