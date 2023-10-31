import 'package:json_annotation/json_annotation.dart';

import 'notification.dart';

part 'notification_detail.g.dart';

@JsonSerializable()
class NotificationDetailEntity {
  @JsonKey()
  NotificationEntity? notification;

  NotificationDetailEntity({
    this.notification,
  });

  NotificationDetailEntity copyWith({
    NotificationEntity? notification,
  }) {
    return NotificationDetailEntity(
      notification: notification ?? this.notification,
    );
  }

  factory NotificationDetailEntity.fromJson(Map<String, dynamic> json) =>
      _$NotificationDetailEntityFromJson(json);
  Map<String, dynamic> toJson() => _$NotificationDetailEntityToJson(this);
}
