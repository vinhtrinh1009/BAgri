import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/ui/widgets/loading_indicator_widget.dart';

class _AppButton extends StatelessWidget {
  String? title;
  bool isLoading;
  bool? isEnable;
  VoidCallback? onPressed;
  double borderRadius;
  Color backgroundColor = Colors.white;
  TextStyle? textStyle = AppTextStyle.whiteS14Bold;
  BoxDecoration? buttonBoxDecoration;
  BoxBorder? border;
  double? height;

  _AppButton({
    this.title = '',
    this.isLoading = false,
    this.isEnable = true,
    this.onPressed,
    this.borderRadius = 8,
    this.textStyle,
    this.buttonBoxDecoration,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height ?? 36,
      width: double.infinity,
      child: ButtonTheme(
        minWidth: 0.0,
        height: 0.0,
        padding: EdgeInsets.all(0),
        child: FlatButton(
          child: _buildBodyWidget(),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(borderRadius),
          ),
          onPressed: isEnable! ? onPressed : null,
        ),
      ),
      decoration: buttonBoxDecoration ??
          BoxDecoration(
            color: isEnable! ? backgroundColor : Color(0xFFCBCBCB),
            borderRadius: BorderRadius.all(Radius.circular(borderRadius)),
            boxShadow: isEnable! ? AppShadow.boxShadow : [],
            border: border,
          ),
    );
  }

  Widget _buildBodyWidget() {
    if (isLoading) {
      return LoadingIndicatorWidget(color: Colors.white);
    } else {
      return Text(
        title!,
        style: textStyle,
      );
    }
  }
}

class AppWhiteButton extends _AppButton {
  AppWhiteButton({
    String title = '',
    bool isEnable = true,
    bool isLoading = false,
    VoidCallback? onPressed,
    double borderRadius = 20,
    TextStyle? textStyle,
    double? height,
  }) {
    this.height = height;
    this.title = title;
    this.isLoading = isLoading;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.blackS14Bold;
    backgroundColor = Colors.white;
    this.borderRadius = borderRadius;
    this.buttonBoxDecoration = BoxDecoration(
        color: isEnable ? backgroundColor : Color(0xFFCBCBCB),
        borderRadius: BorderRadius.all(Radius.circular(borderRadius)),
        border: Border.all(color: AppColors.gray, width: 1));
  }
}

class AppTintButton extends _AppButton {
  AppTintButton({
    String? title = '',
    bool isLoading = false,
    bool? isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.main;
    this.borderRadius = borderRadius ?? 20;
  }
}

class AppBlueButton extends _AppButton {
  AppBlueButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.blue;
    this.borderRadius = borderRadius ?? 20;
    this.borderRadius = borderRadius ?? 20;
  }
}

class AppGreyButton extends _AppButton {
  AppGreyButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    textStyle = AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.buttonGrey;
    this.borderRadius = borderRadius ?? 20;
  }
}

class AppOrangeButton extends _AppButton {
  AppOrangeButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.orange;
    this.borderRadius = borderRadius ?? 20;
  }
}

class AppTintBorderButton extends _AppButton {
  AppTintBorderButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
    BoxBorder? border,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.tintS14;
    this.borderRadius = borderRadius ?? 20;
    this.border = border ?? Border.all(color: AppColors.main);
  }
}

class AppWhiteCustomButton extends StatelessWidget {
  final String title;
  final bool isLoading;
  final VoidCallback? onPressed;

  AppWhiteCustomButton(
      {required this.title, this.isLoading = false, this.onPressed});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 36,
      width: double.infinity,
      child: ButtonTheme(
        minWidth: 0.0,
        height: 0.0,
        padding: EdgeInsets.all(0),
        child: FlatButton(
          child: isLoading
              ? LoadingIndicatorWidget(color: Colors.white)
              : Text(
                  title,
                  style: AppTextStyle.blackS14,
                ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          onPressed: onPressed,
        ),
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(width: 1, color: AppColors.lineGray),
        borderRadius: BorderRadius.all(Radius.circular(20)),
      ),
    );
  }
}

class AppLightBlueButton extends _AppButton {
  AppLightBlueButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.blue009;
    this.borderRadius = borderRadius ?? 20;
    this.borderRadius = borderRadius ?? 20;
  }
}

class AppGreenButton extends _AppButton {
  AppGreenButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.main;
    this.borderRadius = borderRadius ?? 20;
  }
}

class AppRedButton extends _AppButton {
  AppRedButton({
    String title = '',
    bool isLoading = false,
    bool isEnable = true,
    VoidCallback? onPressed,
    double? borderRadius,
    TextStyle? textStyle,
  }) {
    this.title = title;
    this.isLoading = isLoading;
    this.isEnable = isEnable;
    this.onPressed = onPressed;
    //SetupUI
    this.textStyle = textStyle ?? AppTextStyle.whiteS14Bold;
    backgroundColor = AppColors.redD7443B;
    this.borderRadius = borderRadius ?? 20;
  }
}
