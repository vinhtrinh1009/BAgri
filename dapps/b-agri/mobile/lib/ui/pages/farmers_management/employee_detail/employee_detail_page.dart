import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/farmers_management/employee_detail/employee_detail_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_circular_progress_indicator.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_error_list_widget.dart';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:scroll_to_index/scroll_to_index.dart';

class EmployeeDetailPage extends StatefulWidget {
  String farmerId;

  EmployeeDetailPage({Key? key, required this.farmerId}) : super(key: key);

  @override
  _EmployeeDetailPageState createState() => _EmployeeDetailPageState();
}

class _EmployeeDetailPageState extends State<EmployeeDetailPage> {
  late EmployeeDetailCubit _cubit;
  late AutoScrollController _scrollController;

  @override
  void initState() {
    _cubit = BlocProvider.of<EmployeeDetailCubit>(context);
    super.initState();
    _cubit.getFarmerDetail(widget.farmerId);

    _scrollController = AutoScrollController(
      viewportBoundaryGetter: () =>
          Rect.fromLTRB(0, 0, 0, MediaQuery.of(context).padding.bottom),
      axis: Axis.horizontal,
    );
  }

  Future<void> refreshData() async {
    await _cubit.getFarmerDetail(widget.farmerId);
  }

  @override
  Widget build(BuildContext context) {
    DateTime dateToday = DateTime.now();
    int currentYear = dateToday.year;

    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Thông tin nhân công',
      ),
      body: SafeArea(
        child: BlocBuilder<EmployeeDetailCubit, EmployeeDetailState>(
          buildWhen: (prev, current) =>
              prev.loadStatus != current.loadStatus ||
              prev.farmerDetail != current.farmerDetail,
          builder: (context, state) {
            if (state.loadStatus == LoadStatus.LOADING) {
              return Center(
                child: AppCircularProgressIndicator(),
              );
            } else if (state.loadStatus == LoadStatus.FAILURE) {
              return AppErrorListWidget(onRefresh: () async {
                refreshData();
              });
            } else if (state.loadStatus == LoadStatus.SUCCESS) {
              return Padding(
                  padding: EdgeInsets.symmetric(horizontal: 18),
                  child: RefreshIndicator(
                    color: AppColors.main,
                    onRefresh: () async {
                      refreshData();
                    },
                    child: SingleChildScrollView(
                      physics: AlwaysScrollableScrollPhysics(),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          SizedBox(height: 20),
                          Text(
                            'Thông tin:',
                            style: AppTextStyle.blackS18Bold,
                          ),
                          SizedBox(height: 10),
                          Text(
                            'Họ và tên: ${state.farmerDetail?.fullname ?? ""}',
                            style: AppTextStyle.blackS16,
                          ),
                          SizedBox(height: 10),
                          Text(
                            'Số điện thoại: ${state.farmerDetail?.phone ?? ""}',
                            style: AppTextStyle.blackS16,
                          ),
                          SizedBox(height: 10),
                          Text(
                            'Công trong tháng: ' +
                                '${state.farmerDetail?.workdays == null ? "" : "${state.farmerDetail!.workdays} công"}',
                            style: AppTextStyle.blackS16,
                          ),
                          SizedBox(height: 10),
                          Text(
                            'Người quản lý: ${state.farmerDetail?.manager?.fullname ?? ""}',
                            style: AppTextStyle.blackS16,
                          ),
                          SizedBox(height: 35),
                          Text(
                            'Công việc thực hiện trong tháng:',
                            style: AppTextStyle.blackS18Bold,
                          ),
                          SizedBox(height: 10),
                          Text(
                            '$currentYear',
                            style: AppTextStyle.blackS18Bold,
                          ),
                          SizedBox(height: 10),
                          Container(
                            height: 35,
                            padding: EdgeInsets.symmetric(horizontal: 12),
                            decoration: BoxDecoration(
                                color: AppColors.grayE5,
                                borderRadius: BorderRadius.circular(16)),
                            child: Row(
                              children: [
                                GestureDetector(
                                  onTap: () async {
                                    _cubit.changeCurrentTaskList(
                                        _cubit.state.chosenMonth - 1);
                                    await _scrollController.scrollToIndex(
                                        _cubit.state.chosenMonth - 1,
                                        preferPosition:
                                            AutoScrollPosition.begin);
                                  },
                                  child: Icon(
                                    Icons.arrow_back_ios_rounded,
                                    size: 15,
                                  ),
                                ),
                                SizedBox(width: 14),
                                Expanded(
                                  child: BlocBuilder<EmployeeDetailCubit,
                                      EmployeeDetailState>(
                                    buildWhen: (prev, current) =>
                                        prev.chosenMonth != current.chosenMonth,
                                    builder: (context, state) {
                                      return ListView.separated(
                                        controller: _scrollController,
                                        shrinkWrap: true,
                                        scrollDirection: Axis.horizontal,
                                        itemBuilder: (context, index) => Center(
                                          child: GestureDetector(
                                            onTap: () {
                                              _cubit.changeCurrentTaskList(
                                                  index + 1);
                                            },
                                            child: AutoScrollTag(
                                              controller: _scrollController,
                                              index: index,
                                              key: ValueKey(index),
                                              child: Text(
                                                'T${index + 1}',
                                                style: (index + 1) ==
                                                        state.chosenMonth
                                                    ? AppTextStyle.tintS16
                                                    : AppTextStyle.blackS16,
                                              ),
                                            ),
                                          ),
                                        ),
                                        separatorBuilder: (context, index) =>
                                            SizedBox(width: 30),
                                        itemCount: 12,
                                      );
                                    },
                                  ),
                                ),
                                SizedBox(width: 14),
                                GestureDetector(
                                  onTap: () async {
                                    _cubit.changeCurrentTaskList(
                                        _cubit.state.chosenMonth + 1);
                                    await _scrollController.scrollToIndex(
                                        _cubit.state.chosenMonth - 1,
                                        preferPosition:
                                            AutoScrollPosition.begin);
                                  },
                                  child: Icon(
                                    Icons.arrow_forward_ios_rounded,
                                    size: 15,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          SizedBox(height: 20),
                          BlocBuilder<EmployeeDetailCubit, EmployeeDetailState>(
                            buildWhen: (prev, current) =>
                                prev.taskMapByDay != current.taskMapByDay,
                            builder: (context, state) {
                              return ListView.separated(
                                shrinkWrap: true,
                                physics: NeverScrollableScrollPhysics(),
                                itemBuilder: (context, index) {
                                  List<TaskEntity> listTaskByDay =
                                      state.taskMapByDay[index + 1]!;
                                  if (listTaskByDay.isEmpty)
                                    return SizedBox();
                                  else
                                    return Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'Tháng ${state.chosenMonth} Ngày ${index + 1}',
                                          style: AppTextStyle.tintS16Bold,
                                        ),
                                        SizedBox(height: 10),
                                        ListView.separated(
                                            shrinkWrap: true,
                                            physics:
                                                NeverScrollableScrollPhysics(),
                                            itemBuilder: (context, taskIndex) {
                                              TaskEntity task =
                                                  listTaskByDay[taskIndex];
                                              return _buildTask(
                                                  task.start_time ?? "",
                                                  task.end_time ?? "",
                                                  task.name ?? "");
                                            },
                                            separatorBuilder:
                                                (context, taskIndex) {
                                              return SizedBox(
                                                height: 8,
                                              );
                                            },
                                            itemCount: listTaskByDay.length)
                                      ],
                                    );
                                },
                                separatorBuilder: (context, index) {
                                  List<TaskEntity> listTaskByDay =
                                      state.taskMapByDay[index + 1]!;
                                  if (listTaskByDay.isEmpty)
                                    return SizedBox();
                                  else
                                    return SizedBox(height: 10);
                                },
                                itemCount: state.taskMapByDay.length,
                              );
                            },
                          ),
                          SizedBox(height: 10),
                        ],
                      ),
                    ),
                  ));
            } else
              return SizedBox();
          },
        ),
      ),
    );
  }

  _buildTask(String startTime, String endTime, String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 15),
      child: Row(
        children: [
          Column(
            children: [
              Text(
                startTime,
                style: AppTextStyle.blackS14,
              ),
              SizedBox(height: 5),
              Text(
                endTime,
                style: AppTextStyle.greyS14,
              )
            ],
          ),
          SizedBox(width: 6),
          Container(
            height: 38,
            width: 1,
            color: AppColors.main,
          ),
          SizedBox(width: 6),
          Expanded(
            child: Text(
              title,
              style: AppTextStyle.blackS16,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}
