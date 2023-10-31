part of 'notification_management_cubit.dart';

class NotificationManagementState extends Equatable {
  List<NotificationEntity>? notificationList;
  LoadStatus? loadStatus;

  NotificationManagementState({
    this.notificationList,
    this.loadStatus,
  });

  NotificationManagementState copyWith({
    List<NotificationEntity>? notificationList,
    LoadStatus? loadStatus,
  }) {
    return NotificationManagementState(
      notificationList: notificationList ?? this.notificationList,
      loadStatus: loadStatus ?? this.loadStatus,
    );
  }

  @override
  List<dynamic> get props => [
        this.notificationList,
        this.loadStatus,
      ];
}
