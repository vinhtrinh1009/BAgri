import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/repositories/notification_repository.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_detail/notification_detail_cubit.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_detail/notification_detail_page.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_management_cubit.dart';
import 'package:flutter_base/ui/pages/notification_management/notification_management_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Handler notificationManagementHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return NotificationManagementPage();
});

Handler notificationDetailHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  NotificationArgument args =
      context!.settings!.arguments as NotificationArgument;

  return BlocProvider(
    create: (context) {
      final repository = RepositoryProvider.of<NotificationRepository>(context);
      return NotificationDetailCubit(repository: repository);
    },
    child: NotificationDetailPage(
      notification_id: args.notification_id,
    ),
  );
});
