import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class AppDeleteDialog extends StatelessWidget {
  VoidCallback? onConfirm;
  AppDeleteDialog({
    Key? key,
    this.onConfirm,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: EdgeInsets.symmetric(horizontal: 20),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Padding(
        padding:
            const EdgeInsets.only(top: 20, left: 20, right: 15, bottom: 15),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Thông báo',
              style: AppTextStyle.blackS16Bold,
            ),
            SizedBox(height: 18),
            Text('Bạn có chắc chắn muốn xóa?', style: AppTextStyle.blackS16),
            SizedBox(height: 25),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                GestureDetector(
                  onTap: () {
                    Navigator.pop(context, false);
                  },
                  child: Text(
                    'Hủy',
                    style: TextStyle(
                        color: AppColors.redLighterTextButton, fontSize: 16),
                  ),
                ),
                SizedBox(width: 20),
                GestureDetector(
                  onTap: onConfirm,
                  child: Text(
                    'Xác nhận',
                    style: TextStyle(
                        color: AppColors.greenLighterTextButton, fontSize: 16),
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
