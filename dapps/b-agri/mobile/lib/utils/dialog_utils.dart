import 'dart:io';
import 'package:collection/collection.dart' show IterableExtension;
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_images.dart';

import 'package:flutter_base/ui/dialogs/app_dialog.dart';
import 'package:flutter_base/ui/dialogs/file_picker_dialog.dart';
import 'package:flutter_base/ui/dialogs/photos_dialog.dart';

import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';
import 'package:flutter_document_picker/flutter_document_picker.dart';
import 'package:image_picker/image_picker.dart';

import 'package:tiengviet/tiengviet.dart';

class DialogUtils {
  static Future<FileInfo?> pickFile(BuildContext context,
      {List<FileSourceType> sourceTypes = const [
        // FileSourceType.camera,
        FileSourceType.library,
        FileSourceType.document
      ]}) async {
    FileInfo? file = await showModalBottomSheet(
      context: context,
      useRootNavigator: true,
      backgroundColor: Colors.transparent,
      builder: (BuildContext context) => FilePickerDialog(
        sources: sourceTypes,
      ),
    );
    return file;
  }

  static Future<File?> pickImageFromCamera() async {
    final picker = ImagePicker();
    final pickedFile = await picker.getImage(source: ImageSource.camera);
    if (pickedFile != null) {
      return File(pickedFile.path);
    } else {
      return null;
    }
  }

  static Future<File?> pickImageFromLibrary() async {
    final picker = ImagePicker();
    final pickedFile = await picker.getImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      return File(pickedFile.path);
    } else {
      return null;
    }
  }

  static Future<File?> pickDocument() async {
    //Without parameters:
    final path = await FlutterDocumentPicker.openDocument();
    if ((path ?? "").isNotEmpty) {
      return File(path!);
    } else {
      return null;
    }

    // //With parameters:
    // FlutterDocumentPickerParams params = FlutterDocumentPickerParams(
    // allowedFileExtensions: ['mwfbak'],
    // allowedUtiTypes: ['com.sidlatau.example.mwfbak'],
    // allowedMimeTypes: ['application/*'],
    // invalidFileNameSymbols: ['/'],
    // );
    //
    // final path = await FlutterDocumentPicker.openDocument(params: params);
  }

  static void showDatePicker(
    BuildContext context, {
    DateTime? minTime,
    DateTime? maxTime,
    DateChangedCallback? onConfirm,
    locale: LocaleType.en,
    DateTime? currentTime,
    DatePickerTheme? theme,
  }) {
    DatePicker.showDatePicker(
      context,
      minTime: minTime,
      maxTime: maxTime,
      onConfirm: onConfirm,
      locale: LocaleType.vi,
      currentTime: currentTime,
      theme: DatePickerTheme(),
    );
  }

  static void showDateTimePicker(
    BuildContext context, {
    DateTime? minTime,
    DateTime? maxTime,
    DateChangedCallback? onConfirm,
    locale: LocaleType.en,
    DateTime? currentTime,
    DatePickerTheme? theme,
  }) {
    DatePicker.showDateTimePicker(
      context,
      minTime: minTime,
      maxTime: maxTime,
      onConfirm: onConfirm,
      locale: LocaleType.vi,
      currentTime: currentTime,
      theme: DatePickerTheme(),
    );
  }

  static void showSuccessDialog(
    BuildContext context, {
    Widget? icon,
    required String title,
    String? okText,
    bool autoDismiss = false,
    bool showCloseButton = false,
    VoidCallback? onOkPressed,
    VoidCallback? onDismissed,
    bool dismissible = false,
    double? marginHorizontal,
    double? iconPosition,
  }) {
    AppDialog(
      context: context,
      icon: icon ?? Image.asset(AppImages.icSuccess),
      title: title,
      okText: okText,
      onOkPressed: onOkPressed,
      autoDismiss: autoDismiss,
      showCloseButton: showCloseButton,
      onDismissed: onDismissed,
      dismissible: dismissible,
      marginHorizontal: marginHorizontal,
      iconPosition: iconPosition,
    ).show();
  }

  static void showErrorDialog(
    BuildContext context, {
    Widget? icon,
    required String title,
    String? okText,
    TextStyle? titleStyle,
    bool autoDismiss = false,
    bool showCloseButton = false,
    VoidCallback? onOkPressed,
    VoidCallback? onDismissed,
    bool dismissible = false,
  }) {
    AppDialog(
      context: context,
      icon: icon ?? Image.asset(AppImages.icError),
      title: title,
      okText: okText,
      titleStyle: titleStyle,
      onOkPressed: onOkPressed,
      onDismissed: onDismissed,
      autoDismiss: autoDismiss,
      showCloseButton: showCloseButton,
      dismissible: dismissible,
    ).show();
  }

  static void showNotificationDialog(
    BuildContext context, {
    Widget? icon,
    required String title,
    String? okText,
    TextStyle? titleStyle,
    bool autoDismiss = false,
    bool showCloseButton = false,
    VoidCallback? onOkPressed,
    VoidCallback? onDismissed,
    bool dismissible = false,
  }) {
    AppDialog(
      context: context,
      icon: icon ?? Image.asset(AppImages.icBAgri, width: 60),
      title: title,
      okText: okText,
      titleStyle: titleStyle,
      onOkPressed: onOkPressed,
      onDismissed: onDismissed,
      autoDismiss: autoDismiss,
      showCloseButton: showCloseButton,
      dismissible: dismissible,
    ).show();
  }

  static showPhotosDialog(BuildContext context, List<String?> images,
      {int? selectedIndex, bool closeButton = false}) {
    if (images.length == 0 || images == []) return;
    if (selectedIndex != null &&
        (selectedIndex >= images.length || selectedIndex < 0)) return;
    showDialog(
      useRootNavigator: true,
      context: context,
      builder: (BuildContext context) => PhotosDialog(
        images: images,
        selectedIndex: selectedIndex ?? 0,
        closeButton: closeButton,
      ),
    );
  }

  static void showDialogAccept(
    BuildContext context, {
    required String title,
    String? okText,
    String? cancelText,
    bool autoDismiss = false,
    bool showCloseButton = false,
    VoidCallback? onOkPressed,
    VoidCallback? onDismissed,
    bool dismissible = false,
    double? marginHorizontal,
    double? iconPosition,
  }) {
    AppDialog(
      context: context,
      title: title,
      okText: okText,
      cancelText: cancelText,
      onOkPressed: onOkPressed,
      autoDismiss: autoDismiss,
      showCloseButton: showCloseButton,
      onDismissed: onDismissed,
      dismissible: dismissible,
      marginHorizontal: marginHorizontal,
      iconPosition: iconPosition,
    ).show();
  }
}
