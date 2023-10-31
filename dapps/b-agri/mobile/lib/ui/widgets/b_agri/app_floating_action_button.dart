import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class AppFloatingActionButton extends FloatingActionButton {
  final VoidCallback onPressed;
  AppFloatingActionButton({required this.onPressed})
      : super(
            onPressed: onPressed,
            backgroundColor: AppColors.main,
            child: Text(
              '+',
              style: AppTextStyle.whiteS14Bold.copyWith(fontSize: 30),
            ));
}
