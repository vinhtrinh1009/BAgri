import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/notification/notification.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'notification_detail/notification_detail_page.dart';
import 'notification_management_cubit.dart';

class NotificationManagementPage extends StatefulWidget {
  const NotificationManagementPage({Key? key}) : super(key: key);

  @override
  _NotificationManagementPageState createState() =>
      _NotificationManagementPageState();
}

class _NotificationManagementPageState
    extends State<NotificationManagementPage> {
  late NotificationManagementCubit _cubit;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _cubit = BlocProvider.of<NotificationManagementCubit>(context);
    _cubit.getListNotification();
  }

  Future<void> _refreshData() async {
    await _cubit.getListNotification();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        title: 'Thông báo',
        context: context,
      ),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 25),
            Expanded(
                child: BlocBuilder<NotificationManagementCubit,
                    NotificationManagementState>(
              buildWhen: (prev, current) =>
                  prev.loadStatus != current.loadStatus,
              builder: (context, state) {
                if (state.loadStatus == LoadStatus.LOADING)
                  return Center(
                      child: CircularProgressIndicator(
                    color: AppColors.main,
                  ));
                else if (state.loadStatus == LoadStatus.FAILURE)
                  return Center(child: Text("Có lỗi xảy ra"));
                else if (state.loadStatus == LoadStatus.SUCCESS)
                  return RefreshIndicator(
                    color: AppColors.main,
                    onRefresh: () async {
                      _refreshData();
                    },
                    child: ListView.separated(
                        padding:
                            EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        shrinkWrap: true,
                        itemBuilder: (context, index) {
                          NotificationEntity notification =
                              state.notificationList![index];
                          return _buildItem(
                              title: notification.title ?? '',
                              description: notification.description ?? '',
                              isSeen: notification.seen ?? false,
                              onPressed: () async {
                                bool isSeen =
                                    await Application.router!.navigateTo(
                                  appNavigatorKey.currentContext!,
                                  Routes.notificationDetail,
                                  routeSettings: RouteSettings(
                                    arguments: NotificationArgument(
                                      notification_id:
                                          notification.notification_id,
                                    ),
                                  ),
                                );
                                if (isSeen) {
                                  _refreshData();
                                }
                              });
                        },
                        separatorBuilder: (context, index) {
                          return SizedBox(height: 15);
                        },
                        itemCount: state.notificationList?.length ?? 0),
                  );
                else
                  return SizedBox();
              },
            ))
          ],
        ),
      ),
    );
  }

  _buildItem({
    required String title,
    required String description,
    required bool isSeen,
    VoidCallback? onPressed,
  }) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        padding:
            const EdgeInsets.only(left: 10, right: 10, top: 10, bottom: 30),
        decoration: BoxDecoration(
          color: isSeen ? Colors.white : AppColors.grayEC,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: AppTextStyle.blackS16Bold,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: Text(
                    '$description',
                    style: AppTextStyle.blackS16,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
