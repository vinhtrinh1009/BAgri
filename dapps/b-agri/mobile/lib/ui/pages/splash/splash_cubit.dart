import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/database/share_preferences_helper.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/models/entities/user/user_entity.dart';

import 'package:flutter_base/repositories/auth_repository.dart';

import 'package:rxdart/rxdart.dart';

part 'splash_state.dart';

enum SplashNavigator {
  OPEN_HOME,
  OPEN_LOGIN,
  OPEN_GARDEN_QLV,
  OPEN_LOAD_DATA_FAILURE,
}

class SplashCubit extends Cubit<SplashState> {
  AuthRepository? authBagriRepository;

  final messageController = PublishSubject<String>();
  final navigatorController = PublishSubject<SplashNavigator>();

  SplashCubit({
    this.authBagriRepository,
  }) : super(SplashState());

  void fetchInitialData() async {
    String? token = await SharedPreferencesHelper.getToken();
    String? role = await SharedPreferencesHelper.getRole();
    UserEntity? _userInfo = await SharedPreferencesHelper.getUserInfo();

    ///Check login and fetch profile
    if (token == null) {
      navigatorController.sink.add(SplashNavigator.OPEN_LOGIN);
    } else {
      if (role == 'ktv') {
        GlobalData.instance.token = token;
        GlobalData.instance.role = role;
        GlobalData.instance.userEntity = _userInfo;
        navigatorController.sink.add(SplashNavigator.OPEN_HOME);
      } else {
        GlobalData.instance.token = token;
        GlobalData.instance.role = role;
        GlobalData.instance.userEntity = _userInfo;
        navigatorController.sink.add(SplashNavigator.OPEN_GARDEN_QLV);
        // navigatorController.sink.add(SplashNavigator.OPEN_HOME);
      }
    }
  }

  @override
  Future<void> close() {
    messageController.close();
    navigatorController.close();
    return super.close();
  }
}
