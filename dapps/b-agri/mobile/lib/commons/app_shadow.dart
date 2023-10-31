import 'package:flutter/material.dart';

import 'app_colors.dart';

class AppShadow {
  static final boxShadow = [
    BoxShadow(
      color: AppColors.shadowColor,
      blurRadius: 3,
      spreadRadius: 1.5,
      offset: Offset(0, 4),
    )
  ];

  static final appBoxShadow = BoxShadow(
    color: AppColors.shadowColor,
    blurRadius: 2,
    spreadRadius: 1,
    offset: Offset(0, 2.5),
  );

  static final tabBarBoxShadow = [
    BoxShadow(
      color: AppColors.shadowColor,
      blurRadius: 6,
      offset: Offset(0, 3),
    ),
  ];

  static final boxShadowHideBottom = [
    BoxShadow(
      color: AppColors.lightGray,
      blurRadius: 2,
      offset: Offset(0, -2),
    ),
  ];

  static final boxShadowBottomBar = [
    BoxShadow(
      color: Color(0xffEDEDED),
      blurRadius: 1,
      offset: Offset(0, -1),
    ),
  ];

  static final boxShadowHideTop = [
    BoxShadow(
      color: Color(0x32000029),
      blurRadius: 3,
      offset: Offset(0, 1),
    ),
  ];

  static final boxShadowNormal = [
    BoxShadow(
      offset: Offset(0, 2),
      color: Color(0x32000029),
      blurRadius: 4.0,
    ),
  ];

  static final bottomButtonShadow = [
    BoxShadow(
      color: AppColors.shadowColor,
      blurRadius: 5,
      offset: Offset(0, -5),
    ),
  ];
}
