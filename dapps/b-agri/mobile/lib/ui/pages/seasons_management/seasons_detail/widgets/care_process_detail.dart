import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/repositories/season_repository.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/detail_by_day/care_process_day_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/detail_by_day/care_process_day_detail.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_base/utils/date_utils.dart' as Util;

import '../season_detail_cubit.dart';

GlobalKey actionKey = GlobalKey();

class CareProcessDetail extends StatefulWidget {
  String seasonId;
  CareProcessDetail({
    Key? key,
    required this.seasonId,
  }) : super(key: key);

  @override
  State<CareProcessDetail> createState() => _CareProcessDetailState();
}

class _CareProcessDetailState extends State<CareProcessDetail> {
  bool isOpenInfoDialog = false;
  late SeasonDetailCubit _cubit;
  late List<StageEntity>? stageList;
  late String? startDay;

  double graphHeight = 150;
  int duration = 0;

  //check which day have task
  int timeRange = 0;

  @override
  void initState() {
    _cubit = BlocProvider.of<SeasonDetailCubit>(context);
    super.initState();
    stageList = _cubit.state.season?.process?.stages;
    startDay = _cubit.state.season?.start_date;

    //config graph height and duration
    if (stageList != null) {
      graphHeight = 120;
      for (int i = 0; i < stageList!.length; i++) {
        StageEntity stage = stageList![i];
        graphHeight += 30;
        for (int j = 0; j < stage.steps!.length; j++) {
          StepEntity step = stage.steps![j];
          // config day have task
          step.startDay = timeRange;
          if (step.actual_day != null) {
            timeRange += (step.actual_day! - 1);
          } else {
            timeRange += (step.from_day! - 1);
          }
          step.endDay = timeRange;
          timeRange += 1;
          graphHeight += 30;
          //
          if (step.actual_day != null) {
            duration += step.actual_day as int;
          } else {
            duration += step.from_day as int;
          }
        }
      }
    }
  }

  String getDateParam(String startDay, int index) {
    DateTime startDateTime =
        Util.DateUtils.fromStringFormatStrikeThrough(startDay)!;
    DateTime currentDateTime = startDateTime.add(Duration(days: index));
    return Util.DateUtils.toDateAPIString(currentDateTime);
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          Container(
            height: graphHeight + 2,
            padding: EdgeInsets.zero,
            child: Row(
              children: [
                _buildInfoDialog(),
                Expanded(
                  child: ListView.builder(
                    itemBuilder: (_, index) {
                      return GestureDetector(
                        onTap: () {
                          Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => BlocProvider(
                                    create: (context) {
                                      SeasonRepository seasonRepository =
                                          RepositoryProvider.of<
                                              SeasonRepository>(context);
                                      return CareProcessDayCubit(
                                          seasonRepository: seasonRepository);
                                    },
                                    child: CareProcessDayDetail(
                                      index: index + 1,
                                      seasonId: widget.seasonId,
                                      date: getDateParam(startDay!, index),
                                    ),
                                  )));
                        },
                        child: Container(
                          width: 70,
                          height: double.infinity,
                          decoration: BoxDecoration(
                            color: AppColors.blueED,
                            border: Border(
                              top: BorderSide(color: AppColors.blue29),
                              bottom: BorderSide(color: AppColors.blue29),
                              right: BorderSide(color: AppColors.blue29),
                            ),
                          ),
                          child: Stack(
                            children: [
                              Column(
                                children: [
                                  Container(
                                    padding:
                                        EdgeInsets.symmetric(horizontal: 5),
                                    alignment: Alignment.center,
                                    height: 30,
                                    child: Text(
                                      'Ngày ${index + 1}',
                                      style: AppTextStyle.blackS16.copyWith(
                                          color: AppColors.blue29,
                                          fontWeight: FontWeight.w500),
                                    ),
                                  ),
                                ],
                              ),
                              Column(
                                children: [
                                  ...List.generate(stageList?.length ?? 0,
                                      (stageIndex) {
                                    StageEntity stage = stageList![stageIndex];
                                    return Column(
                                      children: [
                                        Container(height: 30),
                                        ...List.generate(
                                            stage.steps?.length ?? 0,
                                            (stepIndex) {
                                          StepEntity step =
                                              stage.steps![stepIndex];
                                          int start = step.startDay!;
                                          int end = step.endDay!;
                                          if (index >= start && index <= end)
                                            return Container(
                                              height: 30,
                                              alignment: Alignment.center,
                                              child: Container(
                                                height: 15,
                                                decoration: BoxDecoration(
                                                    color: _getTitleColor(
                                                        stageIndex),
                                                    borderRadius:
                                                        BorderRadius.only(
                                                      topLeft: Radius.circular(
                                                          index == start
                                                              ? 8
                                                              : 0),
                                                      bottomLeft:
                                                          Radius.circular(
                                                              index == start
                                                                  ? 8
                                                                  : 0),
                                                      topRight: Radius.circular(
                                                          index == end ? 8 : 0),
                                                      bottomRight:
                                                          Radius.circular(
                                                              index == end
                                                                  ? 8
                                                                  : 0),
                                                    )),
                                              ),
                                            );
                                          else
                                            return SizedBox(height: 30);
                                        })
                                      ],
                                    );
                                  })
                                ],
                              )
                            ],
                          ),
                        ),
                      );
                    },
                    shrinkWrap: true,
                    scrollDirection: Axis.horizontal,
                    itemCount: duration,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  _buildInfoDialog() {
    if (isOpenInfoDialog) {
      return Container(
        height: graphHeight + 2,
        color: AppColors.grayEA,
        width: 170,
        alignment: Alignment.topCenter,
        child: ListView.builder(
          itemCount: stageList?.length ?? 0,
          itemBuilder: (context, index) {
            StageEntity stage = stageList![index];
            return Column(
              children: [
                _buildPhaseInfoTitle(index),
                ListView.builder(
                  itemBuilder: (context, indexStep) {
                    return _buildPhaseInfoItem(
                        stage.steps![indexStep].name ?? "");
                  },
                  shrinkWrap: true,
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: stage.steps?.length ?? 0,
                )
              ],
            );
          },
          shrinkWrap: true,
          physics: NeverScrollableScrollPhysics(),
        ),
      );
    } else {
      return GestureDetector(
        key: actionKey,
        onTap: () {
          setState(() {
            isOpenInfoDialog = !isOpenInfoDialog;
          });
        },
        child: Container(
          decoration: BoxDecoration(
              color: AppColors.grayCA,
              border: Border.all(color: AppColors.blue29)),
          alignment: Alignment.center,
          width: 20,
          child: FittedBox(
            child: Icon(
              Icons.add,
              color: Colors.white,
            ),
          ),
        ),
      );
    }
  }

  _buildPhaseInfoTitle(int index) {
    return Container(
      height: 30,
      padding: EdgeInsets.only(left: 14),
      color: AppColors.grayCA,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Text(
              'GIAI ĐOẠN ${index + 1}',
              style: TextStyle(
                  color: _getTitleColor(index),
                  fontSize: 16,
                  fontWeight: FontWeight.bold),
            ),
          ),
          if (index == 0)
            InkWell(
              onTap: () {
                setState(() {
                  isOpenInfoDialog = !isOpenInfoDialog;
                });
              },
              child: Container(
                height: 30,
                width: 40,
                alignment: Alignment.center,
                child: Container(
                  height: 2,
                  width: 13,
                  color: Colors.white,
                ),
              ),
            ),
        ],
      ),
    );
  }

  Color _getTitleColor(index) {
    switch (index) {
      case 0:
        return AppColors.green28;
      case 1:
        return AppColors.yellowA4;
      case 2:
        return AppColors.blue44;
      case 3:
        return AppColors.orangeD7;
      default:
        return AppColors.green28;
    }
  }

  Color _getColor(index) {
    switch (index) {
      case 0:
        return AppColors.blue29;
      case 1:
        return AppColors.green45;
      case 2:
        return AppColors.orangeE9;
      case 3:
        return AppColors.redFF;
      default:
        return AppColors.blue29;
    }
  }

  _buildPhaseInfoItem(String title) {
    return Container(
      height: 30,
      color: AppColors.grayEA,
      child: Row(
        children: [
          SizedBox(width: 14),
          Text(
            title,
            style: TextStyle(color: AppColors.textBlack, fontSize: 16),
          ),
        ],
      ),
    );
  }
}
