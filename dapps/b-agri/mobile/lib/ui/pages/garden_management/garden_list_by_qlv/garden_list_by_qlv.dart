import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';

import 'package:flutter_base/models/entities/garden/season_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/garden_task_page.dart';
import 'package:flutter_base/ui/pages/home/home_page.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_management_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_emty_data_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';

import 'package:flutter_base/ui/widgets/error_list_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'garden_list_by_qlv_cubit.dart';

class GardenListByQVLPage extends StatefulWidget {
  @override
  _GardenListByQVLState createState() => _GardenListByQVLState();
}

class _GardenListByQVLState extends State<GardenListByQVLPage> {
  GardenListByQlvCubit? _cubit;
  AppCubit? _appCubit;
  late NotificationManagementCubit _notificationCubit;

  final _scrollController = ScrollController();
  final _scrollThreshold = 200.0;

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<GardenListByQlvCubit>(context);
    _appCubit = BlocProvider.of<AppCubit>(context);
    _notificationCubit = BlocProvider.of<NotificationManagementCubit>(context);

    _appCubit!.getData();
    _cubit!.fetchGardensByManagerId();
    _notificationCubit.getListNotification();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: AppColors.main,
      body: buildBody(),
      drawer: MainDrawer(),
    );
  }

  Widget buildBody() {
    return SafeArea(
      child: Column(
        children: [
          _buildHeader(),
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(12.0),
                    topRight: Radius.circular(12.0)),
              ),
              child: BlocBuilder<GardenListByQlvCubit, GardenListByQlvState>(
                bloc: _cubit,
                buildWhen: (previous, current) =>
                    previous.getGardenStatus != current.getGardenStatus,
                builder: (context, state) {
                  if (state.getGardenStatus == LoadStatus.LOADING) {
                    return Center(
                        child: CircularProgressIndicator(
                      color: AppColors.main,
                    ));
                  } else if (state.getGardenStatus == LoadStatus.FAILURE) {
                    return _buildFailureList();
                  } else if (state.getGardenStatus == LoadStatus.SUCCESS) {
                    return state.listGardenData!.length != 0
                        ? RefreshIndicator(
                            onRefresh: _onRefreshData,
                            child: ListView.builder(
                              padding: EdgeInsets.only(
                                  left: 10, right: 10, top: 10, bottom: 25),
                              physics: AlwaysScrollableScrollPhysics(),
                              itemCount: state.listGardenData!.length,
                              shrinkWrap: true,
                              primary: false,
                              controller: _scrollController,
                              itemBuilder: (context, index) {
                                return _gardenItemView(
                                    state.listGardenData![index]);
                              },
                            ),
                          )
                        : Expanded(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Center(
                                  child: EmptyDataWidget(),
                                ),
                              ],
                            ),
                          );
                  } else {
                    return Container();
                  }
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      height: 60,
      color: AppColors.main,
      child: Stack(
        children: [
          Container(
            height: 60,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'Chọn vườn',
                  style: TextStyle(fontSize: 22, color: Colors.white),
                ),
              ],
            ),
          ),
          Builder(builder: (context) {
            return GestureDetector(
              onTap: () {
                Scaffold.of(context).openDrawer();
              },
              child: Align(
                alignment: Alignment.topLeft,
                child: Container(
                    height: 60,
                    width: 60,
                    alignment: Alignment.center,
                    child: Image.asset(
                      AppImages.icMenuFold,
                      width: 19,
                      height: 15,
                      fit: BoxFit.fill,
                    )),
              ),
            );
          }),
          GestureDetector(
            onTap: () {
              redirectNotificationPage();
            },
            child: Align(
              alignment: Alignment.topRight,
              child: Container(
                  height: 60,
                  width: 60,
                  alignment: Alignment.center,
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
                          top: -3,
                          right: -5,
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
                                  if (state.notificationList![i].seen ==
                                      false) {
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
                  )),
            ),
          ),
        ],
      ),
    );
  }

  Widget _gardenItemView(GardenEntity data) {
    String gardenId = data.garden_id ?? '';
    String name = data.name ?? '';
    int area = data.area ?? 0;
    ProcessEntity? process = data.process;
    SeasonEntity? season = data.season;

    return GestureDetector(
      onTap: () {
        if (season!.season_id != null) {
          _handleRouteGardenDetail(data);
        } else {
          showSnackBar('Hiện tại vườn chưa có mùa vụ');
        }
      },
      child: Container(
          height: 60,
          margin: EdgeInsets.symmetric(horizontal: 3, vertical: 10),
          padding: EdgeInsets.only(left: 10, top: 10, right: 10, bottom: 10),
          decoration: BoxDecoration(
            color: AppColors.grayEC,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '$name',
                style: AppTextStyle.greyS16Bold,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          )),
    );
  }

  Widget _buildEmptyList() {
    return ErrorListWidget(
      text: S.of(context).no_data_show,
      onRefresh: _onRefreshData,
    );
  }

  Widget _buildFailureList() {
    return ErrorListWidget(
      text: S.of(context).error_occurred,
      onRefresh: _onRefreshData,
    );
  }

  Future<void> _onRefreshData() async {
    _cubit!.fetchGardensByManagerId();
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }

  void _handleRouteGardenDetail(GardenEntity garden) {
    Application.router!.navigateTo(
      appNavigatorKey.currentContext!,
      Routes.gardenTask,
      routeSettings: RouteSettings(
        arguments: GardenTaskArgument(
          garden_id: garden.garden_id,
          name: garden.name,
          process_id: garden.process?.process_id,
          season_id: garden.season?.season_id,
        ),
      ),
    );
  }

  void _onScroll() {
    final maxScroll = _scrollController.position.maxScrollExtent;
    final currentScroll = _scrollController.position.pixels;
    if (maxScroll - currentScroll <= _scrollThreshold) {
      // _cubit!.fetchNextGardenData();
    }
  }

  void redirectNotificationPage() {
    Application.router?.navigateTo(context, Routes.notificationManagement);
  }

  @override
  bool get wantKeepAlive => true;
}
