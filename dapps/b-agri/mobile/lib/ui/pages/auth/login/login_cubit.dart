import 'package:bloc/bloc.dart';
import 'package:dio/dio.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/database/share_preferences_helper.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/models/entities/role/role_entity.dart';
import 'package:flutter_base/models/entities/user/user_entity.dart';
import 'package:flutter_base/models/response/object_response.dart';

import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/repositories/user_repository.dart';

import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:flutter_base/utils/logger.dart';
import 'package:flutter_base/utils/validators.dart';
import 'package:rxdart/rxdart.dart';

part 'login_state.dart';

enum LoginNavigator {
  OPEN_HOME,
  OPEN_GARDEN,
}

class LoginCubit extends Cubit<LoginState> {
  AuthRepository? repository;
  UserRepository userRepository;

  LoginCubit({this.repository, required this.userRepository})
      : super(LoginState());

  final navigatorController = PublishSubject<LoginNavigator>();
  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    navigatorController.close();
    showMessageController.close();
    return super.close();
  }

  void clearInformation() {
    emit(state.copyWith(username: "", password: ""));
  }

  void signIn(String username, String password) async {
    //validate
    if (username.isEmpty) {
      showMessageController.sink.add(SnackBarMessage(
        message: 'Chưa nhập tên đăng nhập',
        type: SnackBarType.ERROR,
      ));
      return;
    }
    if (password.isEmpty) {
      showMessageController.sink.add(SnackBarMessage(
        message: 'Chưa nhập mật khẩu',
        type: SnackBarType.ERROR,
      ));
      return;
    }
    emit(state.copyWith(LoginStatus: LoginStatusBagri.LOADING));
    try {
      final result = await repository!.signIn(username, password);
      SharedPreferencesHelper.setToken(result.data!.token!);
      GlobalData.instance.token = result.data?.token;

      emit(state.copyWith(LoginStatus: LoginStatusBagri.SUCCESS));
      if (result.data?.token != null) {
        try {
          final ObjectResponse<UserEntity> userRes =
              await userRepository.getProfile();
          if (userRes.data!.role == 'ktv') {
            navigatorController.sink.add(LoginNavigator.OPEN_HOME);
          } else {
            navigatorController.sink.add(LoginNavigator.OPEN_GARDEN);
            // navigatorController.sink.add(LoginNavigator.OPEN_HOME);
          }
          SharedPreferencesHelper.setRole(userRes.data!.role ?? "");
          GlobalData.instance.role = userRes.data!.role;
          SharedPreferencesHelper.setUserInfo(userRes.data!);
          GlobalData.instance.userEntity = userRes.data!;
        } catch (error) {
          logger.e(error);
          if (error is DioError) {
            emit(state.copyWith(LoginStatus: LoginStatusBagri.FAILURE));
            showMessageController.sink.add(SnackBarMessage(
              message: error.response!.data['error']['message'],
              type: SnackBarType.ERROR,
            ));
          }
        }
      } else {
        emit(state.copyWith(LoginStatus: LoginStatusBagri.FAILURE));
      }
    } catch (error) {
      logger.e(error);
      if (error is DioError) {
        emit(state.copyWith(LoginStatus: LoginStatusBagri.FAILURE));
        showMessageController.sink.add(SnackBarMessage(
          message: error.response!.data['error']['message'],
          type: SnackBarType.ERROR,
        ));
      }
    }
  }

  void usernameChange(String username) {
    emit(state.copyWith(username: username));
  }

  void passChange(String pass) {
    emit(state.copyWith(password: pass));
  }

  void changeRole(RoleEntity? value) {
    emit(state.copyWith(role: value));
  }
}
