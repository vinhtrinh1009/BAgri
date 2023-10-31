import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_circular_progress_indicator.dart';

class AppButton extends StatelessWidget {
  Color color;
  String? title;
  TextStyle? textStyle;
  double? height;
  double? width;
  VoidCallback? onPressed;
  Widget? child;
  bool isLoading;
  bool isEnabled;
  double? border;

  AppButton(
      {Key? key,
      this.title,
      required this.color,
      this.child,
      this.onPressed,
      this.textStyle,
      this.height,
      this.isLoading = false,
      this.isEnabled = true,
      this.width,
      this.border})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: isEnabled ? onPressed : null,
      child: Container(
        height: height ?? 40,
        width: width ?? 80,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: isEnabled ? color : Color(0xFFCBCBCB),
          borderRadius: BorderRadius.circular(border ?? 16),
        ),
        child: isLoading
            ? Padding(
                padding: EdgeInsets.symmetric(vertical: 5),
                child: FittedBox(
                    child: CircularProgressIndicator(
                  color: Colors.white,
                )),
              )
            : child ??
                Text(
                  title!,
                  style: textStyle ?? AppTextStyle.whiteS14,
                ),
      ),
    );
  }
}
