import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/screen_size.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/dialogs/app_dialog.dart';
import 'package:flutter_base/ui/pages/splash/splash_cubit.dart';
import 'package:flutter_base/utils/utils.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:permission_handler/permission_handler.dart';

class SplashPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _SplashPageState();
  }
}

class _SplashPageState extends State<SplashPage> {
  late SplashCubit _cubit;
  late StreamSubscription _navigationSubscription;

  @override
  void initState() {
    final authBagriRepository = RepositoryProvider.of<AuthRepository>(context);
    _cubit = SplashCubit(
      authBagriRepository: authBagriRepository,
    );
    super.initState();
    Utils.determinePosition();

    _navigationSubscription = _cubit.navigatorController.stream.listen((event) {
      Future.delayed(const Duration(seconds: 2), () {
        switch (event) {
          case SplashNavigator.OPEN_GARDEN_QLV:
            showGardenManagementByQLV();
            break;
          case SplashNavigator.OPEN_HOME:
            showHome();
            break;
          case SplashNavigator.OPEN_LOGIN:
            showLogin();
            break;
          case SplashNavigator.OPEN_LOAD_DATA_FAILURE:
            showErrorHapped();
            break;
        }
      });
    });
    _setup();
  }

  void _setup() async {
    //Request permission
    var status = await Permission.storage.status;
    if (status.isDenied) {
      // You can request multiple permissions at once.
      await Permission.storage.request();
    }
    _cubit.fetchInitialData();
  }

  @override
  void dispose() {
    _navigationSubscription.cancel();
    _cubit.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // SplashBackgroundWidget(),
          Container(
            width: double.infinity,
            height: double.infinity,
            child: Center(
              child: Container(
                  child: Image.asset(AppImages.icBAgri,
                      width: 225, height: 225, fit: BoxFit.fill)),
            ),
          ),
          Container(
            alignment: Alignment.bottomCenter,
            margin: EdgeInsets.only(
                bottom: ScreenSize.of(context).bottomPadding + 10),
          ),
        ],
      ),
    );
  }

  void showHome() {
    Application.router?.navigateTo(context, Routes.home, replace: true);
  }

  void showGardenManagementByQLV() {
    Application.router!
        .navigateTo(context, Routes.gardenListByQVL, clearStack: true);
  }

  void showLogin() {
    Application.router?.navigateTo(context, Routes.login, replace: true);
  }

  void showErrorHapped() {
    AppDialog(
      context: context,
      type: DialogType.ERROR,
      title: S.of(context).common_fetchDataFailure,
      description: "Không thể kết nối tới máy chủ. Xin vui lòng thử lại!",
      okText: "Thử lại",
      onOkPressed: () {
        _cubit.fetchInitialData();
      },
      dismissible: false,
    ).show();
  }
}
