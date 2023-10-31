import 'package:json_annotation/json_annotation.dart';

part 'notification.g.dart';

@JsonSerializable()
class NotificationListData {
  List<NotificationEntity>? notifications;

  NotificationListData({
    this.notifications,
  });

  NotificationListData copyWith({
    List<NotificationEntity>? notifications,
  }) {
    return NotificationListData(
      notifications: notifications ?? this.notifications,
    );
  }

  factory NotificationListData.fromJson(Map<String, dynamic> json) =>
      _$NotificationListDataFromJson(json);
  Map<String, dynamic> toJson() => _$NotificationListDataToJson(this);
}

@JsonSerializable()
class NotificationEntity {
  String? title;
  String? description;
  String? notification_id;
  bool? seen;

  factory NotificationEntity.fromJson(Map<String, dynamic> json) =>
      _$NotificationEntityFromJson(json);
  Map<String, dynamic> toJson() => _$NotificationEntityToJson(this);

  NotificationEntity({
    this.title,
    this.description,
    this.notification_id,
    this.seen,
  });

  NotificationEntity copyWith({
    String? title,
    String? description,
    String? notification_id,
    bool? seen,
  }) {
    return NotificationEntity(
      title: title ?? this.title,
      description: description ?? this.description,
      notification_id: notification_id ?? this.notification_id,
      seen: seen ?? this.seen,
    );
  }
}
