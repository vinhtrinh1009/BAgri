import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:flutter_base/utils/dialog_utils.dart';

class FileInfo {
  final File? file;
  final FileSourceType? sourceType;

  FileInfo({
    this.file,
    this.sourceType,
  });
}

enum FileSourceType {
  camera,
  library,
  document,
}

extension SourceTypeExtension on FileSourceType? {
  String get title {
    switch (this) {
      case FileSourceType.camera:
        return "Camera";
      case FileSourceType.library:
        return "Thư viện ảnh";
      case FileSourceType.document:
        return "File tài liệu";
      default:
        return "";
    }
  }

  Widget get icon {
    switch (this) {
      case FileSourceType.camera:
        return Image.asset(AppImages.icAttachCamera);
      case FileSourceType.library:
        return Image.asset(AppImages.icAttachFile);
      case FileSourceType.document:
        return Image.asset(AppImages.icAttachImage);
      default:
        return Container();
    }
  }
}

class FilePickerDialog extends StatelessWidget {
  final String title;
  final List<FileSourceType>? sources;

  FilePickerDialog({
    this.title = "Chọn ảnh hoặc file cần tải",
    this.sources,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      key: _scaffoldKey,
      body: Column(
        children: [
          Spacer(),
          Container(
            decoration: BoxDecoration(
              color: Colors.transparent,
              borderRadius: BorderRadius.only(
                topRight: Radius.circular(19.0),
                topLeft: Radius.circular(19.0),
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Stack(
                  children: [
                    Container(
                      height: 46,
                      margin: EdgeInsets.only(top: 20),
                      width: double.infinity,
                      child: Center(
                        child: Text(title, style: AppTextStyle.blackS14),
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.only(
                            topLeft: Radius.circular(20),
                            topRight: Radius.circular(20)),
                      ),
                    ),
                    Positioned(
                      right: 0,
                      top: 0,
                      child: GestureDetector(
                        onTap: () {
                          Navigator.pop(context);
                        },
                        child: Container(
                          width: 40,
                          height: 40,
                          child: Image.asset(AppImages.icCircleCloseBig),
                        ),
                      ),
                    ),
                  ],
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16),
                  height: 1,
                  color: Colors.grey,
                ),
                Container(
                  color: Colors.white,
                  child: Container(
                    margin: EdgeInsets.only(top: 20, bottom: 20),
                    color: Colors.white,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: (sources ?? []).map((e) {
                        return SourceItemWidget(
                          sourceType: e,
                          onPressed: () {
                            _handlePickFile(context, e);
                          },
                        );
                      }).toList(),
                    ),
                  ),
                ),
                Container(
                  color: Colors.white,
                  height: 20,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  final _scaffoldKey = GlobalKey<ScaffoldState>();

  void _handlePickFile(BuildContext context, FileSourceType sourceType) async {
    File? file;
    String error = "";
    String typeError = "";
    switch (sourceType) {
      case FileSourceType.camera:
        file = await DialogUtils.pickImageFromCamera();
        //Đã chuyển giá trị dung lượng tối đa sang file config
        error = (file != null && file.lengthSync() > AppConfig.maxImageFileSize)
            ? "${S.of(context).max_image_size}"
            : "";

        break;
      case FileSourceType.library:
        file = await DialogUtils.pickImageFromLibrary();
        error = (file!.lengthSync() > AppConfig.maxImageFileSize)
            ? "${S.of(context).max_image_size}"
            : "";
        String fileType = file.path.split('.').last;
        if (fileType == 'gif') {
          typeError = "${S.of(context).not_allow_upload_gif}";
        }

        break;
      case FileSourceType.document:
        file = await DialogUtils.pickDocument();
        error = (file!.lengthSync() > AppConfig.maxDocumentFileSize)
            ? "${S.of(context).max_file_size}"
            : "";

        String fileType = file.path.split('.').last;
        if (fileType == 'gif') {
          typeError = "${S.of(context).not_allow_upload_gif}";
        }

        break;
    }
    if (file != null) {
      if ((error).isNotEmpty) {
        _showMessage(SnackBarMessage(message: error, type: SnackBarType.ERROR));
        return;
      } else {
        if (typeError.isNotEmpty) {
          _showMessage(
              SnackBarMessage(message: typeError, type: SnackBarType.ERROR));
          return;
        }
        Navigator.pop(context, FileInfo(file: file, sourceType: sourceType));
      }
    } else {
      Navigator.pop(context);
    }
  }

  void _showMessage(SnackBarMessage message) {
    _scaffoldKey.currentState!.removeCurrentSnackBar();
    _scaffoldKey.currentState!.showSnackBar(AppSnackBar(message: message));
  }
}

class SourceItemWidget extends StatelessWidget {
  final FileSourceType? sourceType;
  final VoidCallback? onPressed;

  SourceItemWidget({this.sourceType, this.onPressed});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Column(
        children: [
          CircleAvatar(
            minRadius: 30,
            backgroundColor: AppColors.main,
            child: Container(
              padding: EdgeInsets.all(5),
              height: 50,
              child: sourceType.icon,
            ),
          ),
          SizedBox(height: 6),
          Text(
            sourceType.title,
            style: AppTextStyle.blackS12,
          ),
        ],
      ),
    );
  }
}
