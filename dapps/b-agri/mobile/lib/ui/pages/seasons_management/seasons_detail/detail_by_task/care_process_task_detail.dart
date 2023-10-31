import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/detail_by_task/care_process_task_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_circular_progress_indicator.dart';
import 'package:flutter_base/ui/widgets/b_agri/attach_file/attach_file_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/attach_file/file_by_task_widget.dart';
import 'package:flutter_base/utils/date_utils.dart' as util;
import 'package:flutter_bloc/flutter_bloc.dart';

class CareProcessTaskDetail extends StatefulWidget {
  int day;
  String taskId;

  CareProcessTaskDetail({
    Key? key,
    required this.day,
    required this.taskId,
  }) : super(key: key);

  @override
  State<CareProcessTaskDetail> createState() => _CareProcessTaskDetailState();
}

class _CareProcessTaskDetailState extends State<CareProcessTaskDetail> {
  late CareProcessTaskCubit _cubit;

  @override
  void initState() {
    _cubit = BlocProvider.of<CareProcessTaskCubit>(context);
    super.initState();

    _cubit.getTaskDetail(widget.taskId);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildTitleBar(context),
        Expanded(
          child: BlocBuilder<CareProcessTaskCubit, CareProcessTaskState>(
            buildWhen: (prev, current) => prev.loadStatus != current.loadStatus,
            builder: (context, state) {
              if (state.loadStatus == LoadStatus.LOADING)
                return Stack(
                  children: [
                    Center(child: AppCircularProgressIndicator()),
                    _buildCloseButton(context),
                  ],
                );
              else if (state.loadStatus == LoadStatus.FAILURE)
                return Stack(
                  children: [
                    Center(child: Text("Có lỗi xảy ra")),
                    _buildCloseButton(context),
                  ],
                );
              else if (state.loadStatus == LoadStatus.SUCCESS) {
                DateTime? startTime =
                    util.DateUtils.fromString(state.taskDetail!.start_time!);

                DateTime? endTime =
                    util.DateUtils.fromString(state.taskDetail!.end_time!);
                String startTimeString = util.DateUtils.toDateString(startTime!,
                    format: AppConfig.timeDisplayFormat);
                String endTimeString = util.DateUtils.toDateString(endTime!,
                    format: AppConfig.timeDisplayFormat);

                String? items = _cubit.state.taskDetail!.items;
                List<Widget> widgetsImage = [];
                final filePaths = _cubit.state.taskDetail!.result ?? [];
                for (int i = 0; i < filePaths.length; i++) {
                  widgetsImage.add(FileByTaskWidget(
                    filePath: filePaths[i],
                  ));
                }

                return SingleChildScrollView(
                  child: Stack(
                    children: [
                      Padding(
                        padding: EdgeInsets.only(left: 15, top: 20),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Chi tiết công việc',
                              style: AppTextStyle.blackS16Bold,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Mô tả công việc: ${state.taskDetail!.description}',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Thời gian: $startTimeString đến $endTimeString',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Người thực hiện:',
                              style: AppTextStyle.greyS16,
                            ),
                            Wrap(
                              spacing: 10,
                              children: List.generate(
                                  state.taskDetail!.farmers?.length ?? 0,
                                  (index) {
                                FarmerEntity farmer =
                                    state.taskDetail!.farmers![index];
                                return Container(
                                  height: 28,
                                  padding: EdgeInsets.symmetric(horizontal: 15),
                                  margin: EdgeInsets.symmetric(vertical: 10),
                                  decoration: BoxDecoration(
                                      color: AppColors.grayC4,
                                      borderRadius: BorderRadius.circular(18)),
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      SizedBox(
                                          height: 18,
                                          width: 18,
                                          child: Image.asset(
                                            AppImages.icEmployeeAvatar,
                                            fit: BoxFit.fill,
                                          )),
                                      SizedBox(width: 7),
                                      Text(
                                        farmer.fullName ?? "",
                                        style: AppTextStyle.greyS14,
                                      )
                                    ],
                                  ),
                                );
                              }),
                            ),
                            SizedBox(height: 5),
                            Text(
                              'Vật tư sử dụng: $items',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Kết quả:',
                              style: AppTextStyle.greyS16,
                            ),
                            if (widgetsImage.length == 0)
                              Padding(
                                  padding: EdgeInsets.symmetric(horizontal: 90),
                                  child: Image.asset(AppImages.icImageDefault)),
                            if (widgetsImage.length > 0)
                              Wrap(
                                spacing: 20,
                                alignment: WrapAlignment.start,
                                crossAxisAlignment: WrapCrossAlignment.start,
                                children: List.generate(
                                  widgetsImage.length,
                                  (index) {
                                    return widgetsImage[index];
                                  },
                                ),
                              ),
                          ],
                        ),
                      ),
                      _buildCloseButton(context),
                    ],
                  ),
                );
              } else
                return SizedBox();
            },
          ),
        ),
      ],
    );
  }

  _buildCloseButton(BuildContext context) {
    return Align(
      alignment: Alignment.topRight,
      child: Padding(
        padding: EdgeInsets.only(right: 10, top: 5),
        child: GestureDetector(
          onTap: () {
            Navigator.of(context).pop();
          },
          child: Text(
            'X',
            style: AppTextStyle.blackS16,
          ),
        ),
      ),
    );
  }

  _buildTitleBar(BuildContext context) {
    return Container(
      height: 27,
      alignment: Alignment.center,
      decoration: BoxDecoration(color: AppColors.blueC0),
      child: Stack(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                'Ngày ${widget.day}',
                style: AppTextStyle.blackS16.copyWith(
                    color: AppColors.blue29, fontWeight: FontWeight.w500),
              )
            ],
          ),
          Positioned(
            left: 10,
            child: GestureDetector(
              child: Icon(
                Icons.keyboard_backspace,
                color: Colors.white,
                size: 20,
              ),
              onTap: () {
                Navigator.of(context).pop();
                Navigator.of(context).pop();
              },
            ),
          ),
        ],
      ),
    );
  }
}
