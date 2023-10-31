import 'package:bloc/bloc.dart';
import 'package:flutter_base/models/entities/notification/notification.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/notification_repository.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/enums/load_status.dart';
part 'notification_management_state.dart';

class NotificationManagementCubit extends Cubit<NotificationManagementState> {
  NotificationRepository repository;

  NotificationManagementCubit({required this.repository})
      : super(NotificationManagementState());

  Future<void> getListNotification() async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final ObjectResponse<NotificationListData> result =
          await repository.getListNotification();
      if (result != null) {
        emit(state.copyWith(
            notificationList: result.data!.notifications,
            loadStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
