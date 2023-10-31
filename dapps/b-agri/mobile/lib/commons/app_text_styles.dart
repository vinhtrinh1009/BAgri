import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'app_colors.dart';

class AppTextStyle {
  static final _textStyle = TextStyle(fontFamily: AppConfig.fontFamily);

  ///Black
  static final black = _textStyle.copyWith(color: AppColors.textBlack);
  //Green
  static final green = _textStyle.copyWith(color: AppColors.greenRequest);
  //s10
  static final blackS10 = black.copyWith(fontSize: 10);
  static final blackS10Bold = blackS10.copyWith(fontWeight: FontWeight.bold);

  //s12
  static final blackS12 = black.copyWith(fontSize: 12);
  static final blackS12Bold = blackS12.copyWith(fontWeight: FontWeight.bold);
  static final blackS12W800 = blackS12.copyWith(fontWeight: FontWeight.w800);
  static final blackS12W300 = blackS12.copyWith(fontWeight: FontWeight.w300);
  static final blackS12Regular = blackS12.copyWith(fontWeight: FontWeight.w400);
  static final blackTextIntro = blackS12.copyWith(color: AppColors.textBlack);

  //s13
  static final blackS13 = black.copyWith(fontSize: 13);

  //s14
  static final blackS14 = black.copyWith(fontSize: 14);
  static final blackS14SemiBold =
      blackS14.copyWith(fontWeight: FontWeight.w600);
  static final blackS14Bold = blackS14.copyWith(fontWeight: FontWeight.bold);
  static final blackS14W800 = blackS14.copyWith(fontWeight: FontWeight.w800);
  static final blackS14W300 = blackS14.copyWith(fontWeight: FontWeight.w300);
  static final blackS14Regular = blackS14.copyWith(fontWeight: FontWeight.w400);

  static final greenS14 = green.copyWith(fontSize: 14);
  static final greenS16 = green.copyWith(fontSize: 16);

  //s30
  static final green30 = green.copyWith(fontSize: 30);
  static final green30Bold = green30.copyWith(fontWeight: FontWeight.bold);

  //s16
  static final blackS16 = black.copyWith(fontSize: 16);
  static final blackS16Bold = blackS16.copyWith(fontWeight: FontWeight.bold);
  static final blackS16W800 = blackS16.copyWith(fontWeight: FontWeight.w800);

  //s18
  static final blackS18 = black.copyWith(fontSize: 18);
  static final blackS18Bold = blackS18.copyWith(fontWeight: FontWeight.bold);
  static final blackS18W800 = blackS18.copyWith(fontWeight: FontWeight.w800);

  //s24
  static final blueS24 = blue.copyWith(fontSize: 24);
  static final blueS24Bold = blueS24.copyWith(fontWeight: FontWeight.bold);

  //s30
  static final blackS30 = black.copyWith(fontSize: 30);
  static final blackS30Bold = blackS30.copyWith(fontWeight: FontWeight.bold);

  ///White
  static final white = _textStyle.copyWith(color: Colors.white);

  //s9
  static final whiteS9 = white.copyWith(fontSize: 9);
  static final whiteS9Bold = whiteS9.copyWith(fontWeight: FontWeight.bold);

  //s10
  static final whiteS10 = white.copyWith(fontSize: 10);
  static final whiteS10Bold = whiteS10.copyWith(fontWeight: FontWeight.bold);

  //s12
  static final whiteS12 = white.copyWith(fontSize: 12);
  static final whiteS12Bold = whiteS12.copyWith(fontWeight: FontWeight.bold);
  static final whiteS12W800 = whiteS12.copyWith(fontWeight: FontWeight.w800);

  //s14
  static final whiteS14 = white.copyWith(fontSize: 14);
  static final whiteS14Bold = whiteS14.copyWith(fontWeight: FontWeight.bold);
  static final whiteS14W800 = whiteS14.copyWith(fontWeight: FontWeight.w800);
  static final whiteS14Regular = whiteS14.copyWith(fontWeight: FontWeight.w400);

  //s16
  static final whiteS16 = white.copyWith(fontSize: 16);
  static final whiteS16Bold = whiteS16.copyWith(fontWeight: FontWeight.bold);
  static final whiteS16W800 = whiteS16.copyWith(fontWeight: FontWeight.w800);

  //s18
  static final whiteS18 = white.copyWith(fontSize: 18);
  static final whiteS18Bold = whiteS18.copyWith(fontWeight: FontWeight.bold);
  static final whiteS18W800 = whiteS18.copyWith(fontWeight: FontWeight.w800);

  //s24
  static final white24 = white.copyWith(fontSize: 24);
  static final white24Bold = white24.copyWith(fontWeight: FontWeight.bold);
  static final white24W800 = white24.copyWith(fontWeight: FontWeight.w800);

  ///Gray
  static final grey = _textStyle.copyWith(color: AppColors.gray);
  static final greySmall =
      _textStyle.copyWith(color: AppColors.gray, fontSize: 12);

  //s10
  static final greyS10 = grey.copyWith(fontSize: 10);
  static final greyS10Bold = greyS10.copyWith(fontWeight: FontWeight.bold);
  static final greyS10W800 = greyS10.copyWith(fontWeight: FontWeight.w800);
  static final greyS10W300 = greyS10.copyWith(fontWeight: FontWeight.w300);

  //s12
  static final greyS12 = grey.copyWith(fontSize: 12);
  static final greyS12Bold = greyS12.copyWith(fontWeight: FontWeight.bold);
  static final greyS12W800 = greyS12.copyWith(fontWeight: FontWeight.w800);
  static final greyS12W300 = greyS12.copyWith(fontWeight: FontWeight.w300);

  //s14
  static final greyS14 = grey.copyWith(fontSize: 14);
  static final greyS14Bold = greyS14.copyWith(fontWeight: FontWeight.bold);
  static final greyS14W800 = greyS14.copyWith(fontWeight: FontWeight.w800);
  static final greyS14W300 = greyS14.copyWith(fontWeight: FontWeight.w300);

  //s16
  static final greyS16 = grey.copyWith(fontSize: 16);
  static final greyS16Bold = greyS16.copyWith(fontWeight: FontWeight.bold);
  static final greyS16W300 = greyS16.copyWith(fontWeight: FontWeight.w300);
  static final greyS16W800 = greyS16.copyWith(fontWeight: FontWeight.w800);

  //s18
  static final greyS18 = grey.copyWith(fontSize: 18);
  static final greyS18Bold = greyS18.copyWith(fontWeight: FontWeight.bold);
  static final greyS18W800 = greyS18.copyWith(fontWeight: FontWeight.w800);

  ///Tint
  static final tint = _textStyle.copyWith(color: AppColors.main);

  //s10
  static final tintS10 = tint.copyWith(fontSize: 10);
  static final tintS10Bold = tintS10.copyWith(fontWeight: FontWeight.bold);

  //s11
  static final tintS11 = tint.copyWith(fontSize: 11);

  //s12
  static final tintS12 = tint.copyWith(fontSize: 12);
  static final tintS12Bold = tintS12.copyWith(fontWeight: FontWeight.bold);
  static final tintS12W800 = tintS12.copyWith(fontWeight: FontWeight.w800);
  static final tintS12Regular = tintS12.copyWith(fontWeight: FontWeight.w400);

  //s14
  static final tintS14 = tint.copyWith(fontSize: 14);
  static final tintS14Bold = tintS14.copyWith(fontWeight: FontWeight.bold);
  static final tintS14W300 = tintS14.copyWith(fontWeight: FontWeight.w300);
  static final tintS14W800 = tintS14.copyWith(fontWeight: FontWeight.w800);

  //s16
  static final tintS16 = tint.copyWith(fontSize: 16);
  static final tintS16Bold = tintS16.copyWith(fontWeight: FontWeight.bold);
  static final tintS16W800 = tintS16.copyWith(fontWeight: FontWeight.w800);

  //s17
  static final tintS17 = tint.copyWith(fontSize: 17);
  static final tintS17Bold = tintS17.copyWith(fontWeight: FontWeight.bold);
  static final tintS17W800 = tintS17.copyWith(fontWeight: FontWeight.w800);

  //s18
  static final tintS18 = tint.copyWith(fontSize: 18);
  static final tintS18Bold = tintS18.copyWith(fontWeight: FontWeight.bold);
  static final tintS18W800 = tintS18.copyWith(fontWeight: FontWeight.w800);

  //s24
  static final tintS24 = tint.copyWith(fontSize: 24);
  static final tintS24Bold = tintS24.copyWith(fontWeight: FontWeight.bold);
  static final tintS24W800 = tintS24.copyWith(fontWeight: FontWeight.w800);

  ///blue
  static final blue = _textStyle.copyWith(color: AppColors.blue);

  //s12
  static final blueS12 = blue.copyWith(fontSize: 12);
  static final blueS12Bold = blueS12.copyWith(fontWeight: FontWeight.bold);
  static final blueS12W800 = blueS12.copyWith(fontWeight: FontWeight.w800);

  //s14
  static final blueS14 = blue.copyWith(fontSize: 14);
  static final blueS14Bold = blueS14.copyWith(fontWeight: FontWeight.bold);
  static final blueS14W800 = blueS14.copyWith(fontWeight: FontWeight.w800);
  static final blueS14W300 = blueS14.copyWith(fontWeight: FontWeight.w300);
  static final blueS14Regular = blueS14.copyWith(fontWeight: FontWeight.w400);

  //s16
  static final blueS16 = blue.copyWith(fontSize: 16);
  static final blueS16Bold = blueS16.copyWith(fontWeight: FontWeight.bold);
  static final blueS16W800 = blueS16.copyWith(fontWeight: FontWeight.w800);
  static final blueS16W300 = blueS16.copyWith(fontWeight: FontWeight.w300);

  //s18
  static final blueS18 = blue.copyWith(fontSize: 18);
  static final blueS18Bold = blueS18.copyWith(fontWeight: FontWeight.bold);
  static final blueS18W800 = blueS18.copyWith(fontWeight: FontWeight.w800);
  static final blueS18W300 = blueS18.copyWith(fontWeight: FontWeight.w300);

  ///orange
  static final orange = _textStyle.copyWith(color: AppColors.orange);

  //s12
  static final orangeS12 = orange.copyWith(fontSize: 12);
  static final orangeS12Bold = orangeS12.copyWith(fontWeight: FontWeight.bold);

  //s14
  static final orangeS14 = orange.copyWith(fontSize: 14);
  static final orangeS14Bold = orangeS14.copyWith(fontWeight: FontWeight.bold);
  static final orangeS14W800 = orangeS14.copyWith(fontWeight: FontWeight.w800);
  static final orangeS14W300 = orangeS14.copyWith(fontWeight: FontWeight.w300);
  static final orangeS14Regular =
      orangeS14.copyWith(fontWeight: FontWeight.w400);

  //s15
  static final orangeS15 = orange.copyWith(fontSize: 15);
  static final orangeS15Bold = orangeS15.copyWith(fontWeight: FontWeight.bold);

  //s16
  static final orangeS16 = orange.copyWith(fontSize: 16);
  static final orangeS16Bold = orangeS16.copyWith(fontWeight: FontWeight.bold);
  static final orangeS16W800 = orangeS16.copyWith(fontWeight: FontWeight.w800);
  static final orangeS16W300 = orangeS16.copyWith(fontWeight: FontWeight.w300);

  //s18
  static final orangeS18 = orange.copyWith(fontSize: 18);

  ///red
  static final red = _textStyle.copyWith(color: AppColors.red);

  //s12
  static final redS10 = red.copyWith(fontSize: 10);
  static final redS12 = red.copyWith(fontSize: 12);
  static final redS14 = red.copyWith(fontSize: 14);

  //s16
  static final redS16 = red.copyWith(fontSize: 16);
  static final redS16Bold = redS16.copyWith(fontWeight: FontWeight.bold);

  ///Error text style
  static final errorTextStyle = blackS14;

  static final textLease =
      _textStyle.copyWith(color: AppColors.textLeaseF58220);
  static final textLeaseS16 = textLease.copyWith(fontSize: 16);
  static final textLeaseS16Bold =
      textLeaseS16.copyWith(fontWeight: FontWeight.bold);
  static final textLeaseS14 = textLease.copyWith(fontSize: 14);

  //s30
  static final textLeaseS30 = textLease.copyWith(fontSize: 30);
  static final textLeaseS30Bold =
      textLeaseS30.copyWith(fontWeight: FontWeight.bold);

  ///violet
  //s14
  static final violet = _textStyle.copyWith(color: AppColors.violetAA01B7);
  static final violetS14 = violet.copyWith(fontSize: 14);
  static final violetS14Bold = violetS14.copyWith(fontWeight: FontWeight.bold);

  ///redFF0000
  //s12
  static final redFF0 = _textStyle.copyWith(color: AppColors.redFF0000);
  static final redFF0S12 = redFF0.copyWith(fontSize: 12);

  ///Text button
  static final redTextButton = _textStyle.copyWith(
      fontSize: 16,
      color: AppColors.redTextButton,
      fontStyle: FontStyle.italic,
      decoration: TextDecoration.underline);

  static final blueTextButton = _textStyle.copyWith(
      fontSize: 16,
      color: AppColors.blueTextButton,
      fontStyle: FontStyle.italic,
      decoration: TextDecoration.underline);
}
