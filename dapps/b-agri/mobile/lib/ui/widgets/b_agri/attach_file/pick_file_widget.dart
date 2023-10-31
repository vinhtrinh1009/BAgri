import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/ui/widgets/loading_indicator_widget.dart';

class PickFileWidget extends StatelessWidget {
  final VoidCallback? onPressed;
  final isLoading;

  PickFileWidget({
    this.onPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        GestureDetector(
          onTap: () {
            if (isLoading != true) {
              onPressed?.call();
            }
          },
          child: Container(
            height: 40,
            width: 40,
            color: Colors.transparent,
            child: Column(
              children: [
                Image.asset(
                  AppImages.icUpload,
                  width: 40,
                  height: 40,
                ),
                Spacer(),
              ],
            ),
          ),
        ),
        Visibility(
          visible: isLoading == true,
          child: Container(
            height: 40,
            width: 40,
            child: Center(
              child: LoadingIndicatorWidget(),
            ),
          ),
        ),
      ],
    );
  }
}
