import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/models/entities/user/user_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/auth_repository.dart';

import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_management_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/utils/dialog_utils.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

import 'home_cubit.dart';

class HomePage extends StatefulWidget {
  HomePage();

  @override
  State<StatefulWidget> createState() {
    return _HomePageState();
  }
}

class _HomePageState extends State<HomePage> {
  HomeCubit? _cubit;
  AppCubit? _appCubit;
  late NotificationManagementCubit _notificationCubit;

  @override
  void initState() {
    final repository = RepositoryProvider.of<AuthRepository>(context);
    _cubit = BlocProvider.of<HomeCubit>(context);
    _appCubit = BlocProvider.of<AppCubit>(context);
    _notificationCubit = BlocProvider.of<NotificationManagementCubit>(context);

    super.initState();
    _appCubit!.getData();
    _notificationCubit.getListNotification();
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        resizeToAvoidBottomInset: false,
        backgroundColor: AppColors.main,
        body: _buildBody(),
        drawer: MainDrawer(),
      ),
    );
  }

  Widget _buildBody() {
    return SafeArea(
      child: Column(
        children: [
          _buildHeader(),
          Expanded(
              child: Container(
            padding: EdgeInsets.only(top: 10, bottom: 10),
            decoration: BoxDecoration(
              color: Colors.white,
            ),
            child: SingleChildScrollView(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  CategoryItem(
                    title: 'Quản lý vườn',
                    color: AppColors.green289768,
                    urlImage: AppImages.icGarden,
                    ridirectPage: redirectGarden,
                  ),
                  CategoryItem(
                    title: 'Quản lý mùa vụ',
                    color: AppColors.brown975D28,
                    urlImage: AppImages.icSeason,
                    ridirectPage: redirectSeason,
                  ),
                  CategoryItem(
                    title: 'Quản lý quy trình',
                    color: AppColors.blue4493DB,
                    urlImage: AppImages.icProcedure,
                    ridirectPage: redirectProcess,
                  ),
                  CategoryItem(
                    title: 'Quản lý nhân công',
                    color: AppColors.orangeE9703C,
                    urlImage: AppImages.icLabor,
                    ridirectPage: redirectEmployee,
                  ),
                ],
              ),
            ),
          ))
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      height: 100,
      decoration: BoxDecoration(
        color: AppColors.main,
      ),
      padding: EdgeInsets.only(left: 15, right: 19),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Builder(builder: (context) {
            return GestureDetector(
              onTap: () {
                Scaffold.of(context).openDrawer();
              },
              child: Padding(
                padding: const EdgeInsets.only(top: 13),
                child: Image.asset(
                  AppImages.icMenuFold,
                  width: 19,
                  height: 15,
                  fit: BoxFit.fill,
                ),
              ),
            );
          }),
          Expanded(
              child: Padding(
            padding: const EdgeInsets.only(top: 7),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                      width: 50,
                      height: 46,
                      child: Image.asset(
                        AppImages.icCloudBA,
                        fit: BoxFit.fill,
                      )),
                  Container(
                    height: 30,
                    child: BlocBuilder<AppCubit, AppState>(
                      builder: (context, state) {
                        if (state.weather != null) {
                          return Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                '${state.weather!.main!.temp!.toInt()}℃',
                                style: AppTextStyle.whiteS12
                                    .copyWith(fontSize: 20),
                              ),
                              Text(
                                '  |  ',
                                style: AppTextStyle.whiteS12
                                    .copyWith(fontSize: 20),
                              ),
                              Image.asset(
                                AppImages.icHumidity,
                                width: 10,
                                height: 15,
                                fit: BoxFit.fill,
                              ),
                              Text(
                                ' ${state.weather!.main!.humidity!.toInt()}%',
                                style: AppTextStyle.whiteS12
                                    .copyWith(fontSize: 20),
                              ),
                            ],
                          );
                        } else {
                          return Container();
                        }
                      },
                    ),
                  ),
                ]),
          )),
          GestureDetector(
            onTap: () {
              redirectNotificationPage();
            },
            child: Padding(
              padding: const EdgeInsets.only(top: 13),
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  Image.asset(
                    AppImages.icNotificationBA,
                    width: 16,
                    height: 19,
                    fit: BoxFit.fill,
                  ),
                  Positioned(
                      top: -5,
                      right: -7,
                      child: BlocBuilder<NotificationManagementCubit,
                          NotificationManagementState>(
                        buildWhen: (prev, current) =>
                            prev.loadStatus != current.loadStatus,
                        builder: (context, state) {
                          if (state.loadStatus == LoadStatus.SUCCESS) {
                            var length = 0;
                            for (int i = 0;
                                i < state.notificationList!.length;
                                i++) {
                              if (state.notificationList![i].seen == false) {
                                length++;
                              }
                            }
                            if (length > 0) {
                              return CircleAvatar(
                                backgroundColor: Colors.red,
                                radius: 8,
                                child: FittedBox(
                                  child: Text(
                                    '$length',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                ),
                              );
                            } else {
                              return SizedBox();
                            }
                          } else
                            return SizedBox();
                        },
                      ))
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  void redirectNotificationPage() {
    Application.router?.navigateTo(context, Routes.notificationManagement);
  }

  void redirectGarden() {
    Application.router?.navigateTo(context, Routes.gardenList);
  }

  void redirectSeason() {
    Application.router?.navigateTo(context, Routes.seasonManagement);
  }

  void redirectProcess() {
    Application.router?.navigateTo(context, Routes.tabProcess);
  }

  void redirectEmployee() {
    Application.router?.navigateTo(context, Routes.employeeManagement);
  }
}

class CategoryItem extends StatelessWidget {
  final String? title;
  final Color? color;
  final String? urlImage;
  final VoidCallback? ridirectPage;

  const CategoryItem({
    Key? key,
    this.title,
    this.color,
    this.urlImage,
    this.ridirectPage,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: ridirectPage,
      child: Container(
        height: 80,
        padding: EdgeInsets.symmetric(vertical: 22, horizontal: 20),
        margin: EdgeInsets.symmetric(horizontal: 15, vertical: 8),
        decoration: BoxDecoration(
          color: color!,
          borderRadius: BorderRadius.all(Radius.circular(10)),
        ),
        alignment: Alignment.center,
        child: Row(
          children: [
            SizedBox(width: 40),
            Image.asset(
              urlImage!,
              height: 36,
              width: 36,
              fit: BoxFit.cover,
            ),
            SizedBox(width: 20),
            Expanded(
              child: Text(
                title!,
                style: AppTextStyle.whiteS14Bold.copyWith(fontSize: 20),
                overflow: TextOverflow.ellipsis,
              ),
            )
          ],
        ),
      ),
    );
  }
}

class MainDrawer extends StatefulWidget {
  @override
  _MainDrawerState createState() => _MainDrawerState();
}

class _MainDrawerState extends State<MainDrawer> {
  AppCubit? _appCubit;
  UserEntity? _userInfo;
  @override
  void initState() {
    super.initState();
    _appCubit = BlocProvider.of<AppCubit>(context);
    _userInfo = GlobalData.instance.userEntity;
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Scaffold(
        appBar: AppBarWidget(
          title: "",
          context: context,
        ),
        body: ListView(
          // Important: Remove any padding from the ListView.
          padding: EdgeInsets.zero,
          children: [
            Container(
              height: 100,
              child: DrawerHeader(
                decoration: BoxDecoration(),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${_userInfo?.fullname ?? ""}',
                      style: TextStyle(color: Colors.black87, fontSize: 20),
                    ),
                    SizedBox(
                      height: 10,
                    ),
                    Row(
                      children: [
                        Text(
                          'Vai trò: ',
                          style: TextStyle(color: Colors.black87, fontSize: 18),
                        ),
                        Text(
                          '${_userInfo?.role == "ktv" ? "Kỹ Thuật Viên" : "Quản Lý Vườn"}',
                          style: TextStyle(color: AppColors.main, fontSize: 18),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            GestureDetector(
              onTap: () {
                Application.router!.navigateTo(
                  context,
                  Routes.changePassword,
                );
              },
              child: Container(
                height: 35,
                padding: EdgeInsets.symmetric(horizontal: 10),
                child: Row(
                  children: [
                    IconButton(
                        padding: EdgeInsets.only(right: 10),
                        onPressed: () {},
                        icon: Image.asset(
                          AppImages.icChangePass,
                          fit: BoxFit.fill,
                        )),
                    Text('Đổi mật khẩu'),
                  ],
                ),
              ),
            ),
            SizedBox(
              height: 5,
            ),
            GestureDetector(
              onTap: () {
                showTokenExpiredDialog();
              },
              child: Container(
                height: 35,
                padding: EdgeInsets.symmetric(horizontal: 10),
                child: Row(
                  children: [
                    IconButton(
                        padding: EdgeInsets.only(right: 10),
                        onPressed: () {},
                        icon: Image.asset(
                          AppImages.icLogout,
                          fit: BoxFit.fill,
                        )),
                    Text(
                      'Đăng xuất',
                      style: TextStyle(color: Color(0xFFD7443B)),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void showTokenExpiredDialog() {
    DialogUtils.showNotificationDialog(
      context,
      title: "Bạn có chắc chắc muốn đăng xuất?",
      okText: "Xác nhận!",
      showCloseButton: true,
      onOkPressed: () {
        _appCubit!.removeUserSection();
        Application.router!
            .navigateTo(context, Routes.login, clearStack: true, replace: true);
      },
    );
  }
}
