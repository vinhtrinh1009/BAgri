part of 'notification_detail_cubit.dart';

class NotificationDetailState extends Equatable {
  LoadStatus? getStatus;
  NotificationEntity? data;

  NotificationDetailState({
    this.getStatus,
    this.data,
  });

  NotificationDetailState copyWith({
    LoadStatus? getStatus,
    NotificationEntity? data,
  }) {
    return NotificationDetailState(
      getStatus: getStatus ?? this.getStatus,
      data: data ?? this.data,
    );
  }

  @override
  List<Object?> get props => [
        this.getStatus,
        this.data,
      ];
}
