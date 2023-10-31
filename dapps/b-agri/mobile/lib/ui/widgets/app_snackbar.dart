import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';

class SnackBarMessage {
  final String? message;
  final SnackBarType type;

  SnackBarMessage({
    this.message,
    this.type = SnackBarType.SUCCESS,
  });
}

enum SnackBarType {
  SUCCESS,
  ERROR,
  INFO,
}

extension SnackBarTypeExtension on SnackBarType {
  Color get backgroundColor {
    switch (this) {
      case SnackBarType.SUCCESS:
        return Color(0xFF9FC2FF);
      case SnackBarType.ERROR:
        return Color(0xFFFFEDED);
      default:
        return Color(0xFF9FC2FF);
    }
  }

  Color get messageColor {
    switch (this) {
      case SnackBarType.SUCCESS:
        return AppColors.main;
      case SnackBarType.ERROR:
        return Color(0xFFFF0000);
      default:
        return AppColors.main;
    }
  }

  Widget get prefixIcon {
    switch (this) {
      case SnackBarType.SUCCESS:
        return Icon(Icons.check_circle_outline, color: AppColors.main, size: 16);
      case SnackBarType.ERROR:
        return Image.asset(AppImages.icWarning, width: 16, height: 16, fit: BoxFit.contain);
      default:
        return Icon(Icons.info_outline, color: AppColors.main, size: 16);
    }
  }
}

class AppSnackBar extends SnackBar {
  final SnackBarMessage message;

  AppSnackBar({
    required this.message,
  }) : super(
          elevation: 0,
          content: Container(
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.all(Radius.circular(10)),
                color: message.type.backgroundColor,
              ),
              child: Row(
                children: [
                  Container(child: message.type.prefixIcon),
                  SizedBox(width: 8),
                  Expanded(
                    child: Container(
                      child: Text(message.message!,
                          style: TextStyle(
                            fontSize: 12,
                            color: message.type.messageColor,
                            fontWeight: FontWeight.w300,
                          )),
                    ),
                  ),
                ],
              ),
            ),
          ),
          padding: EdgeInsets.all(28),
          backgroundColor: Colors.transparent,
        );
}
