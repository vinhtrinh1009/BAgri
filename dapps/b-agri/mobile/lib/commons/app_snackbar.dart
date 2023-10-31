import 'package:flutter/material.dart';
import 'package:get/get.dart';

class AppSnackbar {
  AppSnackbar._();

  static bool? get isShowing {
    return Get.isSnackbarOpen;
  }

  static void showInfo({String? title, String? message}) {
    Get.snackbar(
      title ?? "Thông báo",
      message ?? "",
      backgroundColor: Colors.white,
      colorText: Colors.black,
    );
  }

  static void showWarning({String? title, String? message}) {
    Get.snackbar(
      title ?? "Cảnh báo",
      message ?? "",
      backgroundColor: Colors.amber,
      colorText: Colors.white,
    );
  }

  static void showError({String? title, String? message}) {
    Get.snackbar(
      title ?? "Lỗi",
      message ?? "",
      backgroundColor: Colors.red,
      colorText: Colors.white,
    );
  }
}