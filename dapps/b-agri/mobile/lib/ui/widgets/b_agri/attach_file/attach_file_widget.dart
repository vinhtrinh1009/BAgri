import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/models/entities/file/file_entity.dart';
import 'package:flutter_base/ui/components/app_cache_image.dart';

class AttachedFileWidget extends StatelessWidget {
  final String? filePath;
  final VoidCallback? onDeletePressed;

  AttachedFileWidget({
    this.filePath,
    this.onDeletePressed,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          height: 120,
          width: 95,
          margin: EdgeInsets.all(8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.all(Radius.circular(10)),
                child: Container(
                  height: 95,
                  width: 95,
                  child: _buildContentWidget(),
                ),
              ),
              SizedBox(height: 8),
              Text(
                filePath!.split("/").last,
                style: AppTextStyle.blackS10,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
        Positioned(
          top: 0,
          right: 0,
          child: GestureDetector(
            onTap: onDeletePressed,
            child: Container(
              width: 32,
              height: 32,
              padding: EdgeInsets.only(right: 2, top: 2),
              alignment: Alignment.topRight,
              child: Image.asset(AppImages.icCircleClose, width: 16),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildContentWidget() {
    String? fileType = filePath!.split(".").last;
    if (fileType.toLowerCase() == 'png' ||
        fileType.toLowerCase() == 'jpg' ||
        fileType.toLowerCase() == 'jpeg') {
      return Container(
        height: 95,
        width: 95,
        child: AppCacheImage(
          url: '$filePath',
        ),
      );
    } else if (fileType.toLowerCase() == "txt") {
      return Container(
        height: 95,
        width: 95,
        color: Color(0xFFF0F0F0),
        padding: EdgeInsets.all(15),
        child: Image.asset(AppImages.icAttachTxt),
      );
    } else if (fileType.toLowerCase() == "doc" ||
        fileType.toLowerCase() == "docx") {
      return Container(
        height: 95,
        width: 95,
        color: Color(0xFFF0F0F0),
        padding: EdgeInsets.all(20),
        child: Image.asset(AppImages.icAttachDoc),
      );
    } else {
      return Container(
        height: 95,
        width: 95,
        color: Color(0xFFF0F0F0),
        child: Image.asset(AppImages.icAttachPDF),
      );
    }
  }
}
