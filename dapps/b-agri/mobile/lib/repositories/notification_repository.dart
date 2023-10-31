import 'package:flutter_base/models/entities/notification/notification.dart';
import 'package:flutter_base/models/entities/notification/notification_detail.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/network/api_client_bagri.dart';

abstract class NotificationRepository {
  Future<ObjectResponse<NotificationListData>> getListNotification();

  Future<ObjectResponse<NotificationDetailEntity>> getNotificationDataById(
      {String? notifiId});
}

class NotificationRepositoryImpl extends NotificationRepository {
  ApiClient? _apiClient;

  NotificationRepositoryImpl(ApiClient? client) {
    _apiClient = client;
  }

  @override
  Future<ObjectResponse<NotificationListData>> getListNotification() async {
    return await _apiClient!.getListNotification();
  }

  Future<ObjectResponse<NotificationDetailEntity>> getNotificationDataById(
      {String? notifiId}) async {
    return await _apiClient!.getNotificationDataById(notifiId: notifiId);
  }
}
