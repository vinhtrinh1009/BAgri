import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';

class AppSnackBar extends SnackBar {
  final String message;
  AppSnackBar({required this.message})
      : super(
          elevation: 0,
          backgroundColor: AppColors.main,
          behavior: SnackBarBehavior.floating,
          margin: EdgeInsets.symmetric(horizontal: 23, vertical: 10),
          padding: EdgeInsets.zero,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
          content: Container(
            height: 40,
            alignment: Alignment.center,
            child: Text(
              message,
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white, fontSize: 18),
            ),
          ),
          duration: Duration(seconds: 2),
        );
}
