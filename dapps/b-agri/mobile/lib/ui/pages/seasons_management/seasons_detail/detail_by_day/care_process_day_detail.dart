import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/season/season_task_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/season_repository.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/detail_by_day/care_process_day_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/detail_by_task/care_process_task_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/detail_by_task/care_process_task_detail.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class CareProcessDayDetail extends StatefulWidget {
  int index;
  String seasonId;
  String date;

  CareProcessDayDetail({
    Key? key,
    required this.index,
    required this.seasonId,
    required this.date,
  }) : super(key: key);

  @override
  State<CareProcessDayDetail> createState() => _CareProcessDayDetailState();
}

class _CareProcessDayDetailState extends State<CareProcessDayDetail> {
  late CareProcessDayCubit _cubit;
  ScrollController controller = ScrollController();
  double graphHeight = 35;
  @override
  void initState() {
    _cubit = BlocProvider.of<CareProcessDayCubit>(context);
    super.initState();
    _cubit.getSeasonTaskByDay(seasonId: widget.seasonId, date: widget.date);
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          _buildTitleBar(context, widget.index),
          BlocConsumer<CareProcessDayCubit, CareProcessDayState>(
            listenWhen: (prev, current) =>
                prev.loadStatus != current.loadStatus,
            listener: (context, state) {
              if (state.loadStatus == LoadStatus.SUCCESS) {
                for (SeasonTaskEntity e in state.taskList!) {
                  graphHeight += 25;
                }
                graphHeight += 100;
              }
            },
            buildWhen: (prev, current) => prev.loadStatus != current.loadStatus,
            builder: (context, state) {
              return SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Container(
                  height: graphHeight + 2,
                  child: Stack(
                    children: [
                      ListView.builder(
                        itemBuilder: (context, index) {
                          return Container(
                            width: 60,
                            height: double.infinity,
                            decoration: BoxDecoration(
                              color: AppColors.blueED,
                              border: Border(
                                top: BorderSide(color: AppColors.blue29),
                                bottom: BorderSide(color: AppColors.blue29),
                                right: BorderSide(color: AppColors.blue29),
                              ),
                            ),
                            child: Column(
                              children: [
                                Container(
                                  height: 25,
                                  padding: EdgeInsets.only(
                                    left: 5,
                                    right: 5,
                                  ),
                                  alignment: Alignment.center,
                                  child: Text(
                                    '${index}h',
                                    style: AppTextStyle.blackS16.copyWith(
                                        color: AppColors.blue29,
                                        fontWeight: FontWeight.w500),
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                        shrinkWrap: true,
                        scrollDirection: Axis.horizontal,
                        physics: NeverScrollableScrollPhysics(),
                        itemCount: 24,
                      ),
                      Column(
                        children: [
                          SizedBox(height: 25),
                          ...List.generate(state.taskList?.length ?? 0,
                              (taskIndex) {
                            SeasonTaskEntity task = state.taskList![taskIndex];
                            int startTime =
                                int.parse(task.start_time!.split(":")[0]);
                            int endTime =
                                int.parse(task.end_time!.split(":")[0]);
                            int taskDuration = endTime - startTime + 1;
                            int rowItemCount = 24 - taskDuration + 1;
                            return Container(
                              height: 25,
                              child: SingleChildScrollView(
                                physics: NeverScrollableScrollPhysics(),
                                scrollDirection: Axis.horizontal,
                                child: Row(
                                  children: [
                                    ...List.generate(rowItemCount, (hourIndex) {
                                      if (hourIndex == startTime) {
                                        return GestureDetector(
                                          onTap: () {
                                            Navigator.of(context).push(
                                                MaterialPageRoute(
                                                    builder: (context) =>
                                                        BlocProvider(
                                                          create: (context) {
                                                            SeasonRepository
                                                                seasonRepository =
                                                                RepositoryProvider
                                                                    .of<SeasonRepository>(
                                                                        context);
                                                            return CareProcessTaskCubit(
                                                                seasonRepository:
                                                                    seasonRepository);
                                                          },
                                                          child:
                                                              CareProcessTaskDetail(
                                                            day: widget.index,
                                                            taskId:
                                                                task.task_id ??
                                                                    "",
                                                            // taskId:
                                                            //     task.task_id ?? "",
                                                          ),
                                                        )));
                                          },
                                          child: Container(
                                            width:
                                                (60 * taskDuration).toDouble(),
                                            child: Container(
                                              height: 15,
                                              margin: EdgeInsets.symmetric(
                                                  vertical: 5),
                                              padding: EdgeInsets.symmetric(
                                                  horizontal: 5),
                                              decoration: BoxDecoration(
                                                  color: AppColors.blue29,
                                                  borderRadius:
                                                      BorderRadius.circular(8)),
                                              alignment: Alignment.center,
                                              child: Text(
                                                task.name ?? "",
                                                overflow: TextOverflow.ellipsis,
                                                style: AppTextStyle.whiteS14,
                                              ),
                                            ),
                                          ),
                                        );
                                      } else
                                        return Container(
                                          width: 60,
                                        );
                                    })
                                  ],
                                ),
                              ),
                            );
                          })
                        ],
                      )
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Container _buildTitleBar(BuildContext context, int index) {
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
                'Ngày $index',
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
              },
            ),
          ),
        ],
      ),
    );
  }
}
