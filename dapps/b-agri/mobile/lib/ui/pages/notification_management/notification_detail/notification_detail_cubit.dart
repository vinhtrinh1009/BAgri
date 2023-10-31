import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/notification/notification.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/notification_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:rxdart/rxdart.dart';
part 'notification_detail_state.dart';

class NotificationDetailCubit extends Cubit<NotificationDetailState> {
  NotificationRepository? repository;

  NotificationDetailCubit({this.repository}) : super(NotificationDetailState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void fetchNotifiDetail(String? notifiId) async {
    emit(state.copyWith(getStatus: LoadStatus.LOADING));
    try {
      final response =
          await repository!.getNotificationDataById(notifiId: notifiId);
      if (response != null) {
        emit(state.copyWith(
          getStatus: LoadStatus.SUCCESS,
          data: response.data!.notification,
        ));
      } else {
        emit(state.copyWith(getStatus: LoadStatus.FAILURE));
      }
    } catch (error) {
      emit(state.copyWith(getStatus: LoadStatus.FAILURE));
    }
  }
}
