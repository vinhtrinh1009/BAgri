import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class AppBarWidget extends AppBar {
  AppBarWidget({
    Key? key,
    bool showBackButton = true,
    required BuildContext context,
    VoidCallback? onBackPressed,
    String title = "",
    Color? backgroundColor,
    List<Widget> rightActions = const [],
  }) : super(
          key: key,
          centerTitle: true,
          title: Text(
            title,
            style: const TextStyle(fontWeight: FontWeight.w400, fontSize: 20),
            overflow: TextOverflow.ellipsis,
          ),
          elevation: 0,
          backgroundColor: backgroundColor ?? AppColors.main,
          leading: showBackButton
              ? IconButton(
                  onPressed: onBackPressed ??
                      () {
                        Navigator.of(context).pop();
                      },
                  icon: const Icon(
                    Icons.keyboard_backspace,
                    color: Colors.white,
                  ))
              : null,
          actions: rightActions,
        );
}
