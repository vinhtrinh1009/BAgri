import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/notification/notification.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'notification_detail_cubit.dart';

class NotificationDetailPage extends StatefulWidget {
  final String? notification_id;
  NotificationDetailPage({Key? key, this.notification_id}) : super(key: key);

  @override
  _NotificationDetailPageState createState() => _NotificationDetailPageState();
}

class _NotificationDetailPageState extends State<NotificationDetailPage> {
  NotificationDetailCubit? _cubit;
  final _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<NotificationDetailCubit>(context);
    _cubit!.fetchNotifiDetail(widget.notification_id);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
          context: context,
          title: 'Chi tiết thông báo',
          onBackPressed: () {
            Navigator.of(context).pop(true);
          }),
      body: SafeArea(
        child: buildBody(),
      ),
    );
  }

  Widget buildBody() {
    return BlocBuilder<NotificationDetailCubit, NotificationDetailState>(
      bloc: _cubit,
      buildWhen: (previous, current) => previous.getStatus != current.getStatus,
      builder: (context, state) {
        if (state.getStatus == LoadStatus.LOADING) {
          return Center(
              child: CircularProgressIndicator(
            color: AppColors.main,
          ));
        } else if (state.getStatus == LoadStatus.FAILURE) {
          return Container();
        } else if (state.getStatus == LoadStatus.SUCCESS) {
          NotificationEntity notification = state.data!;
          return Padding(
              padding: EdgeInsets.symmetric(horizontal: 18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(height: 40),
                  Text(
                    notification.title!,
                    style: AppTextStyle.blackS16Bold,
                  ),
                  SizedBox(height: 10),
                  Text(
                    notification.description!,
                    style: AppTextStyle.blackS16,
                  ),
                ],
              ));
        } else
          return SizedBox();
      },
    );
  }
}

class NotificationArgument {
  String? notification_id;
  String? title;
  String? description;

  NotificationArgument({this.title, this.description, this.notification_id});
}
