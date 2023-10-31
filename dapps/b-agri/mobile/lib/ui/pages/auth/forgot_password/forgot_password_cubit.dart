import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/utils/logger.dart';

part 'forgot_password_state.dart';

class ForgotPasswordCubit extends Cubit<ForgotPasswordState> {
  AuthRepository? repository;

  ForgotPasswordCubit({this.repository}) : super(ForgotPasswordState());

  @override
  Future<void> close() {
    return super.close();
  }

  void forgotPassword(String userName, String phone) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final result = await repository!.forgotPassword(userName, phone);
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
}
