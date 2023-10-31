import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class EmptyDataWidget extends StatelessWidget {
  String? title;
  String? description;
  Widget? icon;
  EmptyDataWidget({
    this.title,
    this.description,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: 8,
        ),
        icon ??
            Image.asset(
              AppImages.icNoData,
              width: 60,
              height: 60,
              fit: BoxFit.cover,
            ),
        SizedBox(
          height: 10,
        ),
        Text(
          title ?? 'Không có dữ liệu',
          style: AppTextStyle.greyS16W300,
        ),
        SizedBox(
          height: 4,
        ),
        Text(description ?? '', style: AppTextStyle.greyS14)
      ],
    );
  }
}
