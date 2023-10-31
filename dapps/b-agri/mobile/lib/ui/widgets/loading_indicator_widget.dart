import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';

class LoadingIndicatorWidget extends StatelessWidget {
  final Color color;
  final double size;

  LoadingIndicatorWidget({this.color = AppColors.main, this.size = 24});

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: Container(
        width: size,
        height: size,
        child: CircularProgressIndicator(
          backgroundColor: color,
          valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFffa700)),
        ),
      ),
    );
  }
}
