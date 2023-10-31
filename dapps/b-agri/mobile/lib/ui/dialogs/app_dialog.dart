import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

enum DialogType { INFO, SUCCESS, ERROR }

class AppDialog {
  final BuildContext context;
  final DialogType type;
  final Widget? icon;
  final String? title;
  final String? description;
  final String? okText;
  final VoidCallback? onOkPressed;
  final String? cancelText;
  final VoidCallback? onCancelPressed;
  final bool dismissible;
  final VoidCallback? onDismissed;
  final bool autoDismiss;
  final bool showCloseButton;
  final TextStyle? titleStyle;
  final double? marginHorizontal;
  final double? iconPosition;

  AppDialog({
    required this.context,
    this.type = DialogType.INFO,
    this.icon,
    this.titleStyle,
    this.title,
    this.description,
    this.okText = '',
    this.onOkPressed,
    this.cancelText = '',
    this.onCancelPressed,
    this.onDismissed,
    this.dismissible = false,
    this.autoDismiss = false,
    this.showCloseButton = false,
    this.marginHorizontal = 40,
    this.iconPosition = 20,
  });

  Timer? t;
  void show() {
    //Auto dismiss after 3 seconds
    if (autoDismiss) {
      t = Timer(Duration(seconds: 3), () {
        dismiss();
      });
    }
    showDialog(
        useRootNavigator: true,
        barrierDismissible: true,
        context: context,
        builder: (BuildContext context) {
          return _buildDialog;
        });
  }

  Widget get _buildDialog {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: WillPopScope(
        onWillPop: _onWillPop,
        child: GestureDetector(
          onTap: () {
            if (dismissible == true) {
              dismiss();
            }
          },
          child: Container(
            color: Colors.transparent,
            height: double.infinity,
            width: double.infinity,
            child: Stack(
              children: [
                Container(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Stack(
                        children: [
                          Container(
                            margin: EdgeInsets.symmetric(
                                horizontal: marginHorizontal ?? 40,
                                vertical: 20),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius:
                                  BorderRadius.all(Radius.circular(10)),
                            ),
                            padding: EdgeInsets.symmetric(
                                horizontal: 12, vertical: 4),
                            child: Column(
                              children: [
                                _buildHeaderIcon,
                                _buildTitleText,
                                // _buildDescriptionText,
                                _buildActions,
                              ],
                            ),
                          ),
                          Positioned(
                            top: 0,
                            right: iconPosition ?? 20,
                            child: Visibility(
                              visible: showCloseButton,
                              child: GestureDetector(
                                onTap: dismiss,
                                child: Container(
                                  height: 40,
                                  width: 40,
                                  child: Center(
                                    child: Image.asset(AppImages.icCircleClose),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget get _buildHeaderIcon {
    if (icon != null) {
      return Container(child: icon);
    }
    switch (type) {
      case DialogType.INFO:
        return Container();
      case DialogType.SUCCESS:
        return Container(child: Image.asset(AppImages.icSuccess));
      case DialogType.ERROR:
        return Container(child: Image.asset(AppImages.icError));
    }
  }

  Widget get _buildTitleText {
    if ((title ?? '').isEmpty) return Container();
    return Container(
      margin: EdgeInsets.only(top: 4),
      child: Text(
        title ?? '',
        textAlign: TextAlign.center,
        style: titleStyle ?? AppTextStyle.blackS14.copyWith(height: 1.4),
      ),
    );
  }

  Widget get _buildActions {
    bool showOkButton = (okText ?? '').isNotEmpty;
    bool showCancelButton = (cancelText ?? '').isNotEmpty;
    List<Widget> buttons = [];

    if (showCancelButton) {
      buttons.add(_buildCancelButton);
    }
    if (showOkButton) {
      buttons.add(_buildOkButton);
    }
    if (buttons.isEmpty) {
      return Container(height: 14);
    }
    return Container(
      // color: Colors.red,
      height: 36,
      // padding: EdgeInsets.only(bottom: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: buttons,
      ),
    );
  }

  Widget get _buildOkButton {
    return TextButton(
      onPressed: () {
        dismiss();
        onOkPressed?.call();
      },
      child: Text(
        okText!,
        style: AppTextStyle.tintS14.copyWith(height: 1.4),
      ),
    );
  }

  Widget get _buildCancelButton => TextButton(
        onPressed: () {
          dismiss();
          onCancelPressed?.call();
        },
        child: Text(
          cancelText!,
          style: TextStyle(
            fontSize: 14,
            color: Color(0xFF005CF7),
            fontWeight: FontWeight.bold,
            height: 1.4,
          ),
        ),
      );

  dismiss() {
    t?.cancel();
    Navigator.of(context, rootNavigator: true).pop();
    onDismissed?.call();
  }

  Future<bool> _onWillPop() async {
    return dismissible;
  }
}
