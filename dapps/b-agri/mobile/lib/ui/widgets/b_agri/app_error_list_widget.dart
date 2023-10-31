import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';

class AppErrorListWidget extends StatelessWidget {
  RefreshCallback onRefresh;
  AppErrorListWidget({Key? key, required this.onRefresh}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      color: AppColors.main,
      onRefresh: onRefresh,
      child: Stack(
        children: [
          Center(
            child: Text("Có lỗi xảy ra"),
          ),
          ListView(
            physics: AlwaysScrollableScrollPhysics(),
            children: [Container()],
          ),
        ],
      ),
    );
  }
}
